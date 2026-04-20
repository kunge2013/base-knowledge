"""
6. PII Detection Middleware Example

Detect and handle Personally Identifiable Information (PII) in conversations
using configurable strategies.
"""

from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware
import re
from langchain.messages import HumanMessage
from llm_config import get_llm

print("=" * 60)
print("PII Detection Middleware Example")
print("Detect and handle PII with configurable strategies")
print("=" * 60)

print("\n🔧 Configuration:")
print("   Built-in types: email (redact), credit_card (mask)")
print("   Custom: api_key (block), phone_number (mask), ssn (hash with validation)")
print("\nStrategies:")
print("   - block: Raise exception when PII detected")
print("   - redact: Replace with [REDACTED]")
print("   - mask: Partially mask (e.g., ****-****-****-1234)")
print("   - hash: Replace with deterministic hash")


# Custom SSN detector with validation rules
def detect_ssn(content: str) -> list[dict[str, str | int]]:
    """Detect SSN with validation.

    Returns a list of dictionaries with 'text', 'start', and 'end' keys.
    """
    matches = []
    pattern = r"\d{3}-\d{2}-\d{4}"
    for match in re.finditer(pattern, content):
        ssn = match.group(0)
        # Validate: first 3 digits shouldn't be 000, 666, or 900-999
        first_three = int(ssn[:3])
        if first_three not in [0, 666] and not (900 <= first_three <= 999):
            matches.append({
                "text": ssn,
                "start": match.start(),
                "end": match.end(),
            })
    return matches


# Create agent with multiple PII middleware
agent = create_agent(
    model=get_llm("gpt-4.1"),
    tools=[],
    middleware=[
        # Built-in PII types
        PIIMiddleware("email", strategy="redact", apply_to_input=True, apply_to_output=True),
        PIIMiddleware("credit_card", strategy="mask", apply_to_input=True, apply_to_output=True),
        # Custom PII with regex string
        PIIMiddleware(
            "api_key",
            detector=r"sk-[a-zA-Z0-9]{32}",
            strategy="block",
        ),
        # Custom PII with compiled regex
        PIIMiddleware(
            "phone_number",
            detector=re.compile(r"\+?\d{1,3}[\s.-]?\d{3,4}[\s.-]?\d{4}"),
            strategy="mask",
        ),
        # Custom PII with detector function
        PIIMiddleware(
            "ssn",
            detector=detect_ssn,
            strategy="hash",
        ),
    ],
)

print("\n✅ Agent created successfully with multiple PII detectors!")

# Test with a query containing PII
print("\n🚀 Invoking agent with a query containing PII...")
query = """My email is john.doe@example.com and my phone is +1-555-123-4567.
My credit card is 4111-1111-1111-1111 and my SSN is 123-45-6789.
Can you help me schedule a doctor appointment?"""
print(f"\n👤 User input (contains PII):\n{query}")
print("\n🤖 Processing with PII detection...")
print("-" * 60)

# The middleware automatically processes the input before it reaches the LLM
result = agent.invoke({
    "messages": [HumanMessage(content=query)]
})

print("-" * 60)
print("\n📄 LLM Response after PII processing:")
if isinstance(result, dict) and 'messages' in result:
    last_msg = result['messages'][-1]
    if hasattr(last_msg, 'content'):
        print(last_msg.content)
    else:
        print(last_msg)
else:
    print(result)

print("\n" + "=" * 60)
print("PII Detection middleware example completed!")
print("\n💡 The middleware automatically detects and transforms PII:")
print("   - apply_to_input: Check user messages before model call")
print("   - apply_to_output: Check AI messages after model call")
print("   - apply_to_tool_results: Check tool result messages after execution")

