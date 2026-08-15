# Supply-Chain-MultiAgent-System
SupplyChainMultiAgent is a multi-agent AI system for supply chain and logistics risk analysis, built with Gemini and Google ADK. It coordinates specialized agents for inventory, forecasting, procurement, and delivery to identify risks, compare products, track events, maintain session state, and generate recommendations.


### Multi-Agent AI System for Supply Chain and Logistics Risk Analysis

SupplyChainMultiAgent is a multi-agent AI system built with Python, Google ADK, and Gemini. It coordinates specialized agents and tools to analyze inventory, demand forecasts, procurement, deliveries, and supply chain risks.

The system combines operational data from different areas of the supply chain to identify risks, compare multiple products, maintain session state, track operational events, and generate actionable recommendations.

---

## Overview

Supply chains generate information across multiple operational areas:

- Inventory
- Demand forecasting
- Procurement
- Purchase orders
- Deliveries
- Supply shortages
- Delivery delays
- Risk assessment

In a traditional workflow, this information may exist in different systems or departments. An analyst must manually collect the information, compare it, calculate risks, and determine which products require attention.

SupplyChainMultiAgent was designed to automate this process through a coordinated multi-agent architecture.

Instead of relying on a single agent to perform every task, the system uses specialized components responsible for specific areas of the supply chain.

---

# Problem Statement

Supply chain risk analysis often requires combining information from several operational sources.

For example, determining whether a product is at risk may require answering:

1. How much inventory is currently available?
2. What is the forecasted demand?
3. How much supply is currently incoming?
4. Will the incoming supply cover a potential shortage?
5. Is the delivery on time?
6. Is the delivery delayed?
7. Which product has the highest overall risk?
8. What action should be taken?

Performing these steps manually can be slow, repetitive, and error-prone.

The objective of SupplyChainMultiAgent is to create an AI-powered system capable of coordinating these tasks and producing a unified supply chain risk assessment.

---

# Solution

SupplyChainMultiAgent uses a multi-agent architecture in which a root coordinator manages specialized supply chain capabilities.

The system can:

- Retrieve inventory information.
- Retrieve demand forecasts.
- Retrieve procurement information.
- Retrieve delivery information.
- Calculate supply risk.
- Calculate delivery risk.
- Determine overall supply chain risk.
- Compare multiple products.
- Save operational information into session state.
- Record supply chain events.
- Retrieve previous information from the current session.
- Generate recommendations based on the analysis.

The system is designed to use factual information obtained through tools rather than inventing operational data.

---

# Architecture

The main architecture is based on a coordinating root agent and specialized supply chain capabilities.

```text
                         USER
                           |
                           v
                 SupplyChainMultiAgent
                      Root Agent
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
      Inventory         Forecast        Procurement
        Agent             Agent             Agent
          |                |                |
          +----------------+----------------+
                           |
                           v
                     Delivery Agent
                           |
                           v
                Supply Chain Workflow
                           |
              +------------+------------+
              |            |            |
              v            v            v
        Supply Risk   Delivery Risk  Recommendation
              |            |            |
              +------------+------------+
                           |
                           v
                    Overall Risk
                           |
             +-------------+-------------+
             |                           |
             v                           v
        Session State                 Events


# Multi-Agent Design

The system uses a coordinating root agent with specialized supply chain capabilities.

### Root Agent
Coordinates the analysis, selects the appropriate tools, maintains session context, and combines results.

### Inventory Agent
Provides current inventory and available units.

### Forecast Agent
Provides forecasted demand for each product.

### Procurement Agent
Provides incoming supply, purchase orders, status, and expected arrival dates.

### Delivery Agent
Provides delivery status, quantities, and expected delivery dates.

---

# Risk Analysis

## Supply Risk

Supply risk is calculated using:

- Current inventory
- Forecasted demand
- Incoming supply

Potential shortage:

shortage = max(forecasted_demand - current_inventory, 0)
