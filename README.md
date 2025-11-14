# **1. Information**

This project contains **basic Python code** using the **LangChain** framework to create a simple agent powered by the **OpenAI (GPT-4o-mini) wrapper**.

The agent demonstrates several essential features:

* ✅ **Dynamic Prompting** (context-aware system messages)
* ✅ **Tool Error Handling**
* ✅ **Structured Output** using Pydantic models
* ✅ **Tool Integration** (example: search tool)

For full documentation, refer to:
👉 [https://docs.langchain.com/oss/python/langchain/agents](https://docs.langchain.com/oss/python/langchain/agents)

---

# **2. Setup Instructions**

## **2.1. Create a Virtual Environment (optional but recommended)**

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## **2.2. Install Required Libraries**

Make sure your virtual environment (if used) is activated, then install dependencies:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install langchain langchain-openai langchain-community python-dotenv
```

---

## **2.3. Run the Project**

Start the agent by running:

```bash
python main.py
```

Make sure you have **OPENAI_API_KEY** set in your environment or in a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

