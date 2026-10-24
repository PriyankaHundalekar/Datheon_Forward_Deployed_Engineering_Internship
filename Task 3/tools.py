import json
from mock_apis import EnterpriseAPIService

TOOLS_SCHEMA = [
    {
        "name": "lookup_inventory",
        "description": "Retrieves real-time stock levels, warehouse location, and pricing for a product from the ERP.",
        "is_sensitive": False,  # Read-only operation
        "parameters": {
            "type": "object",
            "properties": {
                "product_id": {"type": "string", "description": "The product code, e.g., 'PRD-101', 'PRD-102'."}
            },
            "required": ["product_id"]
        }
    },
    {
        "name": "update_lead_status",
        "description": "Updates the pipeline status and owner for a lead in the CRM.",
        "is_sensitive": True,   # Sensitive Write Operation requires HITL
        "parameters": {
            "type": "object",
            "properties": {
                "lead_id": {"type": "string", "description": "The CRM Lead ID, e.g., 'LEAD-501'."},
                "new_status": {"type": "string", "description": "New status: 'New', 'Contacted', 'Qualified', 'Proposal Sent', 'Closed Won', 'Closed Lost'."},
                "assigned_owner": {"type": "string", "description": "Optional owner name to assign."}
            },
            "required": ["lead_id", "new_status"]
        }
    },
    {
        "name": "create_support_ticket",
        "description": "Creates a new IT or operational support ticket in the enterprise system.",
        "is_sensitive": True,   # Sensitive Write Operation requires HITL
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Brief title of the issue."},
                "priority": {"type": "string", "description": "Priority level: 'Low', 'Medium', 'High', 'Critical'."},
                "department": {"type": "string", "description": "Target department, e.g., 'IT', 'Logistics', 'Billing'."},
                "description": {"type": "string", "description": "Detailed description of the issue."}
            },
            "required": ["title", "priority", "department", "description"]
        }
    }
]

def execute_tool(tool_name: str, kwargs: dict) -> dict:
    """Routes tool execution requests to the appropriate mock API service."""
    if tool_name == "lookup_inventory":
        return EnterpriseAPIService.get_inventory(kwargs.get("product_id", ""))
    elif tool_name == "update_lead_status":
        return EnterpriseAPIService.update_lead_status(
            lead_id=kwargs.get("lead_id", ""),
            new_status=kwargs.get("new_status", ""),
            assigned_owner=kwargs.get("assigned_owner")
        )
    elif tool_name == "create_support_ticket":
        return EnterpriseAPIService.create_support_ticket(
            title=kwargs.get("title", ""),
            priority=kwargs.get("priority", "Medium"),
            department=kwargs.get("department", "General"),
            description=kwargs.get("description", "")
        )
    else:
        return {"status": "error", "message": f"Unknown tool name '{tool_name}'."}