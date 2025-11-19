# Import LLM Wrappers and Agent Creation Utilities
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

# import for dynamic tool
from langchain.agents.middleware import wrap_tool_call
from langchain_core.messages import ToolMessage

#import pydantic model for structured output
from pydantic import BaseModel
from langchain.agents.structured_output import ToolStrategy

# import for environment variables
from dotenv import load_dotenv

#import for dynamic prompt
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from typing import TypedDict

from tools import wiki_tool, get_weather, calculate_division
load_dotenv()

class HumanInfo(BaseModel):
    name: str
    age: int
    occupation: str

class Context(TypedDict):
    user_role: str

@dynamic_prompt
def user_role_prompt(request: ModelRequest) -> str:   
    """Generate system prompt based on user role in context."""
    user_role = request.runtime.context.get("user_role", "user")
    base_prompt = "You are a helpful assistant."

    if user_role =="expert":
        return base_prompt + " Provide detailed and technical explanations."
    elif user_role =="beginner":
        return base_prompt + " Provide simple and easy-to-understand explanations."
    return base_prompt

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
    middleware=[handle_tool_errors, user_role_prompt],
    context_schema=Context,
    response_format=ToolStrategy(HumanInfo)
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "Who is Elon Musk?"}]},
    context={"user_role": "beginner"}
)
print(result["structured_response"])