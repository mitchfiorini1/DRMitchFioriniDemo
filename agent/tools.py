import re
import json
from langchain_core.tools import tool
from integrations.slack_client import fetch_thread, post_message
from integrations.linear_client import get_ticket, update_ticket

@tool
def fetch_slack_thread(channel_id: str, thread_ts: str) -> str:
    """Fetch all messages from a Slack thread and return them as a readable conversation."""
    messages = fetch_thread(channel_id, thread_ts)
    formatted = "\n".join([f"- {m['user']}: {m['text']}" for m in messages])
    return formatted

@tool
def get_linear_ticket(ticket_id: str) -> str:
    """Fetch the current state of a Linear ticket by its ID (e.g. DEM-1)."""
    ticket = get_ticket(ticket_id)
    return json.dumps(ticket, indent=2)

@tool
def update_linear_ticket(ticket_id: str, updates_json: str) -> str:
    """
    Update a Linear ticket with the provided changes.
    updates_json should be a JSON string with optional fields:
    - status: new status name (e.g. 'In Progress', 'Done')
    - dueDate: new due date in YYYY-MM-DD format
    - comment: a comment to add to the ticket
    """
    try:
        updates = json.loads(updates_json)
        success = update_ticket(ticket_id, updates)
        if success:
            return f"Successfully updated {ticket_id} with: {updates}"
        else:
            return f"Failed to update {ticket_id}"
    except json.JSONDecodeError:
        return "Error: updates_json must be valid JSON"

@tool
def post_slack_message(channel_id: str, thread_ts: str, message: str) -> str:
    """Post a message back into a Slack thread."""
    post_message(channel_id, thread_ts, message)
    return "Message posted successfully"