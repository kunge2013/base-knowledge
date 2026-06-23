# Streaming Chapter Code Examples

This directory contains Python code examples demonstrating LangChain's streaming system, which lets you surface real-time updates from agent runs to your application.

## Files

| File | Description |
|------|-------------|
| `llm_config.py` | LLM configuration for all examples |
| `01_agent_progress.py` | Stream agent progress using stream_mode="updates" |
| `02_llm_tokens.py` | Stream LLM tokens using stream_mode="messages" |
| `03_custom_updates.py` | Stream custom updates from tools using stream writer |
| `04_multiple_modes.py` | Stream multiple modes simultaneously |
| `05_thinking_tokens.py` | Stream thinking/reasoning tokens from models |
| `06_streaming_tool_calls.py` | Stream tool calls and responses |
| `07_human_in_the_loop.py` | Handle human-in-the-loop interrupts during streaming |
| `08_streaming_from_sub_agents.py` | Stream from sub-agents with agent identification |

## Key Concepts

### Streaming Modes
- **updates**: Streams state updates after each agent step
- **messages**: Streams tuples of (token, metadata) from LLM invocations
- **custom**: Streams custom data from inside graph nodes using stream writer

### Streaming Benefits
- **Improved UX**: Display output progressively before complete response is ready
- **Reduced perceived latency**: Show real-time feedback during model execution
- **Better user engagement**: Interactive experiences with live updates

### Advanced Features
- **Thinking tokens**: Stream model reasoning as it's generated
- **Tool calls**: Stream partial JSON and completed tool calls
- **Multiple modes**: Stream updates, messages, and custom data simultaneously
- **Sub-graphs**: Identify and stream from different agents in multi-agent systems
