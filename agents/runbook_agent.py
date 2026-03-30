from agent_framework import Agent
from agent_framework.azure import AzureOpenAIChatClient
from tools import search_runbooks


def make_runbook_agent(client: AzureOpenAIChatClient) -> Agent:
    return Agent(
        client=client,
        name="RunbookRAGAgent",
        instructions=(
            "You are an on-call engineer with access to the runbook library. "
            "Use search_runbooks to find relevant procedures for the incident. "
            "Return the top 3 most relevant runbooks with their action steps."
        ),
        tools=[search_runbooks],
    )
