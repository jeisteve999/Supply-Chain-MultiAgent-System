from google.adk.agents import Agent

def get_purchase_orders(product_name: str) -> str:
    """Returns incoming purchase order information for a product."""

    purchase_orders = {
        "product a": {
            "incoming_quantity": 50,
            "status": "In transit",
            "expected_arrival": "2026-08-14",
        },
        "product b": {
            "incoming_quantity": 30,
            "status": "Processing",
            "expected_arrival": "2026-08-16",
        },
        "product c": {
            "incoming_quantity": 100,
            "status": "In transit",
            "expected_arrival": "2026-08-18",
        },
    }

    product = product_name.lower()

    if product in purchase_orders:
        order = purchase_orders[product]

        return (
            f"Product: {product_name}\n"
            f"Incoming quantity: {order['incoming_quantity']}\n"
            f"Status: {order['status']}\n"
            f"Expected arrival: {order['expected_arrival']}"
        )

    return f"No purchase order information is available for {product_name}"


procurement_agent = Agent(
    name="procurement_agent",
    model="gemini-3.5-flash",
    description="Specialized agent for procurement and incoming purchase orders.",
    instruction="""
You are ProcurementAgent, a specialized supply chain procurement agent.

Your responsibility is to provide information about purchase orders
and incoming inventory.

Use the get_purchase_orders tool when the user asks about:
- purchase orders
- incoming inventory
- replenishment
- supplier orders
- quantities on order
- expected arrival of purchased products

Never invent procurement data.

If information is unavailable, clearly state that it is unavailable.
""",
    tools=[get_purchase_orders],
)
