#!/bin/bash

# Complete Poker Server Startup Script with Browser Launch

echo "🃏 Starting Texas Hold'em Poker Server..."
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

# Check if required packages are installed
echo "Checking dependencies..."
python3 -c "import fastapi" 2>/dev/null || {
    echo "⚠️  FastAPI not found. Installing dependencies..."
    pip install fastapi uvicorn[standard] websockets
}

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
POKER_HTML="$SCRIPT_DIR/poker.html"

# Check if poker.html exists
if [ ! -f "$POKER_HTML" ]; then
    echo "❌ Error: poker.html not found in $SCRIPT_DIR"
    exit 1
fi

echo ""
echo "✅ Starting server on http://localhost:8001"
echo ""

# Start a simple HTTP server in the background for serving the HTML file
echo "📝 Starting web server for HTML file on port 8080..."
python3 -m http.server 8080 --directory "$SCRIPT_DIR" > /dev/null 2>&1 &
HTTP_SERVER_PID=$!

# Wait a moment for the server to start
sleep 1

# Open browser (platform-specific)
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "🌐 Opening browser..."
    open "http://localhost:8080/poker.html"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "🌐 Opening browser..."
    xdg-open "http://localhost:8080/poker.html" 2>/dev/null || sensible-browser "http://localhost:8080/poker.html" 2>/dev/null || echo "Please open http://localhost:8080/poker.html in your browser"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    echo "🌐 Opening browser..."
    start "http://localhost:8080/poker.html"
else
    echo "📝 Please open http://localhost:8080/poker.html in your browser"
fi

echo ""
echo "🎮 Game URL: http://localhost:8080/poker.html"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Cleanup function
cleanup() {
    echo ""
    echo "Stopping servers..."
    kill $HTTP_SERVER_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start the poker server (this will block)
python3 "$SCRIPT_DIR/poker_server.py"

# If we get here, clean up
kill $HTTP_SERVER_PID 2>/dev/null

