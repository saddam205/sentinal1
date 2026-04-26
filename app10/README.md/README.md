# SENTINEL-1 CyberSec Lab v6.5

An AI-powered cybersecurity research platform combining a multi-layer neural detection pipeline, real-time event correlation, and a FastAPI web dashboard. Built for authorised penetration testing, threat intelligence research, and ML-based intrusion detection.

---

## Table of contents

1. [Architecture overview](#architecture-overview)
2. [Project structure](#project-structure)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Training the models](#training-the-models)
7. [Running the server](#running-the-server)
8. [API reference](#api-reference)
9. [Neural pipeline layers](#neural-pipeline-layers)
10. [Correlation engine](#correlation-engine)
11. [Known limitations & warnings](#known-limitations--warnings)
12. [Legal notice](#legal-notice)

---

## Architecture overview

```
HTTP / WebSocket clients
        │
        ▼
  fast8.py  (FastAPI + Socket.IO entrypoint)
        │
        ├── integration_adapter.py  (normalise tool output → SecurityEvent)
        │         │
        │         └── correlation_engine.py  (event bus, attack graph, risk scoring)
        │
        ├── orchestrator.py  (SentinelOrchestrator + ActiveExploitEngine)
        │         │
        │         └── sentinel_utils.py  (SafetyCage command validator)
        │
        └── sentinel_brain.py  (7-layer NeuralPipeline)
                  │
                  ├── Layer 1 — CNN pattern scanner       (train_cicids2017.py)
                  ├── Layer 2 — MLP network detector      (train_cicids2017.py)
                  ├── Layer 3 — GNN graph analyser        (train_pipeline.py)
                  ├── Layer 4 — MiniLM + FAISS RAG        (train_pipeline.py)
                  ├── Layer 5 — Bayesian / EMBER          (train_ember.py)
                  ├── Layer 6 — SOREL LightGBM            (train_sorel.py)
                  └── Layer 7 — DeepSeek LoRA (optional)  (train_pipeline.py)
```

---

## Project structure

```
sentinel/
├── fast8.py                # Main FastAPI + Socket.IO application
├── sentinel_brain.py       # 7-layer neural inference pipeline
├── orchestrator.py         # Master controller, exploit engine
├── correlation_engine.py   # Event correlation, attack graph, risk engine
├── integration_adapter.py  # Tool output normaliser → correlation engine
├── sentinel_utils.py       # SafetyCage validator, internet intel helper
├── math_education.py       # Educational math utilities (optional module)
│
├── train_cicids2017.py     # Train MLP on CICIDS2017 network traffic data
├── train_ember.py          # Train RandomForest on EMBER 2018 malware data
├── train_sorel.py          # Train LightGBM on SOREL-20M malware data
├── train_pipeline.py       # Orchestrated training runner (all layers)
├── evaluate_models.py      # Unified model evaluation + reporting
├── test_models.py          # Quick model sanity-check script
│
├── models/                 # Saved model files (git-ignored)
│   ├── layer2_cnn.pth
│   ├── layer3_gnn.pth
│   ├── layer3_minilm/
│   ├── layer4_bayesian.pkl
│   ├── ember_feature_size.json
│   └── faiss.index
│
├── data/                   # Datasets (git-ignored — download separately)
│   ├── cicids2017/
│   ├── ember/ember2018/
│   └── sorel/
│
├── templates/              # Jinja2 HTML templates
├── static/                 # JS / CSS assets
├── requirements.txt
└── README.md
```

---

## Requirements

- Python **3.10 – 3.12**
- CUDA 12.x (optional, for GPU acceleration)
- Redis (required for Celery task queue)
- A running `msfrpcd` daemon if using Metasploit integration

See `requirements.txt` for all Python dependencies.

---

## Installation

### 1. Clone and create a virtual environment

```bash
git clone https://github.com/your-org/sentinel.git
cd sentinel
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 2. Install Python dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### GPU build (CUDA 12.1)

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

#### Optional extras

```bash
# Graph neural networks
pip install torch-geometric

# LLM fine-tuning
pip install peft bitsandbytes

# Metasploit integration
pip install pymetasploit3

# EMBER feature extraction (install from source)
git clone https://github.com/endgameinc/ember
pip install -e ember/
```

### 3. Install and start Redis

```bash
# Ubuntu / Debian
sudo apt install redis-server && sudo systemctl start redis

# macOS
brew install redis && brew services start redis

# Docker
docker run -d -p 6379:6379 redis:7-alpine
```

### 4. Generate SSL certificates (for HTTPS mode)

```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

---

## Configuration

The application reads configuration from environment variables. Create a `.env` file in the project root:

```env
# Database
DATABASE_URL=sqlite:///./sentinel.db
# or PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/sentinel

# Auth
SECRET_KEY=your-secret-key-here          # openssl rand -hex 32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Redis / Celery
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Model paths (override defaults)
MODEL_DIR=./models

# Metasploit RPC (optional)
MSF_HOST=127.0.0.1
MSF_PORT=55553
MSF_PASSWORD=sentinel
```

---

## Training the models

Download the required datasets first. **Do not train on the wrong dataset** — each script expects specific data formats:

| Script | Dataset | Download |
|---|---|---|
| `train_cicids2017.py` | CICIDS2017 network flows CSV | [UNB CIC](https://www.unb.ca/cic/datasets/ids-2017.html) |
| `train_ember.py` | EMBER 2018 malware JSONL | [Endgame EMBER](https://github.com/endgameinc/ember) |
| `train_sorel.py` | SOREL-20M malware JSONL | [Sophos SOREL](https://github.com/sophos/SOREL-20M) |

Place datasets at:
```
data/cicids2017/cicids2017_combined.csv
data/ember/ember2018/train_features_0.jsonl  (through _5)
data/sorel/*.jsonl
```

### Train individual models

```bash
# Network intrusion detector (CICIDS2017)
python train_cicids2017.py

# Malware detector (EMBER 2018)
python train_ember.py

# SOREL LightGBM classifier
python train_sorel.py
```

### Train the full pipeline at once

```bash
python train_pipeline.py
```

This runs CNN → MiniLM → Bayesian in sequence and saves a `training_report.json`.

### Evaluate trained models

```bash
python evaluate_models.py
python test_models.py          # quick sanity check
```

---

## Running the server

```bash
# Development (HTTP, auto-reload)
uvicorn fast8:app --host 0.0.0.0 --port 8000 --reload

# Production (HTTPS)
uvicorn fast8:app --host 0.0.0.0 --port 9090 \
    --ssl-keyfile key.pem --ssl-certfile cert.pem

# Or run the built-in launcher
python fast8.py
```

The dashboard is available at `https://localhost:9090` after startup.

---

## API reference

All endpoints are prefixed with `/api/`.

### Auth

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/auth/register` | Register a new user |
| `POST` | `/api/auth/token` | Obtain a JWT access token |

### Scans

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/scan/nmap` | Run an Nmap scan against a target |
| `POST` | `/api/scan/nikto` | Run a Nikto web scan |
| `POST` | `/api/scan/sqlmap` | Run SQLMap against a URL |
| `GET`  | `/api/scan/history` | List past scans for current user |

### Correlation engine

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/correlation/dashboard` | Risk score, attack graph, recent events |
| `GET` | `/api/correlation/predict` | AI prediction of next attack step |
| `GET` | `/api/correlation/attack-graph` | Full or asset-filtered attack graph |

### Neural pipeline

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/analyze` | Run a payload through all 7 neural layers |
| `GET`  | `/api/models/status` | Layer availability and model versions |

### WebSocket

Connect to `ws://host/ws/{user_id}` for real-time scan progress and layer updates.

Socket.IO events emitted by the server:

| Event | Payload |
|---|---|
| `layer_update` | `{layer, probability, status, details}` |
| `scan_complete` | `{scan_id, results, mitre_phases}` |
| `alert` | `{severity, message, event_id}` |

---

## Neural pipeline layers

| # | Name | Model type | Training data | Purpose |
|---|---|---|---|---|
| 1 | CNN Pattern Scanner | 2D CNN | Network packet byte streams | Visual anomaly detection |
| 2 | MLP Network Detector | MLP (4-layer) | CICIDS2017 CSV | Binary intrusion classification |
| 3 | GNN Graph Analyser | GCN (2-layer) | Synthetic / custom graphs | Attack path graph analysis |
| 4 | MiniLM RAG | SentenceTransformer + FAISS | Security text corpus | Semantic threat lookup |
| 5 | Bayesian EMBER | RandomForest + CalibratedClassifierCV | EMBER 2018 | PE malware probability |
| 6 | SOREL LightGBM | LightGBM + PCA + TF-IDF | SOREL-20M | Malware family classification |
| 7 | DeepSeek LoRA | Causal LM (LoRA fine-tuned) | Custom exploit corpus | Exploit reasoning (optional) |

---

## Correlation engine

`correlation_engine.py` runs as an in-process event bus. When a tool scan completes, `integration_adapter.py` normalises the output into typed `SecurityEvent` dataclasses and publishes them to the bus. The engine then:

- Maps events to **MITRE ATT&CK phases** (`AttackPhase` enum)
- Maintains a **sliding risk score** via `RiskEngine`
- Builds a **directed attack graph** of observed paths per asset
- Feeds an **intelligence memory** that improves predictions over time
- Exposes predictions via `DecisionEngine.predict_next_attack()`

Supported source tool normalisers: `nmap`, `nikto`, `sqlmap`, `hydra`, `dirb`, `whois`.

---

## Known limitations & warnings

- **`train_cicids2017.py` was previously using the wrong dataset** (UCI Online Retail). The fixed version expects CICIDS2017 network flow CSVs. If you trained with an older version of the file, retrain the model.

- **Dummy Bayesian model**: if EMBER data is not found during `train_pipeline.py`, a random-data fallback model is saved with a `"DummyRandomForestCalibrated"` marker in `ember_feature_size.json`. This model produces meaningless predictions. Always train on real EMBER data for production.

- **DeepSeek LoRA layer** requires a CUDA GPU with at least 8 GB VRAM and the `peft` + `bitsandbytes` packages. It is skipped gracefully on CPU-only machines.

- **Metasploit integration** requires a running `msfrpcd` daemon (`msfrpcd -P sentinel -S`) on port 55553. Features are disabled automatically if the daemon is unreachable.

- **`SafetyCage`** in `sentinel_utils.py` validates AI-generated commands against a whitelist before shell execution. Never bypass it or extend the whitelist without careful review.

---

## Legal notice

This tool is intended **exclusively for authorised security research and penetration testing** on systems you own or have explicit written permission to test. Unauthorised use against systems you do not own is illegal in most jurisdictions. The authors accept no liability for misuse.