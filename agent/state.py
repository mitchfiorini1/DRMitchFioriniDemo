from typing import TypedDict, Optional

class AgentState(TypedDict):
    # Slack context
    channel_id: str
    thread_ts: str
    triggered_by: str          # user ID who @mentioned the bot

    # Thread content
    thread_messages: list      # raw messages from the thread

    # Linear context
    ticket_id: Optional[str]   # e.g. "ENG-1"
    current_ticket: Optional[dict]  # fetched from Linear

    # Agent decisions
    proposed_updates: Optional[dict]  # what the LLM extracted
    update_confirmed: bool     # did the Linear update succeed

    # Output
    slack_reply: Optional[str] # message posted back to thread
    error: Optional[str]       # anything that went wrong