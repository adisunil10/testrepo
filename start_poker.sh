#!/bin/bash

# Texas Hold'em Poker Server Startup Script

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

echo ""
echo "✅ Starting server on http://localhost:8001"
echo "📝 Open poker.html in your browser to play"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python3 poker_server.py

