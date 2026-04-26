# integration_adapter.py - Connect Correlation Engine to FastAPI
# v2.0 — Turbo Quant (Layer 8) integrated; async DB fix; safe endpoint registration
from fastapi import Depends, HTTPException, BackgroundTasks
from typing import Dict, List, Any, Optional
import asyncio
import json
import logging
from datetime import datetime


from ultra_fast_rules import UltraFastRuleEngine

_rule_engine = UltraFastRuleEngine()

# ── Turbo Quant Layer 8 ──────────────────────────────────────────────────────
try:
    from turbo_quant import TurboQuantEngine
    _turbo_engine = TurboQuantEngine()
    TURBO_QUANT_AVAILABLE = True
    print("✓ Turbo Quant Layer 8 loaded into integration_adapter")
except ImportError:
    TURBO_QUANT_AVAILABLE = False
    _turbo_engine = None
    print("⚠ turbo_quant.py not found — Turbo Quant disabled in adapter")

# Configure logging
logger = logging.getLogger(__name__)

# Import correlation engine with alias to avoid collision with DB models
try:
    from correlation_engine import (
        CorrelationSystemFactory,
        SecurityEvent as EngineEvent,
        EventType,
        SeverityLevel
    )
    CORRELATION_ENGINE_AVAILABLE = True
except ImportError as e:
    logger.error(f"CRITICAL: correlation_engine.py not found: {e}")
    CORRELATION_ENGINE_AVAILABLE = False
    # Define dummy classes for when correlation engine is not available
    class CorrelationSystemFactory:
        @classmethod
        def create_complete_system(cls, *args, **kwargs):
            return None
    
    class EngineEvent:
        pass

# Global correlation system instance
correlation_system = None

def init_correlation_system(rag_system=None, llm_reasoner=None, vector_store=None):
    """Initialize the correlation system singleton"""
    global correlation_system
    
    if not CORRELATION_ENGINE_AVAILABLE:
        print("⚠ Correlation Engine not available - skipping initialization")
        return None
    
    try:
        correlation_system = CorrelationSystemFactory.create_complete_system(
            rag_system=rag_system,
            llm_reasoner=llm_reasoner,
            vector_store=vector_store
        )
        print("✓ Correlation Engine Intelligence Layer initialized")
        return correlation_system
    except Exception as e:
        logger.error(f"Failed to initialize correlation system: {e}")
        return None

def get_correlation_system():
    """FastAPI Dependency to get correlation system"""
    if correlation_system is None:
        raise HTTPException(status_code=503, detail="Correlation system not initialized")
    return correlation_system

# ==================== LOGIC FUNCTIONS ====================

