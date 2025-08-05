"""Run `pip install duckduckgo-search openai` to install dependencies."""

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.in_memory import InMemoryStorage
from agno.tools.duckduckgo import DuckDuckGoTools

# Create an agent with in-memory storage
# Note: In-memory storage is perfect for temporary sessions, testing, or when you don't need persistence
agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    storage=InMemoryStorage(),  # Sessions stored in memory only
    tools=[DuckDuckGoTools()],
    add_history_to_messages=True,
)

# The agent will remember the conversation within the same session
agent.print_response("How many people live in Canada?")
agent.print_response("What is their national anthem called?")

# Print session information
print(f"Agent session ID: {agent.session_id}")
print(f"Storage mode: {agent.storage.mode}")
print(f"Number of stored sessions: {len(agent.storage.get_all_session_ids())}")

# Create another agent instance with the same session_id to demonstrate session persistence
# within the same program execution
agent2 = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    storage=agent.storage,  # Share the same storage instance
    session_id=agent.session_id,  # Use the same session
    tools=[DuckDuckGoTools()],
    add_history_to_messages=True,
)

print("\n--- Using the same session with a new agent instance ---")
agent2.print_response("What was my first question?")