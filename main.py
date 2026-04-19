import os
from dotenv import load_dotenv
load_dotenv()

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from langchain_core.messages import HumanMessage
from agent.graph import agent

app = App(token=os.environ["SLACK_BOT_TOKEN"])

@app.event("app_mention")
def handle_mention(event, say):
    channel_id = event.get("channel")
    thread_ts = event.get("thread_ts") or event.get("ts")
    user = event.get("user")

    print(f"✅ Mention received from {user} in thread {thread_ts}")

    # Kick off the agent
    initial_message = HumanMessage(
        content=f"""A user tagged me in a Slack thread.
Channel ID: {channel_id}
Thread timestamp: {thread_ts}
Triggered by user: {user}

Please fetch the thread, find any Linear tickets mentioned, and apply any updates discussed."""
    )

    result = agent.invoke({"messages": [initial_message]})
    print(f"✅ Agent completed. Final message: {result['messages'][-1].content}")

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()