# agents/

Specialist agent factories for the MAF Incident Triage pipeline.
Each file is self-contained and independently deployable to Azure AI Foundry Agent Service.

## Files

| File | Agent | Role | Tools |
|---|---|---|---|
| `log_agent.py` | `LogAnalysisAgent` | SRE log analyst — fetches and interprets error logs | `search_logs` |
| `runbook_agent.py` | `RunbookRAGAgent` | On-call engineer — searches runbook corpus for remediation steps | `search_runbooks` |
| `severity_agent.py` | `SeverityScorerAgent` | SRE lead — calculates composite severity score from SLI metrics | `score_severity` |
| `synthesis_agent.py` | `SynthesisAgent` | Incident commander — synthesizes specialist results into remediation report | none |
| `__init__.py` | — | Re-exports all four `make_*` factories | — |

## Usage

```python
from agents import make_log_agent, make_runbook_agent, make_severity_agent, make_synthesis_agent
from triage import make_client

client = make_client()
log_agent    = make_log_agent(client)
runbook_agent = make_runbook_agent(client)
severity_agent = make_severity_agent(client)
synthesis_agent = make_synthesis_agent(client)
```

## Pattern

Each factory follows the same shape:

```python
def make_<name>_agent(client: AzureOpenAIChatClient) -> Agent:
    return Agent(
        client=client,
        name="<AgentName>",
        instructions="...",
        tools=[...],   # empty for synthesis agent
    )
```

Tools are plain Python functions from `tools.py` — MAF auto-generates JSON Schema
from type annotations for LLM tool calling.

## Orchestration

All three specialist agents run **concurrently** via `ConcurrentBuilder` in `triage.py`.
The synthesis agent runs after, receiving the combined specialist output via `.with_aggregator()`.

## OTel

Each agent produces a named OTel span automatically (MAF zero-config observability).
Set `ENABLE_SENSITIVE_DATA=true` and `AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED=true`
to include prompt/completion content in spans.
