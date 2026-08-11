def analyze_supply_risk(
    inventory: int,
    forecast: int,
    incoming: int,
) -> str:
    """Analyzes supply risk based on inventory, demand and incoming supply."""

    shortage = forecast - inventory

    if shortage <= 0:
        surplus = abs(shortage)

        return (
            "Supply Risk: LOW\n"
            f"Current inventory: {inventory} units\n"
            f"Forecasted demand: {forecast} units\n"
            f"Incoming supply: {incoming} units\n"
            "There is no potential shortage.\n"
            f"Current inventory surplus: {surplus} units.\n"
            "Recommendation: Continue monitoring inventory and demand."
        )

    if incoming >= shortage:
        remaining_inventory = (
            inventory + incoming - forecast
        )

        return (
            "Supply Risk: LOW\n"
            f"Current inventory: {inventory} units\n"
            f"Forecasted demand: {forecast} units\n"
            f"Incoming supply: {incoming} units\n"
            f"Potential shortage before replenishment: {shortage} units.\n"
            "Incoming supply covers the shortage.\n"
            f"Projected remaining inventory after forecasted demand: "
            f"{remaining_inventory} units.\n"
            "Recommendation: Monitor the incoming shipment and "
            "confirm that it arrives before the forecasted demand period."
        )

    remaining_shortage = shortage - incoming

    return (
        "Supply Risk: HIGH\n"
        f"Current inventory: {inventory} units\n"
        f"Forecasted demand: {forecast} units\n"
        f"Incoming supply: {incoming} units\n"
        f"Potential shortage: {shortage} units.\n"
        "Incoming supply is not sufficient.\n"
        f"Remaining shortage after incoming supply: "
        f"{remaining_shortage} units.\n"
        "Recommendation: Review replenishment options and "
        "consider expediting additional supply."
    )


def analyze_delivery_risk(
    delivery_status: str,
) -> str:
    """Analyzes delivery risk based on delivery status."""

    status = delivery_status.lower()

    if status == "delayed":
        return (
            "Delivery Risk: HIGH\n"
            "The delivery is delayed. "
            "Review the shipment and consider corrective action."
        )

    if status == "on time":
        return (
            "Delivery Risk: LOW\n"
            "The delivery is currently on schedule."
        )

    return (
        "Delivery Risk: UNKNOWN\n"
        "The delivery status could not be clearly evaluated."
    )


def generate_supply_chain_recommendation(
    supply_risk: str,
    delivery_risk: str,
) -> str:
    """Generates an overall supply chain recommendation."""

    supply = supply_risk.upper()
    delivery = delivery_risk.upper()

    if supply == "HIGH" and delivery == "HIGH":
        return (
            "Overall Supply Chain Risk: CRITICAL\n"
            "The product has both a supply shortage and a "
            "delivery risk. Review replenishment options, "
            "expedite incoming shipments, and monitor the "
            "delivery closely."
        )

    if supply == "HIGH" and delivery == "LOW":
        return (
            "Overall Supply Chain Risk: HIGH\n"
            "The product has a supply shortage, but the "
            "delivery is currently on schedule. "
            "Review additional replenishment options."
        )

    if supply == "LOW" and delivery == "HIGH":
        return (
            "Overall Supply Chain Risk: HIGH\n"
            "Supply is currently sufficient, but the delivery "
            "is delayed. Monitor the shipment and evaluate "
            "alternative delivery options if necessary."
        )

    if supply == "LOW" and delivery == "LOW":
        return (
            "Overall Supply Chain Risk: LOW\n"
            "Supply and delivery are currently under control. "
            "Continue monitoring inventory and incoming shipments."
        )

    return (
        "Overall Supply Chain Risk: UNKNOWN\n"
        "There is insufficient information to determine the "
        "overall supply chain risk."
    )