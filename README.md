The repo is an AI agent that monitors Slack threads and automatically updates Linear tickets based on team conversations.

## What It Does

When tagged in a Slack thread, the agent:
1. Reads the full thread conversation
2. Identifies any Linear ticket references (e.g. DEM-1)
3. Determines what needs to be changed based on the thread (status, due dates, notes)
4. Updates the Linear ticket automatically
5. Posts a confirmation back to the thread


## Setup

1. Clone the repo

```bash
git clone https://github.com/mitchfiorini1/DRMitchFioriniDemo.git
cd DRMitchFioriniDemo
```

2. Create and activate virtual environment

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Configure environment variables

```
cp .env.example .env
```

Then populate with proper keys/tokens

4. Slack App Configuration

Create a Slack app at api.slack.com/apps with:
- Socket Mode enabled
- Bot Token Scopes: app_mentions:read, channels:history, chat:write, users:read
- Event Subscriptions: app_mention

5. Run the agent

```
python main.py
```

## Why ReAct?

Rather than a hardcoded pipeline, this agent uses a ReAct loop. The LLM decides which tools to call and in what order based on what it finds in the thread. This makes it flexible enough to handle varied conversation styles without brittle rule-based logic.

## Why Socket Mode?

Socket Mode opens a WebSocket connection from your machine outward to Slack so it never needs to reach your local server.
