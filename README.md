# 🤖 Retail Agentic AI: Text-to-SQL Assistant

An autonomous Large Language Model agent designed to democratize data access for retail operations teams. This tool translates plain English operational questions into syntactically correct SQL, executes the queries against a database, and returns conversational analytical answers.

## Features
* **Autonomous Querying:** Eliminates the need for manual SQL scripting by leveraging LangChain to dynamically read schema and generate queries.
* **Deterministic Execution:** Utilizes Google's Gemini 2.5 Flash model with a temperature setting of 0 to ensure accurate, repeatable mathematical aggregations.
* **Sandbox Environment:** Safely developed and tested against a localized SQLite database containing synthetic high-volume transaction data across multiple product categories.
* **Interactive CLI:** Includes a continuous loop for analysts to query metrics like Gross Merchandise Value (GMV) and Average Order Value (AOV) on the fly.

## Tech Stack
* **Orchestration:** LangChain, LangChain Experimental
* **LLM Engine:** Google Gemini (`gemini-2.5-flash`)
* **Database:** SQLite, SQLAlchemy, Pandas (for synthetic data generation)
* **Environment:** Python 3.x, Antigravity IDE / VS Code

## Local Setup & Usage
1. Clone the repository and install dependencies: `pip install langchain langchain-google-genai langchain-experimental sqlalchemy pandas`
2. Generate the synthetic database: Run `python create_db.py` to create `retail_sandbox.db`.
3. Set your API key in the terminal: 
   * Windows PowerShell: `$env:GOOGLE_API_KEY="your_key"`
   * Bash/Linux: `export GOOGLE_API_KEY="your_key"`
4. Launch the agent: Run `python agent.py` and begin typing plain English queries into the prompt.