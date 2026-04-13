# LangChain Tools - Chapter 5 Code Examples

This directory contains complete, runnable code examples for LangChain Tools
following the 5.Tools.md article.

## Files

| File | Description |
|------|-------------|
| `llm_config.py` | Shared LLM configuration (all examples use this) |
| `01-basic-definition.py` | Basic tool definition with `@tool` decorator. Shows how type hints and docstrings become tool schema. |
| `02-customize-properties.py` | Customizing tool name, description, and parameter documentation. |
| `03-pydantic-schema.py` | Advanced schema with Pydantic BaseModel. Complex nested inputs, validation, optional fields. |
| `04-context-access.py` | Accessing runtime context: `config` (immutable thread config) and `runtime` (state, store, stream). |
| `05-tool-node.py` | ToolNode for LangGraph. Parallel execution, error handling, conditional routing. |
| `06-prebuilt-tools.py` | Using prebuilt tools from langchain-community (Wikipedia, Arxiv). |
| `07-server-side-tools.py` | Best practices for server-side tool deployment: rate limiting, authentication, validation, security. |

## Requirements

```bash
pip install -r ../requirements.txt
```

Additional dependencies for some examples:
- `langchain-community`: For prebuilt tools
- `arxiv`: For Arxiv search
- `wikipedia`: For Wikipedia search

## Running the Examples

Each file is standalone and can be run directly:

```bash
python 01-basic-definition.py
python 02-customize-properties.py
# etc...
```

All examples:
- Print tool execution logs
- Call the actual LLM
- Print the final response
- Explain key concepts at the end

## Configuration

Set your API keys in a `.env` file in the project root:

```env
OPENAI_API_KEY=your-api-key-here
OPENAI_BASE_URL=https://your-openai-endpoint.com  # Optional
TOOL_API_KEY=your-tool-api-key     # Optional for server-side example
```

## Key Concepts Covered

1. **Tool Creation** - `@tool` decorator, automatic schema inference
2. **Customization** - Override names, descriptions, parameter docs
3. **Pydantic Schema** - Complex inputs with validation
4. **Context Access** - Accessing config, state, store from tools
5. **ToolNode** - LangGraph integration, parallel execution
6. **Prebuilt Tools** - Leveraging the LangChain ecosystem
7. **Server-Side** - Production best practices (auth, rate limiting, security)