async def process_tool_output(
    tool_name: str,
    output: Dict[str, Any],
    target: str,
    user_id: int,
    db_session,
    background_tasks: BackgroundTasks
):
    """
    Normalize tool results, score via Turbo Quant, store in DB,
    and feed to the AI correlation engine.

    Returns a dict that always includes a 'turbo_quant' key when Layer 8
    is available, so the caller can act on fast-path decisions immediately.
    """
    rule_result = _rule_engine.process({
        "ip": target,
        "threat_score": output.get("threat_score", 0.5),
        "failed_attempts": output.get("failed_attempts", 0)
    })

    # 🚫 Instant decision
    if rule_result["decision"] == "block":
        return {
            "status": "blocked_by_rules",
            "rule_engine": rule_result
        }

    # ✅ Skip heavy pipeline
    if rule_result["decision"] == "allow":
        return {
            "status": "allowed_fast_path",
            "rule_engine": rule_result
        }
    if correlation_system is None:
        logger.warning("Correlation system not initialized, skipping event processing")
        return {"status": "skipped", "reason": "correlation_system_not_initialized"}

    try:
        system = correlation_system
        normalizer = system['normalizer']

        # ── Normalise ────────────────────────────────────────────────────────
        normalize_func = getattr(normalizer, f"normalize_{tool_name}", None)
        if not normalize_func:
            logger.warning(f"No normalizer found for tool: {tool_name}")
            return {"error": f"No normalizer found for tool: {tool_name}"}

        events: List[EngineEvent] = normalize_func(output, target)

        if not events:
            logger.info(f"No events generated from {tool_name} output")
            return {"status": "no_events", "events_count": 0}

        # ── Publish to event bus (non-blocking) ──────────────────────────────
        # publish_many may be sync or async — handle both safely
        publish = system['event_bus'].publish_many
        if asyncio.iscoroutinefunction(publish):
            background_tasks.add_task(publish, events)
        else:
            loop = asyncio.get_event_loop()
            background_tasks.add_task(
                lambda: loop.run_in_executor(None, publish, events)
            )

        # ── Turbo Quant fast-path gate ────────────────────────────────────────
        turbo_result: Optional[Dict] = None
        if TURBO_QUANT_AVAILABLE and _turbo_engine:
            # Build minimal layer signals from the normalised events
            tool_outputs_for_turbo = [
                {
                    "success_probability": float(e.confidence) if hasattr(e, "confidence") else 0.5
                }
                for e in events
            ]
            turbo_result = _turbo_engine.process(
                cnn_output   = output.get("cnn_output",   {}),
                gnn_paths    = output.get("gnn_paths",    []),
                rag_results  = output.get("rag_results",  []),
                bnn_decision = output.get("bnn_decision", {}),
                tool_outputs = tool_outputs_for_turbo,
            )
            logger.info(
                "Turbo Quant [%s]: score=%.3f decision=%s drift=%.5f",
                tool_name,
                turbo_result["turbo_score"],
                turbo_result["quant_decision"],
                turbo_result["calibration_drift"],
            )

            # If Turbo Quant fast-rejects, skip DB write and return immediately
            if turbo_result["quant_decision"] == "fast_reject":
                logger.warning(
                    "Turbo Quant fast-rejected %s output for target %s (score=%.3f)",
                    tool_name, target, turbo_result["turbo_score"]
                )
                return {
                    "status":       "fast_rejected",
                    "events_count": len(events),
                    "turbo_quant":  turbo_result,
                }

        # ── Persist events ───────────────────────────────────────────────────
        for event in events:
            await store_event_in_db(event, user_id, db_session)

        # ── Collect MITRE phases ─────────────────────────────────────────────
        mitre_phases = list({
            e.mitre_phase.value
            for e in events
            if getattr(e, "mitre_phase", None)
        })

        result: Dict[str, Any] = {
            "status":       "synchronized",
            "events_count": len(events),
            "mitre_phases": mitre_phases,
        }
        if turbo_result:
            result["turbo_quant"] = turbo_result

        return result

    except Exception as e:
        logger.error(f"Error processing tool output: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "error": str(e)}

async def store_event_in_db(event: EngineEvent, user_id: int, db_session):
    """
    Maps EngineEvent (Dataclass) to SecurityEventDB (SQLAlchemy Model).

    SQLAlchemy's synchronous session.commit() is blocking I/O.
    We offload it to a thread-pool executor so we don't stall the event loop.
    """
    try:
        # Import inside function to strictly avoid circular import with fast13.py
        from fast13 import SecurityEventDB

        db_event = SecurityEventDB(
            event_id    = event.event_id,
            event_type  = event.event_type.value if hasattr(event.event_type, 'value') else str(event.event_type),
            severity    = event.severity,
            asset       = event.asset,
            evidence    = json.dumps(event.evidence),
            timestamp   = event.timestamp,
            source_tool = event.source_tool,
            confidence  = event.confidence,
            tags        = json.dumps(event.tags),
            mitre_phase = event.mitre_phase.value if event.mitre_phase else None,
            user_id     = user_id,
        )
        db_session.add(db_event)

        # Commit on thread pool — never block the async event loop
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, db_session.commit)

        logger.debug(f"Stored event {event.event_id} in database")

    except Exception as e:
        logger.error(f"Database Sync Error: {e}")
        db_session.rollback()

# ==================== FASTAPI ROUTER ====================

