import re

from app.inventory_agent import get_inventory
from app.forecast_agent import get_forecast
from app.procurement_agent import get_purchase_orders
from app.delivery_agent import get_delivery_status

from app.supply_chain_analysis import (
    analyze_supply_risk,
    analyze_delivery_risk,
    generate_supply_chain_recommendation,
)

from google.adk.tools.tool_context import ToolContext


def extract_number(
    text: str,
    label: str,
) -> int:
    """Extracts an integer value following a specific label."""

    pattern = rf"{re.escape(label)}\s*:?\s*(\d+)"

    match = re.search(
        pattern,
        text,
        re.IGNORECASE,
    )

    if not match:
        raise ValueError(
            f"Could not find '{label}' in tool response."
        )

    return int(match.group(1))


def extract_delivery_status(
    text: str,
) -> str:
    """Extracts delivery status from a delivery tool response."""

    pattern = r"Delivery status\s*:\s*(.+)"

    match = re.search(
        pattern,
        text,
        re.IGNORECASE,
    )

    if not match:
        raise ValueError(
            "Could not find 'Delivery status' in tool response."
        )

    return match.group(1).strip()


def extract_risk_level(
    text: str,
) -> str:
    """Extracts a risk level from an analysis result."""

    pattern = (
        r"(?:Supply Risk|Delivery Risk)"
        r"\s*:\s*"
        r"(LOW|HIGH|UNKNOWN|CRITICAL)"
    )

    match = re.search(
        pattern,
        text,
        re.IGNORECASE,
    )

    if not match:
        raise ValueError(
            "Could not find a valid risk level in analysis result."
        )

    return match.group(1).upper()


def calculate_overall_risk(
    supply_risk: str,
    delivery_risk: str,
) -> str:
    """Calculates the overall supply chain risk."""

    supply = supply_risk.upper()
    delivery = delivery_risk.upper()

    if supply == "HIGH" and delivery == "HIGH":
        return "CRITICAL"

    if supply == "HIGH" or delivery == "HIGH":
        return "HIGH"

    if supply == "LOW" and delivery == "LOW":
        return "LOW"

    return "UNKNOWN"


def run_supply_chain_analysis(
    product: str,
    tool_context: ToolContext,
) -> str:
    """Runs a complete supply chain risk analysis."""


    inventory_result = get_inventory(product)

    if inventory_result.startswith(
        "No inventory information"
    ):
        return inventory_result

    record_supply_chain_event(
        "inventory_checked",
        product,
        inventory_result,
        tool_context,
    )


    forecast_result = get_forecast(product)

    if forecast_result.startswith(
        "No forecast information"
    ):
        return forecast_result

    record_supply_chain_event(
        "forecast_checked",
        product,
        forecast_result,
        tool_context,
    )


    procurement_result = get_purchase_orders(product)

    if procurement_result.startswith(
        "No purchase order information"
    ):
        return procurement_result

    record_supply_chain_event(
        "purchase_order_checked",
        product,
        procurement_result,
        tool_context,
    )


    delivery_result = get_delivery_status(product)

    if delivery_result.startswith(
        "No delivery information"
    ):
        return delivery_result

    record_supply_chain_event(
        "delivery_checked",
        product,
        delivery_result,
        tool_context,
    )


    inventory = extract_number(
        inventory_result,
        "Available units",
    )

    forecast = extract_number(
        forecast_result,
        "Forecasted demand",
    )

    incoming = extract_number(
        procurement_result,
        "Incoming quantity",
    )

    delivery_status = extract_delivery_status(
        delivery_result,
    )

    risk_result = analyze_supply_risk(
        inventory=inventory,
        forecast=forecast,
        incoming=incoming,
    )

    supply_risk = extract_risk_level(
        risk_result,
    )

    record_supply_chain_event(
        "supply_risk_analysis_completed",
        product,
        risk_result,
        tool_context,
    )


    delivery_risk_result = analyze_delivery_risk(
        delivery_status,
    )

    delivery_risk = extract_risk_level(
        delivery_risk_result,
    )

    record_supply_chain_event(
        "delivery_risk_analysis_completed",
        product,
        delivery_risk_result,
        tool_context,
    )


    overall_risk = calculate_overall_risk(
        supply_risk,
        delivery_risk,
    )

    recommendation = (
        generate_supply_chain_recommendation(
            supply_risk,
            delivery_risk,
        )
    )

    record_supply_chain_event(
        "overall_risk_analysis_completed",
        product,
        recommendation,
        tool_context,
    )


    shortage = max(
        forecast - inventory,
        0,
    )

    tool_context.state["current_product"] = product
    tool_context.state["inventory"] = inventory
    tool_context.state["forecast"] = forecast
    tool_context.state["incoming_supply"] = incoming
    tool_context.state["shortage"] = shortage
    tool_context.state["supply_risk"] = supply_risk
    tool_context.state["delivery_status"] = delivery_status
    tool_context.state["delivery_risk"] = delivery_risk
    tool_context.state["overall_risk"] = overall_risk
    tool_context.state["recommendation"] = recommendation

    return (
        f"{inventory_result}\n"
        f"{forecast_result}\n"
        f"{procurement_result}\n"
        f"{delivery_result}\n"
        f"{risk_result}\n"
        f"{delivery_risk_result}\n"
        f"{recommendation}"
    )


