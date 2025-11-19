from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
from tools import get_user_info
load_dotenv()

agent = create_agent(
    model="gpt-4o-mini",
    tools=[get_user_info],
    checkpointer=InMemorySaver(),
)

thread_id = "session1"

print("Chatbot is ready. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Chat ended.")
        break

    # 5. Invoke agent with memory
    result = agent.invoke(
        {"messages": [{"role": "user", "content": user_input}]},
        config={"thread_id": thread_id}
    )

    bot_reply = result["messages"][-1].content
    print("Bot:", bot_reply)