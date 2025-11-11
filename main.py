from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.agents.middleware import wrap_tool_call
from langchain_core.messages import ToolMessage
from dotenv import load_dotenv
from tools import wiki_tool, get_weather, calculate_division
load_dotenv()

@wrap_tool_call
def handle_tool_errors(request, handler):
    """Handle tool execution errors with custom messages."""
    try:
        return handler(request)
    except Exception as e:
        # Return a custom error message to the model
        return ToolMessage(
            content=f"Tool error: Please check your input and try again. ({str(e)})",
            tool_call_id=request.tool_call["id"]
        )

model = ChatOpenAI(model_name="gpt-4o-mini")

agent = create_agent(
    model=model,
    tools=[get_weather, calculate_division],
    middleware=[handle_tool_errors],
    system_prompt="You are a helpful assistant that can anwer questions using tools only."
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "Calculate 6/0"}]}
)
print(result["messages"][-1].content)
