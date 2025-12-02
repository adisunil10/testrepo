# Texas Hold'em Poker - Multiplayer Web Application

A beautiful, real-time multiplayer Texas Hold'em poker game web application similar to pokernow.club.

## Features

- 🎮 Real-time multiplayer gameplay via WebSockets
- 🎴 Full Texas Hold'em poker rules implementation
- 🎨 Beautiful, modern UI with card animations
- 👥 Support for 2-9 players per game room
- 💰 Customizable blinds (small/big blind)
- 📱 Responsive design for desktop and mobile
- 🔒 Room-based game system with shareable room IDs
- 🎯 Complete hand evaluation (Royal Flush down to High Card)
- 💵 Chip management and betting rounds
- 🃏 Dealer button rotation
- 📊 Real-time pot and betting display

## Quick Start

### Prerequisites

- Python 3.10+
- All dependencies from `requirements.txt` (FastAPI and uvicorn are already included)

### Installation

1. **Install dependencies** (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the poker server**:
   ```bash
   python poker_server.py
   ```
   
   The server will start on `http://localhost:8001`

3. **Open the game in your browser**:
   - Open `poker.html` in your web browser, or
   - If you have a local web server running, navigate to it
   - You can also use Python's built-in server:
     ```bash
     python -m http.server 8080
     ```
     Then open `http://localhost:8080/poker.html`

## How to Play

### Creating a Game

1. Enter your name
2. Set your preferred small blind and big blind amounts
3. Click "Create Room"
4. Share your Room ID with friends

### Joining a Game

1. Enter your name
2. Enter the Room ID you received
3. Click "Join Room"

### Gameplay

- **Pre-Flop**: Players receive 2 hole cards, betting begins
- **Flop**: 3 community cards are dealt
- **Turn**: 4th community card is dealt
- **River**: 5th and final community card is dealt
- **Showdown**: Remaining players reveal their hands, best hand wins

### Actions

- **Fold**: Give up your hand and forfeit any bets
- **Check**: Pass action without betting (only if no bet to call)
- **Call**: Match the current bet
- **Bet/Raise**: Increase the betting amount
- **All In**: Bet all your remaining chips

## Architecture

### Backend (`poker_server.py`)

- FastAPI server with WebSocket support
- Complete poker game logic including:
  - Deck management and card dealing
  - Hand evaluation (all poker hands)
  - Betting rounds and pot management
  - Player turn management
  - Room and player management

### Frontend

- **`poker.html`**: Main HTML structure
- **`poker.css`**: Styling and animations
- **`poker.js`**: WebSocket client, UI updates, game interactions

## Game Rules Implemented

- ✅ Blinds system (small/big blind)
- ✅ Betting rounds (Pre-Flop, Flop, Turn, River)
- ✅ Hand rankings (Royal Flush → High Card)
- ✅ Pot management and side pots
- ✅ All-in handling
- ✅ Dealer button rotation
- ✅ Player actions (Fold, Check, Call, Bet, Raise, All-In)

## Technical Details

### WebSocket Protocol

The client and server communicate via WebSocket with the following message types:

**Client → Server:**
- `join`: Join a game room
- `start_hand`: Start a new hand
- `action`: Player action (fold, check, call, bet, raise, all_in)
- `get_state`: Request current game state

**Server → Client:**
- `game_state`: Current game state update
- `error`: Error message

### Card Representation

Cards are represented as strings like `"A♥"`, `"K♠"`, `"10♦"`, etc.

### Room System

- Each room supports up to 9 players
- Rooms are created with unique IDs (8-character)
- Players can leave and rejoin
- Game state persists in room until all players leave

## Customization

### Change Default Chips

Edit `poker_server.py`:
```python
Player(id=player_id, name=name, chips=1000)  # Change 1000 to your amount
```

### Change Default Blinds

Edit the default values in `poker.html`:
```html
<input type="number" id="small-blind" value="10">
<input type="number" id="big-blind" value="20">
```

### Change Max Players

Edit `poker_server.py`:
```python
self.max_players = 9  # Change to desired max
```

## Troubleshooting

### Server won't start

- Make sure port 8001 is not already in use
- Check that all dependencies are installed
- Try changing the port in `poker_server.py` (last line)

### Can't connect to server

- Verify the server is running: `http://localhost:8001/`
- Check browser console for WebSocket errors
- Make sure firewall isn't blocking the connection

### Cards not displaying

- Check browser console for JavaScript errors
- Verify CSS file is loading correctly
- Try hard refresh (Ctrl+Shift+R or Cmd+Shift+R)

## Future Enhancements

Potential features to add:

- [ ] Spectator mode
- [ ] Chat functionality
- [ ] Game history and hand replays
- [ ] Tournament mode
- [ ] Player statistics
- [ ] Reconnection handling
- [ ] Password-protected rooms
- [ ] Timer for actions
- [ ] Hand history display
- [ ] Export game logs

## License

This is a free, open-source project for educational and personal use.

## Credits

Built with:
- FastAPI for the backend
- WebSocket for real-time communication
- Vanilla JavaScript for the frontend
- Pure CSS for styling

Enjoy playing poker! 🎰🃏

