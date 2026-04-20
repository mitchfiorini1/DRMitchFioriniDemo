import streamlit as st
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from integrations.linear_client import get_ticket, _run_query

st.set_page_config(
    page_title="Ticket Sync Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Ticket Sync Agent")
st.caption("AI-powered Slack → Linear ticket updates")

# ── Live Ticket Status ──────────────────────────────────────────────
st.subheader("📋 Live Ticket Status")

if st.button("🔄 Refresh"):
    st.rerun()

try:
    result = _run_query("""
    query {
        issues {
            nodes {
                identifier
                title
                state { name }
                dueDate
                updatedAt
            }
        }
    }
    """)
    issues = result["data"]["issues"]["nodes"]

    for issue in issues:
        col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
        with col1:
            st.code(issue["identifier"])
        with col2:
            st.write(issue["title"])
        with col3:
            status = issue["state"]["name"]
            color = "🟢" if status == "Done" else "🟡" if status == "In Progress" else "⚪"
            st.write(f"{color} {status}")
        with col4:
            st.write(issue.get("dueDate") or "No due date")

except Exception as e:
    st.error(f"Could not fetch tickets: {e}")

# ── How It Works ────────────────────────────────────────────────────
st.divider()
st.subheader("⚙️ How It Works")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.info("**1. Trigger**\nTag the bot in any Slack thread")
with col2:
    st.info("**2. Read**\nAgent fetches and reads the full thread")
with col3:
    st.info("**3. Reason**\nLLM extracts what changed and why")
with col4:
    st.info("**4. Act**\nLinear updated, Slack notified")