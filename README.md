# 🛡️ SENTINEL-1 v6.5 — AI-Powered Autonomous Cybersecurity Platform

> **Next-generation intelligent threat detection, autonomous exploitation, and real-time defense orchestration**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.103-green.svg)](https://fastapi.tiangolo.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.1-red.svg)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🚀 Overview

**Sentinel-1** is an **AI-powered cybersecurity research platform** combining:

- 🧠 **9-Layer Neural Cyber-Brain** — Multi-stage intelligence pipeline
- 🔍 **Real-time Threat Analysis** — Event-driven correlation engine
- 🤖 **Autonomous Decision Making** — Bayesian + Reinforcement Learning
- 🎯 **Intelligent Exploitation** — DeepSeek-powered payload generation
- 📊 **Live Observability** — Prometheus + Grafana + Socket.IO
- ⚡ **Sub-millisecond Defense** — UltraFast deterministic rules

**Designed for:** Authorized penetration testing, security research, red team operations, and defensive automation labs.

---

## ⚠️ Legal Disclaimer

This tool is intended **exclusively for**:
- ✅ Authorized security testing on systems you own or have explicit written permission to test
- ✅ Ethical hacking labs and research environments
- ✅ Authorized penetration testing engagements
- ✅ Security research and education

**❌ DO NOT use on systems without permission. Unauthorized use may violate laws.**

---

## 🏗️ System Architecture

### Full System Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                      BROWSER CLIENT                             │
│  Dashboard | Attack Graph | Risk Radar | Emily AI Panel         │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTP REST + Socket.IO
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                    FASTAPI CORE (fast15.py)                      │
│  • 80+ API routes  • JWT Auth  • Socket.IO Event Bus             │
│  • 21 Pentesting Tools  • Real-time Streaming                    │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│            9-LAYER NEURAL CYBER-BRAIN PIPELINE                  │
│                                                                  │
│  L9 UltraFast Rules ─┐  (Sub-millisecond deterministic)         │
│                      ├─→ L1 CNN Pattern Scanner                  │
│                      │   L2 GNN Attack Strategist                │
│                      │   L3 MiniLM RAG Knowledge Base            │
│                      │   L4 BNN Arbiter (Decision Gate)          │
│                      │   L5 GAN Payload Evolver                  │
│                      │   L6 Emily AI Hacker (DeepSeek LLM)       │
│                      │   L7 Correlation Spine (Nervous System)   │
│                      │   L8 TurboQuant (INT8 Fast Inference)     │
│                      ▼                                            │
│            RISK SCORING + ATTACK PATHS                          │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│           BACKEND MODULES & EXECUTION ENGINE                    │
│                                                                  │
│  • Correlation Engine      • Integration Adapter                │
│  • RAG System (FAISS)      • SafetyCage Validator               │
│  • Attack Graph Builder    • Metasploit Bridge                  │
│  • Penetration Tools (21)  • Event Bus                          │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│              DATA STORES & MONITORING                            │
│                                                                  │
│  SQLite | FAISS Index | Redis | Prometheus | Grafana            │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🧠 The 9-Layer Cyber-Brain

### Layer 1: **CNN Pattern Scanner** 🎨
- **Purpose:** Visual anomaly detection from network traffic patterns
- **Model:** 2D Convolutional Neural Network
- **Input:** Network packet byte streams (64×64 images)
- **Output:** Anomaly score + 256-d pattern embedding

### Layer 2: **GNN Attack Strategist** 🕸️
- **Purpose:** Graph-based attack path planning
- **Model:** Graph Neural Network (GCN)
- **Function:** Maps network topology → identifies critical nodes → ranks attack paths
- **Output:** Ranked list of attack vectors with impact scores

### Layer 3: **MiniLM RAG Knowledge Base** 📚
- **Purpose:** Semantic similarity search for attack patterns
- **Model:** Sentence-Transformers (MiniLM-L6-v2) + FAISS
- **KB:** Enterprise attack taxonomy + MITRE ATT&CK + CVE database
- **Output:** Top-k similar attack patterns with confidence scores

### Layer 4: **BNN Arbiter** ⚖️
- **Purpose:** Probabilistic Bayesian decision-making
- **Model:** Bayesian Neural Network with confidence calibration
- **Decisions:** 
  - `EXECUTE` (confidence ≥ 0.85) → Proceed with exploitation
  - `EVOLVE` (high uncertainty) → Mutate and retry
  - `ANALYZE` (low confidence) → Escalate to human
- **Output:** Confidence score + reasoning + target layer

### Layer 5: **GAN Payload Evolver** 🧬
- **Purpose:** Payload mutation and evasion optimization
- **Model:** Generative Adversarial Network
- **Function:** Generates & mutates payloads → evaluates evasion fitness
- **Output:** Evolved payloads with evasion scores (0-100%)

### Layer 6: **Emily AI Hacker** 🤖
- **Purpose:** 4-step reasoning for exploit generation
- **Model:** DeepSeek-Coder-1.3B (with 4-bit quantization or LoRA)
- **Reasoning Steps:**
  1. IDENTIFY entry points
  2. EVALUATE impact
  3. RECOMMEND strategy
  4. CRITIQUE weaknesses
- **Output:** Structured exploit plan + Metasploit commands + risk assessment

### Layer 7: **Correlation Spine** 🔗
- **Purpose:** Central nervous system & event orchestration
- **Function:** Coordinates all layers → reinforcement learning loop
- **Events:** Tool outputs → Decisions → Outcomes → Weight updates
- **Output:** Attack graph + risk timeline + next-step predictions

### Layer 8: **TurboQuant** ⚡
- **Purpose:** Ultra-fast INT8 quantized inference
- **Model:** 128-d embedding compression + INT8 quantization
- **Throughput:** 3.1× faster than Layer 4
- **Output:** `fast_approve` / `fast_reject` / `defer_to_full_pipeline`

### Layer 9: **UltraFast Rules Engine** 🚀
- **Purpose:** Sub-millisecond deterministic decision-making
- **Model:** Whitelist/blacklist + threat scoring heuristics
- **Decision:** `block` / `allow` / `escalate` (before neural pipeline)
- **Latency:** <1ms per request

---

## 📊 Key Features

### 🔐 Security & Validation
- ✅ JWT-based authentication with bcrypt
- ✅ **SafetyCage validator** — Command whitelist enforcement
- ✅ Regex-based DANGER_ZONE detection
- ✅ Sanitized command execution with timeout protection
- ✅ Optional: Metasploit RPC sandbox

### 🎯 Penetration Tools (21 Integrated)

**Traditional Tools:**
- Nmap, SQLMap, Nikto, Gobuster, WPScan
- Hydra, John the Ripper, Aircrack-ng
- Dirb, Wireshark, BurpSuite, BloodHound

**Advanced Tools (Kali 2025):**
- AdaptixC2, Fluxion, MetasploitMCP
- AtomicOperator, GEF, SSTImap, XSStrike, WPProbe

### 🤖 AI Capabilities
- Real-time layer-by-layer processing (Socket.IO streaming)
- Autonomous exploit chain generation
- Evasion-aware payload mutation
- Multi-stage attack recommendations
- LLM-powered strategic reasoning

### 📈 Observability
- **Prometheus metrics** — Attack counters, layer timing, accuracy
- **Grafana dashboards** — Real-time visualization
- **Socket.IO events** — Live UI updates (layer_update, tool_started, scan_complete)
- **Correlation tracking** — Event timeline + attack graph + MITRE mappings

### 💾 Knowledge Management
- FAISS vector index (~16K MITRE ATT&CK tactics)
- Automatic embedding of successful attacks
- RAG-based pattern retrieval (similarity search)
- Intelligence memory feedback loop

---

## 📋 Prerequisites

- **Python** 3.10 – 3.12
- **CUDA** 12.1 (optional, for GPU acceleration)
- **Redis** (optional, for caching)
- **8GB RAM** minimum (16GB+ recommended for LLM layers)
- **Kali Linux** or security-focused distro (for tools)

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/saddam205/sentinal1.git
cd sentinal1
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**For GPU Support (CUDA 12.1):**

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

**Optional: DeepSeek LLM (Emily AI)**

```bash
pip install transformers peft bitsandbytes
# Download DeepSeek model (first run)
```

### 4. Generate SSL Certificates (HTTPS)

```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

### 5. Configure Environment

Create `.env` file:

```env
# Database
DATABASE_URL=sqlite:///./sentinel.db

# Auth
SECRET_KEY=your-secret-key-here          # openssl rand -hex 32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Redis (optional)
REDIS_URL=redis://localhost:6379/0
REDIS_AVAILABLE=false

# Model paths
MODEL_DIR=./models
RAG_INDEX_PATH=./models/mitre_index.faiss

# Metasploit (optional)
MSF_HOST=127.0.0.1
MSF_PORT=55553
MSF_PASSWORD=sentinel
```

### 6. Download RAG Knowledge Base

```bash
# Automatically loads on first run
# Or manually:
python -c "from rag_system import build_rag; build_rag()"
```

---

## 🚀 Running Sentinel-1

### Development Mode (HTTP with auto-reload)

```bash
python run.py
# or
uvicorn fast15:app --host 0.0.0.0 --port 8000 --reload
```

### Production Mode (HTTPS)

```bash
uvicorn fast15:app --host 0.0.0.0 --port 9090 \
    --ssl-keyfile key.pem --ssl-certfile cert.pem
```

### Access Dashboard

- **Dashboard:** https://localhost:9090
- **API Docs:** https://localhost:9090/docs (Swagger)
- **ReDoc:** https://localhost:9090/redoc

---

## 📡 API Reference

### Authentication

| Method | Path | Description |
|--------|------|-------------|
| POST | `/login` | User login (returns JWT token) |
| POST | `/register` | Create new user account |
| POST | `/logout` | Logout (invalidate token) |
| GET | `/api/users/me` | Get current user info |

### Scanning & Analysis

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/scan/url` | Run full 9-layer pipeline on target |
| GET | `/api/scan/status/{scan_id}` | Get scan progress |
| GET | `/api/scan/vulnerability` | Get detected vulnerabilities |
| GET | `/api/scan/history` | Get past scans |
| GET | `/api/pipeline/history` | Get all pipeline executions |

### AI & Exploitation

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/emily/analyze` | Emily AI strategic analysis |
| POST | `/api/emily/generate-payload` | Generate exploit payload |
| GET | `/api/emily/status` | Get Emily AI status |
| POST | `/api/attack/execute` | Execute penetration tool |
| GET | `/api/attack/suggestions` | Get attack recommendations |
| GET | `/api/attacks` | List all executed attacks |

### Intelligence & Correlation

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/correlation/dashboard` | Correlation engine status |
| GET | `/api/correlation/predict` | Predict next attack step |
| GET | `/api/correlation/attack-graph` | Full attack graph visualization |
| POST | `/api/ai/rag/search` | Search knowledge base |
| GET | `/api/ai/chat` | AI chat endpoint (WebSocket) |

### Monitoring

| Method | Path | Description |
|--------|------|-------------|
| GET | `/metrics` | Prometheus metrics |
| GET | `/api/status` | System health check |
| GET | `/api/metrics/summary` | Summary statistics |

### WebSocket Events

Connect to `ws://localhost:9090/ws/{user_id}` for real-time updates:

| Event | Payload |
|-------|---------|
| `layer_update` | `{layer, confidence, status, details}` |
| `tool_started` | `{tool_id, tool_name, target}` |
| `tool_complete` | `{tool_id, results, duration_ms}` |
| `scan_complete` | `{scan_id, final_risk_score, attack_paths}` |
| `ai_suggestion` | `{suggestion_id, type, content}` |
| `alert` | `{severity, message, event_id}` |

---

## 🔬 Usage Examples

### Example 1: Scan a Target URL

```bash
curl -X POST "https://localhost:9090/api/scan/url" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "target": "example.com",
    "ports": [80, 443, 8080],
    "scan_type": "full",
    "enable_emily": true
  }'
```

### Example 2: Generate Exploit with Emily AI

```bash
curl -X POST "https://localhost:9090/api/emily/generate-payload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "vulnerability": "SQL Injection",
    "target": "example.com",
    "lhost": "attacker.com",
    "lport": 4444
  }'
```

### Example 3: Get Attack Recommendations

```bash
curl -X GET "https://localhost:9090/api/attack/suggestions?target=example.com&ports=22,80,443" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Example 4: Search Knowledge Base (RAG)

```bash
curl -X POST "https://localhost:9090/api/ai/rag/search" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How to exploit SQL injection in WordPress?",
    "top_k": 5
  }'
