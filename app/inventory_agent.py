import pandas as pd
from google.adk.agents import Agent


DATA_PATH = "data/supply_chain_dataset1.csv"


def get_inventory(sku_id: str, warehouse_id: str = "") -> str:
    """Returns the latest inventory information for a SKU and warehouse."""

    df = pd.read_csv(DATA_PATH)

    filtered = df[df["SKU_ID"].str.upper() == sku_id.upper()]

    if warehouse_id:
        filtered = filtered[
            filtered["Warehouse_ID"].str.upper() == warehouse_id.upper()
        ]

    if filtered.empty:
        return f"No inventory information is available for {sku_id}."

    latest = filtered.sort_values("Date").iloc[-1]

    return (
        f"SKU: {latest['SKU_ID']}\n"
        f"Warehouse: {latest['Warehouse_ID']}\n"
        f"Date: {latest['Date']}\n"
        f"Inventory level: {int(latest['Inventory_Level'])} units\n"
        f"Reorder point: {int(latest['Reorder_Point'])} units\n"
        f"Units sold: {int(latest['Units_Sold'])}\n"
        f"Demand forecast: {latest['Demand_Forecast']:.2f}"
    )


inventory_agent = Agent(
    name="inventory_agent",
    model="gemini-3.5-flash",
    description="Specialized agent responsible for inventory analysis.",
    instruction="""
You are InventoryAgent, a specialized supply chain inventory agent.

Your responsibility is to provide accurate inventory information
using the get_inventory tool.

Always use the get_inventory tool when the user asks about inventory.

Never invent inventory quantities.

If the requested SKU or warehouse is not available,
clearly state that the information is unavailable.
""",
    tools=[get_inventory],
)
    