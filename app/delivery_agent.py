from google.adk.agents import Agent


def get_delivery_status(product_name: str) -> str:
    """Returns delivery status information for a product."""

    deliveries = {
        "product a": {
            "status": "On time",
            "quantity": 100,
            "expected_date": "2026-08-12",
        },
        "product b": {
            "status": "Delayed",
            "quantity": 60,
            "expected_date": "2026-08-20",
        },
        "product c": {
            "status": "On time",
            "quantity": 120,
            "expected_date": "2026-08-17",
        },
    }

    product = product_name.lower()

    if product in deliveries:
        delivery = deliveries[product]

        return (
            f"Product: {product_name}\n"
            f"Delivery status: {delivery['status']}\n"
            f"Delivery quantity: {delivery['quantity']}\n"
            f"Expected delivery date: {delivery['expected_date']}"
        )

    return f"No delivery information is available for {product_name}"


delivery_agent = Agent(
    name="delivery_agent",
    model="gemini-3.5-flash",
    description="Specialized agent for delivery and shipment status analysis.",
    instruction="""
You are DeliveryAgent.

Your responsibility is to analyze delivery and shipment status.

Use the get_delivery_status tool when the user asks about:
- delivery status
- shipment status
- expected delivery dates
- delayed deliveries
- delivered quantities

Never invent delivery information.
If there is no information for a product, clearly state that
no delivery information is available.
""",
    tools=[get_delivery_status],
)