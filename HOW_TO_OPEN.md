# How to Open the Poker Game in Your Browser

## Option 1: Simple Direct Method (Easiest)

1. **Start the server:**
   ```bash
   python poker_server.py
   ```

2. **Open the HTML file directly in your browser:**
   - **On Mac**: Double-click `poker.html` in Finder, or drag it to your browser
   - **On Windows**: Right-click `poker.html` → "Open with" → Choose your browser
   - **On Linux**: Right-click → "Open with" → Choose your browser

   OR manually:
   - Open your browser (Chrome, Firefox, Safari, etc.)
   - Press `Cmd+O` (Mac) or `Ctrl+O` (Windows/Linux)
   - Navigate to the `poker.html` file and open it

## Option 2: Using a Web Server (Recommended)

1. **In one terminal, start the poker server:**
   ```bash
   python poker_server.py
   ```

2. **In another terminal, start a simple web server:**
   ```bash
   python -m http.server 8080
   ```

3. **Open your browser and go to:**
   ```
   http://localhost:8080/poker.html
   ```

## Option 3: All-in-One Script (Automatic Browser Opening)

Run the complete startup script that opens everything for you:

```bash
./start_poker_complete.sh
```

This will:
- Start the poker server
- Start a web server for the HTML file
- Automatically open your browser to the game

## Quick Visual Guide

### Method 1: Direct File Opening
```
1. Start server:  python poker_server.py
2. Open poker.html in browser (double-click or drag to browser)
```

### Method 2: Web Server
```
Terminal 1: python poker_server.py
Terminal 2: python -m http.server 8080
Browser:    http://localhost:8080/poker.html
```

### Method 3: Automated Script
```
./start_poker_complete.sh
(Everything opens automatically!)
```

## Troubleshooting

**"Connection refused" error?**
- Make sure the poker server is running on port 8001
- Check terminal for any error messages

**CSS/styling not loading?**
- Use Option 2 (web server) instead of opening file directly
- This ensures all files load correctly

**Want to access from another device?**
- Find your IP address: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
- Access from other device: `http://YOUR_IP:8080/poker.html`
- Make sure both devices are on the same network

## Which Method Should I Use?

- **Option 1**: Fastest, good for quick testing
- **Option 2**: Best for sharing with friends on your network
- **Option 3**: Easiest, does everything automatically

Choose what works best for you! 🎮

