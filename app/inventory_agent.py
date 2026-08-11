from google.adk.agents import Agent

def get_inventory(product_name: str) -> str:
    """Returns the current inventory quantity for a product."""
    
    inventory = {
        "product a": 150,
        "product b": 80,
        "product c": 220,
    }
    
    product = product_name.lower()
    
    if product in inventory:
        return (f"Product: {product_name}\n"
                f"Available units: {inventory[product]}"
        )            
    
    return f"No inventory information is available for {product_name}"

inventory_agent = Agent(
    name ="inventory_agent",
    model= "gemini-3.5-flash",
    description ="Specialized agent responsible for inventory analysis",
    instruction = """
    You are InventoryAgent, a specialized supply chain inventory agent.
    
    Your responsibility is to provide accurate information about
    currently inventory levels.
    
    Always use the get_inventory tool when user asks about
    available inventory.
    
    Never invent inventory quantities.
    
    If inventory information is not available, clearly say so.
    """,
    tools= [get_inventory],
)
    