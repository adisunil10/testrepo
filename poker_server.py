"""
Texas Hold'em Poker Server with WebSocket support
Real-time multiplayer poker game server
"""
import asyncio
import json
import random
import uuid
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn


# Enums
class Suit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"


class Rank(Enum):
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"


class GameStage(Enum):
    WAITING = "waiting"
    PRE_FLOP = "pre_flop"
    FLOP = "flop"
    TURN = "turn"
    RIVER = "river"
    SHOWDOWN = "showdown"
    FINISHED = "finished"


class PlayerAction(Enum):
    FOLD = "fold"
    CHECK = "check"
    CALL = "call"
    BET = "bet"
    RAISE = "raise"
    ALL_IN = "all_in"


# Card and Deck
@dataclass
class Card:
    suit: Suit
    rank: Rank
    
    def __str__(self):
        return f"{self.rank.value}{self.suit.value}"
    
    def to_dict(self):
        return {"suit": self.suit.value, "rank": self.rank.value}


class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Suit for rank in Rank]
        self.shuffle()
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal(self) -> Card:
        return self.cards.pop()


# Player
@dataclass
class Player:
    id: str
    name: str
    chips: int = 1000
    current_bet: int = 0
    has_acted: bool = False
    is_all_in: bool = False
    folded: bool = False
    hole_cards: List[Card] = None
    position: int = -1
    
    def __post_init__(self):
        if self.hole_cards is None:
            self.hole_cards = []
    
    def to_dict(self, hide_cards: bool = True):
        return {
            "id": self.id,
            "name": self.name,
            "chips": self.chips,
            "current_bet": self.current_bet,
            "has_acted": self.has_acted,
            "is_all_in": self.is_all_in,
            "folded": self.folded,
            "hole_cards": [] if hide_cards and self.hole_cards else [str(card) for card in self.hole_cards],
            "position": self.position,
            "total_chips": self.chips + self.current_bet
        }
    
    def bet(self, amount: int) -> int:
        actual_bet = min(amount, self.chips)
        self.chips -= actual_bet
        self.current_bet += actual_bet
        if self.chips == 0:
            self.is_all_in = True
        return actual_bet


