from agent_framework import Agent
from agent_framework.azure import AzureOpenAIChatClient
from tools import search_logs


def make_log_agent(client: AzureOpenAIChatClient) -> Agent:
    return Agent(
        client=client,
        name="LogAnalysisAgent",
        instructions=(
            "You are a site reliability engineer specializing in log analysis. "
            "Use the search_logs tool to fetch recent logs for the service named in the alert, "
            "then identify root causes, error patterns, and cascading failures. "
            "Be concise — 3-5 bullet points max."
        ),
        tools=[search_logs],
    )
