"""28_rate_limiting.py
Example: Rate limiting with InMemoryRateLimiter.
"""

from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain.chat_models import init_chat_model

# Configure a rate limiter to avoid hitting provider limits
# Controls requests per second in the same process
rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.1,  # 1 request every 10 seconds
    check_every_n_seconds=0.1,  # Check every 100ms whether allowed to make a request
    max_bucket_size=10,  # Controls the maximum burst size
)

model = init_chat_model(
    model="gpt-5",
    model_provider="openai",
    rate_limiter=rate_limiter
)
