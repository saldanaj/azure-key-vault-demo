# Azure Key Vault Rotation Demo

A comprehensive demonstration of Azure Key Vault secret and key rotation with real-time monitoring through a local web dashboard. This project shows how applications can consume Key Vault secrets and keys by name (without specifying versions) to automatically pick up rotations.

## 🎯 What This Demo Shows

- **Automatic Rotation Pickup**: Applications request secrets/keys by name only, automatically receiving the latest versions
- **Real-time Monitoring**: Local web dashboard displays current status, versions, and rotation history
- **Manual Rotation Control**: Rotate secrets and keys on-demand through the dashboard or CLI
- **Best Practices**: Demonstrates proper Azure identity authentication and Key Vault integration patterns

## 📁 Repository Structure

```
├── requirements.txt         # Consolidated Python dependencies
├── setup-dashboard.sh       # One-command dashboard setup script
├── start-dashboard.sh       # Dashboard startup script
├── app/python/             # Command-line interface for Key Vault operations
│   ├── kv_cli/             # CLI module
│   └── requirements.txt    # References root requirements
├── dashboard/              # Local web dashboard (Flask)
│   ├── app.py              # Flask application
│   ├── templates/          # HTML templates
│   ├── .env               # Configuration (created by setup)
│   └── requirements.txt    # References root requirements
├── keyvault/               # Reusable Key Vault operations module
│   ├── client.py           # Key Vault client wrapper
│   ├── rotator.py          # Rotation logic
│   └── config.py           # Configuration management
├── infra/                  # Bicep infrastructure templates
│   ├── main.bicep          # Main infrastructure template
│   └── modules/            # Bicep modules
├── scripts/                # Deployment and utility scripts
│   ├── deploy.sh           # Infrastructure deployment
│   ├── seed.sh             # Create initial secrets/keys
│   ├── rotate-*.sh         # Manual rotation scripts
│   └── destroy.sh          # Cleanup script
└── docs/                   # Detailed documentation
```

## 🚀 Quick Start Guide

### Prerequisites

1. **Azure Subscription** with sufficient permissions to create:
   - Resource Groups
   - Key Vaults
   - User-assigned Managed Identities

2. **Development Environment**:
   - **Option A (Recommended)**: VS Code with Dev Containers extension
   - **Option B**: Local machine with Python 3.8+, Azure CLI, and Bicep CLI

3. **Azure CLI** installed and logged in:
   ```bash
   az login
   ```

### Step 1: Environment Setup

#### Option A: Using Dev Container (Recommended)

1. **Open in VS Code**: 
   - Install the "Dev Containers" extension
   - Open this repository in VS Code
   - When prompted, click "Reopen in Container"
   - Wait for the container to build (installs all dependencies automatically)

2. **Verify Setup**:
   ```bash
   # These should all work in the dev container
   az --version
   bicep --version
   python --version
   ```

#### Option B: Local Setup

1. **Install Dependencies**:
   ```bash
   # Install Azure CLI (if not already installed)
   curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
   
   # Install Bicep CLI
   az bicep install
   
   # Install Python dependencies
   pip install -r requirements.txt
   ```

2. **Login to Azure**:
   ```bash
   az login
   ```

### Step 2: Deploy Infrastructure

1. **Set Environment Variables**:
   ```bash
   export RG=akv-rot-demo              # Resource group name
   export LOCATION=eastus              # Azure region
   export PREFIX=akvdemo               # Unique prefix for resources
   ```

2. **Deploy Infrastructure**:
   ```bash
   ./scripts/deploy.sh
   ```
   
   This script will:
   - Create a resource group
   - Deploy a Key Vault with Standard tier
   - Create a user-assigned managed identity
   - Configure appropriate permissions
   - Output the Key Vault name for next steps

3. **Note the Output**: Save the Key Vault name from the deployment output:
   ```
   Key Vault Name: akv2-kv-abc123def456
   ```

### Step 3: Seed Initial Data

Create the initial secret and key that will be used for rotation demonstrations:

```bash
export KV_NAME=akv2-kv-abc123def456  # Use your actual Key Vault name
./scripts/seed.sh
```

This creates:
- **Secret**: `demo-secret` with an initial value
- **Key**: `demo-key` (RSA 2048-bit) for cryptographic operations

### Step 4: Set Up the Local Dashboard

#### Option A: One-Command Setup (Recommended)

```bash
./setup-dashboard.sh
```

This script will:
- Detect your deployed Key Vault automatically
- Prompt for secret and key names (defaults: `demo-secret`, `demo-key`)
- Create a virtual environment
- Install all dependencies
- Generate configuration files
- Display startup instructions

#### Option B: Manual Setup

```bash
# Navigate to dashboard directory
cd dashboard

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create configuration file
cat > .env << EOF
KV_NAME=akv2-kv-abc123def456
SECRET_NAME=demo-secret
KEY_NAME=demo-key
EOF

# Return to root directory
cd ..
```

### Step 5: Start the Dashboard

```bash
./start-dashboard.sh
```

The dashboard will start on http://localhost:5000 and display:
- Real-time secret and key status
- Version information and creation dates
- Rotation timeline and history
- Interactive rotation controls

### Step 6: Test Rotation Functionality

#### Via Dashboard (Recommended)
1. Open http://localhost:5000 in your browser
2. Click "Rotate Secret" or "Rotate Key" buttons
3. Watch the status update in real-time
4. View the rotation timeline at the bottom

#### Via Command Line
```bash
# Rotate secret manually
KV_NAME=$KV_NAME ./scripts/rotate-secret-now.sh

# Rotate key manually  
KV_NAME=$KV_NAME ./scripts/rotate-key-now.sh
```

