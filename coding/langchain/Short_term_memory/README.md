# Short-term Memory Chapter Code Examples

This directory contains Python code examples demonstrating LangChain's short-term memory system, which lets your application remember previous interactions within a single thread or conversation.

## Files

| File | Description |
|------|-------------|
| `llm_config.py` | LLM configuration for all examples |
| `01_basic_usage.py` | Basic usage of short-term memory with checkpointer |
| `02_custom_state.py` | Customize agent memory with custom state schema |
| `03_trim_messages.py` | Trim messages to fit context window using middleware |
| `04_delete_messages.py` | Delete messages from graph state using RemoveMessage |
| `05_summarize_messages.py` | Summarize message history using built-in middleware |
| `06_tool_read_state.py` | Read short-term memory from tools |
| `07_tool_write_state.py` | Write short-term memory from tools using Command |
| `08_dynamic_prompt.py` | Create dynamic prompts based on conversation state |

## Key Concepts

### Short-term Memory vs Long-term Memory
- **Short-term memory**: Thread-level persistence, remembers interactions within a single conversation
- **Long-term memory**: Cross-session persistence, stores data across different threads and sessions

### Checkpointer
- **InMemorySaver**: In-memory storage for development and testing
- **PostgresSaver**: PostgreSQL storage for production applications
- **Purpose**: Persist and resume conversation state using thread_id

### Memory Management Strategies
- **Trim messages**: Remove first or last N messages before calling LLM
- **Delete messages**: Delete messages from graph state permanently
- **Summarize messages**: Summarize earlier messages and replace them with a summary

### Middleware
- **@before_model**: Process messages before model calls
- **@after_model**: Process messages after model calls
- **@dynamic_prompt**: Create dynamic prompts based on conversation state
- **SummarizationMiddleware**: Built-in middleware for summarization
