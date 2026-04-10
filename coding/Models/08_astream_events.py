"""08_astream_events.py
Example: Streaming semantic events with astream_events.
"""

import asyncio
from llm_config import default_llm


async def stream_events():
    async for event in default_llm.astream_events("Hello"):
        if event["event"] == "on_chat_model_start":
            print(f"Input: {event['data']['input']}")

        elif event["event"] == "on_chat_model_stream":
            print(f"Token: {event['data']['chunk'].text}")

        elif event["event"] == "on_chat_model_end":
            print(f"Full message: {event['data']['output'].text}")

        else:
            pass


# Run the async stream
if __name__ == "__main__":
    asyncio.run(stream_events())