#### Via CLI Tool
```bash
# Activate virtual environment (if not using dev container)
source .venv/bin/activate

# Read current secret value
python -m kv_cli read-secret --vault "$KV_NAME" --show-value

# Sign data with current key
python -m kv_cli sign --vault "$KV_NAME" --data "hello world"
```

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `KV_NAME` | Azure Key Vault name | - | ✅ |
| `SECRET_NAME` | Name of the secret to monitor | `demo-secret` | ✅ |
| `KEY_NAME` | Name of the key to monitor | `demo-key` | ✅ |
| `PORT` | Dashboard port | `5000` | ❌ |

### Dashboard Configuration

The dashboard configuration is stored in `dashboard/.env`:
```env
KV_NAME=your-keyvault-name
SECRET_NAME=demo-secret
KEY_NAME=demo-key
```

## 📊 Understanding the Dashboard

### Status Cards
- **Secret Status**: Shows current version, creation date, enabled status, and total versions
- **Key Status**: Displays key information, version details, and properties
- **Rotation Timeline**: Historical view of all rotations with timestamps

### Interactive Controls
- **🔄 Rotate Secret**: Creates a new secret version with a fresh value
- **🔑 Rotate Key**: Generates a new key version
- **🔥 Rotate Both**: Rotates both secret and key simultaneously
- **🔄 Refresh Now**: Manually refresh all status information

### Auto-refresh
The dashboard automatically polls for updates every 5 seconds to show real-time changes.

## 🛠 Advanced Usage

### CLI Operations

The repository includes a full-featured CLI for Key Vault operations:

```bash
# Activate environment (if needed)
source .venv/bin/activate

# Available commands
python -m kv_cli --help

# Read secret metadata
python -m kv_cli read-secret --vault $KV_NAME

# Read secret value (careful in production!)
python -m kv_cli read-secret --vault $KV_NAME --show-value

# Sign data with key
python -m kv_cli sign --vault $KV_NAME --data "sensitive data"

# List all secret versions
python -m kv_cli list-versions --vault $KV_NAME --type secret

# List all key versions
python -m kv_cli list-versions --vault $KV_NAME --type key
```

### Custom Rotation Logic

The rotation logic is modular and can be customized in `keyvault/rotator.py`:

```python
from keyvault.rotator import rotate_secret, rotate_key_version

# Rotate with custom value
result = rotate_secret("my-vault", "my-secret", custom_value="new-password")

# Rotate key with specific key type
result = rotate_key_version("my-vault", "my-key", key_type="RSA", key_size=4096)
```

### Integration with Other Applications

The `keyvault/` module can be imported into other Python applications:

```python
from keyvault.client import KeyVaultClient

# Initialize client
client = KeyVaultClient("my-vault-name")

# Get current secret
secret_info = client.get_secret_status("my-secret")

# Get current key
key_info = client.get_key_status("my-key")
```

## 🧹 Cleanup

### Stop the Dashboard
```bash
# Press Ctrl+C in the terminal running the dashboard
```

### Remove Azure Resources
```bash
# Remove all Azure resources
RG=akv-rot-demo ./scripts/destroy.sh
```

### Clean Local Environment
```bash
# Remove virtual environments
rm -rf dashboard/.venv
rm -rf .venv

# Remove configuration files
rm -f dashboard/.env
```

## 🔍 Troubleshooting

### Common Issues

#### "Failed to refresh status: HTTP 404"
- **Cause**: Dashboard can't connect to the local server
- **Solution**: Ensure the dashboard is running with `./start-dashboard.sh`

#### "KeyProperties object has no attribute 'key_type'"
- **Cause**: Issue with Azure SDK key properties
- **Solution**: This should be fixed in the current version. If you see this, restart the dashboard.

#### "Authentication failed"
- **Cause**: Not logged into Azure CLI or insufficient permissions
- **Solution**: 
  ```bash
  az login
  az account show  # Verify correct subscription
  ```

#### "Key Vault not found"
- **Cause**: Incorrect Key Vault name or insufficient permissions
- **Solution**: 
  ```bash
  # List available Key Vaults
  az keyvault list --query "[].name" -o table
  
  # Verify permissions
  az keyvault show --name $KV_NAME
  ```

### Debug Mode

Enable debug logging in the dashboard by editing `dashboard/app.py`:
```python
app.debug = True
```

### Logs

Dashboard logs are displayed in the terminal where you started it. For more detailed logs:
```bash
export AZURE_LOG_LEVEL=DEBUG
./start-dashboard.sh
```

## 📚 Additional Documentation

- **[Architecture Overview](docs/00-overview.md)**: Detailed system architecture
- **[Deployment Guide](docs/10-deploy.md)**: Advanced deployment scenarios  
- **[Usage Examples](docs/20-run-demo.md)**: More usage examples and scenarios
- **[Cleanup Guide](docs/30-cleanup.md)**: Comprehensive cleanup procedures

## 🔒 Security Considerations

- **Local Development Only**: This dashboard is designed for development and demonstration
- **Credentials**: Uses Azure CLI authentication (`DefaultAzureCredential`)
- **Network**: Dashboard runs on localhost only (not exposed externally)
- **Permissions**: Requires Key Vault permissions for the authenticated user

## 🎯 Next Steps

After completing this demo, consider:

1. **Production Implementation**: Adapt the patterns for production applications
2. **Automated Rotation**: Implement scheduled rotation using Azure Functions or other schedulers
3. **Monitoring Integration**: Connect to Azure Monitor or other observability platforms
4. **Multi-Environment**: Extend to development, staging, and production environments

---

**Need Help?** Check the troubleshooting section above or review the detailed documentation in the `docs/` directory.
