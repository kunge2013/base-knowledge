"""30_http_proxy.py
Example: Configuring HTTP proxy for OpenAI chat model.
"""

from langchain_openai import ChatOpenAI

# Configure OpenAI with HTTP proxy
model = ChatOpenAI(
    model="gpt-4.1",
    openai_proxy="http://proxy.example.com:8080"
)
