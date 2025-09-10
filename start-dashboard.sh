#!/bin/bash

# Quick start script for the Azure Key Vault Dashboard

set -e

echo "🚀 Starting Azure Key Vault Dashboard..."

# Navigate to dashboard directory
cd "$(dirname "$0")/dashboard"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run setup-dashboard.sh first."
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ Configuration file (.env) not found. Please run setup-dashboard.sh first."
    exit 1
fi

# Start the Flask application
echo "🌐 Dashboard will be available at http://localhost:5000"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

python app.py
