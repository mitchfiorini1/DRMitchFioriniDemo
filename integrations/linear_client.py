import os
import httpx
from dotenv import load_dotenv
load_dotenv()

LINEAR_API_URL = "https://api.linear.app/graphql"

def _run_query(query: str, variables: dict = None):
    """Execute a GraphQL query against the Linear API."""
    response = httpx.post(
        LINEAR_API_URL,
        headers={"Authorization": os.environ["LINEAR_API_KEY"]},
        json={"query": query, "variables": variables or {}}
    )
    response.raise_for_status()
    return response.json()

def get_ticket(ticket_id: str) -> dict:
    """Fetch a ticket by its identifier (e.g. 'DEM-1')."""
    query = """
    query {
        issues {
            nodes {
                id
                identifier
                title
                state { name }
                assignee { name email }
                dueDate
            }
        }
    }
    """
    result = _run_query(query)
    issues = result["data"]["issues"]["nodes"]
    match = next((i for i in issues if i["identifier"] == ticket_id), None)
    if not match:
        raise Exception(f"Ticket {ticket_id} not found in Linear")
    return match

def update_ticket(ticket_id: str, updates: dict) -> bool:
    """
    Update a ticket in Linear.
    updates can contain: status, dueDate, comment
    """
    ticket = get_ticket(ticket_id)
    internal_id = ticket["id"]
    results = []

    if "status" in updates:
        state_id = get_state_id(updates["status"])
        if state_id:
            mutation = """
            mutation UpdateIssue($id: String!, $stateId: String!) {
                issueUpdate(id: $id, input: { stateId: $stateId }) {
                    success
                }
            }
            """
            r = _run_query(mutation, {"id": internal_id, "stateId": state_id})
            results.append(r["data"]["issueUpdate"]["success"])

    if "dueDate" in updates:
        mutation = """
        mutation UpdateIssue($id: String!, $dueDate: TimelessDate!) {
            issueUpdate(id: $id, input: { dueDate: $dueDate }) {
                success
            }
        }
        """
        r = _run_query(mutation, {"id": internal_id, "dueDate": updates["dueDate"]})
        results.append(r["data"]["issueUpdate"]["success"])

    if "comment" in updates:
        mutation = """
        mutation CreateComment($issueId: String!, $body: String!) {
            commentCreate(input: { issueId: $issueId, body: $body }) {
                success
            }
        }
        """
        r = _run_query(mutation, {"issueId": internal_id, "body": updates["comment"]})
        results.append(r["data"]["commentCreate"]["success"])

    return all(results)

def get_state_id(state_name: str) -> str:
    """Look up a workflow state ID by name."""
    query = """
    query {
        workflowStates {
            nodes { id name }
        }
    }
    """
    result = _run_query(query)
    states = result["data"]["workflowStates"]["nodes"]
    match = next((s for s in states if s["name"].lower() == state_name.lower()), None)
    return match["id"] if match else None