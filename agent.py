from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_experimental.sql import SQLDatabaseChain
import os

# 1. Connect to the local sandbox database
db = SQLDatabase.from_uri("sqlite:///retail_sandbox.db")

# 2. Initialize the reasoning engine 
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=""GOOGLE_API_KEY"",  # Replace AQ... with your full copied key
    temperature=0
)

# 3. Create the autonomous database chain
agent = SQLDatabaseChain.from_llm(llm, db, verbose=True)

# 4. Test an operational query in plain English
while True:
    user_prompt = input("\nAsk a retail question (or type 'exit'): ")
    if user_prompt.lower() == 'exit':
        break
    agent.invoke(user_prompt)