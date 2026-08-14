import re

from app.inventory_agent import get_inventory
from app.forecast_agent import get_forecast
from app.procurement_agent import get_purchase_orders
from app.delivery_agent import get_delivery_status

from app.supply_chain_analysis import (
    analyze_supply_risk,
    analyze_delivery_risk,
    analyze_overall_risk,
    generate_supply_chain_recommendation,
)

from google.adk.tools.tool_context import ToolContext


def extract_number(text: str, label: str) -> float:
    """Extracts a numeric value following a label."""

    pattern = rf"{re.escape(label)}\s*:?\s*(-?\d+(?:\.\d+)?)"

    match = re.search(pattern, text, re.IGNORECASE)

    if not match:
        raise ValueError(
            f"Could not find '{label}' in tool response."
        )

    return float(match.group(1))


def extract_risk_level(text: str, label: str) -> str:
    """Extracts a risk level from an analysis result."""

    pattern = rf"{re.escape(label)}\s*:\s*(LOW|MEDIUM|HIGH|CRITICAL)"

    match = re.search(pattern, text, re.IGNORECASE)

    if not match:
        raise ValueError(
            f"Could not find '{label}' in analysis result."
        )

    return match.group(1).upper()


def run_supply_chain_analysis(
    sku: str,
    warehouse_id: str,
    tool_context: ToolContext,
) -> str:
    """
    Runs a complete supply chain analysis for a SKU and warehouse.

    The workflow retrieves factual information from the specialized
    supply chain tools and sends the results to the risk analysis
    functions.
    """



    inventory_result = get_inventory(
        sku,
        warehouse_id,
    )

    if inventory_result.startswith(
        "No inventory information"
    ):
        return inventory_result

    record_supply_chain_event(
        "inventory_checked",
        sku,
        inventory_result,
        tool_context,
    )


    forecast_result = get_forecast(
        sku,
        warehouse_id,
    )

    if forecast_result.startswith(
        "No forecast information"
    ):
        return forecast_result

    record_supply_chain_event(
        "forecast_checked",
        sku,
        forecast_result,
        tool_context,
    )



    procurement_result = get_purchase_orders(
        sku,
        warehouse_id,
    )

    if procurement_result.startswith(
        "No procurement information"
    ):
        return procurement_result

    record_supply_chain_event(
        "procurement_checked",
        sku,
        procurement_result,
        tool_context,
    )



    delivery_result = get_delivery_status(
        sku,
        warehouse_id,
    )

    if delivery_result.startswith(
        "No delivery information"
    ):
        return delivery_result

    record_supply_chain_event(
        "delivery_checked",
        sku,
        delivery_result,
        tool_context,
    )

    inventory = extract_number(
        inventory_result,
        "Inventory level",
    )

    forecast = extract_number(
        forecast_result,
        "Demand forecast",
    )

    order_quantity = extract_number(
        procurement_result,
        "Order quantity",
    )

    supplier_lead_time = extract_number(
        procurement_result,
        "Supplier lead time",
    )



    supply_risk_result = analyze_supply_risk(
        inventory_level=inventory,
        demand_forecast=forecast,
        incoming_supply=order_quantity,
    )

    supply_risk = extract_risk_level(
        supply_risk_result,
        "Supply Risk",
    )

    record_supply_chain_event(
        "supply_risk_analysis_completed",
        sku,
        supply_risk_result,
        tool_context,
    )



    delivery_risk_result = analyze_delivery_risk(
        supplier_lead_time_days=supplier_lead_time,
    )

    delivery_risk = extract_risk_level(
        delivery_risk_result,
        "Delivery Risk",
    )

    record_supply_chain_event(
        "delivery_risk_analysis_completed",
        sku,
        delivery_risk_result,
        tool_context,
    )



    overall_risk_result = analyze_overall_risk(
        supply_risk=supply_risk,
        delivery_risk=delivery_risk,
    )

    overall_risk = extract_risk_level(
        overall_risk_result,
        "Overall Supply Chain Risk",
    )

    recommendation = generate_supply_chain_recommendation(
        supply_risk=supply_risk,
        delivery_risk=delivery_risk,
        overall_risk=overall_risk,
    )

    record_supply_chain_event(
        "overall_risk_analysis_completed",
        sku,
        (
            f"{overall_risk_result}\n"
            f"Recommendation: {recommendation}"
        ),
        tool_context,
    )



    potential_shortage = max(
        forecast - inventory,
        0,
    )

    projected_inventory = (
        inventory
        + order_quantity
        - forecast
    )



    tool_context.state["current_sku"] = sku
    tool_context.state["current_warehouse"] = warehouse_id

    tool_context.state["inventory"] = inventory
    tool_context.state["forecast"] = forecast

    tool_context.state["order_quantity"] = order_quantity
    tool_context.state["incoming_supply"] = order_quantity

    tool_context.state["supplier_lead_time"] = supplier_lead_time

    tool_context.state["shortage"] = potential_shortage
    tool_context.state["projected_inventory"] = projected_inventory

    tool_context.state["supply_risk"] = supply_risk
    tool_context.state["delivery_risk"] = delivery_risk
    tool_context.state["overall_risk"] = overall_risk

    tool_context.state["recommendation"] = recommendation


    return (
        f"{inventory_result}\n\n"
        f"{forecast_result}\n\n"
        f"{procurement_result}\n\n"
        f"{delivery_result}\n\n"
        f"{supply_risk_result}\n\n"
        f"{delivery_risk_result}\n\n"
        f"{overall_risk_result}\n"
        f"Potential Shortage: "
        f"{potential_shortage:.2f} units\n"
        f"Projected Inventory After Demand: "
        f"{projected_inventory:.2f} units\n"
        f"Recommendation: {recommendation}"
    )


