from langchain_anthropic import ChatAnthropic
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode, tools_condition
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
import operator

# Define tools list
from agent.tools import (
    fetch_slack_thread,
    get_linear_ticket,
    update_linear_ticket,
    post_slack_message
)

tools = [
    fetch_slack_thread,
    get_linear_ticket,
    update_linear_ticket,
    post_slack_message
]

# create LLM and bind tools
llm = ChatAnthropic(model="claude-opus-4-5").bind_tools(tools)

# State is just a list of messages — the LLM reasons through them
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]

SYSTEM_PROMPT = """You are a ticket management agent. When triggered in a Slack thread:

1. Use fetch_slack_thread to read the full conversation
2. Identify any Linear ticket IDs mentioned (format: ABC-123)
3. Use get_linear_ticket to fetch the current ticket state
4. Reason about what has changed based on the conversation
5. Use update_linear_ticket to apply any changes (status, due date, comments)
6. Use post_slack_message to confirm what you updated in the thread

Be precise. Only update fields that were clearly discussed in the thread.
Format your final Slack message clearly showing what was changed."""

def call_llm(state: AgentState):
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("llm", call_llm)
    graph.add_node("tools", ToolNode(tools))

    graph.set_entry_point("llm")

    # tools_condition checks if the LLM wants to call a tool or is done
    graph.add_conditional_edges("llm", tools_condition)
    graph.add_edge("tools", "llm")

    return graph.compile()

agent = build_graph()