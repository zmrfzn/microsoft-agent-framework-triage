"""
MAF Incident Triage Pipeline — entrypoint and orchestration only.
Experts Live India — Microsoft Agent Framework demo

Architecture:
  Alert → [LogAgent | RunbookAgent | SeverityAgent] (parallel) → SynthesisAgent
"""

import asyncio
import json
import os
import random
from pathlib import Path

from dotenv import load_dotenv

from agent_framework.orchestrations import ConcurrentBuilder
from agent_framework.azure import AzureOpenAIChatClient
from agents import make_log_agent, make_runbook_agent, make_severity_agent, make_synthesis_agent
from tools import set_alert, _ALERTS

load_dotenv()

# ── OTel Tracing ──────────────────────────────────────────────────────────────
def _setup_tracing() -> None:
    from agent_framework.observability import enable_instrumentation, create_resource, create_metric_views
    exporters_enabled = []

    if conn_str := os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
        os.environ.setdefault("OTEL_SERVICE_NAME", "maf-incident-triage")
        from azure.monitor.opentelemetry import configure_azure_monitor
        configure_azure_monitor(
            connection_string=conn_str,
            views=create_metric_views(),
            resource=create_resource(),
        )
        enable_instrumentation(enable_sensitive_data=True)
        exporters_enabled.append("Azure Monitor")

    if nr_key := os.getenv("NEW_RELIC_LICENSE_KEY"):
        import requests
        from opentelemetry import trace
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        session = requests.Session()
        session.verify = False
        nr_endpoint = os.environ.get("NEW_RELIC_OTLP_ENDPOINT", "https://otlp.nr-data.net:4318/v1/traces")
        trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(OTLPSpanExporter(
            endpoint=nr_endpoint,
            headers={"api-key": nr_key},
            session=session,
        )))
        exporters_enabled.append("New Relic")

    if exporters_enabled:
        if "Azure Monitor" not in exporters_enabled:
            from agent_framework.observability import configure_otel_providers
            configure_otel_providers()
        print(f"OTel tracing → {', '.join(exporters_enabled)}")

_setup_tracing()

# ── Data ──────────────────────────────────────────────────────────────────────
ALERT = random.choice(_ALERTS) if _ALERTS and _ALERTS[0] else {}

# ── Azure Client ──────────────────────────────────────────────────────────────
def make_client() -> AzureOpenAIChatClient:
    """Create Azure OpenAI client using API key and cognitiveservices endpoint."""
    import httpx
    from openai import AsyncAzureOpenAI

    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    if not api_key or not endpoint:
        raise ValueError("AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT are required.")
    ssl_verify = os.environ.get("AZURE_OPENAI_DISABLE_SSL", "false").lower() != "true"
    async_client = AsyncAzureOpenAI(
        api_key=api_key,
        azure_endpoint=endpoint,
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
        http_client=httpx.AsyncClient(verify=ssl_verify),
    )
    return AzureOpenAIChatClient(
        async_client=async_client,
        deployment_name=os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME", "gpt-5-nano"),
    )


# ── Pipeline ──────────────────────────────────────────────────────────────────
async def run_triage(alert: dict) -> str:
    from opentelemetry import trace
    tracer = trace.get_tracer("maf-incident-triage")

    with tracer.start_as_current_span(
        "triage_pipeline",
        attributes={
            "alert.id": alert.get("alert_id", "unknown"),
            "alert.service": alert.get("service", "unknown"),
            "alert.severity": alert.get("severity_raw", "unknown"),
        },
    ):
        return await _run_triage_inner(alert)


async def _run_triage_inner(alert: dict) -> str:
    set_alert(alert)  # wire alert into tool functions
    client = make_client()
    alert_text = json.dumps(alert, indent=2)

    print("\n[1/2] Specialist agents running in parallel...")

    def combine_specialist_results(results: list) -> str:
        return "\n\n---\n\n".join(
            f"### {r.executor_id}\n{r.agent_response.text}"
            for r in results
        )

    workflow = (
        ConcurrentBuilder(
            participants=[
                make_log_agent(client),
                make_runbook_agent(client),
                make_severity_agent(client),
            ]
        )
        .with_aggregator(combine_specialist_results)
        .build()
    )

    from agent_framework._types import AgentResponse
    stream = workflow.run(f"Analyze this incident alert:\n\n{alert_text}", stream=True)
    async for event in stream:
        if event.type == "executor_invoked" and event.executor_id:
            print(f"  ▶ {event.executor_id} started")
        elif event.type == "executor_completed" and event.executor_id:
            print(f"  ✓ {event.executor_id} done")
        elif event.type == "executor_failed" and event.executor_id:
            print(f"  ✗ {event.executor_id} FAILED: {event.details}")
        elif event.type == "data" and event.executor_id:
            if isinstance(event.data, AgentResponse) and event.data.text:
                print(f"\n  [{event.executor_id}]\n{event.data.text}\n")

    specialist_result = await stream.get_final_response()
    outputs = specialist_result.get_outputs()
    combined = outputs[0] if outputs else ""

    print("[2/2] Synthesizing remediation report...")
    synthesis = make_synthesis_agent(client)
    synthesis_response = await synthesis.run(
        f"Original alert:\n{alert_text}\n\n"
        f"Specialist analysis:\n{combined}\n\n"
        f"Produce the remediation report."
    )

    return synthesis_response.text


# ── Entrypoint ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if not ALERT:
        raise SystemExit("ERROR: data/alert.json not found. Run from the project root directory.")
    print(f"Triaging alert: {ALERT['alert_id']} — {ALERT['title']}\n")
    report = asyncio.run(run_triage(ALERT))
    print("\n" + "=" * 60)
    print("REMEDIATION REPORT")
    print("=" * 60)
    print(report)