def save_supply_chain_state(
    sku: str,
    warehouse_id: str,
    tool_context: ToolContext,
) -> str:
    """Runs analysis and saves the resulting supply chain state."""

    result = run_supply_chain_analysis(
        sku,
        warehouse_id,
        tool_context,
    )

    record_supply_chain_event(
        "state_saved",
        sku,
        result,
        tool_context,
    )

    return (
        f"Supply chain state updated for "
        f"{sku} at {warehouse_id}.\n\n"
        f"{result}"
    )


def record_supply_chain_event(
    event_type: str,
    sku: str,
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
        "sku": sku,
        "details": details,
    }

    events.append(event)

    tool_context.state["supply_chain_events"] = events

    return (
        f"Event recorded: {event_type} for {sku}."
    )


def get_supply_chain_state(
    sku: str,
    warehouse_id: str,
    tool_context: ToolContext,
) -> dict:
    """Returns the current supply chain state."""

    current_sku = tool_context.state.get(
        "current_sku"
    )

    current_warehouse = tool_context.state.get(
        "current_warehouse"
    )

    if (
        current_sku != sku
        or current_warehouse != warehouse_id
    ):
        return {
            "sku": sku,
            "warehouse": warehouse_id,
            "status": "not_analyzed",
            "message": (
                f"No saved state is available for "
                f"{sku} at {warehouse_id}."
            ),
        }

    return {
        "sku": sku,
        "warehouse": warehouse_id,
        "inventory": tool_context.state.get("inventory"),
        "forecast": tool_context.state.get("forecast"),
        "order_quantity": tool_context.state.get(
            "order_quantity"
        ),
        "incoming_supply": tool_context.state.get(
            "incoming_supply"
        ),
        "supplier_lead_time": tool_context.state.get(
            "supplier_lead_time"
        ),
        "shortage": tool_context.state.get(
            "shortage"
        ),
        "projected_inventory": tool_context.state.get(
            "projected_inventory"
        ),
        "supply_risk": tool_context.state.get(
            "supply_risk"
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
    warehouse_id: str,
    tool_context: ToolContext,
) -> str:
    """Analyzes multiple SKUs for one warehouse."""

    product_list = [
        product.strip()
        for product in products.split(",")
        if product.strip()
    ]

    if not product_list:
        return "No SKUs were provided."

    results = []

    for sku in product_list:

        result = run_supply_chain_analysis(
            sku,
            warehouse_id,
            tool_context,
        )

        results.append(
            f"=== {sku} / {warehouse_id} ===\n"
            f"{result}"
        )

    return "\n\n".join(results)