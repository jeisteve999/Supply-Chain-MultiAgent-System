def analyze_supply_risk(
    inventory_level: float,
    demand_forecast: float,
    incoming_supply: float = 0,
) -> str:
    """
    Analyzes supply risk using current inventory,
    forecasted demand, and incoming supply.
    """

    projected_inventory = (
        inventory_level + incoming_supply - demand_forecast
    )

    potential_shortage = max(-projected_inventory, 0)

    if projected_inventory < 0:
        risk = "HIGH"
    elif projected_inventory <= demand_forecast * 0.25:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return (
        f"Supply Risk: {risk}\n"
        f"Current Inventory: {inventory_level} units\n"
        f"Forecasted Demand: {demand_forecast} units\n"
        f"Incoming Supply: {incoming_supply} units\n"
        f"Potential Shortage: {potential_shortage} units\n"
        f"Projected Inventory: {projected_inventory} units"
    )


def analyze_delivery_risk(
    supplier_lead_time_days: float,
) -> str:
    """
    Analyzes delivery risk using supplier lead time.
    """

    if supplier_lead_time_days <= 7:
        risk = "LOW"
    elif supplier_lead_time_days <= 14:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return (
        f"Delivery Risk: {risk}\n"
        f"Supplier Lead Time: {supplier_lead_time_days} days"
    )


def analyze_overall_risk(
    supply_risk: str,
    delivery_risk: str,
) -> str:
    """
    Determines the overall supply chain risk.
    """

    if "HIGH" in supply_risk and "HIGH" in delivery_risk:
        overall_risk = "CRITICAL"
    elif "HIGH" in supply_risk or "HIGH" in delivery_risk:
        overall_risk = "HIGH"
    elif "MEDIUM" in supply_risk or "MEDIUM" in delivery_risk:
        overall_risk = "MEDIUM"
    else:
        overall_risk = "LOW"

    return f"Overall Supply Chain Risk: {overall_risk}"


def generate_supply_chain_recommendation(
    supply_risk: str,
    delivery_risk: str,
    overall_risk: str,
) -> str:
    """
    Generates an operational recommendation based on supply chain risk.
    """

    if overall_risk == "CRITICAL":
        recommendation = (
            "Immediate action required. Review inventory, "
            "accelerate replenishment, and investigate supplier lead time."
        )

    elif overall_risk == "HIGH":
        recommendation = (
            "High risk detected. Review replenishment requirements "
            "and supplier delivery lead time."
        )

    elif overall_risk == "MEDIUM":
        recommendation = (
            "Moderate risk detected. Monitor inventory levels, "
            "demand forecasts, and supplier lead time."
        )

    else:
        recommendation = (
            "Supply chain conditions are currently stable. "
            "Continue monitoring inventory, demand, and replenishment."
        )

    return (
        f"Supply Risk: {supply_risk}\n"
        f"Delivery Risk: {delivery_risk}\n"
        f"Overall Risk: {overall_risk}\n"
        f"Recommendation: {recommendation}"
    )