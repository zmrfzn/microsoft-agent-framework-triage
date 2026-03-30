---
theme: dracula
title: "Microsoft Agent Framework: The Open-Source Engine for Agentic AI Apps"
info: |
  ## MAF Talk — Experts Live India
  Multi-agent incident triage pipeline on Azure AI Foundry
class: text-center
transition: slide-left
mdc: true
lineNumbers: true
---

# Microsoft Agent Framework

## The Open-Source Engine for Agentic AI Apps

<br>

**Experts Live India** · Level 200 · 30 min

<br>

> Building a real multi-agent incident triage pipeline on Azure AI Foundry

<!--
⏱ TIME: 1 min
🎙 TALKING POINTS:
- Introduce yourself, your role, and one sentence about why you care about agents
- "By the end of this talk, you'll have a running multi-agent pipeline you can fork and deploy"
- Don't linger, this is a warm-up slide
📌 TRANSITION: "Let me start with a question I keep hearing from every team I talk to…"
-->

---
transition: fade-out
---

# The Question Everyone Is Asking

<br>

> *"Is agentic AI actually production-ready, or is it still demos and hype?"*

<br>

<v-clicks>

- ✅ **What** the agent framework landscape looks like in 2026
- ✅ **Why** multi-agent is the future (and why it's hard)
- ✅ **How** Microsoft Agent Framework (MAF) solves the complexity
- ✅ **Demo:** A real multi-agent incident triage pipeline you can run today

</v-clicks>

<v-click>

> **Spoiler:** Microsoft's TRIANGLE system already runs 97% automated triage on **600M logs/day**. This is not theoretical.

</v-click>

<!--
⏱ TIME: 2 min
🎙 TALKING POINTS:
- Ask the question out loud, pause 3 seconds
- "I asked this same question 6 months ago. Today I'll show you the answer."
- Reveal bullets one by one to build anticipation
- Drop the TRIANGLE stat last as a credibility anchor
📌 TRANSITION: "To understand where we are, let's talk about where we came from…"
-->

---
transition: slide-left
---

# AutoGen vs Semantic Kernel: The Split

<br>

| | **AutoGen** | **Semantic Kernel** |
|---|---|---|
| Origin | Microsoft Research | Microsoft Product |
| Focus | Multi-agent conversations | Plugin/memory orchestration |
| Language | Python | Python + .NET + Java |
| Pattern | AssistantAgent + GroupChat | Kernel + Planners + Plugins |
| Problem | Research-grade, hard to ship | Single-agent centric |
| Timeline | 2023 → archived 2025 | 2023 → merged into MAF 2026 |

<v-click>

> Both were **great tools for their time**, but neither was the complete picture.

</v-click>

<!--
⏱ TIME: 2 min
🎙 TALKING POINTS:
- "If you've used either of these, you know the pain."
- Don't bash either. Acknowledge their legacy. Many in the audience may have used them.
- Emphasize the split: Research vs Product, multi-agent vs single-agent
- Click to reveal the punchline: "What if you could have both?"
📌 TRANSITION: "That's exactly what happened. Let me introduce MAF."
-->

---
transition: slide-up
---

# Microsoft Agent Framework (MAF)

### The unified successor to AutoGen + Semantic Kernel

<br>

```
  AutoGen (Research, 2023)
          \
           >──── Microsoft Agent Framework (MAF)
          /             |
  Semantic Kernel       └── on Azure AI Foundry
    (Product, 2023)
```

- 🔓 **Open-source:** `github.com/microsoft/agent-framework`
- 📦 **Install:** `pip install agent-framework --pre`
- ✅ **RC status:** Production-ready, March 2026
- 🧩 **Patterns:** Orchestrator, ConcurrentBuilder, HandoffBuilder
- 📊 **Tracing:** OpenTelemetry → Azure Monitor, built-in

<!--
⏱ TIME: 2 min
🎙 TALKING POINTS:
- "This is the convergence moment. AutoGen team + SK team → one framework, one SDK."
- Show the ASCII merge diagram, let it sink in
- Emphasize RC = not alpha, not beta. "You can build on this today."
- 🚫 Don't use AutoGen or Semantic Kernel directly, both are deprecated in favor of MAF
📌 TRANSITION: "So why multi-agent at all? Why not just one really good agent?"
-->

---
transition: slide-left
---

# What One Agent Can't Do Well

Imagine triaging a P1 incident with a single agent:

```
Alert → [Single GPT-4o agent]
         → analyzes logs
         → searches runbooks
         → scores severity
         → writes remediation
→ Result in ~60–90s (sequential, single thread)
```

- 🐢 **Sequential bottleneck:** each step blocks the next
- 🧠 **Context overload:** all knowledge crammed into one prompt
- 🔧 **Tool conflicts:** generalist vs specialist tension
- ❌ **No isolation:** one bad tool call corrupts the whole run

<!--
⏱ TIME: 2 min
🎙 TALKING POINTS:
- "Raise your hand if you've built a single-agent system and hit a wall." (audience engagement)
- Walk through the sequential flow. 60–90s is too slow for a P1
- Isolation is key: "One hallucinated search result poisons the severity score AND the remediation."
📌 TRANSITION: "What if each of these steps was a separate specialist, running at the same time?"
-->

---
transition: fade-out
---

# Why Multi-Agent Changes Everything

<div class="grid grid-cols-2 gap-8">

<div>

### ⚡ Parallelism
Run specialists concurrently: log analysis + runbook search + severity scoring **all at once**

</div>

<div>

### 🎯 Specialization
Each agent gets its own system prompt, tools, and scope

</div>

<div>

### 🛡️ Resilience
One agent fails → others still complete. Per-agent retry strategies.

</div>

<div>

### 🔍 Observability
Each agent = a named OTel span. Debug any agent in isolation.

</div>

</div>

<v-click>

> **Microsoft TRIANGLE:** 97% triage accuracy · 600M logs/day &nbsp;|&nbsp; **BMW:** 12× faster fleet analysis

</v-click>

<!--
⏱ TIME: 2 min
🎙 TALKING POINTS:
- Walk the 4 quadrants: parallelism (speed), specialization (quality), resilience (reliability), observability (debugging)
- "Each of these solves a real problem we just saw on the previous slide"
- Final click: proof points, let the numbers land
📌 TRANSITION: "But multi-agent isn't free. It comes with its own complexity tax."
-->

---
transition: slide-left
---

# The Multi-Agent Complexity Problem

### What gets hard when you go multi-agent:

- 🔀 **Orchestration:** Who decides what runs when?
- 📦 **State:** How do results flow between agents safely?
- 🌐 **Consistency:** How do you avoid conflicting agent outputs?
- 🔍 **Debugging:** How do you trace a failure across 4 agents?
- 💸 **Cost:** Multi-agent = 3–10× token usage. Who's watching?

<v-click>

### MAF's answer:

```python
ConcurrentBuilder()   # run agents in parallel, collect results
HandoffBuilder()      # fan-in: pass results to synthesis agent
```

OTel tracing is **automatic**, one named span per agent call

</v-click>

<!--
⏱ TIME: 2 min
🎙 TALKING POINTS:
- Let the audience read the 5 challenges
- Cost: "If you have 4 agents each using GPT-4o, your token bill just 4x'd."
- Click reveal: "MAF gives you ConcurrentBuilder and HandoffBuilder. That's the answer."
⚠️ CODE NOTE (for code walkthrough): In this demo, convergence is handled via
  `.with_aggregator()` on ConcurrentBuilder — not a separate HandoffBuilder invocation.
  Both are valid MAF patterns. `.with_aggregator()` is a callback that receives all
  agent results and returns the combined string passed to the synthesis agent.
  HandoffBuilder is used for sequential A→B→C handoff chains; for fan-out/fan-in,
  .with_aggregator() is the idiomatic choice.
🔗 KEY LINKS (for QR codes later):
- ConcurrentBuilder: https://github.com/microsoft/agent-framework/blob/main/docs/orchestrations/concurrent.md
- HandoffBuilder: https://github.com/microsoft/agent-framework/blob/main/docs/orchestrations/handoff.md
- OTel integration: https://github.com/microsoft/agent-framework/blob/main/docs/tracing.md
- Samples: https://github.com/microsoft/Agent-Framework-Samples
📌 TRANSITION: "Let me give you a mental model for where multi-agent maturity stands."
-->

---
transition: slide-up
---

# The Multi-Agent Maturity Model

<br>

```
┌────────────────────────────────────────────────┐
│                                                │
│  Level 4: Self-Organizing Agent Mesh  ← future │
│           Autonomous agent spawning            │
│                                                │
│  Level 3: Concurrent Specialist Pool  ← demo⭐ │
│           Parallel experts + synthesis         │
│                                                │
│  Level 2: Sequential Agent Chain               │
│           A → B → C handoff                    │
│                                                │
│  Level 1: Single Agent + Tools    ← most teams │
│           One agent, multiple tools            │
│                                                │
└────────────────────────────────────────────────┘
```

<v-click>

> Today we build **Level 3**. Most production systems are still Level 1.

</v-click>

<!--
⏱ TIME: 1.5 min
🎙 TALKING POINTS:
- "This is a framework I use to think about multi-agent maturity."
- Point at Level 1: "This is where most teams are today."
- Point at Level 3: "This is what we're about to demo."
- Level 4: "Where the research is heading. Not production-ready yet."
- Click reveal: "The jump from 1 to 3 is the biggest ROI you can get right now."
📌 TRANSITION: "OK, let's build Level 3. Here's the scenario."
-->

---
transition: fade-out
---

# Demo: Payment API Is Down 🚨

```json
{
  "alert_id": "INC-20240315-0042",
  "service": "payment-api",
  "title": "High CPU + memory spike on payment-api pods",
  "description": "CPU: 94%, Memory: 87%, CrashLoopBackOff,
                   P95 latency: 12s (SLA: 2s), Error rate: 18%"
}
```

1. Alert lands → **Orchestrator** decomposes the incident
2. **Three specialist agents** fan out in parallel
3. **Synthesis agent** produces the remediation report

> Same pattern as Microsoft TRIANGLE · Completed in ~15 seconds

<!--
⏱ TIME: 1.5 min
🎙 TALKING POINTS:
- "This is a realistic P1 alert. If you've done on-call, you've seen these at 3am."
- Read the JSON briefly: CPU 94%, CrashLoopBackOff, 12s P95 (SLA is 2s), 18% error rate
- Walk through the 3 steps: decompose → parallel → synthesize
⚠️ DEMO NOTE: The demo actually has TWO alert scenarios (payment-api OOM + auth-service
  Redis exhaustion) and picks one randomly each run. Both produce equally interesting output.
  If the demo shows the auth-service alert, just swap "payment-api" for "auth-service" in narration.
📌 TRANSITION: "Here's the architecture."
-->

---
transition: slide-left
---

# Architecture: The Triage Pipeline

```
  Alert Event
      │
      ▼
  Orchestrator Agent
      │
      ├── ConcurrentBuilder (parallel) ──┐
      │                                  │
      ▼            ▼             ▼       │
  Log Agent    Runbook Agent  Severity   │
  (Monitor)    (AI Search)    Scorer     │
      │            │             │       │
      └────────────┴─────────────┘       │
                   │                     │
      HandoffBuilder (converge) ─────────┘
                   │
                   ▼
           Synthesis Agent
                   │
                   ▼
        Remediation Report + OTel spans
```

<!--
⏱ TIME: 2 min
🎙 TALKING POINTS:
- Walk top-to-bottom slowly. This is the slide people will photograph
- "Alert → orchestrator → fans out to 3 specialists via ConcurrentBuilder"
- "All three run at the SAME TIME. No waiting."
- "Results converge via HandoffBuilder → synthesis agent writes the report."
⚠️ ARCHITECTURE NOTE (if asked about the Orchestrator Agent):
  In this demo, the orchestrator logic is embedded inside ConcurrentBuilder for
  simplicity — the builder itself decides to fan out to all three specialists in
  parallel. There is no separate GPT-4o orchestrator agent making that decision.
  In a production system you'd add an explicit orchestrator agent that first
  analyses the alert, then decides WHICH specialists to invoke and with what context.
  For a Level 200 demo the builder pattern is cleaner and easier to follow.
⚠️ ARCHITECTURE NOTE (if asked about HandoffBuilder in the diagram):
  The diagram shows HandoffBuilder conceptually for the converge step. In the actual
  code, convergence is via .with_aggregator() on ConcurrentBuilder (a callback that
  receives all AgentExecutorResponse objects). HandoffBuilder is used for sequential
  chain patterns (A hands off to B which hands off to C). Both serve fan-in purposes;
  .with_aggregator() is the right choice here because all three specialists run in the
  same ConcurrentBuilder context.
📌 TRANSITION: "Let me show you the code."
-->

---
transition: slide-left
---

# Project Structure

```
AgentFramework/
├── triage.py          ← pipeline entrypoint (ConcurrentBuilder + run_triage)
├── tools.py           ← search_logs · search_runbooks · score_severity
├── agents/
│   ├── log_agent.py        ← LogAnalysisAgent
│   ├── runbook_agent.py    ← RunbookRAGAgent
│   ├── severity_agent.py   ← SeverityScorerAgent
│   └── synthesis_agent.py  ← SynthesisAgent (incident commander)
├── data/
│   ├── alert.json     ← payment-api P1 incident
│   └── runbooks.json  ← remediation playbooks
└── app.py             ← Streamlit demo UI
```

<v-click>

> Each agent is **independently deployable** to Azure AI Foundry Agent Service

</v-click>

<!--
⏱ TIME: 1 min
🎙 TALKING POINTS:
- "This is the full project. 5 Python files + data."
- "triage.py is the entrypoint — it's the orchestration only. No tool logic, no agent definitions."
- "Each agent file is self-contained — its own instructions, its own tools."
- "In production: deploy each agent independently via Foundry Agent Service. Same code."
- Click reveal: "That's the architecture payoff — you get independent deployability for free."
📌 TRANSITION: "Let's look at the tools first."
-->

---
transition: slide-left
---

# Code: Specialist Tools

```python {all|1-3|4-7|9-11|13-17|all}
def search_logs(
    service: str, time_window_minutes: int = 30
) -> str:
    """Azure Monitor / Log Analytics query."""
    logs = ALERT.get("logs_snippet", [])
    return json.dumps({
        "anomalies_detected": ["OOMKilled", "connection timeout"]
    })

def search_runbooks(keywords: str) -> str:
    """Azure AI Search over runbook corpus."""
    ...

def score_severity(
    cpu_pct: float, memory_pct: float,
    error_rate_pct: float, p95_latency_ms: float
) -> str:
    """Composite severity score (1-5) from SLI metrics."""
    ...
```

<v-click>

> **Type-annotated Python** → MAF auto-generates JSON Schema for the LLM

</v-click>

<!--
⏱ TIME: 2 min
🎙 TALKING POINTS:
- Line highlighting walks through each tool function
- "Plain Python functions. Not classes, not plugins, not decorators."
- "MAF reads type annotations + docstrings → auto-generates JSON Schema for GPT-4o"
- "In production: swap mock data for Azure Monitor SDK, Azure AI Search. Zero code structure change."
📌 TRANSITION: "Now let's wire these tools into agents and run them in parallel."
-->

---
transition: slide-left
---

# Code: ConcurrentBuilder + Synthesis

```python {all|1-2|4-8|10-12|14-17|all}
async def run_triage(alert: dict) -> str:
    client = make_client()  # AzureOpenAIChatClient

    # Step 1: Three specialists in parallel
    concurrent = ConcurrentBuilder()
    concurrent.add_agent(make_log_agent(client))
    concurrent.add_agent(make_runbook_agent(client))
    concurrent.add_agent(make_severity_agent(client))

    results = await concurrent.run(
        f"Analyze this incident:\n{json.dumps(alert)}"
    )

    # Step 2: Synthesis, all results converge
    synthesis = make_synthesis_agent(client)
    report = await synthesis.run(combined_results)
    return report
```

<v-click>

> **17 lines of orchestration.** That's the entire multi-agent pipeline.

</v-click>

<!--
⏱ TIME: 2 min
🎙 TALKING POINTS:
- Line highlighting walks through: client → concurrent setup → run → synthesis
- "concurrent.run fires all 3 in parallel. You await the result dict."
- "The synthesis agent gets ALL results combined and writes the report."
- "async/await. MAF is async-native."
📌 TRANSITION: "Now let's see it run live."
-->

---
layout: center
transition: fade-out
---

# 🎬 Live Demo

### Triage Pipeline in Action

<v-clicks>

1. 📥 **Alert ingested** from `data/alert.json`
2. 🚀 **Specialist agents fan out** → 3 parallel calls to GPT-4o
3. 📋 **Results converge** → synthesis agent writes remediation report
4. ⏱️ **Timing output** → parallel vs sequential speedup
5. 🔍 **OTel traces** → spans visible in Azure AI Foundry portal

</v-clicks>

<v-click>

```bash
python triage.py
```

> Let's watch 3 AI specialists triage a P1 incident in real-time ⚡

</v-click>

<!--
⏱ TIME: 6 min (pre-recorded demo + live narration)
🎙 TALKING POINTS:
- Switch to terminal / pre-recorded video
- Click through the 5 steps as the demo progresses
- Narrate: "Alert loaded... orchestrator decomposing... all 3 specialists kick off at once"
- Point out timing: "Log agent: 4s, Runbook: 3s, Severity: 2s, but total only 4s because parallel"
- Show remediation report output
- If time: show Foundry portal OTel trace spans
📌 TRANSITION: "So how do you set this up yourself?"
-->

---
transition: slide-left
disabled: true
---

# Getting Started with MAF

<v-click>

### 1. Install

```bash
pip install agent-framework[azure] --pre
pip install azure-identity python-dotenv
```

</v-click>

<v-click>

### 2. Configure

```bash
# .env file
AZURE_OPENAI_ENDPOINT=https://<resource>.openai.azure.com/
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=gpt-4o
```

</v-click>

<v-click>

### 3. Auth (zero keys in code)

```bash
az login
```

</v-click>

<v-click>

### The core imports:

```python
from agent_framework import Agent
from agent_framework.azure import AzureOpenAIChatClient
from agent_framework.orchestrations import ConcurrentBuilder, HandoffBuilder
```

</v-click>

<!--
⏱ TIME: 1.5 min
🎙 TALKING POINTS:
- Reveal each step on click. "Three steps. That's it."
- "No API keys in code. AzureCliCredential handles auth via your az login session."
- "For .NET: dotnet add package Microsoft.Agents.AI.OpenAI --prerelease"
📌 TRANSITION: "Now let me be honest about what works and what doesn't yet."
-->

---
transition: fade-out
---

# What MAF Gets Right ✅

- 🧩 **Clean orchestration primitives:** `ConcurrentBuilder` + `HandoffBuilder` = fan-out/fan-in in 5 lines
- 📊 **Zero-config observability:** every agent call → named OTel span, no instrumentation needed
- 🚀 **RC = production-ready today.** Not alpha, not beta. Ship with confidence.

<v-click>

### Proven at scale

| System | Result |
|---|---|
| **Microsoft TRIANGLE** | 97% triage accuracy · 600M logs/day |
| **BMW Fleet Analysis** | 12× faster test-fleet data processing |

</v-click>

<v-click>

> These are **the same ConcurrentBuilder + HandoffBuilder patterns** we just demoed.

</v-click>

<!--
⏱ TIME: 1.5 min
🎙 TALKING POINTS:
- Three strengths are visible immediately. Keep it punchy.
- OTel: "I've shipped systems where 60% of the code was observability plumbing. With MAF, it's zero."
- Reveal the proof table: "TRIANGLE: 600M log lines daily. Same pattern as our 17-line pipeline."
📌 TRANSITION: "But let me be honest about what's not there yet."
-->

---
transition: slide-left
---

# The Honest Gaps 🔧

| Gap | Why It Matters |
|---|---|
| **Cross-agent DAG debugging** | Spans exist, but causality across 4+ agents is manual |
| **Shared intermediate state** | Message passing ≠ shared memory |
| **Per-agent cost tracking** | 10× token bill with no per-agent breakdown |
| **Human-in-the-loop** | Approval gates need to be a primitive |
| **Agent unit testing** | Need `pytest-maf` with mock LLM fixtures |
| **Agent identity / RBAC** | One credential for all agents today |

<v-click>

> The framework is ready. The **tooling ecosystem** is 12–18 months behind.

</v-click>

<!--
⏱ TIME: 2 min
🎙 TALKING POINTS:
- "This is my honest assessment. I'm bullish on MAF, but I want to be transparent."
- Pick 3 to elaborate:
  1. Cost tracking: "I ran a 5-agent pipeline in dev. My Azure bill tripled."
  2. HITL: "Imagine an agent recommending 'delete this prod database'. You want a checkpoint."
  3. Testing: "How do you unit test an agent? We need pytest-maf."
- Click reveal: "The framework is solid. The ecosystem is where contributions matter most."
📌 TRANSITION: "So let me leave you with three things to remember."
-->

---
transition: slide-up
---

# Three Things to Remember

<v-click>

### 1️⃣ MAF is the unified successor
AutoGen + Semantic Kernel → **one framework, one SDK**

</v-click>

<v-click>

### 2️⃣ Multi-agent ≠ complexity tax
`ConcurrentBuilder` + `HandoffBuilder` = orchestration in **5 lines**, not 500

</v-click>

<v-click>

### 3️⃣ OTel + Foundry = your debugging superpower
Every agent action → **named spans, zero config**

</v-click>

<v-click>

> **Agentic AI is not hype. It's engineering.**

</v-click>

<!--
⏱ TIME: 1.5 min
🎙 TALKING POINTS:
- "If you forget everything else, remember these three."
- Click each one, let it land
- 1: "If someone starts a new project with AutoGen or SK, redirect them to MAF."
- 2: "The biggest fear is 'multi-agent is too complex'. It's not."
- 3: "When an agent hallucinates at 3am, you need traces, not logs."
- Final click: "Agentic AI is not hype. It's engineering." (pause)
📌 TRANSITION: "Here are the links."
-->

---
transition: fade-out
---

# Let's Build This Together

<div class="grid grid-cols-2 gap-4 items-center">

<div>

### Code from this talk

```
github.com/microsoft/agent-framework
github.com/microsoft/Agent-Framework-Samples
```

### Reading

- [MAF Intro Blog](https://devblogs.microsoft.com/foundry/introducing-microsoft-agent-framework)
- [MAF RC Announcement](https://devblogs.microsoft.com/foundry/microsoft-agent-framework-reaches-release-candidate)

### Connect

🔗 [linkedin.com/in/zmrfzn](https://linkedin.com/in/zmrfzn)

</div>

<div class="flex flex-col items-center">

<img src="/linkedin-qr.png" class="w-40 h-40 rounded-lg" alt="LinkedIn QR Code" />

<p class="text-sm opacity-60 mt-1">Scan to connect on LinkedIn</p>

</div>

</div>

The question is not *if* you'll build multi-agent systems, it's *when* and *how well*.

> Find me after the talk · Questions?

<!--
⏱ TIME: 1 min (then Q&A)
🎙 TALKING POINTS:
- "All the code is on GitHub. Fork it, run it, break it."
- Point at the QR code: "Scan this to connect on LinkedIn, I'd love to hear what you build."
- If Q&A: "how does this compare to LangGraph?" → "Great but not Azure-native. MAF has OTel + Foundry + managed identity built-in."
- If Q&A: "non-Azure models?" → "MAF supports OpenAI directly too, but Azure gives you managed identity + OTel for free."

TOTAL TIMING BUDGET (30 min):
  Slides 1–4:   7 min   (landscape/context)
  Slides 5–8:   7.5 min (why multi-agent + maturity)
  Slides 9–12:  6 min   (demo setup + code tour)
  Slide 13:     6 min   (LIVE DEMO)
  Slides 15–18: 6.5 min (honest take + close)
  Slide 14:     SKIPPED
  Buffer/Q&A:   ~3 min
-->
