# LangChain Short-term Memory - Chapter 6 Code Examples

This directory contains complete, runnable code examples for LangChain Short-term Memory
following the 6.Short-term memory.md article.

## Files

| File | Description |
|------|-------------|
| `llm_config.py` | Shared LLM configuration (all examples use this) |
| `01-basic-in-memory.py` | Basic example with InMemorySaver. Thread-level persistence, multiple conversations. |
| `02-production-postgres.py` | Production setup with PostgresSaver. Persistence across restarts. |
| `03-custom-state.py` | Extend AgentState with custom fields for additional short-term memory. |
| `04-trim-messages.py` | Trim messages with `@before_model` middleware to fit context window. |
| `05-delete-messages.py` | Delete old messages with `@after_model` middleware to control growth. |
| `06-summarize-messages.py` | Automatic summarization with SummarizationMiddleware. |
| `07-tool-access-memory.py` | Tools read/write short-term memory via `ToolRuntime`. |
| `08-dynamic-prompt-memory.py` | Dynamic prompts from memory with `@dynamic_prompt` middleware. |
| `09-after-model-validation.py` | Post-process/validate responses after model with `@after_model`. |

## Requirements

```bash
pip install -r ../requirements.txt
```

Additional for production Postgres:
```bash
pip install langgraph-checkpoint-postgres psycopg2-binary
```

## Running the Examples

Each file is standalone and can be run directly:

```bash
python 01-basic-in-memory.py
python 02-production-postgres.py
# etc...
```

All examples:
- Print execution logs showing what's happening
- Call the actual LLM
- Print the final response
- Handle API errors gracefully
- Explain key concepts at the end

## Configuration

Set your API keys in a `.env` file in the project root:

```env
OPENAI_API_KEY=your-api-key-here
OPENAI_BASE_URL=https://your-openai-endpoint.com  # Optional
POSTGRES_URI=postgresql://postgres:postgres@localhost:5432/postgres  # For production example
```

## Key Concepts Covered

1. **What is Short-term Memory** - Remembering interactions within a single thread/conversation
2. **Checkpointing** - Persisting agent state between invocations via checkpointer
3. **In-Memory** - Development/testing, lost on restart
4. **Database-backed** - Production, persists across restarts (Postgres, SQLite, etc.)
5. **Custom State** - Extend AgentState to add your own fields
6. **Context Management** - Strategies to fit within context window:
   - **Trimming**: Keep last N messages
   - **Deletion**: Delete oldest messages incrementally
   - **Summarization**: Summarize older messages to retain info
7. **Access Patterns**:
   - **Tools**: Tools can read/write state via `runtime`
   - **Middleware**: `@before_model`, `@after_model`, `@dynamic_prompt` access memory
   - **Dynamic Prompts**: Personalize prompts from stored user info

## Common Context Management Strategies

| Strategy | When to Use | Pros | Cons |
|----------|-------------|------|------|
| Trim | Quick conversations, simple | Simple, fast | Loses older info |
| Delete | Gradual growth of conversation | Simple, incremental | Loses older info |
| Summarize | Long conversations | Retains information | Uses extra LLM tokens/cost |

## Access Points to Short-term Memory

| Where | How | Example |
|-------|-----|---------|
| Tools | `runtime.state`, `runtime.context`, return `Command(update=...)` | 07-tool-access-memory.py |
| before_model | `@before_model` decorator, gets state | 04-trim-messages.py |
| after_model | `@after_model` decorator, gets state | 05-delete-messages.py, 09-after-model-validation.py |
| dynamic_prompt | `@dynamic_prompt`, gets request with state/context | 08-dynamic-prompt-memory.py |
