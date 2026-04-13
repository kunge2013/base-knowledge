# Tools Chapter Code Examples

This directory contains Python code examples demonstrating LangChain's tool system, which extends what agents can do by letting them fetch real-time data, execute code, query external databases, and take actions in the world.

## Files

| File | Description |
|------|-------------|
| `llm_config.py` | LLM configuration for all examples |
| `01_basic_tool_definition.py` | Basic tool definition using @tool decorator |
| `02_custom_tool_properties.py` | Customize tool name and description |
| `03_advanced_schema_definition.py` | Define complex inputs with Pydantic models |
| `04_access_state.py` | Access conversation state from tools |
| `05_update_state.py` | Update agent state from tools using Command |
| `06_context_example.py` | Use context for immutable configuration data |
| `07_long_term_memory.py` | Use persistent store for long-term memory |
| `08_stream_writer.py` | Stream real-time updates from tools during execution |
| `09_execution_info.py` | Access execution context from tools |
| `10_server_info.py` | Access LangGraph Server information from tools |
| `11_tool_node_basic.py` | Basic usage of ToolNode in LangGraph |
| `12_tool_return_string.py` | Tool that returns a string for human-readable results |
| `13_tool_return_object.py` | Tool that returns an object for structured results |
| `14_tool_return_command.py` | Tool that returns a Command to update state |
| `15_error_handling.py` | Configure error handling in ToolNode |
| `16_tools_condition.py` | Use tools_condition for conditional routing in LangGraph |

## Key Concepts

### Tool Definition
- **@tool decorator**: Simple way to create tools with type hints and docstrings
- **Custom properties**: Override tool name and description
- **Advanced schemas**: Use Pydantic models for complex input validation

### Runtime Context
- **ToolRuntime**: Access state, context, store, and execution info
- **State**: Short-term memory for current conversation
- **Context**: Immutable configuration passed at invocation time
- **Store**: Long-term memory across conversations
- **Stream Writer**: Emit real-time updates during execution

### Tool Return Types
- **String**: Human-readable results
- **Object**: Structured data for model to parse
- **Command**: Update graph state and return optional message

### ToolNode
- **Parallel execution**: Execute multiple tools concurrently
- **Error handling**: Configure how tool errors are handled
- **Conditional routing**: Use `tools_condition` for routing based on tool calls
