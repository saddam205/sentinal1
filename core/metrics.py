# core/metrics.py

from prometheus_client import Counter, Histogram, Gauge, start_http_server, REGISTRY
import time

# =========================
# SAFE METRIC HELPER
# =========================

def get_safe_metric(metric_type, name, documentation, labelnames=()):
    """Prevents Duplicated timeseries error by checking REGISTRY first."""
    if name in REGISTRY._names_to_collectors:
        return REGISTRY._names_to_collectors[name]
    return metric_type(name, documentation, labelnames)

# =========================
# GLOBAL METRICS (REFACTORED)
# =========================

# Use the helper for ALL metric definitions
REQUEST_COUNT = get_safe_metric(
    Counter, 
    "sentinel_requests_total", 
    "Total API Requests", 
    ["endpoint"]
)

# Crucial: Fix the name conflict causing your error
# Your error message showed a conflict between 'sentinel_attacks' and 'sentinel_attacks_total'
ATTACK_COUNT = get_safe_metric(
    Counter, 
    "sentinel_attacks_total", 
    "Total Attacks Executed",
    ["type"] # Added label to match your safe_counter call
)

VULN_COUNT = get_safe_metric(
    Gauge, 
    "sentinel_vulnerabilities", 
    "Number of vulnerabilities detected"
)

REQUEST_LATENCY = get_safe_metric(
    Histogram, 
    "sentinel_request_latency_seconds", 
    "Request latency"
)

# =========================
# START METRICS SERVER
# =========================

def start_metrics_server(port=8001):
    # Only start the server if it's not already running to avoid "Address already in use"
    try:
        print(f"📊 Prometheus metrics running on http://localhost:{port}/metrics")
        start_http_server(port)
    except OSError:
        print(f"ℹ️ Metrics server already running on port {port}")

# =========================
# DECORATOR (AUTO TRACK)
# =========================

def track_request(endpoint_name):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            REQUEST_COUNT.labels(endpoint=endpoint_name).inc()
            try:
                return await func(*args, **kwargs)
            finally:
                REQUEST_LATENCY.observe(time.time() - start_time)
        return wrapper
    return decorator