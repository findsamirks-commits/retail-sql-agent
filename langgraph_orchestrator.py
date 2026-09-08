from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage
import os
from typing import TypedDict, Annotated, Literal
from langgraph.graph.message import add_messages
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain_core.messages import AIMessage

# 1. Define the shared whiteboard for the agents
class RetailState(TypedDict):
    messages: Annotated[list, add_messages]
    next_agent: str
    sql_query: str
    raw_data: str

# Initialize connections
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
db = SQLDatabase.from_uri("sqlite:///retail_sandbox.db")
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=False)

# 2. The Conditional Router
def route_query(state: RetailState) -> Literal["sql_specialist", "analyst"]:
    messages = state["messages"]
    last_message = messages[-1].content.lower()
    
    db_keywords = ["gmv", "units", "category", "price", "sales", "revenue", "average", "total"]
    
    if any(keyword in last_message for keyword in db_keywords):
        print("➡️ Router Decision: Handing off to SQL Specialist")
        return "sql_specialist"
    
    print("➡️ Router Decision: Handing off to Business Analyst")
    return "analyst"

# 3. The SQL Specialist Node
def sql_specialist(state: RetailState) -> RetailState:
    print("⚙️ SQL Specialist: Translating and querying the database...")
    question = state["messages"][-1].content
    
    try:
        raw_result = db_chain.invoke(question)
        data = raw_result["result"]
    except Exception as e:
        data = f"Error executing SQL: {str(e)}"
        
    return {"raw_data": data}

# 4. The Business Analyst Node
def analyst(state: RetailState) -> RetailState:
    print("📊 Analyst: Synthesizing retail insights...")
    question = state["messages"][-1].content
    raw_data = state.get("raw_data", "No database query was required.")
    
    prompt = (
        f"You are a Senior Retail Operations Analyst. "
        f"The user asked: '{question}'. "
        f"The raw system data is: '{raw_data}'. "
        f"Provide a concise, professional business answer explaining this metric. Do not show the SQL."
    )
    
    response = llm.invoke(prompt)
    return {"messages": [AIMessage(content=response.content)]}

    
# 5. Compile the Graph
workflow = StateGraph(RetailState)

# Add the nodes (the agents)
workflow.add_node("sql_specialist", sql_specialist)
workflow.add_node("analyst", analyst)

# Wire the logic (the edges)
workflow.add_conditional_edges(
    START,
    route_query,
    {
        "sql_specialist": "sql_specialist",
        "analyst": "analyst"
    }
)

# The SQL specialist always hands its raw data to the Analyst to synthesize
workflow.add_edge("sql_specialist", "analyst")
workflow.add_edge("analyst", END)

# Compile the final application
app = workflow.compile()

# 6. Interactive CLI Loop
if __name__ == "__main__":
    print("\n🚀 Multi-Agent Retail Orchestrator Online. Type 'exit' to quit.")
    while True:
        user_input = input("\nAsk a retail operations question: ")
        if user_input.lower() == 'exit':
            break
        
        # Send the question into the initial graph state
        initial_state = {"messages": [HumanMessage(content=user_input)]}
        result = app.invoke(initial_state)
        
        # Print the final synthesized answer from the Analyst node
        print(f"\nFinal Answer: {result['messages'][-1].content}")