import pandas as pd
from google.adk.agents import Agent


DATA_PATH = "data/supply_chain_dataset1.csv"


def get_forecast(sku_id: str, warehouse_id: str = "") -> str:
    """Returns the latest demand forecast for a SKU and warehouse."""

    df = pd.read_csv(DATA_PATH)

    filtered = df[df["SKU_ID"].str.upper() == sku_id.upper()]

    if warehouse_id:
        filtered = filtered[
            filtered["Warehouse_ID"].str.upper() == warehouse_id.upper()
        ]

    if filtered.empty:
        return f"No forecast information is available for {sku_id}."

    latest = filtered.sort_values("Date").iloc[-1]

    return (
        f"SKU: {latest['SKU_ID']}\n"
        f"Warehouse: {latest['Warehouse_ID']}\n"
        f"Date: {latest['Date']}\n"
        f"Demand forecast: {latest['Demand_Forecast']:.2f}\n"
        f"Units sold: {int(latest['Units_Sold'])}"
    )


forecast_agent = Agent(
    name="forecast_agent",
    model="gemini-3.5-flash",
    description="Specialized agent for supply chain demand forecasting.",
    instruction="""
You are ForecastAgent, a specialized supply chain forecasting agent.

Your responsibility is to provide accurate demand forecast information
using the get_forecast tool.

Always use the get_forecast tool when the user asks about:
- future demand
- expected demand
- demand forecasts
- forecasted quantities

Never invent forecast data.

If the requested SKU or warehouse is not available,
clearly state that the information is unavailable.
""",
    tools=[get_forecast],
)