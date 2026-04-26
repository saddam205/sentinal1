import time
from typing import Dict, List
from datetime import datetime

class UltraFastRuleEngine:
    """
    Layer 9 — Ultra-Fast Rule Engine (UFRE)
    Deterministic, sub-millisecond decisions
    """

    BLOCK_THRESHOLD = 0.9
    ALLOW_THRESHOLD = 0.1

    def __init__(self):
        self.blocklist_ips = set()
        self.allowlist_ips = set(["127.0.0.1", "localhost"])
        self.call_count = 0
        self.blocks = 0
        self.allows = 0
        self.escalations = 0

    def process(self, payload: Dict) -> Dict:
        start = time.perf_counter()
        self.call_count += 1

        ip = payload.get("ip", "")
        threat_score = payload.get("threat_score", 0.5)
        attempts = payload.get("failed_attempts", 0)

        decision = "escalate"
        reason = "unknown"

        # 🚫 HARD BLOCK RULES
        if ip in self.blocklist_ips:
            decision = "block"
            reason = "blacklisted_ip"

        elif attempts > 10:
            decision = "block"
            reason = "brute_force_detected"

        elif threat_score > self.BLOCK_THRESHOLD:
            decision = "block"
            reason = "high_threat_score"

        # ✅ FAST ALLOW RULES
        elif ip in self.allowlist_ips:
            decision = "allow"
            reason = "trusted_ip"

        elif threat_score < self.ALLOW_THRESHOLD:
            decision = "allow"
            reason = "low_risk"

        # 📈 ESCALATE TO AI
        else:
            decision = "escalate"
            reason = "needs_ai"

        elapsed_ms = (time.perf_counter() - start) * 1000

        # stats
        if decision == "block":
            self.blocks += 1
        elif decision == "allow":
            self.allows += 1
        else:
            self.escalations += 1

        return {
            "decision": decision,
            "reason": reason,
            "processing_ms": round(elapsed_ms, 4),
            "timestamp": datetime.utcnow().isoformat()
        }

    def get_stats(self):
        return {
            "total_calls": self.call_count,
            "blocks": self.blocks,
            "allows": self.allows,
            "escalations": self.escalations,
            "block_rate": round(self.blocks / max(1, self.call_count), 4)
        }