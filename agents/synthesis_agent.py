from agent_framework import Agent
from agent_framework.azure import AzureOpenAIChatClient


def make_synthesis_agent(client: AzureOpenAIChatClient) -> Agent:
    return Agent(
        client=client,
        name="SynthesisAgent",
        instructions=(
            "You are the incident commander. You receive analysis from three specialist agents "
            "(log analysis, runbook lookup, severity scoring) and synthesize them into a "
            "structured remediation report. Format your output as:\n\n"
            "## Incident Summary\n"
            "## Root Cause (from logs)\n"
            "## Severity Assessment\n"
            "## Recommended Actions (from runbooks, prioritized)\n"
            "## Escalation Path\n"
        ),
    )
