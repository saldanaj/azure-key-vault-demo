#!/bin/bash

# Azure Key Vault Dashboard Setup Script

set -e

echo "🔐 Azure Key Vault Dashboard Setup"
echo "=================================="

# Check if we're in the right directory
if [ ! -f "dashboard/app.py" ]; then
    echo "❌ Error: Please run this script from the repository root directory"
    exit 1
fi

# Get Key Vault information from existing infrastructure or user input
echo ""
echo "📋 Key Vault Configuration"
echo ""

# Try to get existing configuration from Azure
if command -v az &> /dev/null; then
    echo "🔍 Checking for existing Key Vault deployments..."
    
    # Try to find Key Vault from Azure CLI
    KV_NAME=$(az keyvault list --query "[0].name" -o tsv 2>/dev/null || echo "")
    
    if [ ! -z "$KV_NAME" ]; then
        echo "✅ Found Key Vault: $KV_NAME"
        KV_URI="https://${KV_NAME}.vault.azure.net"
    else
        echo "ℹ️  No Key Vault found in current subscription"
    fi
fi

# Get Key Vault details from user if not found
if [ -z "$KV_NAME" ]; then
    echo ""
    read -p "Enter your Key Vault name: " KV_NAME
    KV_URI="https://${KV_NAME}.vault.azure.net"
fi

# Get secret and key names
echo ""
read -p "Enter secret name (default: demo-secret): " SECRET_NAME
SECRET_NAME=${SECRET_NAME:-demo-secret}

read -p "Enter key name (default: demo-key): " KEY_NAME
KEY_NAME=${KEY_NAME:-demo-key}

# Create .env file
echo ""
echo "📝 Creating configuration file..."

cat > dashboard/.env << EOF
# Azure Key Vault Configuration
KV_URI=${KV_URI}
KV_NAME=${KV_NAME}
SECRET_NAME=${SECRET_NAME}
KEY_NAME=${KEY_NAME}

# Flask Configuration
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=true
EOF

echo "✅ Configuration saved to dashboard/.env"

# Set up Python virtual environment
echo ""
echo "🐍 Setting up Python environment..."

cd dashboard

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✅ Virtual environment created"
fi

source .venv/bin/activate

echo "📦 Installing dependencies..."
pip install -r ../requirements.txt > /dev/null 2>&1
echo "✅ Dependencies installed"

cd ..

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To start the dashboard:"
echo "  cd dashboard"
echo "  source .venv/bin/activate"
echo "  python app.py"
echo ""
echo "Then open: http://localhost:5000"
echo ""
echo "Make sure you're logged in to Azure CLI:"
echo "  az login"
