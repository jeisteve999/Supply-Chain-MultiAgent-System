from google.adk.agents import Agent
import pandas as pd


DATA_PATH = "data/supply_chain_dataset1.csv"


def get_delivery_status(
    product_name: str,
    warehouse_id: str,
) -> str:
    """Returns delivery and supplier lead-time information."""

    df = pd.read_csv(DATA_PATH)

    product = product_name.upper()
    warehouse = warehouse_id.upper()

    data = df[
        (df["SKU_ID"] == product)
        & (df["Warehouse_ID"] == warehouse)
    ]

    if data.empty:
        return (
            f"No delivery information is available for "
            f"{product_name} at warehouse {warehouse_id}."
        )

    latest = data.sort_values("Date").iloc[-1]

    return (
        f"SKU: {latest['SKU_ID']}\n"
        f"Warehouse: {latest['Warehouse_ID']}\n"
        f"Supplier: {latest['Supplier_ID']}\n"
        f"Date: {latest['Date']}\n"
        f"Supplier lead time: "
        f"{latest['Supplier_Lead_Time_Days']} days"
    )


delivery_agent = Agent(
    name="delivery_agent",
    model="gemini-3.5-flash-lite",
    description=(
        "Specialized agent for supplier lead-time "
        "and delivery timing analysis."
    ),
    instruction="""
You are DeliveryAgent, a specialized supply chain
delivery and supplier lead-time agent.

Your responsibility is to provide accurate information
about supplier lead times and delivery timing metrics
available in the dataset.

Always use the get_delivery_status tool when the user
asks about:

- delivery information
- supplier lead time
- delivery timing
- supplier delivery performance

Never invent delivery data.

The dataset does not provide:

- actual delivery dates
- shipment status
- delayed/on-time status
- tracking information

Therefore, never invent values such as:

- "On time"
- "Delayed"
- "In transit"

Use Supplier_Lead_Time_Days as the available
delivery-timing metric.

If information is unavailable, clearly state that
it is unavailable.
""",
    tools=[get_delivery_status],
)