#!/bin/bash
echo "🛡️ Installing Sentinel-1 Dependencies..."

# Update pip
pip install --upgrade pip

# Install required packages
pip install fastapi uvicorn[standard] sqlalchemy python-jose[cryptography] passlib[bcrypt]
pip install python-multipart prometheus-client numpy matplotlib jinja2 python-socketio
pip install websockets cryptography pydantic email-validator

echo "✅ Installation complete!"
echo "🚀 Run with: python fast6.py"