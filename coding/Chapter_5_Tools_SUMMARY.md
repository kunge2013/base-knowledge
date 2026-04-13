# Chapter 5: Tools - Summary

This chapter covers **Tools** in LangChain - how to create, customize, and use tools with LLMs. Tools extend LLM capabilities by letting them interact with external systems, APIs, and data.

## Overview of Files

| File                                                                       | Topic                 | Key Concepts                                                            |
| -------------------------------------------------------------------------- | --------------------- | ----------------------------------------------------------------------- |
| [01-basic-definition.py](./Chapter_5_Tools/01-basic-definition.py)         | Basic Tool Definition | `@tool` decorator, type hints → schema, docstring → description         |
| [02-customize-properties.py](./Chapter_5_Tools/02-customize-properties.py) | Customize Properties  | Custom name/description, docstring parsing, `parse_docstring`           |
| [03-pydantic-schema.py](./Chapter_5_Tools/03-pydantic-schema.py)           | Pydantic Schema       | Complex nested inputs, field validation, optional fields                |
| [04-context-access.py](./Chapter_5_Tools/04-context-access.py)             | Context Access        | `config` (immutable), `runtime` (state/store), reserved parameter names |
| [05-tool-node.py](./Chapter_5_Tools/05-tool-node.py)                       | ToolNode (LangGraph)  | Parallel execution, error handling, routing                             |
| [06-prebuilt-tools.py](./Chapter_5_Tools/06-prebuilt-tools.py)             | Prebuilt Tools        | Wikipedia, Arxiv, langchain-community ecosystem                         |
| [07-server-side-tools.py](./Chapter_5_Tools/07-server-side-tools.py)       | Server-Side Tools     | Rate limiting, auth, validation, security best practices                |
|                                                                            |                       |                                                                         |

## Key Takeaways

### 1. Tool Creation Basics

- Use the `@tool` decorator to convert any Python function into a LangChain `Tool`
- **Type hints** → automatically generate JSON schema for parameters
- **Docstring** → becomes the tool description the LLM reads
- Minimal code, works out of the box for simple cases

### 2. Customization Options

- Override tool name: `@tool(name="custom_name")`
- Override description: `@tool(description="Custom description")`
- Control parameter description parsing via `parse_docstring`
- Detailed docstring with `Args:` sections → detailed parameter descriptions for LLM

### 3. Advanced Schemas with Pydantic

- For complex inputs with validation, use Pydantic `BaseModel`
- Supports nested models (e.g., `OrderInfo` contains `ProductItem` and `ShippingAddress`)
- All Pydantic features available: validators, `Field` descriptions, optional fields
- Automatic JSON schema generation for LLM function calling
- Validation happens **before** your tool runs - fail fast

### 4. Context Access

Two special reserved parameter names that are automatically injected:

- **`config`**: Immutable thread configuration (user_id, settings, etc.)
- **`runtime`**: Gives access to:
  - `runtime.state` - Current graph state (read-only)
  - `runtime.store` - Long-term key-value storage
  - `runtime.stream` - Stream tokens back to client

This enables tools that interact with the current execution context.

### 5. ToolNode for LangGraph

`ToolNode` is a prebuilt LangGraph node that:

- Automatically executes all requested tool calls (parallel if multiple requested)
- Handles errors (configurable: raise, return, or fallback)
- Adds `ToolMessage` responses back to conversation state
- Works seamlessly with conditional routing: back to agent after tools, or exit
- Supports state injection for tools that need context

### 6. Prebuilt Tools in the Ecosystem

LangChain has hundreds of prebuilt tools:

- **Search**: Wikipedia, Arxiv, Tavily, Google, Bing
- **Database**: SQL, MongoDB, Redis, etc.
- **File**: CSV, PDF, JSON, Excel
- **Code**: Python REPL, Bash
- **APIs**: GitHub, Slack, Notion, Gmail, many more
- All in `langchain_community.tools`

### 7. Server-Side Best Practices

When deploying tools in production:

- **Authentication**: Always validate API keys / user auth
- **Rate Limiting**: Prevent abuse with per-user limits
- **Input Validation**: Validate *all* inputs on the server (never trust client)
- **Audit Logging**: Log all invocations for compliance and debugging
- **Security**: Sanitize inputs (e.g., only allow SELECT for SQL queries)
- **Timeouts**: Set timeouts for external calls
- **Error Handling**: Proper error messages to LLM/client without leaking sensitive info

## Common Patterns

### Return Types

- **str**: Most common - text response to LLM
- **dict/object**: Structured data (automatically handled)
- **Command**: Update graph state directly from tool (LangGraph)

### Reserved Names

Never name your parameters `config` or `runtime` unless you *want* them injected.

### Error Handling

- Raise `ToolException` for tool-level errors that should be returned to the LLM
- ToolNode can be configured to handle errors automatically
- Let the LLM see the error so it can recover

## Dependencies

```python
langchain>=0.3.0
langchain-core>=0.3.0
langchain-openai>=0.2.0
langgraph>=0.2.0
langchain-community>=0.3.0  # For prebuilt tools
pydantic>=2.0               # For advanced schemas
arxiv>=2.1.0                # For Arxiv example
wikipedia>=1.5.0            # For Wikipedia example
```

## Running the Examples

Each example is standalone:

```bash
cd Chapter_5_Tools
python 01-basic-definition.py
python 02-customize-properties.py
# ... etc
```

All examples:
- Print tool execution logs
- Invoke the actual LLM
- Print the final response
- Summarize key points at the end
