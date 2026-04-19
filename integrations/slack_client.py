import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

def fetch_thread(channel_id: str, thread_ts: str) -> list:
    """Fetch all messages in a Slack thread."""
    try:
        result = client.conversations_replies(
            channel=channel_id,
            ts=thread_ts
        )
        messages = result["messages"]
        # Return clean list of {user, text} dicts
        return [
            {
                "user": m.get("user", "unknown"),
                "text": m.get("text", "")
            }
            for m in messages
        ]
    except SlackApiError as e:
        raise Exception(f"Slack API error: {e.response['error']}")

def post_message(channel_id: str, thread_ts: str, text: str):
    """Post a reply into a Slack thread."""
    try:
        client.chat_postMessage(
            channel=channel_id,
            thread_ts=thread_ts,
            text=text
        )
    except SlackApiError as e:
        raise Exception(f"Slack API error: {e.response['error']}")