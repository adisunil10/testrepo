#!/bin/bash
PORT=${1:-8000}
echo "Killing process on port $PORT..."
lsof -ti:$PORT | xargs kill -9 2>/dev/null && echo "Port $PORT is now free!" || echo "No process found on port $PORT"