```

---

## 🎯 Workflow: Full Attack Chain

### Step-by-Step Process

1. **User initiates scan** → POST `/api/scan/url`

2. **L9 UltraFast Rules** → Sub-millisecond check (block/allow/escalate)

3. **Neural Pipeline** (if escalated):
   - **L1 CNN** → Analyzes packet patterns
   - **L2 GNN** → Maps attack graph
   - **L3 RAG** → Retrieves similar attacks
   - **L4 BNN** → Makes probabilistic decision
   - **L5 GAN** → Evolves payloads (if needed)
   - **L6 Emily** → Generates exploit strategy
   - **L7 Spine** → Correlates events

4. **L8 TurboQuant** → Fast verification (INT8 inference)

5. **Execution** → SafetyCage validates → Tool runs → Results captured

6. **Real-time UI updates** → Socket.IO layer_update events → Dashboard refreshes

7. **Attack recorded** → Correlation engine updates graph → Risk score updated

8. **Feedback loop** → Outcome stored → RL weights adjusted

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| **L9 UltraFast latency** | <1 ms |
| **L8 TurboQuant throughput** | 3.1× faster than L4 |
| **Full pipeline (L1→L7)** | ~500ms (GPU) / ~2s (CPU) |
| **L6 Emily (DeepSeek)** | ~800ms (4-bit quant) / ~3s (full precision) |
| **Tool execution** | Variable (10s - 5min depending on tool) |
| **RAG search (FAISS)** | <50ms (16K vectors) |
| **Metasploit integration** | ~1s (if daemon available) |

---

## 🗂️ Project Structure

```
sentinal1/
├── fast15.py                      # Main FastAPI app (14,888 lines)
├── sentinel_brain.py              # 9-layer neural pipeline
├── orchestrator.py                # Neural orchestration
├── correlation_engine.py          # Event correlation + risk scoring
├── integration_adapter.py          # Tool output normalization
├── rag_system.py                  # FAISS vector search
├── turbo_quant.py                 # Layer 8: INT8 quantization
├── ultra_fast_rules.py            # Layer 9: Deterministic rules
├── sentinel_utils.py              # SafetyCage validator
├── math_education.py              # Educational utilities
│
├── templates/
│   ├── results.html               # Main SPA dashboard (2,867 lines)
│   └── ...
│
├── static/
│   ├── css/
│   ├── js/
│   └── img/
│
├── models/
│   ├── mitre_index.faiss          # Pre-built FAISS index
│   ├── mitre_texts.json           # MITRE ATT&CK corpus
│   └── ...
│
├── requirements.txt               # Python dependencies
├── alembic/                       # Database migrations
├── .gitignore
├── README.md                      # This file
└── run.py                         # Entry point
```

---

## 🔧 Configuration

### SafetyCage Whitelist

Edit `sentinel_utils.py` to add/remove allowed commands:

```python
SAFE_COMMANDS = {
    'nmap': r'^nmap\s+(-[a-zA-Z0-9]+\s+)*[\w\.\-]+$',
    'sqlmap': r'^sqlmap\s+-u\s+https?://.*',
    # Add more...
}
```

### Layer Weights (BNN Arbiter)

Modify in `sentinel_brain.py`:

```python
self.weights = {
    'cnn': 0.25,
    'gnn': 0.25,
    'minilm': 0.20,
    'tools': 0.30
}
```

---

## 🐛 Troubleshooting

### Issue: "CUDA not available"
**Solution:** Falls back to CPU. Install CUDA drivers or use CPU mode.

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### Issue: "DeepSeek model too large"
**Solution:** Use 4-bit quantization (auto-enabled).

```python
# In sentinel_brain.py
quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16
)
```

### Issue: "FAISS index not found"
**Solution:** Auto-generates on first run. Or manually:

```bash
python -c "from rag_system import build_rag; build_rag()"
```

### Issue: "Metasploit daemon unreachable"
**Solution:** Features gracefully disable. Start MSF RPC:

```bash
msfrpcd -P sentinel -a 127.0.0.1 -p 55553 -S
```

### Issue: "Port 9090 already in use"
**Solution:** Use different port:

```bash
uvicorn fast15:app --host 0.0.0.0 --port 8080
```

---

## 📈 Monitoring & Grafana

### Prometheus Metrics Exported

```
ATTACK_TOTAL                    # Total attacks executed
LAYER_PROCESSING_TIME           # Per-layer timing histogram
BNN_CONFIDENCE_SCORE            # Decision confidence
GAN_EVASION_SCORE               # Payload evasion percentage
CORRELATION_EVENTS_TOTAL        # Events processed
RAG_SEARCH_LATENCY              # Knowledge base query time
```

### Access Grafana Dashboard

```
http://localhost:9090/grafana-proxy/d/sentinel-main
```

---

## 🚀 Deployment

### Docker Deployment

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 9090
CMD ["uvicorn", "fast15:app", "--host", "0.0.0.0", "--port", "9090"]
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sentinel-1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sentinel
  template:
    metadata:
      labels:
        app: sentinel
    spec:
      containers:
      - name: sentinel
        image: saddam205/sentinel:latest
        ports:
        - containerPort: 9090
        env:
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: sentinel-secrets
              key: secret-key
```