# Hand Evaluation
class HandEvaluator:
    RANK_VALUES = {r: idx for idx, r in enumerate(Rank)}
    
    @staticmethod
    def evaluate_hand(cards: List[Card]) -> Tuple[int, List[int]]:
        """Returns (hand_rank, tiebreaker) where higher is better"""
        if len(cards) < 5:
            return (0, [])
        
        # Get all 5-card combinations from 7 cards
        from itertools import combinations
        best_rank = 0
        best_tiebreaker = []
        
        for combo in combinations(cards, 5):
            rank, tiebreaker = HandEvaluator._evaluate_five_cards(list(combo))
            if rank > best_rank or (rank == best_rank and tiebreaker > best_tiebreaker):
                best_rank = rank
                best_tiebreaker = tiebreaker
        
        return (best_rank, best_tiebreaker)
    
    @staticmethod
    def _evaluate_five_cards(cards: List[Card]) -> Tuple[int, List[int]]:
        """Evaluate a 5-card hand"""
        ranks = sorted([HandEvaluator.RANK_VALUES[c.rank] for c in cards], reverse=True)
        suits = [c.suit for c in cards]
        
        rank_counts = {}
        for r in ranks:
            rank_counts[r] = rank_counts.get(r, 0) + 1
        counts = sorted(rank_counts.values(), reverse=True)
        
        is_flush = len(set(suits)) == 1
        is_straight = HandEvaluator._is_straight(ranks)
        
        # Royal flush
        if is_straight and is_flush and ranks[0] == HandEvaluator.RANK_VALUES[Rank.ACE]:
            return (9, ranks)
        
        # Straight flush
        if is_straight and is_flush:
            return (8, ranks)
        
        # Four of a kind
        if counts == [4, 1]:
            four = [r for r in rank_counts if rank_counts[r] == 4][0]
            kicker = [r for r in rank_counts if rank_counts[r] == 1][0]
            return (7, [four, kicker])
        
        # Full house
        if counts == [3, 2]:
            three = [r for r in rank_counts if rank_counts[r] == 3][0]
            two = [r for r in rank_counts if rank_counts[r] == 2][0]
            return (6, [three, two])
        
        # Flush
        if is_flush:
            return (5, ranks)
        
        # Straight
        if is_straight:
            return (4, ranks)
        
        # Three of a kind
        if counts == [3, 1, 1]:
            three = [r for r in rank_counts if rank_counts[r] == 3][0]
            kickers = sorted([r for r in rank_counts if rank_counts[r] == 1], reverse=True)
            return (3, [three] + kickers)
        
        # Two pair
        if counts == [2, 2, 1]:
            pairs = sorted([r for r in rank_counts if rank_counts[r] == 2], reverse=True)
            kicker = [r for r in rank_counts if rank_counts[r] == 1][0]
            return (2, pairs + [kicker])
        
        # One pair
        if counts == [2, 1, 1, 1]:
            pair = [r for r in rank_counts if rank_counts[r] == 2][0]
            kickers = sorted([r for r in rank_counts if rank_counts[r] == 1], reverse=True)
            return (1, [pair] + kickers)
        
        # High card
        return (0, ranks)
    
    @staticmethod
    def _is_straight(ranks: List[int]) -> bool:
        """Check if ranks form a straight (including A-2-3-4-5)"""
        unique_ranks = sorted(set(ranks))
        if len(unique_ranks) < 5:
            return False
        
        # Check for normal straight
        for i in range(len(unique_ranks) - 4):
            if unique_ranks[i+4] - unique_ranks[i] == 4:
                return True
        
        # Check for wheel (A-2-3-4-5)
        if set(unique_ranks) & {0, 1, 2, 3, 4, 12}:  # Contains A and/or 2,3,4,5
            wheel = {12, 0, 1, 2, 3}  # A, 2, 3, 4, 5
            if len(set(unique_ranks) & wheel) == 5:
                return True
        
        return False
    
    @staticmethod
    def get_hand_name(hand_rank: int) -> str:
        names = {
            9: "Royal Flush",
            8: "Straight Flush",
            7: "Four of a Kind",
            6: "Full House",
            5: "Flush",
            4: "Straight",
            3: "Three of a Kind",
            2: "Two Pair",
            1: "One Pair",
            0: "High Card"
        }
        return names.get(hand_rank, "Unknown")


