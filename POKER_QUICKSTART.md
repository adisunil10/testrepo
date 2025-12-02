# Texas Hold'em Poker - Quick Start Guide

## 🚀 Quick Start (3 steps)

### 1. Start the Server
```bash
python poker_server.py
```
Server runs on `http://localhost:8001`

### 2. Open the Game
Open `poker.html` in your web browser, or use a simple server:
```bash
python -m http.server 8080
```
Then visit `http://localhost:8080/poker.html`

### 3. Play!
- Create a room or join with a Room ID
- Share the Room ID with friends
- Start playing!

## 📋 Files Created

- **`poker_server.py`** - Backend server with WebSocket support
- **`poker.html`** - Frontend HTML
- **`poker.css`** - Beautiful styling
- **`poker.js`** - Client-side game logic
- **`POKER_README.md`** - Full documentation
- **`start_poker.sh`** - Quick startup script

## 🎮 How to Play

1. **Create/Join Room**: Enter your name and create or join a room
2. **Wait for Players**: Need at least 2 players to start
3. **Start Hand**: Click "Start Game" when ready
4. **Play**: Use buttons to fold, check, call, bet, raise, or go all-in
5. **Win**: Best hand wins the pot!

## ✨ Features

- ✅ Real-time multiplayer (2-9 players)
- ✅ Full Texas Hold'em rules
- ✅ Beautiful card animations
- ✅ Customizable blinds
- ✅ Room-based system
- ✅ Hand evaluation (all poker hands)

## 🐛 Troubleshooting

**Server won't start?**
- Check if port 8001 is available
- Install dependencies: `pip install fastapi uvicorn`

**Can't connect?**
- Make sure server is running
- Check browser console for errors
- Verify firewall settings

**Cards not showing?**
- Check that CSS file loads
- Try hard refresh (Ctrl+Shift+R)

Enjoy playing! 🃏🎰

