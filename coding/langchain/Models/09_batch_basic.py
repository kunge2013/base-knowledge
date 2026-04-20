"""09_batch_basic.py
Example: Batching multiple independent requests.
"""

from llm_config import default_llm

# Process multiple inputs in parallel for better performance
responses = default_llm.batch([
    "Why do parrots have colorful feathers?",
    "How do airplanes fly?",
    "What is quantum computing?"
])
for response in responses:
    print(response)
    print(80 *"=")
