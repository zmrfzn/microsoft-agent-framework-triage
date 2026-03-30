"""
Triage tool functions — simulate Azure Monitor, Azure AI Search, SLI metrics.
In production: swap mock data for real SDK calls.
"""

import json
from pathlib import Path
from typing import Annotated

from pydantic import Field

DATA_DIR = Path(__file__).parent / "data"

try:
    RUNBOOKS = json.loads((DATA_DIR / "runbooks.json").read_text())
    _ALERTS = [
        json.loads((DATA_DIR / "alert.json").read_text()),
        json.loads((DATA_DIR / "alert2.json").read_text()),
    ]
except (FileNotFoundError, json.JSONDecodeError):
    RUNBOOKS = []
    _ALERTS = [{}]

# Alert is set at pipeline runtime via set_alert()
_current_alert: dict = {}


def set_alert(alert: dict) -> None:
    """Set the active alert for tool calls."""
    global _current_alert
    _current_alert = alert


def search_logs(
    service: Annotated[str, Field(description="Service name to fetch logs for")],
    time_window_minutes: Annotated[int, Field(description="Minutes of history to search")] = 30,
) -> str:
    """Fetch recent error logs for a service. Simulates Azure Monitor / Log Analytics query."""
    logs = _current_alert.get("logs_snippet", [])
    return json.dumps({
        "service": service,
        "window_minutes": time_window_minutes,
        "log_count": len(logs),
        "entries": logs,
        "anomalies_detected": ["OOMKilled", "connection timeout", "circuit breaker OPEN", "OutOfMemoryError"]
    }, indent=2)


def search_runbooks(
    keywords: Annotated[str, Field(description="Comma-separated single-word keywords (e.g. 'oom,memory,kubernetes')")],
) -> str:
    """Search runbook corpus for relevant remediation procedures. Simulates Azure AI Search."""
    terms = [k.strip().lower() for k in keywords.split(",")]
    matches = []
    for rb in RUNBOOKS:
        score = sum(1 for t in terms if t in rb["title"].lower() or any(t in tag for tag in rb["tags"]))
        if score > 0:
            matches.append({"score": score, **rb})
    matches.sort(key=lambda x: x["score"], reverse=True)
    return json.dumps({"query": keywords, "results": matches[:3]}, indent=2)


def score_severity(
    cpu_pct: Annotated[float, Field(description="CPU utilization percentage")],
    memory_pct: Annotated[float, Field(description="Memory utilization percentage")],
    error_rate_pct: Annotated[float, Field(description="Request error rate percentage")],
    p95_latency_ms: Annotated[float, Field(description="P95 latency in milliseconds")],
) -> str:
    """Calculate composite severity score (1=low, 5=critical) from SLI metrics."""
    score = 1
    if cpu_pct > 90 or memory_pct > 85: score += 2
    elif cpu_pct > 75 or memory_pct > 70: score += 1
    if error_rate_pct > 10: score += 2
    elif error_rate_pct > 1: score += 1
    if p95_latency_ms > 5000: score += 1
    score = min(score, 5)
    label = {1: "LOW", 2: "MODERATE", 3: "HIGH", 4: "CRITICAL", 5: "CRITICAL"}[score]
    return json.dumps({
        "severity_score": score,
        "severity_label": label,
        "inputs": {"cpu_pct": cpu_pct, "memory_pct": memory_pct,
                   "error_rate_pct": error_rate_pct, "p95_latency_ms": p95_latency_ms},
        "sla_breach": p95_latency_ms > 2000 or error_rate_pct > 1
    }, indent=2)
