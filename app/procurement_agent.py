from google.adk.agents import Agent
import pandas as pd


DATA_PATH = "data/supply_chain_dataset1.csv"


def get_purchase_orders(
    product_name: str,
    warehouse_id: str,
) -> str:
    """Returns procurement information for a SKU and warehouse."""

    df = pd.read_csv(DATA_PATH)

    product = product_name.upper()
    warehouse = warehouse_id.upper()

    data = df[
        (df["SKU_ID"] == product)
        & (df["Warehouse_ID"] == warehouse)
    ]

    if data.empty:
        return (
            f"No procurement information is available for "
            f"{product_name} at warehouse {warehouse_id}."
        )

    latest = data.sort_values("Date").iloc[-1]

    return (
        f"SKU: {latest['SKU_ID']}\n"
        f"Warehouse: {latest['Warehouse_ID']}\n"
        f"Supplier: {latest['Supplier_ID']}\n"
        f"Date: {latest['Date']}\n"
        f"Order quantity: {latest['Order_Quantity']} units\n"
        f"Supplier lead time: "
        f"{latest['Supplier_Lead_Time_Days']} days"
    )


procurement_agent = Agent(
    name="procurement_agent",
    model="gemini-3.5-flash-lite",
    description=(
        "Specialized agent for procurement and "
        "replenishment analysis."
    ),
    instruction="""
You are ProcurementAgent, a specialized supply chain
procurement and replenishment agent.

Your responsibility is to provide accurate procurement
information available in the dataset.

Always use the get_purchase_orders tool when the user
asks about:

- purchase orders
- order quantities
- replenishment
- suppliers
- incoming procurement quantities
- supplier lead time related to procurement

Never invent procurement data.

The dataset does not provide:

- purchase order status
- exact arrival dates
- shipment tracking

Do not invent these values.

If information is unavailable, clearly state that
it is unavailable.
""",
    tools=[get_purchase_orders],
)