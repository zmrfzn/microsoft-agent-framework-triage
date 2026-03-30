# Context — MAF Incident Triage Talk (Experts Live India)

Paste this at the start of any new Claude or Claude Code session to restore
full context for this project.

---

## Session Context

I am building a conference talk demo for **Experts Live India** (30 min, Level 200).

**Talk title:** Microsoft Agent Framework: The Open-Source Engine for Agentic AI Apps

**Status:** Demo complete and working. Slides complete (Slidev).

---

## What Has Been Built

A multi-agent incident triage pipeline using Microsoft Agent Framework (MAF):

- `triage.py` — pipeline entrypoint using `ConcurrentBuilder` + synthesis agent
- `tools.py` — `search_logs`, `search_runbooks`, `score_severity` (mock Azure integrations)
- `agents/` — 4 agent factories: LogAnalysisAgent, RunbookRAGAgent, SeverityScorerAgent, SynthesisAgent
- `app.py` — Streamlit demo UI (on `streamlit-demo` branch)
- Two alert scenarios: payment-api OOM (INC-20240315-0042), auth-service Redis exhaustion (INC-20240822-0117)
- OTel tracing: New Relic OTLP working; Azure Monitor wired but Foundry portal not yet showing spans

## Architecture

```
Alert --> [ConcurrentBuilder]
               |
   ┌───────────┼───────────┐
   ▼           ▼           ▼
LogAgent  RunbookAgent  SeverityAgent
   └───────────┼───────────┘
         [.with_aggregator()]
               |
         SynthesisAgent
               |
        Remediation Report
        + OTel trace spans
```

MAF patterns: `ConcurrentBuilder` + `.with_aggregator()` (not HandoffBuilder in code,
though HandoffBuilder is referenced conceptually in slides)

---

## Framework and Stack

- **MAF** `agent-framework==1.0.0rc5` — unified successor to AutoGen + Semantic Kernel
- Do NOT use AutoGen or Semantic Kernel directly
- Python 3.11, `uv` for package management
- Azure OpenAI `gpt-5-nano` on `devrel-aim-resource.cognitiveservices.azure.com`
- API version: `2024-12-01-preview`
- App Insights: `maf-demo-insights` linked to `maf-triage` Foundry project

---

## Running

```bash
# CLI
source .venv/bin/activate && python triage.py

# Streamlit (streamlit-demo branch)
streamlit run app.py

# With New Relic APM
./run_demo.sh
```

Add `AZURE_OPENAI_DISABLE_SSL=true` to `.env` if on corporate proxy.

---

## Key Links

- MAF intro: https://devblogs.microsoft.com/foundry/introducing-microsoft-agent-framework-the-open-source-engine-for-agentic-ai-apps/
- MAF RC: https://devblogs.microsoft.com/foundry/microsoft-agent-framework-reaches-release-candidate/
- MAF GitHub: https://github.com/microsoft/agent-framework
- Samples: https://github.com/microsoft/Agent-Framework-Samples
- Slides: `docs/antigravity/slidev/slides.md`

---

## Open Items

- Foundry portal Tracing tab not showing spans — needs portal action:
  connect `maf-demo-insights` to `maf-triage` project in Foundry portal
- Task 8 (demo polish — timing output, v1.0 tag) not done
