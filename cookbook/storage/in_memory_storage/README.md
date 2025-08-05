# In-Memory Storage Examples

This directory contains examples demonstrating how to use `InMemoryStorage` with Agno agents, workflows, and teams.

## Overview

`InMemoryStorage` provides a flexible, lightweight storage solution that keeps all session data in memory. This storage backend is ideal for:

- **Testing and development**: No file system or database setup required
- **Temporary sessions**: When you don't need data persistence across program restarts
- **High-performance scenarios**: Fastest storage option with no I/O operations
- **Custom storage mechanisms**: Bring your own dictionary for flexible persistence options
- **External system integration**: Connect to Redis, databases, or custom storage solutions

## Key Features

- **Zero configuration**: No setup required, works out of the box
- **Flexible storage**: Use built-in dictionary or provide your own for custom persistence
- **External integration**: Connect to Redis, databases, or any external storage system
- **All modes supported**: Works with agents, workflows, teams, and workflow_v2
- **Full feature set**: Supports filtering, recent sessions, and all standard operations
- **Shared storage**: Multiple agents/workflows can share the same storage dictionary
- **Memory efficient**: Data is automatically cleared when the program ends
- **Thread-safe**: Safe for use in concurrent applications

## Examples

### Agent Storage
[`in_memory_storage_for_agent.py`](./in_memory_storage_for_agent.py)

Demonstrates basic agent usage with in-memory storage, including:
- Creating an agent with `InMemoryStorage`
- Session persistence within the same program execution
- Sharing sessions between agent instances

### Workflow Storage
[`in_memory_storage_for_workflow.py`](./in_memory_storage_for_workflow.py)

Shows workflow session management with in-memory storage:
- Workflow session creation and persistence
- Memory sharing across workflow instances
- Session information and statistics

### Team Storage
[`in_memory_storage_for_team.py`](./in_memory_storage_for_team.py)

Illustrates team coordination with in-memory storage:
- Multi-agent team session management
- Team memory persistence within program execution
- Follow-up queries referencing previous conversations

## Usage

### Basic Setup

```python
from agno.storage.in_memory import InMemoryStorage

# For agents (default)
agent_storage = InMemoryStorage()

# For workflows
workflow_storage = InMemoryStorage(mode="workflow")

# For teams
team_storage = InMemoryStorage(mode="team")
```

### Bring Your Own Dictionary (Flexible Storage Integration)

The real power of InMemoryStorage comes from providing your own dictionary for custom storage mechanisms, in case the current first-class supported storage offerings are too opinionated:

```python
from agno.storage.in_memory import InMemoryStorage
from agno.agent import Agent
from agno.models.openai import OpenAIChat
import json
import boto3

# Example: Save and load sessions to/from S3
def save_sessions_to_s3(sessions_dict, bucket_name, key_name):
    """Save sessions dictionary to S3"""
    s3 = boto3.client('s3')
    s3.put_object(
        Bucket=bucket_name,
        Key=key_name,
        Body=json.dumps(sessions_dict, default=str)
    )

def load_sessions_from_s3(bucket_name, key_name):
    """Load sessions dictionary from S3"""
    s3 = boto3.client('s3')
    try:
        response = s3.get_object(Bucket=bucket_name, Key=key_name)
        return json.loads(response['Body'].read())
    except:
        return {}  # Return empty dict if file doesn't exist

# Step 1: Create agent with external dictionary
my_sessions = {}
storage = InMemoryStorage(storage_dict=my_sessions)

agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    storage=storage,
    add_history_to_messages=True,
)

# Run some conversations
agent.run("What is the capital of France?")
agent.run("What is its population?")

print(f"Sessions in memory: {len(my_sessions)}")

# Step 2: Save sessions to S3
save_sessions_to_s3(my_sessions, "my-bucket", "agent-sessions.json")
print("Sessions saved to S3!")

# Step 3: Later, load sessions from S3 and use with new agent
loaded_sessions = load_sessions_from_s3("my-bucket", "agent-sessions.json")
new_storage = InMemoryStorage(storage_dict=loaded_sessions)

new_agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    storage=new_storage,
    session_id=agent.session_id,  # Use same session ID
    add_history_to_messages=True,
)

# This agent now has access to the previous conversation
new_agent.run("What was my first question?")
```

### Common Operations

```python
# Create storage
storage = InMemoryStorage()

# Get all sessions
all_sessions = storage.get_all_sessions()

# Filter sessions by user
user_sessions = storage.get_all_sessions(user_id="user123")

# Get recent sessions
recent = storage.get_recent_sessions(limit=5)

# Delete a session
storage.delete_session("session_id")

# Clear all sessions
storage.drop()
```

## Important Notes

⚠️ **Data Persistence**: Session data is **not persistent** across program restarts unless you provide an external dictionary with your own persistence mechanism.

⚠️ **Memory Usage**: All session data is stored in RAM. For applications with many long sessions, monitor memory usage.

**Performance**: Fastest storage option available - no disk I/O or network calls.

**Flexibility**: Use built-in storage or provide your own dictionary for custom persistence, external system integration, or shared storage.

**Simplicity**: Zero configuration required, perfect for quick prototypes and testing.

## When to Use In-Memory Storage

**Good for:**
- Development and testing
- Short-lived applications
- Custom storage integration
- Stateless microservices
- Demo applications
- Quick prototypes

**Good for (with external dictionary):**
- Production systems with custom persistence mechanisms
- Integration with existing storage infrastructure
- Custom session management and analytics

## Running the Examples

1. Install dependencies:
```bash
pip install openai duckduckgo-search newspaper4k lxml_html_clean agno
```

2. Run individual examples:
```bash
# Agent example
python cookbook/storage/in_memory_storage/in_memory_storage_for_agent.py

# Workflow example
python cookbook/storage/in_memory_storage/in_memory_storage_for_workflow.py

# Team example
python cookbook/storage/in_memory_storage/in_memory_storage_for_team.py

# External dictionary examples
python cookbook/storage/in_memory_storage/external_storage_dict_example.py
```