def save_supply_chain_state(
    product: str,
    tool_context: ToolContext,
) -> str:
    """Gets supply chain information and saves it to session state."""

    inventory_result = get_inventory(product)

    if inventory_result.startswith(
        "No inventory information"
    ):
        return inventory_result


    forecast_result = get_forecast(product)

    if forecast_result.startswith(
        "No forecast information"
    ):
        return forecast_result


    procurement_result = get_purchase_orders(product)

    if procurement_result.startswith(
        "No purchase order information"
    ):
        return procurement_result


    delivery_result = get_delivery_status(product)

    if delivery_result.startswith(
        "No delivery information"
    ):
        return delivery_result

    inventory = extract_number(
        inventory_result,
        "Available units",
    )

    forecast = extract_number(
        forecast_result,
        "Forecasted demand",
    )

    incoming = extract_number(
        procurement_result,
        "Incoming quantity",
    )

    delivery_status = extract_delivery_status(
        delivery_result,
    )

    risk_result = analyze_supply_risk(
        inventory=inventory,
        forecast=forecast,
        incoming=incoming,
    )

    supply_risk = extract_risk_level(
        risk_result,
    )


    delivery_risk_result = analyze_delivery_risk(
        delivery_status,
    )

    delivery_risk = extract_risk_level(
        delivery_risk_result,
    )



    overall_risk = calculate_overall_risk(
        supply_risk,
        delivery_risk,
    )

    recommendation = (
        generate_supply_chain_recommendation(
            supply_risk,
            delivery_risk,
        )
    )


    shortage = max(
        forecast - inventory,
        0,
    )

    tool_context.state["current_product"] = product
    tool_context.state["inventory"] = inventory
    tool_context.state["forecast"] = forecast
    tool_context.state["incoming_supply"] = incoming
    tool_context.state["shortage"] = shortage
    tool_context.state["supply_risk"] = supply_risk
    tool_context.state["delivery_status"] = delivery_status
    tool_context.state["delivery_risk"] = delivery_risk
    tool_context.state["overall_risk"] = overall_risk
    tool_context.state["recommendation"] = recommendation

    record_supply_chain_event(
        "state_saved",
        product,
        recommendation,
        tool_context,
    )

    return (
        f"Supply chain state updated for {product}.\n"
        f"Inventory: {inventory}.\n"
        f"Forecast: {forecast}.\n"
        f"Incoming supply: {incoming}.\n"
        f"Shortage: {shortage}.\n"
        f"Supply risk: {supply_risk}.\n"
        f"Delivery status: {delivery_status}.\n"
        f"Delivery risk: {delivery_risk}.\n"
        f"Overall risk: {overall_risk}.\n"
        f"Recommendation: {recommendation}"
    )


def record_supply_chain_event(
    event_type: str,
    product: str,
    details: str,
    tool_context: ToolContext,
) -> str:
    """Records an operational supply chain event."""

    events = tool_context.state.get(
        "supply_chain_events",
        [],
    )

    event = {
        "event_type": event_type,
        "product": product,
        "details": details,
    }

    events.append(event)

    tool_context.state["supply_chain_events"] = events

    return (
        f"Event recorded: {event_type} for {product}."
    )


def get_supply_chain_state(
    product: str,
    tool_context: ToolContext,
) -> dict:
    """Returns the current supply chain state for a product."""

    current_product = tool_context.state.get(
        "current_product"
    )

    if current_product != product:
        return {
            "product": product,
            "status": "not_analyzed",
            "message": (
                f"No saved state is available for {product}."
            ),
        }

    return {
        "product": product,
        "inventory": tool_context.state.get(
            "inventory"
        ),
        "forecast": tool_context.state.get(
            "forecast"
        ),
        "incoming_supply": tool_context.state.get(
            "incoming_supply"
        ),
        "shortage": tool_context.state.get(
            "shortage"
        ),
        "supply_risk": tool_context.state.get(
            "supply_risk"
        ),
        "delivery_status": tool_context.state.get(
            "delivery_status"
        ),
        "delivery_risk": tool_context.state.get(
            "delivery_risk"
        ),
        "overall_risk": tool_context.state.get(
            "overall_risk"
        ),
        "recommendation": tool_context.state.get(
            "recommendation"
        ),
        "status": "available",
    }


def get_supply_chain_events(
    tool_context: ToolContext,
) -> list:
    """Returns the supply chain event history."""

    return tool_context.state.get(
        "supply_chain_events",
        [],
    )

def analyze_multiple_products(
    products: str,
    tool_context: ToolContext,
) -> str:
    """Analyzes multiple products and returns a risk summary."""

    product_list = [
        product.strip()
        for product in products.split(",")
        if product.strip()
    ]

    if not product_list:
        return "No products were provided."

    results = []

    for product in product_list:
        result = run_supply_chain_analysis(
            product,
            tool_context,
        )

        results.append(
            f"=== {product} ===\n"
            f"{result}"
        )

    return "\n\n".join(results)