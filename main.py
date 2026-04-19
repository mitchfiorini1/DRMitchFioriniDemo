import os
from dotenv import load_dotenv
load_dotenv()

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(token=os.environ["SLACK_BOT_TOKEN"])

@app.event("app_mention")
def handle_mention(event, say):
    print(f"✅ Bot mentioned by {event.get('user')}")
    print(f"   Channel: {event.get('channel')}")
    print(f"   Thread: {event.get('thread_ts')}")
    print(f"   Text: {event.get('text')}")

    # Acknowledge in the thread
    say(text="Got it, looking at this thread now...", thread_ts=event.get("thread_ts"))

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()