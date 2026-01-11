from typing import Literal, Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.types import Command, interrupt

# --- 1. Define State ---
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# --- 2. Define Tools ---
def file_expense(amount: float, reason: str):
    """Files an expense report. Call this ONLY after obtaining necessary approvals if required."""
    print(f"Executing Tool: File Expense - ${amount} for {reason}")
    return f"Expense of ${amount} for '{reason}' has been FILED."

tools = [file_expense]
tool_node = ToolNode(tools)

# --- 3. Define Model ---
model = ChatOpenAI(model="gpt-4o", temperature=0)
model_with_tools = model.bind_tools(tools)

# --- 4. Define Nodes ---

async def agent_node(state: AgentState, config):
    messages = state.get("messages", [])
    response = await model_with_tools.ainvoke(messages, config)
    return {"messages": [response]}

def should_continue(state: AgentState):
    """
    Check if we need approval.
    """
    last_message = state["messages"][-1]
    
    if not isinstance(last_message, AIMessage) or not last_message.tool_calls:
        return END

    # Check for sensitive tools
    for tool_call in last_message.tool_calls:
        if tool_call["name"] == "file_expense":
            amount = tool_call["args"].get("amount")
            # Logic: If > 100, we need to interrupt?
            # Ideally, we interrupt BEFORE the tool node runs.
            if amount and float(amount) > 100:
                print(f"Detected expense > 100 ({amount}). Interrupting for approval.")
                return "approval_check"

    return "tools"

def approval_check_node(state: AgentState):
    """
    Interrupt the graph to ask for user confirmation.
    """
    # We use LangGraph's native `interrupt`
    # The value returned by `interrupt` will be the input provided when resuming.
    user_approval = interrupt("Please approve this expense.")
    
    # If we resume, we get the value here.
    if user_approval.get("status") == "approved":
        print("Expense APPROVED by user.")
        return Command(goto="tools")
    else:
        print("Expense REJECTED by user.")
        # We need to deny the tool call.
        # We can construct a ToolMessage indicating failure, or just return to agent with a message.
        # Simplest is to start a new loop with a system/human message saying "Denied".
        return Command(
             update={"messages": [SystemMessage(content="User rejected the expense request.")]},
             goto="agent"
        )


# --- 5. Build Graph ---
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)
workflow.add_node("approval_check", approval_check_node)

workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        "approval_check": "approval_check",
        END: END
    }
)

workflow.add_edge("tools", "agent")

# Enable checkpointing for interrupts to work (in CopilotKit, this hooks into the runtime)
# For the demo, we assume CopilotKit SDK handles the checkpointer or we pass it in server.py
# CopilotKit injects a checkpointer automatically when using `LangGraphAgent`.

graph = workflow.compile()
