"""
Mock Enterprise ERP/CRM REST API Service
Simulates transactional enterprise endpoints.
"""
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MockERP_CRM")

# Mock Databases
INVENTORY_DB = {
    "PRD-101": {"name": "Enterprise Server Rack R740", "stock": 14, "warehouse": "US-East", "unit_price": 4500.00},
    "PRD-102": {"name": "Industrial Router X500", "stock": 3, "warehouse": "EU-West", "unit_price": 1200.00},
    "PRD-103": {"name": "Fiber Optic Cable 100m", "stock": 120, "warehouse": "AP-South", "unit_price": 85.00}
}

LEADS_DB = {
    "LEAD-501": {"client_name": "Acme Corp", "status": "New", "contact_email": "contact@acme.com", "owner": "Unassigned"},
    "LEAD-502": {"client_name": "Global Tech Ltd", "status": "Qualified", "contact_email": "sales@globaltech.com", "owner": "Alice Smith"}
}

TICKETS_DB = {}

class EnterpriseAPIService:
    """Simulates REST API endpoints for ERP and CRM operations."""

    @staticmethod
    def get_inventory(product_id: str) -> Dict[str, Any]:
        """GET /api/v1/erp/inventory/{product_id}"""
        logger.info(f"API CALL: GET /api/v1/erp/inventory/{product_id}")
        product = INVENTORY_DB.get(product_id.upper())
        if not product:
            return {"status": "error", "code": 404, "message": f"Product ID '{product_id}' not found in ERP inventory."}
        return {"status": "success", "code": 200, "data": {"product_id": product_id.upper(), **product}}

    @staticmethod
    def update_lead_status(lead_id: str, new_status: str, assigned_owner: str = None) -> Dict[str, Any]:
        """POST /api/v1/crm/leads/{lead_id}/update [Sensitive Write Operation]"""
        logger.info(f"API CALL: POST /api/v1/crm/leads/{lead_id}/update -> Status: {new_status}")
        lead_key = lead_id.upper()
        if lead_key not in LEADS_DB:
            return {"status": "error", "code": 404, "message": f"Lead ID '{lead_id}' not found in CRM database."}
        
        valid_statuses = ["New", "Contacted", "Qualified", "Proposal Sent", "Closed Won", "Closed Lost"]
        if new_status not in valid_statuses:
            return {"status": "error", "code": 400, "message": f"Invalid status '{new_status}'. Allowed: {valid_statuses}"}

        LEADS_DB[lead_key]["status"] = new_status
        if assigned_owner:
            LEADS_DB[lead_key]["owner"] = assigned_owner

        return {
            "status": "success",
            "code": 200,
            "message": f"Lead {lead_key} updated successfully.",
            "data": LEADS_DB[lead_key]
        }

    @staticmethod
    def create_support_ticket(title: str, priority: str, department: str, description: str) -> Dict[str, Any]:
        """POST /api/v1/erp/tickets/create [Sensitive Write Operation]"""
        logger.info(f"API CALL: POST /api/v1/erp/tickets/create -> Title: {title}")
        ticket_id = f"TCK-{len(TICKETS_DB) + 1001}"
        
        valid_priorities = ["Low", "Medium", "High", "Critical"]
        if priority.title() not in valid_priorities:
            return {"status": "error", "code": 400, "message": f"Invalid priority '{priority}'. Allowed: {valid_priorities}"}

        ticket = {
            "ticket_id": ticket_id,
            "title": title,
            "priority": priority.title(),
            "department": department,
            "description": description,
            "status": "Open"
        }
        TICKETS_DB[ticket_id] = ticket
        return {"status": "success", "code": 201, "message": f"Ticket {ticket_id} created successfully.", "data": ticket}