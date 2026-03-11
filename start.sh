#!/bin/bash

# Summify Startup Script for Linux/Mac

echo "🚀 Starting Summify..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY is not set. Running in MOCK MODE for testing."
    echo ""
    echo "To use real OpenAI API:"
    echo "export OPENAI_API_KEY='your-api-key-here'"
    echo ""
    
    # Try to load from .env file
    if [ -f ".env" ]; then
        echo "Loading from .env file..."
        export $(cat .env | grep -v '#' | xargs)
    else
        echo "✅ No .env file needed - using mock AI mode"
    fi
fi

# Install/upgrade dependencies if needed
echo "📦 Checking dependencies..."
pip install -q -r requirements.txt

# Start the server
echo ""
echo "✅ Starting FastAPI server..."
echo "🌐 Application will be available at: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
