from langchain.messages import AnyMessage, SystemMessage
from langchain.messages import ToolMessage
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import Literal
from typing_extensions import TypedDict, Annotated
import operator
from tools import multiply, add, divide
from dotenv import load_dotenv
load_dotenv()
#Define state schema
class MessagesState(TypedDict):
    messages : Annotated[list[AnyMessage], operator.add]
    llm_calls : int

#create tool list
tool_list = [multiply, add, divide]
tools_by_name = {tool.name: tool for tool in tool_list}

#define model with tools
model = ChatOpenAI(model="gpt-4o-mini")
model_with_tools = model.bind_tools(tool_list)

#llm call function
def llm_call(state:dict):
    """LLM decide wether to use tool or not"""
    return {
        "messages": [
            model_with_tools.invoke(
                [
                    SystemMessage(
                        content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
                    )
                ]
                + state["messages"]
            )
        ],
        "llm_calls": state.get('llm_calls',0) + 1
    }

#define tool node
def tool_node(state:dict):
    """Perform tool calling"""
    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}

#Define end logic
def should_continue(state:dict) -> Literal["tool_node", END]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call."""

    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tool_node"
    return END 


#Build agent
graph_agent = StateGraph(MessagesState)

graph_agent.add_node("llm_call", llm_call)
graph_agent.add_node("tool_node", tool_node)

graph_agent.add_edge(START, "llm_call")
graph_agent.add_conditional_edges(
    "llm_call",
    should_continue,
    ["tool_node", END]
)
graph_agent.add_edge("tool_node", "llm_call")
graph_agent = graph_agent.compile()

from langchain.messages import HumanMessage
messages = [HumanMessage(content="Add 3 and 4.")]
messages = graph_agent.invoke({"messages": messages})
for m in messages["messages"]:
    m.pretty_print()