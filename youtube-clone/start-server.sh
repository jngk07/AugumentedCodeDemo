#!/bin/bash

# YouTube Clone Server Startup Script
echo "🎥 Starting YouTube Clone Server..."
echo "📁 Project Directory: $(pwd)"
echo ""

# Check if Python is available
if command -v python3 &> /dev/null; then
    echo "✅ Python 3 found"
    python3 server.py --open
elif command -v python &> /dev/null; then
    echo "✅ Python found"
    python server.py --open
else
    echo "❌ Python not found. Please install Python to run the server."
    echo "💡 Alternatively, you can open index.html directly in your browser."
    exit 1
fi
