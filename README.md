# Microsoft Agent Framework — Incident Triage Demo

Demo code for the talk **"Microsoft Agent Framework: The Open-Source Engine for Agentic AI Apps"** at **Experts Live India**.

Multi-agent incident triage pipeline using [Microsoft Agent Framework (MAF)](https://github.com/microsoft/agent-framework) on Azure AI Foundry. Three specialist agents run in parallel, converge via an aggregator, and produce a structured remediation report — all fully traced via OpenTelemetry.

---

## Architecture

```
Alert
  │
  ├─[parallel]──────────────────────┐
  ▼           ▼            ▼        │
LogAgent   RunbookAgent  SeverityAgent
  │           │            │
  └─[with_aggregator()]────┘
             │
             ▼
       SynthesisAgent
             │
             ▼
     Remediation Report + OTel traces
```

- **`ConcurrentBuilder`** — fans out to 3 parallel specialist agents
- **`.with_aggregator()`** — merges results before synthesis
- **`Agent`** — each specialist is standalone and independently deployable

---

## Prerequisites

- Python 3.11+
- [`uv`](https://github.com/astral-sh/uv) package manager
- Azure AI Foundry project with a deployed model
- (Optional) [Docker](https://docs.docker.com/get-docker/) — for running Arize Phoenix locally
- (Optional) New Relic account for APM + OTLP traces

---

## Setup

```bash
# Clone
git clone https://github.com/zmrfzn/microsoft-agent-framework-triage.git
cd microsoft-agent-framework-triage

# Create venv and install deps
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Azure AI Foundry credentials
```

### Required `.env` vars

```env
AZURE_OPENAI_ENDPOINT=https://<your-hub>.cognitiveservices.azure.com/
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=<model-deployment-name>
AZURE_OPENAI_API_KEY=<your-api-key>

# Full span content (inputs/outputs in traces)
ENABLE_SENSITIVE_DATA=true
AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED=true

# Corporate proxy SSL bypass (if needed)
AZURE_OPENAI_DISABLE_SSL=true
```

---

## Observability

The pipeline emits [OpenTelemetry](https://opentelemetry.io/) traces using the Gen AI semantic conventions (`gen_ai.*` spans). All three exporters below are optional and independently enabled via environment variables.

### Arize Phoenix (local, OSS)

[Arize Phoenix](https://phoenix.arize.com/) is a free, open-source observability UI that speaks standard OTLP — no SDK changes needed.

```bash
# Start Phoenix (data persists in ~/.phoenix)
docker run -d -p 6006:6006 -v ~/.phoenix:/root/.phoenix \
  --name phoenix arizephoenix/phoenix:latest
```

Then add to `.env`:

```env
PHOENIX_COLLECTOR_ENDPOINT=http://localhost:6006
```

Open [http://localhost:6006](http://localhost:6006) to view traces. Each triage run produces a `triage_pipeline` root span with all specialist and synthesis agent spans nested underneath.

### Azure Monitor / Foundry Tracing

```env
APPLICATIONINSIGHTS_CONNECTION_STRING=<your-connection-string>
```

### New Relic

```env
NEW_RELIC_LICENSE_KEY=<your-ingest-license-key>
# NEW_RELIC_OTLP_ENDPOINT=https://otlp.nr-data.net:4318/v1/traces  # EU: otlp.eu01.nr-data.net
```

All three exporters can be active simultaneously.

---

## Running

### CLI

```bash
source .venv/bin/activate
python triage.py
```

### Streamlit demo UI

```bash
streamlit run app.py
```

### With New Relic APM

```bash
./run_demo.sh
```

### Slides (Slidev)

```bash
cd docs/slides
npm install
npx @slidev/cli --open
```

---

## Project Structure

```
AgentFramework/
├── triage.py               ← Pipeline entrypoint (ConcurrentBuilder + run_triage)
├── tools.py                ← search_logs · search_runbooks · score_severity
├── agents/
│   ├── log_agent.py        ← LogAnalysisAgent
│   ├── runbook_agent.py    ← RunbookRAGAgent
│   ├── severity_agent.py   ← SeverityScorerAgent
│   └── synthesis_agent.py  ← SynthesisAgent (incident commander)
├── app.py                  ← Streamlit demo UI
├── run_demo.sh             ← Launch script (NR APM + SSL bypass)
├── newrelic.ini            ← New Relic agent config
├── data/
│   ├── alert.json          ← Payment-API P1 incident
│   ├── alert2.json         ← Auth-service incident
│   └── runbooks.json       ← OOMKilled, DB pool, circuit breaker runbooks
└── docs/antigravity/slidev/ ← Slidev presentation (slides.md)
```

---

## Talk Resources

- [MAF Intro Blog](https://devblogs.microsoft.com/foundry/introducing-microsoft-agent-framework-the-open-source-engine-for-agentic-ai-apps/)
- [MAF RC Blog](https://devblogs.microsoft.com/foundry/microsoft-agent-framework-reaches-release-candidate/)
- [MAF GitHub](https://github.com/microsoft/agent-framework)
- [Agent Framework Samples](https://github.com/microsoft/Agent-Framework-Samples)

---

## License

MIT
