"""
1. Run: `pip install openai duckduckgo-search newspaper4k lxml_html_clean agno` to install the dependencies
2. Run: `python cookbook/storage/in_memory_storage/in_memory_storage_for_team.py` to run the team
"""

from typing import List

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.in_memory import InMemoryStorage
from agno.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.hackernews import HackerNewsTools
from pydantic import BaseModel


class Article(BaseModel):
    title: str
    summary: str
    reference_links: List[str]


# Create team members
hn_researcher = Agent(
    name="HackerNews Researcher",
    model=OpenAIChat("gpt-4o"),
    role="Gets top stories from hackernews.",
    tools=[HackerNewsTools()],
)

web_searcher = Agent(
    name="Web Searcher",
    model=OpenAIChat("gpt-4o"),
    role="Searches the web for information on a topic",
    tools=[DuckDuckGoTools()],
    add_datetime_to_instructions=True,
)

# Create in-memory storage for team sessions
# Note: In-memory storage is perfect for temporary team sessions, testing, or when persistence isn't needed
team_storage = InMemoryStorage(mode="team")

# Create team with in-memory storage
hn_team = Team(
    name="HackerNews Team",
    mode="coordinate",
    model=OpenAIChat("gpt-4o"),
    members=[hn_researcher, web_searcher],
    storage=team_storage,
    instructions=[
        "First, search hackernews for what the user is asking about.",
        "Then, ask the web searcher to search for each story to get more information.",
        "Finally, provide a thoughtful and engaging summary.",
    ],
    response_model=Article,
    show_tool_calls=True,
    markdown=True,
    show_members_responses=True,
)

print(f"Team session ID: {hn_team.session_id}")
print(f"Storage mode: {hn_team.storage.mode}")
print(f"Number of stored sessions: {len(team_storage.get_all_session_ids())}")

# Run the team
hn_team.print_response("Write an article about the top 2 stories on hackernews")

print(f"\nTeam completed!")
print(f"Number of stored sessions: {len(team_storage.get_all_session_ids())}")

# Demonstrate session retrieval
session = team_storage.read(hn_team.session_id)
if session:
    print(f"Session contains {len(session.memory.get('runs', []))} runs")

# Create another team instance with the same session to show memory persistence
# within the same program execution
print("\n--- Creating new team instance with same session ---")
hn_team2 = Team(
    name="HackerNews Team 2",
    mode="coordinate", 
    model=OpenAIChat("gpt-4o"),
    members=[hn_researcher, web_searcher],
    storage=team_storage,
    session_id=hn_team.session_id,  # Use the same session
    instructions=[
        "You can reference previous conversations.",
        "Provide additional insights based on what was discussed before.",
    ],
    response_model=Article,
    show_tool_calls=True,
    markdown=True,
    show_members_responses=True,
)

# The new team instance should have access to the previous session's memory
previous_session = team_storage.read(hn_team2.session_id)
if previous_session:
    print(f"Previous session found with {len(previous_session.memory.get('runs', []))} runs")
    # Run a follow-up query that references the previous conversation
    hn_team2.print_response("Can you provide more details about the first story we discussed?")
else:
    print("No previous session found")