"""10_batch_max_concurrency.py
Example: Batching with controlled maximum concurrency.
"""

from llm_config import default_llm

# Control maximum number of parallel calls
# Useful when processing large number of inputs
list_of_inputs = [
    "Question 1",
    "Question 2",
    "Question 3",
    # ... many more inputs
]

default_llm.batch(
    list_of_inputs,
    config={
        'max_concurrency': 5,  # Limit to 5 parallel calls
    }
)
