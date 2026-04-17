from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient
from tools import score_severity


def make_severity_agent(client: OpenAIChatClient) -> Agent:
    return Agent(
        client=client,
        name="SeverityScorerAgent",
        instructions=(
            "You are an SRE lead responsible for incident classification. "
            "Use the score_severity tool with metrics from the alert to calculate "
            "a severity score. Return: score (1-5), label, SLA breach status, and "
            "recommended response time (P1=15min, P2=1hr, P3=4hr, P4=next day)."
        ),
        tools=[score_severity],
    )
