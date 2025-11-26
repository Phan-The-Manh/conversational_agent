from unittest import result
from langchain.agents import create_agent
from langgraph.checkpoint.postgres import PostgresSaver  
from dotenv import load_dotenv
load_dotenv()
DB_URI = "postgresql://postgres.gpranulrtpslnxgehtal:[YOUR_PASSWORD]@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres"
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup() # auto create tables in PostgresSql
    agent = create_agent(
        "gpt-5",
        checkpointer=checkpointer,  
    )

    result = agent.invoke(
        {"messages": [{"role": "user", "content": "What is my age and year of study. Just answer with those 2 contents"}]},
        {"configurable": {"thread_id": "1"}},  
)
    print(result["messages"][-1].content)

