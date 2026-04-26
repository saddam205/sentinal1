# integration_adapter.py - Connect Correlation Engine to FastAPI
from fastapi import Depends, HTTPException, BackgroundTasks
from typing import Dict, List, Any, Optional
import json
import logging
from datetime import datetime

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
    """Normalize tool results, store in DB, and feed to the AI engine"""
    if correlation_system is None:
        logger.warning("Correlation system not initialized, skipping event processing")
        return {"status": "skipped", "reason": "correlation_system_not_initialized"}
    
    try:
        system = correlation_system
        normalizer = system['normalizer']
        
        # Dynamic normalization call (e.g., normalize_nmap)
        normalize_func = getattr(normalizer, f"normalize_{tool_name}", None)
        if not normalize_func:
            logger.warning(f"No normalizer found for tool: {tool_name}")
            return {"error": f"No normalizer found for tool: {tool_name}"}
        
        # Generate EngineEvent objects
        events: List[EngineEvent] = normalize_func(output, target)
        
        if not events:
            logger.info(f"No events generated from {tool_name} output")
            return {"status": "no_events", "events_count": 0}
        
        # Add to engine memory in background to keep API responsive
        background_tasks.add_task(system['event_bus'].publish_many, events)
        
        # Store in SQLAlchemy Database
        for event in events:
            await store_event_in_db(event, user_id, db_session)
        
        # Get MITRE phases
        mitre_phases = []
        for e in events:
            if e.mitre_phase:
                mitre_phases.append(e.mitre_phase.value)
        
        return {
            "status": "synchronized",
            "events_count": len(events),
            "mitre_phases": list(set(mitre_phases))
        }
    except Exception as e:
        logger.error(f"Error processing tool output: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "error": str(e)}

async def store_event_in_db(event: EngineEvent, user_id: int, db_session):
    """Maps EngineEvent (Dataclass) to SecurityEventDB (SQLAlchemy Model)"""
    try:
        # Import inside function to strictly avoid circular import with fast8.py
        from fast8 import SecurityEventDB
        
        db_event = SecurityEventDB(
            event_id=event.event_id,
            event_type=event.event_type.value if hasattr(event.event_type, 'value') else str(event.event_type),
            severity=event.severity,
            asset=event.asset,
            evidence=json.dumps(event.evidence),
            timestamp=event.timestamp,
            source_tool=event.source_tool,
            confidence=event.confidence,
            tags=json.dumps(event.tags),
            mitre_phase=event.mitre_phase.value if event.mitre_phase else None,
            user_id=user_id
        )
        db_session.add(db_event)
        db_session.commit()
        logger.debug(f"Stored event {event.event_id} in database")
    except Exception as e:
        logger.error(f"Database Sync Error: {e}")
        db_session.rollback()

# ==================== FASTAPI ROUTER ====================

def add_correlation_endpoints(app):
    """Injects Engine API endpoints into the main FastAPI app"""
    
    if correlation_system is None:
        logger.warning("Correlation system not initialized, correlation endpoints will not be added")
        return app

    @app.get("/api/correlation/dashboard")
    async def get_engine_dashboard(system=Depends(get_correlation_system)):
        try:
            return {
                "risk": {
                    "score": system['risk_engine'].overall_score,
                    "level": system['risk_engine'].get_risk_level(),
                    "trend": system['risk_engine'].get_risk_trend()
                },
                "attack_graph": system['attack_graph'].to_dict(),
                "recent_events": [e.to_dict() for e in system['correlation_engine'].memory[-10:]],
                "intelligence": system['intelligence_memory'].get_learning_stats()
            }
        except Exception as e:
            logger.error(f"Error in correlation dashboard: {e}")
            return {"error": str(e)}

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

    @app.get("/api/correlation/attack-graph")
    async def get_graph(asset: Optional[str] = None, system=Depends(get_correlation_system)):
        try:
            if asset:
                return {"asset": asset, "paths": system['attack_graph'].get_attack_paths(asset)}
            return system['attack_graph'].to_dict()
        except Exception as e:
            logger.error(f"Error in attack graph: {e}")
            return {"error": str(e)}

    return app