# Game Room
class GameRoom:
    def __init__(self, room_id: str, small_blind: int = 10, big_blind: int = 20):
        self.room_id = room_id
        self.players: Dict[str, Player] = {}
        self.dealer_position = 0
        self.current_bet = 0
        self.pot = 0
        self.community_cards: List[Card] = []
        self.stage = GameStage.WAITING
        self.deck = None
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.action_player_index = 0
        self.last_raise_amount = big_blind
        self.min_players_to_start = 2
        self.max_players = 9
        self.hand_history: List[Dict] = []
    
    def add_player(self, player_id: str, name: str) -> bool:
        if len(self.players) >= self.max_players:
            return False
        if player_id in self.players:
            return False
        
        position = len(self.players)
        self.players[player_id] = Player(id=player_id, name=name, position=position)
        return True
    
    def remove_player(self, player_id: str):
        if player_id in self.players:
            del self.players[player_id]
            # Reassign positions
            for idx, (pid, player) in enumerate(self.players.items()):
                player.position = idx
    
    def start_hand(self):
        if len(self.players) < self.min_players_to_start:
            return False
        
        self.stage = GameStage.PRE_FLOP
        self.deck = Deck()
        self.community_cards = []
        self.pot = 0
        self.current_bet = 0
        self.last_raise_amount = self.big_blind
        
        # Reset players
        for player in self.players.values():
            player.current_bet = 0
            player.has_acted = False
            player.folded = False
            player.is_all_in = False
            player.hole_cards = []
        
        # Deal hole cards
        for _ in range(2):
            for player in self.players.values():
                player.hole_cards.append(self.deck.deal())
        
        # Post blinds
        players_list = list(self.players.values())
        if len(players_list) >= 2:
            # Small blind
            sb_player = players_list[self.dealer_position % len(players_list)]
            sb_player.bet(self.small_blind)
            
            # Big blind
            bb_player = players_list[(self.dealer_position + 1) % len(players_list)]
            bb_amount = bb_player.bet(self.big_blind)
            self.current_bet = bb_amount
            
            # Action starts after big blind
            self.action_player_index = (self.dealer_position + 2) % len(players_list)
        
        self.pot = sum(p.current_bet for p in self.players.values())
        return True
    
    def process_action(self, player_id: str, action: str, amount: int = 0) -> Tuple[bool, str]:
        """Process player action. Returns (success, message)"""
        if player_id not in self.players:
            return (False, "Player not found")
        
        player = self.players[player_id]
        
        # Check if it's player's turn
        players_list = list(self.players.values())
        active_players = [p for p in players_list if not p.folded]
        current_player = active_players[self.action_player_index % len(active_players)]
        
        if current_player.id != player_id:
            return (False, "Not your turn")
        
        if player.has_acted and not self._needs_action(player):
            return (False, "You've already acted this round")
        
        # Process action
        if action == "fold":
            player.folded = True
            player.has_acted = True
        
        elif action == "check":
            if self.current_bet > player.current_bet:
                return (False, "Cannot check, must call or fold")
            player.has_acted = True
        
        elif action == "call":
            call_amount = self.current_bet - player.current_bet
            if call_amount > player.chips:
                return (False, "Not enough chips to call")
            player.bet(call_amount)
            player.has_acted = True
        
        elif action == "bet" or action == "raise":
            if self.stage == GameStage.PRE_FLOP and self.current_bet == 0:
                bet_amount = amount
            else:
                raise_amount = amount - self.current_bet
                if raise_amount < self.last_raise_amount:
                    return (False, f"Raise must be at least {self.last_raise_amount}")
                bet_amount = amount
            
            if bet_amount < self.current_bet:
                return (False, "Bet must be at least the current bet")
            
            total_needed = bet_amount - player.current_bet
            if total_needed > player.chips:
                return (False, "Not enough chips")
            
            actual_bet = player.bet(total_needed)
            if action == "raise" and actual_bet > 0:
                self.last_raise_amount = actual_bet
            self.current_bet = player.current_bet
            player.has_acted = True
            
            # Reset action flags for other players
            for p in self.players.values():
                if p != player and not p.folded and not p.is_all_in:
                    p.has_acted = False
        
        elif action == "all_in":
            all_in_amount = player.chips
            player.bet(all_in_amount)
            if player.current_bet > self.current_bet:
                self.current_bet = player.current_bet
                self.last_raise_amount = player.current_bet - max((p.current_bet for p in self.players.values() if p != player), default=0)
                for p in self.players.values():
                    if p != player and not p.folded and not p.is_all_in:
                        p.has_acted = False
            player.has_acted = True
        
        # Update pot
        self.pot = sum(p.current_bet for p in self.players.values())
        
        # Move to next player
        self._move_to_next_player()
        
        # Check if betting round is complete
        if self._betting_round_complete():
            self._advance_stage()
        
        return (True, "Action processed")
    
    def _needs_action(self, player: Player) -> bool:
        """Check if player needs to act (e.g., after a raise)"""
        return (not player.folded and 
                not player.is_all_in and 
                (player.current_bet < self.current_bet or not player.has_acted))
    
    def _move_to_next_player(self):
        """Move action to next active player"""
        players_list = list(self.players.values())
        active_players = [(idx, p) for idx, p in enumerate(players_list) if not p.folded]
        
        if not active_players:
            return
        
        self.action_player_index = (self.action_player_index + 1) % len(players_list)
    
    def _betting_round_complete(self) -> bool:
        """Check if betting round is complete"""
        players_list = list(self.players.values())
        active_players = [p for p in players_list if not p.folded]
        
        if len(active_players) <= 1:
            return True
        
        # All players have acted
        acted_players = sum(1 for p in active_players if p.has_acted or p.is_all_in)
        if acted_players < len(active_players):
            return False
        
        # All bets are equal
        bets = [p.current_bet for p in active_players if not p.is_all_in]
        if not bets:
            return True
        
        return len(set(bets)) == 1
    
    def _advance_stage(self):
        """Advance to next stage of the hand"""
        players_list = list(self.players.values())
        active_players = [p for p in players_list if not p.folded]
        
        # Move bets to pot
        for player in self.players.values():
            self.pot += player.current_bet
            player.current_bet = 0
            player.has_acted = False
        
        # Check for winner
        if len(active_players) == 1:
            winner = active_players[0]
            winner.chips += self.pot
            self.stage = GameStage.FINISHED
            # Move dealer button for next hand
            players_list = list(self.players.values())
            if len(players_list) > 0:
                self.dealer_position = (self.dealer_position + 1) % len(players_list)
            self.pot = 0
            return
        
        # Advance stage
        if self.stage == GameStage.PRE_FLOP:
            # Deal flop
            self.deck.deal()  # Burn card
            for _ in range(3):
                self.community_cards.append(self.deck.deal())
            self.stage = GameStage.FLOP
        elif self.stage == GameStage.FLOP:
            # Deal turn
            self.deck.deal()  # Burn card
            self.community_cards.append(self.deck.deal())
            self.stage = GameStage.TURN
        elif self.stage == GameStage.TURN:
            # Deal river
            self.deck.deal()  # Burn card
            self.community_cards.append(self.deck.deal())
            self.stage = GameStage.RIVER
        elif self.stage == GameStage.RIVER:
            # Showdown
            self.stage = GameStage.SHOWDOWN
            self._determine_winner()
            return
        
        # Reset for new betting round
        self.current_bet = 0
        self.last_raise_amount = self.big_blind
        self.action_player_index = (self.dealer_position + 1) % len(players_list)
    
    def _determine_winner(self):
        """Determine winner(s) at showdown"""
        players_list = list(self.players.values())
        active_players = [p for p in players_list if not p.folded]
        
        if len(active_players) == 0:
            self.stage = GameStage.FINISHED
            return
        
        # Evaluate hands
        player_hands = []
        for player in active_players:
            all_cards = player.hole_cards + self.community_cards
            hand_rank, tiebreaker = HandEvaluator.evaluate_hand(all_cards)
            hand_name = HandEvaluator.get_hand_name(hand_rank)
            player_hands.append({
                "player": player,
                "hand_rank": hand_rank,
                "tiebreaker": tiebreaker,
                "hand_name": hand_name
            })
        
        # Find winner(s)
        player_hands.sort(key=lambda x: (x["hand_rank"], x["tiebreaker"]), reverse=True)
        best_hand = player_hands[0]
        winners = [ph for ph in player_hands 
                  if ph["hand_rank"] == best_hand["hand_rank"] 
                  and ph["tiebreaker"] == best_hand["tiebreaker"]]
        
        # Distribute pot
        pot_per_winner = self.pot // len(winners)
        remainder = self.pot % len(winners)
        
        for i, winner_info in enumerate(winners):
            chips = pot_per_winner + (remainder if i == 0 else 0)
            winner_info["player"].chips += chips
        
        self.stage = GameStage.FINISHED
        
        # Move dealer button for next hand
        players_list = list(self.players.values())
        if len(players_list) > 0:
            self.dealer_position = (self.dealer_position + 1) % len(players_list)
        
        # Reset pot after distributing
        self.pot = 0
    
    def get_game_state(self, player_id: Optional[str] = None) -> dict:
        """Get current game state"""
        players_dict = {}
        for pid, player in self.players.items():
            hide_cards = pid != player_id or self.stage == GameStage.FINISHED or player.folded
            players_dict[pid] = player.to_dict(hide_cards=hide_cards)
        
        return {
            "room_id": self.room_id,
            "players": players_dict,
            "dealer_position": self.dealer_position,
            "current_bet": self.current_bet,
            "pot": self.pot,
            "community_cards": [str(card) for card in self.community_cards],
            "stage": self.stage.value,
            "small_blind": self.small_blind,
            "big_blind": self.big_blind,
            "action_player_index": self.action_player_index,
            "last_raise_amount": self.last_raise_amount
        }


