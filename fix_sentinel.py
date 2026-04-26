#!/usr/bin/env python3
"""
Quick fix script for Sentinel-1 issues
"""

import os
import sys

def fix_imports():
    """Check and fix imports"""
    required = ['fastapi', 'uvicorn', 'sqlalchemy', 'cryptography', 'socketio']
    missing = []
    for pkg in required:
        try:
            __import__(pkg.replace('-', '_'))
        except ImportError:
            missing.append(pkg)
    
    if missing:
        print(f"⚠️ Missing packages: {missing}")
        print("Run: pip install " + " ".join(missing))
        return False
    return True

def create_directories():
    """Create required directories"""
    dirs = ['templates', 'static', 'logs', 'data']
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)
            print(f"📁 Created {d}/")

def create_ssl():
    """Create SSL certificates if missing"""
    if not os.path.exists('key.pem') or not os.path.exists('cert.pem'):
        try:
            from cryptography.hazmat.primitives import serialization
            from cryptography.hazmat.primitives.asymmetric import rsa
            from cryptography.hazmat.primitives import hashes
            from cryptography import x509
            from cryptography.x509.oid import NameOID
            import datetime
            
            private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
            
            subject = issuer = x509.Name([
                x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
            ])
            
            cert = x509.CertificateBuilder().subject_name(
                subject
            ).issuer_name(
                issuer
            ).public_key(
                private_key.public_key()
            ).serial_number(
                x509.random_serial_number()
            ).not_valid_before(
                datetime.datetime.utcnow()
            ).not_valid_after(
                datetime.datetime.utcnow() + datetime.timedelta(days=365)
            ).sign(private_key, hashes.SHA256())
            
            with open('key.pem', 'wb') as f:
                f.write(private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption(),
                ))
            
            with open('cert.pem', 'wb') as f:
                f.write(cert.public_bytes(serialization.Encoding.PEM))
            
            print("✅ SSL certificates created")
        except ImportError:
            print("⚠️ Cannot create SSL certs - cryptography not installed")
            print("Run: pip install cryptography")

def main():
    print("🔧 Sentinel-1 Fix Utility")
    print("=" * 40)
    
    if fix_imports():
        print("✅ All imports OK")
    else:
        sys.exit(1)
    
    create_directories()
    create_ssl()
    
    print("\n✅ Fix complete! Run: python fast6.py")

if __name__ == "__main__":
    main()