"""
MAF Incident Triage Pipeline — Streamlit Demo App
Experts Live India — Microsoft Agent Framework
"""

import asyncio
import json
import os
import time
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# # ── New Relic Python Agent (app-level, not pipeline-level) ────────────────────
# if os.getenv("NEW_RELIC_LICENSE_KEY"):
#     import newrelic.agent
#     newrelic.agent.initialize(environment="production")

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MAF Incident Triage",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Data ──────────────────────────────────────────────────────────────────────
DATA_DIR = Path(__file__).parent / "data"

@st.cache_data
def load_alerts():
    alert1 = json.loads((DATA_DIR / "alert.json").read_text())
    alert2 = json.loads((DATA_DIR / "alert2.json").read_text())
    return {"payment-api (INC-20240315-0042)": alert1, "auth-service (INC-20240822-0117)": alert2}

ALERTS = load_alerts()

ALERT_KEYS = list(ALERTS.keys()) + ["Random"]

# ── Architecture diagram ───────────────────────────────────────────────────────
ARCHITECTURE_DIAGRAM = """\
                Alert / Incident Event
                        │
                        ▼
          ┌─────────────────────────────┐
          │   Orchestrator Agent        │
          │   (GPT-4o via Foundry)      │
          └──────────────┬──────────────┘
                         │
               [concurrent handoff]
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
    ┌──────────┐  ┌──────────┐  ┌──────────┐
    │   Log    │  │ Runbook  │  │Severity  │
    │ Analysis │  │   RAG    │  │ Scorer   │
    │  Agent   │  │  Agent   │  │  Agent   │
    └────┬─────┘  └────┬─────┘  └────┬─────┘
         │              │              │
         └──────────────┼──────────────┘
                        │
               [results converge]
                        ▼
          ┌─────────────────────────────┐
          │     Synthesis Agent         │
          │   (Incident Commander)      │
          └──────────────┬──────────────┘
                         │
                         ▼
          ┌─────────────────────────────┐
          │  Remediation Report         │
          │  + OTel trace spans         │
          └─────────────────────────────┘
"""

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0078d4;
        margin-bottom: 0;
    }
    .subtitle {
        font-size: 1rem;
        color: #666;
        margin-top: 0.2rem;
        margin-bottom: 1.5rem;
    }
    .agent-running {
        color: #f0a500;
        font-family: monospace;
        font-size: 0.95rem;
    }
    .agent-done {
        color: #107c10;
        font-family: monospace;
        font-size: 0.95rem;
    }
    .agent-failed {
        color: #d13438;
        font-family: monospace;
        font-size: 0.95rem;
    }
    .timing-badge {
        background: #f0f6ff;
        border: 1px solid #0078d4;
        border-radius: 6px;
        padding: 6px 14px;
        font-size: 0.9rem;
        color: #0078d4;
        display: inline-block;
        margin-top: 8px;
    }
    .report-box {
        background: #f8f9fa;
        border-left: 4px solid #0078d4;
        border-radius: 4px;
        padding: 1.2rem 1.5rem;
        margin-top: 1rem;
    }
    .stCodeBlock {
        font-size: 0.85rem;
    }
    div[data-testid="stSidebar"] .stButton > button {
        background: #0078d4;
        color: white;
        font-weight: 600;
        font-size: 1rem;
        border-radius: 6px;
        border: none;
        padding: 0.6rem 1rem;
        width: 100%;
        margin-top: 0.5rem;
    }
    div[data-testid="stSidebar"] .stButton > button:hover {
        background: #005a9e;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<p class="main-title">MAF Incident Triage Pipeline</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Microsoft Agent Framework — Experts Live India</p>',
    unsafe_allow_html=True,
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Incident Alert")

    selected_key = st.selectbox(
        "Select Alert",
        options=ALERT_KEYS,
        index=0,
        help="Choose a pre-loaded incident or pick Random",
    )

    import random as _random
    if selected_key == "Random":
        alert_data = _random.choice(list(ALERTS.values()))
    else:
        alert_data = ALERTS[selected_key]

    with st.expander("Alert JSON", expanded=False):
        st.json(alert_data)

    st.divider()

    run_clicked = st.button("Run Triage", use_container_width=True)

    st.divider()
    st.caption("**MAF Patterns Used**")
    st.caption("• ConcurrentBuilder — parallel specialists")
    st.caption("• Synthesis Agent — converge results")
    st.caption("• OTel tracing → Azure Monitor")

# ── Session state ─────────────────────────────────────────────────────────────
if "running" not in st.session_state:
    st.session_state.running = False
if "result" not in st.session_state:
    st.session_state.result = None
if "elapsed" not in st.session_state:
    st.session_state.elapsed = None
if "last_alert" not in st.session_state:
    st.session_state.last_alert = None
if "agent_times" not in st.session_state:
    st.session_state.agent_times = {}

# ── Main area ─────────────────────────────────────────────────────────────────

def show_idle_diagram():
    """Show pipeline architecture when no triage has run yet."""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("Pipeline Architecture")
        st.code(ARCHITECTURE_DIAGRAM, language=None)
        st.caption(
            "Three specialist agents run **in parallel** via `ConcurrentBuilder`, "
            "then a Synthesis Agent produces the remediation report."
        )

async def run_triage_with_events(alert: dict, placeholders: dict) -> tuple[str, dict]:
    """Wrap the pipeline in a root OTel span so all agent spans share a common parent."""
    from agent_framework.observability import get_tracer
    tracer = get_tracer("maf-incident-triage")
    with tracer.start_as_current_span(
        "triage_pipeline",
        attributes={
            "alert.id": alert.get("alert_id", "unknown"),
            "alert.service": alert.get("service", "unknown"),
            "alert.severity": alert.get("severity_raw", "unknown"),
        },
    ):
        return await _run_triage_with_events_inner(alert, placeholders)


async def _run_triage_with_events_inner(alert: dict, placeholders: dict) -> tuple[str, dict]:
    from triage import make_client, make_log_agent, make_runbook_agent, make_severity_agent, make_synthesis_agent
    from agent_framework.orchestrations import ConcurrentBuilder
    from agent_framework._types import AgentResponse

    client = make_client()
    alert_text = json.dumps(alert, indent=2)

    AGENTS = ["LogAnalysisAgent", "RunbookRAGAgent", "SeverityScorerAgent"]
    agent_states = {name: {"status": "pending", "start": None, "end": None} for name in AGENTS}

    def render_specialist_status():
        lines = []
        for name in AGENTS:
            s = agent_states[name]
            if s["status"] == "pending":
                lines.append(f"  ◦ {name} — waiting...")
            elif s["status"] == "running":
                lines.append(f"  ▶ {name} — running...")
            elif s["status"] == "done":
                elapsed = f"{s['end'] - s['start']:.1f}s" if s["start"] and s["end"] else ""
                lines.append(f"  ✓ {name} — done ({elapsed})")
            elif s["status"] == "failed":
                lines.append(f"  ✗ {name} — FAILED")
        return "\n".join(lines)

    # Update: specialists starting
    placeholders["parallel_header"].markdown("**Running specialist agents in parallel...**")
    placeholders["specialist_status"].code(render_specialist_status(), language=None)

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

    stream = workflow.run(
        f"Analyze this incident alert:\n\n{alert_text}",
        stream=True,
    )

    agent_times = {}
    async for event in stream:
        if event.type == "executor_invoked" and event.executor_id:
            name = event.executor_id
            if name in agent_states:
                agent_states[name]["status"] = "running"
                agent_states[name]["start"] = time.time()
                agent_times[name] = {"start": agent_states[name]["start"]}
            placeholders["specialist_status"].code(render_specialist_status(), language=None)

        elif event.type == "executor_completed" and event.executor_id:
            name = event.executor_id
            if name in agent_states:
                agent_states[name]["status"] = "done"
                agent_states[name]["end"] = time.time()
                if name in agent_times:
                    agent_times[name]["end"] = agent_states[name]["end"]
            placeholders["specialist_status"].code(render_specialist_status(), language=None)

        elif event.type == "executor_failed" and event.executor_id:
            name = event.executor_id
            if name in agent_states:
                agent_states[name]["status"] = "failed"
                agent_states[name]["end"] = time.time()
            placeholders["specialist_status"].code(render_specialist_status(), language=None)

    specialist_result = await stream.get_final_response()
    outputs = specialist_result.get_outputs()
    combined = outputs[0] if outputs else ""

    # Update: synthesis phase
    placeholders["synthesis_status"].markdown("**Synthesizing remediation report...**")

    synthesis = make_synthesis_agent(client)
    synthesis_response = await synthesis.run(
        f"Original alert:\n{alert_text}\n\n"
        f"Specialist analysis:\n{combined}\n\n"
        f"Produce the remediation report."
    )

    return synthesis_response.text, agent_times


if run_clicked:
    st.session_state.running = True
    st.session_state.result = None
    st.session_state.elapsed = None
    st.session_state.last_alert = alert_data
    st.session_state.agent_times = {}

    # Build placeholders for live status
    st.subheader(f"Triaging: {alert_data.get('alert_id')} — {alert_data.get('title')}")
    status_container = st.container()

    with status_container:
        parallel_header_ph = st.empty()
        specialist_status_ph = st.empty()
        synthesis_status_ph = st.empty()
        complete_ph = st.empty()

    placeholders = {
        "parallel_header": parallel_header_ph,
        "specialist_status": specialist_status_ph,
        "synthesis_status": synthesis_status_ph,
        "complete": complete_ph,
    }

    t_start = time.time()

    try:
        report, agent_times = asyncio.run(run_triage_with_events(alert_data, placeholders))
        elapsed = time.time() - t_start

        st.session_state.result = report
        st.session_state.elapsed = elapsed
        st.session_state.last_alert = alert_data
        st.session_state.agent_times = agent_times
        st.session_state.running = False
        st.rerun()

    except Exception as exc:
        st.session_state.running = False
        st.error(f"Pipeline failed: {exc}")
        raise

elif st.session_state.result:
    # Show previously computed result
    alert_used = st.session_state.last_alert or alert_data
    st.subheader(f"Triage Complete: {alert_used.get('alert_id')} — {alert_used.get('title')}")

    # Timing summary
    elapsed = st.session_state.elapsed
    agent_times = st.session_state.agent_times

    if agent_times:
        parallel_durations = [
            v["end"] - v["start"]
            for v in agent_times.values()
            if "start" in v and "end" in v
        ]
        parallel_wall = max(parallel_durations) if parallel_durations else 0
        sum_serial = sum(parallel_durations)
        time_saved = sum_serial - parallel_wall if sum_serial > parallel_wall else 0
        timing_msg = (
            f"Pipeline completed in **{elapsed:.1f}s** "
            f"(3 agents ran in parallel — saved ~{time_saved:.1f}s vs serial)"
        )
    else:
        timing_msg = f"Pipeline completed in **{elapsed:.1f}s** (3 agents ran in parallel)"

    st.info(timing_msg)

    # Agent timing breakdown
    if agent_times:
        with st.expander("Agent timing breakdown", expanded=False):
            for name, times in agent_times.items():
                if "start" in times and "end" in times:
                    dur = times["end"] - times["start"]
                    st.caption(f"  ✓ {name}: {dur:.1f}s")

    # Remediation report
    st.subheader("Remediation Report")
    with st.container(border=True):
        st.markdown(st.session_state.result)

    st.divider()
    if st.button("Run another triage"):
        st.session_state.result = None
        st.session_state.elapsed = None
        st.rerun()

else:
    # Idle state — show architecture
    show_idle_diagram()