# FastAPI App
app = FastAPI(title="Texas Hold'em Poker Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Game rooms storage
rooms: Dict[str, GameRoom] = {}
connections: Dict[str, Dict[str, WebSocket]] = {}  # room_id -> {player_id -> websocket}


@app.get("/")
async def root():
    return {"message": "Texas Hold'em Poker Server", "status": "running"}


class RoomCreateRequest(BaseModel):
    name: Optional[str] = None
    small_blind: int = 10
    big_blind: int = 20

@app.post("/api/rooms/create")
async def create_room(request: RoomCreateRequest):
    """Create a new game room"""
    room_id = str(uuid.uuid4())[:8]
    rooms[room_id] = GameRoom(room_id, request.small_blind, request.big_blind)
    connections[room_id] = {}
    return {"room_id": room_id, "message": "Room created"}


@app.get("/api/rooms/{room_id}")
async def get_room_info(room_id: str):
    """Get room information"""
    if room_id not in rooms:
        raise HTTPException(status_code=404, detail="Room not found")
    
    room = rooms[room_id]
    return {
        "room_id": room_id,
        "player_count": len(room.players),
        "max_players": room.max_players,
        "stage": room.stage.value,
        "small_blind": room.small_blind,
        "big_blind": room.big_blind
    }


@app.websocket("/ws/{room_id}/{player_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, player_id: str):
    """WebSocket endpoint for game communication"""
    await websocket.accept()
    
    if room_id not in rooms:
        await websocket.close(code=1008, reason="Room not found")
        return
    
    if room_id not in connections:
        connections[room_id] = {}
    
    connections[room_id][player_id] = websocket
    room = rooms[room_id]
    
    # Send initial game state
    await send_game_state(room_id, player_id)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            action_type = message.get("type")
            
            if action_type == "join":
                player_name = message.get("name", f"Player {player_id[:4]}")
                if room.add_player(player_id, player_name):
                    await broadcast_game_state(room_id, exclude_player=player_id)
                else:
                    await websocket.send_json({"type": "error", "message": "Could not join room"})
            
            elif action_type == "start_hand":
                if room.start_hand():
                    await broadcast_game_state(room_id)
                else:
                    await websocket.send_json({"type": "error", "message": "Cannot start hand"})
            
            elif action_type == "action":
                action = message.get("action")
                amount = message.get("amount", 0)
                success, msg = room.process_action(player_id, action, amount)
                
                if success:
                    await broadcast_game_state(room_id)
                else:
                    await websocket.send_json({"type": "error", "message": msg})
            
            elif action_type == "get_state":
                await send_game_state(room_id, player_id)
            
    except WebSocketDisconnect:
        pass
    finally:
        if room_id in connections and player_id in connections[room_id]:
            del connections[room_id][player_id]
        
        if room_id in rooms:
            room.remove_player(player_id)
            await broadcast_game_state(room_id)


async def send_game_state(room_id: str, player_id: str):
    """Send game state to a specific player"""
    if room_id not in rooms or room_id not in connections:
        return
    
    if player_id not in connections[room_id]:
        return
    
    room = rooms[room_id]
    state = room.get_game_state(player_id)
    
    try:
        await connections[room_id][player_id].send_json({
            "type": "game_state",
            "data": state
        })
    except:
        pass


async def broadcast_game_state(room_id: str, exclude_player: Optional[str] = None):
    """Broadcast game state to all players in room"""
    if room_id not in rooms or room_id not in connections:
        return
    
    room = rooms[room_id]
    disconnected = []
    
    for pid in list(connections[room_id].keys()):
        if pid == exclude_player:
            continue
        
        state = room.get_game_state(pid)
        try:
            await connections[room_id][pid].send_json({
                "type": "game_state",
                "data": state
            })
        except:
            disconnected.append(pid)
    
    # Clean up disconnected players
    for pid in disconnected:
        if pid in connections[room_id]:
            del connections[room_id][pid]
        if room_id in rooms:
            room.remove_player(pid)


if __name__ == "__main__":
    uvicorn.run("poker_server:app", host="0.0.0.0", port=8001, reload=True)

