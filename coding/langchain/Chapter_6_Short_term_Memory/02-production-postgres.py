"""
2. Production: Postgres Checkpointer

In production, use a database-backed checkpointer for persistent short-term memory.
PostgresSaver stores conversation state across application restarts.
"""

import os
from langchain.agents import create_agent
from langchain.tools import tool
from llm_config import get_llm

print("=" * 60)
print("2. Production Postgres Checkpointer Example")
print("Persistent short-term memory in PostgreSQL database")
print("=" * 60)


@tool
def get_user_info(user_id: str) -> str:
    """Get user information by user ID.

    Args:
        user_id: The ID of the user to look up
    """
    print(f"\n[TOOL EXECUTION] get_user_info called with user_id={user_id}")
    result = f"User {user_id}: John Smith, john@example.com"
    print(f"[TOOL RESULT]: {result}")
    return result


print("\n🔧 Configuration:")
print("   - Checkpointer: PostgresSaver")
print("   - Persists across application restarts")
print("   - Auto-creates tables with checkpointer.setup()")
print("\n💡 Note: This example will skip actual connection if DB not available")

# Try to import and use PostgresSaver
try:
    from langgraph.checkpoint.postgres import PostgresSaver

    DB_URI = os.getenv(
        "POSTGRES_URI",
        "postgresql://postgres:postgres@localhost:5432/postgres?sslmode=disable"
    )
    print(f"   Database URI: {DB_URI.split('@')[0]}@***")

    print("\n✅ PostgresSaver imported successfully")

    # Show the code that would be used
    print("\n📝 Code for production:")
    print("```python")
    print("from langchain.agents import create_agent")
    print("from langgraph.checkpoint.postgres import PostgresSaver")
    print()
    print(f"DB_URI = \"{DB_URI}\"")
    print("with PostgresSaver.from_conn_string(DB_URI) as checkpointer:")
    print("    checkpointer.setup()  # Auto-create tables")
    print("    agent = create_agent(")
    print("        get_llm(\"gpt-4.1\"),")
    print("        tools=[get_user_info],")
    print("        checkpointer=checkpointer,")
    print("    )")
    print("```")

    print("\n✅ Agent setup with PostgresSaver ready!")

except ImportError:
    print("\n⚠️  langgraph-checkpoint-postgres not installed")
    print("   Install with: pip install langgraph-checkpoint-postgres")
    print("\n   After installation, you can use PostgresSaver for production.")
    print("\nContinuing with demo...")

    # Fallback to showing just the code example
    print("\n📝 Complete production code:")
    print("```python")
    print("from langchain.agents import create_agent")
    print("from langgraph.checkpoint.postgres import PostgresSaver")
    print()
    print("DB_URI = \"postgresql://postgres:postgres@localhost:5442/postgres?sslmode=disable\"")
    print("with PostgresSaver.from_conn_string(DB_URI) as checkpointer:")
    print("    checkpointer.setup()  # auto create tables in PostgreSQL")
    print("    agent = create_agent(")
    print("        get_llm(\"gpt-4.1\"),")
    print("        tools=[get_user_info],")
    print("        checkpointer=checkpointer,")
    print("    )")
    print("```")

except Exception as e:
    print(f"\n⚠️  Connection error: {e}")
    print("\nThis is expected if PostgreSQL is not running locally.")
    print("The code example above shows how to set it up when you have PostgreSQL running.")

print("\n" + "=" * 60)
print("Production Postgres checkpointer example completed!")
print("\n💡 Production options:")
print("   - Postgres: Full featured, recommended for most apps")
print("   - SQLite: File-based, good for smaller deployments")
print("   - Azure Cosmos DB: For Azure cloud deployments")
print("   - All support the same checkpointer interface")
print("   - State persists across application restarts")
