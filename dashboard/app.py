"""
Azure Key Vault Rotation Dashboard

A local web application for monitoring and controlling Key Vault secret and key rotations.
"""

import os
import sys
from pathlib import Path
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv

# Add the parent directory to the path so we can import keyvault module
sys.path.insert(0, str(Path(__file__).parent.parent))

from keyvault import KeyVaultClient, rotate_secret, rotate_key_version, get_keyvault_config

# Load environment variables from .env file if it exists
load_dotenv()

app = Flask(__name__)

# Global client instance
kv_client = None


def get_client():
    """Get or create Key Vault client instance."""
    global kv_client
    if kv_client is None:
        try:
            kv_client = KeyVaultClient()
        except Exception as e:
            print(f"Failed to initialize Key Vault client: {e}")
            return None
    return kv_client


@app.route('/')
def dashboard():
    """Serve the main dashboard page."""
    try:
        config = get_keyvault_config()
        return render_template('index.html', config=config)
    except Exception as e:
        return f"Configuration error: {e}", 500


@app.route('/api/status')
def get_status():
    """Get current status of secrets and keys."""
    client = get_client()
    if not client:
        return jsonify({"error": "Key Vault client not available"}), 500
    
    try:
        config = get_keyvault_config()
        secret_name = config["secret_name"]
        key_name = config["key_name"]
        
        # Get secret and key status
        secret_status = client.get_secret_status(secret_name)
        key_status = client.get_key_status(key_name)
        timeline = client.get_rotation_timeline(secret_name, key_name)
        
        return jsonify({
            "secret": secret_status,
            "key": key_status,
            "timeline": timeline
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/rotate/secret', methods=['POST'])
def rotate_secret_endpoint():
    """Rotate a secret."""
    try:
        config = get_keyvault_config()
        secret_name = config["secret_name"]
        
        result = rotate_secret(
            secret_name=secret_name,
            rotated_by="dashboard",
            disable_previous=False
        )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/rotate/key', methods=['POST'])
def rotate_key_endpoint():
    """Rotate a key."""
    try:
        config = get_keyvault_config()
        key_name = config["key_name"]
        
        result = rotate_key_version(key_name=key_name, rotated_by="dashboard")
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/health')
def health_check():
    """Health check endpoint."""
    try:
        config = get_keyvault_config()
        return jsonify({
            "status": "healthy",
            "vault_name": config["vault_name"],
            "secret_name": config["secret_name"],
            "key_name": config["key_name"]
        })
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


if __name__ == '__main__':
    # Configuration
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    
    print(f"🚀 Starting Azure Key Vault Rotation Dashboard")
    print(f"🌐 Server: http://{host}:{port}")
    print(f"🔧 Debug mode: {debug}")
    
    try:
        config = get_keyvault_config()
        print(f"🔐 Key Vault: {config['vault_name']}")
        print(f"🗝️  Secret: {config['secret_name']}")
        print(f"🔑 Key: {config['key_name']}")
    except Exception as e:
        print(f"⚠️  Configuration warning: {e}")
    
    app.run(host=host, port=port, debug=debug)
