"""27_server_side_tool_use.py
Example: Server-side tool execution by the provider.
"""

from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-4.1-mini")

# Define a web search tool
tool = {"type": "web_search"}
model_with_tools = model.bind_tools([tool])

# Model handles tool calling server-side
response = model_with_tools.invoke("What was a positive news story from today?")
print(response.content_blocks)

# Output will include:
# [
#     {
#         "type": "server_tool_call",
#         "name": "web_search",
#         "args": {
#             "query": "positive news stories today",
#             "type": "search"
#         },
#         "id": "ws_abc123"
#     },
#     {
#         "type": "server_tool_result",
#         "tool_call_id": "ws_abc123",
#         "status": "success"
#     },
#     {
#         "type": "text",
#         "text": "Here are some positive news stories from today...",
#         "annotations": [
#             {
#                 "end_index": 410,
#                 "start_index": 337,
#                 "title": "article title",
#                 "type": "citation",
#                 "url": "..."
#             }
#         ]
#     }
# ]