def add_correlation_endpoints(app):
    """
    Injects correlation + Turbo Quant API endpoints into the main FastAPI app.

    Routes are always registered.  When the correlation system is not yet
    ready the dependency raises 503 — callers get a clear error instead of
    silently missing routes.
    """
    # ── /api/rule_engine/stats ─────────────────────────────────────
    @app.get("/api/rule_engine/stats")
    async def rule_stats():
        if _rule_engine is None:
            raise HTTPException(status_code=503, detail="Rule Engine not available")
        return _rule_engine.get_stats()
    # ── /api/correlation/dashboard ──────────────────────────────────────────
    @app.get("/api/correlation/dashboard")
    async def get_engine_dashboard(system=Depends(get_correlation_system)):
        try:
            base = {
                "risk": {
                    "score": system['risk_engine'].overall_score,
                    "level": system['risk_engine'].get_risk_level(),
                    "trend": system['risk_engine'].get_risk_trend()
                },
                "attack_graph":   system['attack_graph'].to_dict(),
                "recent_events":  [e.to_dict() for e in system['correlation_engine'].memory[-10:]],
                "intelligence":   system['intelligence_memory'].get_learning_stats(),
            }
            # Attach live Turbo Quant stats when available
            if TURBO_QUANT_AVAILABLE and _turbo_engine:
                base["turbo_quant"] = _turbo_engine.get_stats()
            return base
        except Exception as e:
            logger.error(f"Error in correlation dashboard: {e}")
            return {"error": str(e)}

    # ── /api/correlation/predict ─────────────────────────────────────────────
    @app.get("/api/correlation/predict")
    async def predict_attack(system=Depends(get_correlation_system)):
        """AI Predictive Analysis of the next attack step"""
        try:
            events = system['correlation_engine'].memory
            if not events:
                return {"prediction": "Insufficient data", "confidence": 0}
            return system['decision_engine'].predict_next_attack(events)
        except Exception as e:
            logger.error(f"Error in predict attack: {e}")
            return {"error": str(e)}

    # ── /api/correlation/attack-graph ────────────────────────────────────────
    @app.get("/api/correlation/attack-graph")
    async def get_graph(asset: Optional[str] = None, system=Depends(get_correlation_system)):
        try:
            if asset:
                return {"asset": asset, "paths": system['attack_graph'].get_attack_paths(asset)}
            return system['attack_graph'].to_dict()
        except Exception as e:
            logger.error(f"Error in attack graph: {e}")
            return {"error": str(e)}

    # ── /api/turbo_quant/stats ───────────────────────────────────────────────
    @app.get("/api/turbo_quant/stats")
    async def turbo_quant_stats():
        """Live Turbo Quant Layer 8 performance & calibration stats"""
        if not TURBO_QUANT_AVAILABLE or _turbo_engine is None:
            raise HTTPException(status_code=503, detail="Turbo Quant not available")
        return _turbo_engine.get_stats()

    # ── /api/turbo_quant/score ───────────────────────────────────────────────
    @app.post("/api/turbo_quant/score")
    async def turbo_quant_score(payload: Dict[str, Any]):
        """
        Ad-hoc Turbo Quant scoring endpoint.
        Accepts a free-form dict of layer outputs and returns a turbo_score + decision.
        Useful for frontend polling without running the full pipeline.
        """
        if not TURBO_QUANT_AVAILABLE or _turbo_engine is None:
            raise HTTPException(status_code=503, detail="Turbo Quant not available")
        try:
            result = _turbo_engine.process(
                cnn_output   = payload.get("cnn_output",   {}),
                gnn_paths    = payload.get("gnn_paths",    []),
                rag_results  = payload.get("rag_results",  []),
                bnn_decision = payload.get("bnn_decision", {}),
                tool_outputs = payload.get("tool_outputs", []),
            )
            return result
        except Exception as e:
            logger.error(f"Turbo Quant score error: {e}")
            return {"error": str(e)}

    logger.info("✓ Correlation + Turbo Quant endpoints registered")
    return app

def init_correlation_system(rag_system=None, llm_reasoner=None, vector_store=None):
    """Initialize the correlation system singleton"""
    global correlation_system
    
    if not CORRELATION_ENGINE_AVAILABLE:
        print("⚠ Correlation Engine not available - skipping initialization")
        return None
    
    try:
        correlation_system = CorrelationSystemFactory.create_complete_system(
            rag_system=rag_system,
            llm_reasoner=llm_reasoner,
            vector_store=vector_store
        )
        
        # Check if correlation_system has the expected structure
        if correlation_system is not None:
            # Ensure required components exist
            if 'correlation_engine' in correlation_system:
                # Patch the correlation_engine if it's missing _load_correlation_rules
                if hasattr(correlation_system['correlation_engine'], '_load_correlation_rules'):
                    pass  # Already has it
                else:
                    # Add a fallback implementation
                    def _fallback_load_rules(self_obj, db_session=None):
                        self_obj.correlation_rules = [
                            {
                                'name': 'SQL Injection Chain',
                                'pattern': ['SQL_INJECTION', 'SQL_INJECTION'],
                                'time_window': 300,
                                'action': 'elevate_severity',
                                'new_severity': 8.0
                            }
                        ]
                        return True
                    
                    # Bind the method to the instance
                    import types
                    correlation_system['correlation_engine']._load_correlation_rules = types.MethodType(
                        _fallback_load_rules, correlation_system['correlation_engine']
                    )
                    
                    # Try to call it
                    try:
                        correlation_system['correlation_engine']._load_correlation_rules()
                        print("✓ Correlation engine patched with fallback rules")
                    except Exception as patch_e:
                        print(f"⚠ Could not patch correlation engine: {patch_e}")
            
            print("✓ Correlation Engine Intelligence Layer initialized")
        else:
            print("⚠ Correlation system returned None")
            
        return correlation_system
    except Exception as e:
        logger.error(f"Failed to initialize correlation system: {e}")
        import traceback
        traceback.print_exc()
        return None
if __name__ == "__main__":
    engine = UltraFastRuleEngine()

    test = {
        "ip": "192.168.1.1",
        "threat_score": 0.95,
        "failed_attempts": 12
    }

    print(engine.process(test))
    print(engine.get_stats())