---

## 📚 Documentation

- [API Reference](./docs/API.md)
- [Layer Documentation](./docs/LAYERS.md)
- [RAG Knowledge Base](./docs/RAG.md)
- [Safety & Security](./docs/SAFETY.md)
- [Performance Tuning](./docs/PERFORMANCE.md)

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -am 'Add feature'`)
4. Push to branch (`git push origin feature/your-feature`)
5. Submit a Pull Request

---

## 📄 License

MIT License — See [LICENSE](./LICENSE) file for details.

---

## 👨‍💻 Author

**Saddam (saddam205)**
- AI Engineer | Cybersecurity Researcher | Quant Systems Architect
- GitHub: [@saddam205](https://github.com/saddam205)

---

## 🔗 Related Projects

- **[AI Trading Bot](https://github.com/saddam205/saddam205)** — Quantitative trading system with 7-layer neural ensemble
- **[Enterprise Security Suite](https://github.com/saddam205/enterprise-sec)** — Full-stack security platform

---

## ⭐ Why This Project Stands Out

✨ **Combines AI + Cybersecurity + Systems Design**
- Novel 9-layer neural architecture (CNN→GNN→RAG→BNN→GAN→Emily→Spine→TurboQuant→UltraFast)
- Real-world exploitation orchestration
- Production-grade error handling + observability
- Sub-millisecond attack decision-making
- DeepSeek LLM-powered reasoning

🔐 **Enterprise-Ready Security**
- SafetyCage command validation
- JWT authentication + bcrypt
- MITRE ATT&CK correlation
- Prometheus/Grafana monitoring
- SQLite + FAISS + Redis support

⚡ **Performance-Optimized**
- 3.1× throughput gain (TurboQuant)
- GPU acceleration support
- 4-bit quantization for LLMs
- Socket.IO real-time streaming

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/saddam205/sentinal1/issues)
- **Security:** Please report vulnerabilities responsibly
- **Email:** saddam205@github.com

---

## 🙏 Acknowledgments

- **FastAPI** — Modern async web framework
- **PyTorch** — Deep learning framework
- **Sentence-Transformers** — Semantic embeddings
- **FAISS** — Vector similarity search
- **DeepSeek** — Open-source LLM
- **Kali Linux** — Security tools distribution
- **MITRE ATT&CK** — Threat intelligence framework

---

**Built with ❤️ for the cybersecurity and AI research community**

`v6.5` | Last updated: April 2026 | Status: Active Development
