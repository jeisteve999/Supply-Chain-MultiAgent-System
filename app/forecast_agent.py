from google.adk.agents import Agent

def get_forecast(product_name:str) -> str:
    """Returns the forecasted demand for a product"""
    
    forecast = {
        "product a": 180,
        "product b": 120,
        "product c": 250,
    }
    
    product = product_name.lower()
    
    if product in forecast:
        return (
            f"Product: {product_name}\n"
            f"Forecasted demand: {forecast[product]}"
        )
        
    return f"No forecast information is available for {product_name}"


forecast_agent = Agent (
    name ="forecast_agent",
    model ="gemini-3.5-flash",
    description = "Specialized agent for supply chain demand forecasting.",
    instruction = """ 
    You are ForecastAgent, a specialized supply chain forecastig agent.
    
    Your responsibility is to provide demand forecasts for products.
    
    Use the get_forecast tool whenever the user asks about:
    -future demand
    -expected demand
    -demand forecasts
    -forecasted product quantities
    
    Never invent forecast data
    If the tool does not have information about the requested product,
    Clearly state that forecastdata is unavailable.
    """,
        tools = [get_forecast],
)