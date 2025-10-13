#!/bin/bash
# SilentSignal Setup and Run Script
# Quick setup for hackathon demo

echo "🔍 SilentSignal - AI Emotional Abuse Detection"
echo "=============================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed."
    exit 1
fi

echo "✅ Python environment check passed"

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Check if .env exists, if not create from example
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file from template..."
    cp env_example.txt .env
    echo "📝 Please edit .env file with your NIM endpoint and API key"
fi

# Run tests
echo "🧪 Running tests..."
python3 test_app.py

echo ""
echo "🚀 Setup complete! To run the application:"
echo "   streamlit run app.py"
echo ""
echo "📝 Demo instructions:"
echo "   1. Open the app in your browser"
echo "   2. Click 'Load Example' in the sidebar"
echo "   3. Click 'Analyze Conversation'"
echo "   4. Review the risk assessment and red flags"
echo ""
echo "🛡️ Safety reminder: This tool is for awareness only."
echo "   If you're in immediate danger, call 911."


