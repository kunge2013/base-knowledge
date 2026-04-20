"""
3. Advanced Schema with Pydantic

For complex inputs with multiple fields, validation, and nested structures,
use Pydantic BaseModel to define the tool schema.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from llm_config import get_llm

print("=" * 60)
print("3. Advanced Schema with Pydantic Example")
print("Complex input validation with Pydantic BaseModel")
print("=" * 60)


# Complex nested schema with Pydantic
class ProductItem(BaseModel):
    """A single product in an order."""
    name: str = Field(description="Name of the product")
    quantity: int = Field(description="How many units to order")
    price: float = Field(description="Price per unit")

    @field_validator('quantity')
    @classmethod
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be greater than zero')
        return v

    @field_validator('price')
    @classmethod
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be greater than zero')
        return v


class ShippingAddress(BaseModel):
    """Shipping address for the order."""
    street: str = Field(description="Street address")
    city: str = Field(description="City name")
    zip_code: str = Field(description="ZIP or postal code")
    country: str = Field(description="Country code (2 letters)")


class OrderInfo(BaseModel):
    """Complete order information."""
    customer_name: str = Field(description="Name of the customer")
    email: str = Field(description="Customer's email address")
    products: List[ProductItem] = Field(description="List of products in the order")
    shipping_address: ShippingAddress = Field(description="Where to ship the order")
    express_shipping: bool = Field(False, description="Whether to use express shipping")


@tool
def calculate_order_total(order: OrderInfo) -> str:
    """Calculate the total cost of an order including shipping.

    Validates the order using Pydantic schema before processing.
    """
    print(f"\n[TOOL EXECUTION] calculate_order_total called for customer: {order.customer_name}")
    print(f"   Email: {order.email}")
    print(f"   Products: {len(order.products)} items")

    # Calculate subtotal
    subtotal = sum(item.quantity * item.price for item in order.products)

    # Add shipping cost
    shipping_cost = 15 if order.express_shipping else 5

    # Calculate total
    total = subtotal + shipping_cost

    result = (
        f"Order Summary for {order.customer_name} ({order.email})\n"
        f"----------------------------------------\n"
    )
    for item in order.products:
        item_total = item.quantity * item.price
        result += f"  {item.quantity}x {item.name}: ${item_total:.2f}\n"
    result += f"----------------------------------------\n"
    result += f"Subtotal: ${subtotal:.2f}\n"
    result += f"Shipping: ${shipping_cost:.2f}\n"
    result += f"Total: ${total:.2f}\n"

    print(f"[TOOL RESULT]: Total order amount is ${total:.2f}")
    return result


# Example with optional fields
class SearchFilters(BaseModel):
    """Optional search filters for filtering results."""
    min_price: Optional[float] = Field(None, description="Minimum price filter")
    max_price: Optional[float] = Field(None, description="Maximum price filter")
    categories: Optional[List[str]] = Field(None, description="List of categories to include")
    in_stock_only: bool = Field(True, description="Only include products that are in stock")


@tool
def filter_products(query: str, filters: SearchFilters = None) -> str:
    """Search for products with optional filtering.

    Args:
        query: The search query
        filters: Optional filters for narrowing down results
    """
    filters = filters or SearchFilters()
    print(f"\n[TOOL EXECUTION] filter_products called with query={query}, filters={filters}")

    result = f"Search results for '{query}':\n"
    result += f"  min_price: {filters.min_price}\n"
    result += f"  max_price: {filters.max_price}\n"
    result += f"  categories: {filters.categories}\n"
    result += f"  in_stock_only: {filters.in_stock_only}"

    print(f"[TOOL RESULT]: Returning filtered results as specified")
    return result


print("\n🔧 Configuration:")
print("   - Nested Pydantic models: OrderInfo → ProductItem + ShippingAddress")
print("   - Field validation with @field_validator")
print("   - Optional fields with defaults in SearchFilters")
print("   - Automatic JSON schema generation for LLM function calling")

# Create agent
agent = create_agent(
    model=get_llm("gpt-4.1"),
    tools=[calculate_order_total, filter_products],
    middleware=[],
)

print("\n✅ Agent created successfully!")

# Invoke with a complex query
print("\n🚀 Invoking agent...")
query = """
Create an order for customer John Smith with email john@example.com.
He wants to buy 2 units of Apple at $1.99 each and 1 unit of Banana at $0.99.
Shipping address is 123 Main St, New York, 10001, US. Use express shipping.
Calculate the total.
"""
print(f"\n👤 User: {query.strip()}")
print("🤖 LLM is processing... Will construct complex nested JSON via schema.")
print("-" * 60)

try:
    result = agent.invoke({
        "messages": [HumanMessage(content=query)]
    })

    print("-" * 60)
    print("\n📄 Final Response:")
    if isinstance(result, dict) and 'messages' in result:
        last_msg = result['messages'][-1]
        if hasattr(last_msg, 'content'):
            print(last_msg.content)
        else:
            print(last_msg)
    else:
        print(result)
except Exception as e:
    print("-" * 60)
    print(f"\n❌ Error invoking LLM: {type(e).__name__}: {e}")
    print("\nThis example requires a valid OpenAI API key configured in .env")

print("\n" + "=" * 60)
print("Pydantic schema example completed!")
print("\n💡 Benefits of Pydantic schema:")
print("   - Automatic input validation before your tool runs")
print("   - Complex nested structures are fully supported")
print("   - Field descriptions are visible to the LLM")
print("   - Optional fields with default values work naturally")
print("   - All Pydantic features: validators, serialization, etc. available")
