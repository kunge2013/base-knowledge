"""33_invocation_config.py
Example: Passing custom invocation configuration via RunnableConfig.
"""

from llm_config import default_llm

# Invoke with custom configuration options
response = default_llm.invoke(
    "Tell me a joke",
    config={
        "run_name": "joke_generation",      # Custom name for this run (LangSmith tracing)
        "tags": ["humor", "demo"],          # Tags for filtering and organization
        "metadata": {"user_id": "123"},     # Custom metadata for tracking
        # "callbacks": [my_callback_handler], # Callback handlers
    }
)
