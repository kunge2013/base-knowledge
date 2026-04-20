"""03_invoke_single.py
Example: Invoke model with a single message.
"""

from llm_config import default_llm

# Call invoke with a single message
response = default_llm.invoke("Why do parrots have colorful feathers?")
print(response)
