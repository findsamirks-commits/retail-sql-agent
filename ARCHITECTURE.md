# Production Architecture & Deployment

## 1. Database Connectivity & Security
* **Current State:** Connects to local `sqlite:///retail_sandbox.db`.
* **Production State:** Must map to the live MySQL production URI. 
* **Security:** The database user provisioned for this agent must have strict `SELECT`-only permissions to prevent destructive operations.

## 2. Secrets Management
* **Protocol:** All database credentials and API keys must be migrated to a `.env` file.
* **Tooling:** Utilize `python-dotenv` for local environments and GitHub Secrets for automated deployments.
* **Warning:** Never commit the `.env` file to version control.

## 3. LLM Prompt Engineering
* **Logic:** Custom system prompts are required to explain specific business logic and table joins as the schema scales.
* **Model:** Configured to `gemini-2.5-flash` with a temperature of `0` for deterministic SQL generation.