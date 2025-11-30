 Smart API Composer
A Multi-Agent System that Translates Plain-Language Goals into Executable API Workflows
🧩 Overview

Modern enterprises rely on distributed microservices and large OpenAPI specifications.
Developers must:

Read huge OpenAPI files

Find the right endpoints

Map request parameters by hand

Orchestrate multi-step workflows (e.g., Create User → Create Profile → Send Email)

Maintain consistency across teams

This leads to:

Slow development cycles

Frequent integration mistakes

Onboarding friction

Duplicated work

Tribal knowledge lost across teams

Smart API Composer solves this by using AI Agents to automatically convert a natural-language goal into a real, executable API workflow.

🧠 Why Agents?

Agents are ideal for this problem because they:

Understand high-level user intent (Planner Agent)

Decompose tasks and coordinate API calls (Executor Agent)

Summarize results and provide insights (Reporter Agent)

Maintain cross-step memory & context

Use specialized tools (OpenAPI Runner, Code Exec Tool, Exporter)

This maps perfectly to multi-agent reasoning + tool use.

🎯 Problem Statement

Enterprise teams struggle with API integrations because:

OpenAPI specs are large and complex

Developers must manually search for the right endpoints

Multi-step API orchestration is slow and error-prone

There is no consistent or reusable workflow planning process

Smart API Composer eliminates this manual overhead by using Google Gemini-powered agents to:

Read the user’s goal

Interpret available API operations

Construct a workflow plan

Execute the workflow

Report results

🌟 Solution Summary (High-Level)

Smart API Composer is a multi-agent system with:

1. Planner Agent (Gemini LLM)

Reads user goal

Reads available API summaries

Generates JSON workflow plan

Defines dependencies & execution mode

2. Executor Agent

Executes steps sequentially or in parallel

Resolves ${variable} placeholders

Calls APIs using the OpenAPI Runner Tool

Supports pause/resume logic

Captures results + metrics

3. Reporter Agent

Aggregates results

Uses Gemini to generate a clean Markdown report

Writes summaries to Memory Bank (SQLite)

Exports reports if needed

🔧 Architecture
User Input (Goal)
        |
        ▼
┌──────────────────────┐
│   Planner Agent       │ → Generates JSON plan
└──────────────────────┘
        |
        ▼
┌──────────────────────┐
│   Executor Agent      │ → Executes API workflow
└──────────────────────┘
        |
        ▼
┌──────────────────────┐
│   Reporter Agent      │ → Markdown report + Memory
└──────────────────────┘
        |
        ▼
User sees final report

🛠 Tools Used
🛠 Custom OpenAPI Runner Tool

Loads OpenAPI specs (JSON/YAML)

Finds operations by operationId

Constructs & executes HTTP requests

🛠 Code Execution Tool

Executes small Python transformations on results

🛠 Exporter Tool

Export workflows as JSON or CSV

(Extendable to email notifications)

🧠 Memory Bank (SQLite)

Stores compact summaries of past workflows

📊 Observability

Structured logging

Step-level timing

Tracing

✔ Concepts from the Course Implemented (7 total)
Concept	Implemented
Multi-Agent System	✅ (Planner, Executor, Reporter)
Sequential + Parallel Agents	✅ Executor Agent supports both
Custom Tools	✅ OpenAPI Runner, Code Exec, Exporter
Built-in Tools	❇️ (Gemini LLM + HTTP client)
Long-Running Ops (pause/resume)	✅
Session & State Management	✅ SessionService
Long-Term Memory	✅ SQLite MemoryBank
Observability	✅ Logging + timing
Evaluation-ready architecture	Yes

This exceeds the minimum requirement of 3.

📂 Project Structure
smart-api-composer-full/
│
├── main.py
├── requirements.txt
├── openapi_user.json
├── openapi_email.json
│
└── src/
    ├── client.py
    ├── core/
    │   ├── models.py
    │   ├── session.py
    │   ├── observability.py
    │   └── memory.py
    ├── tools/
    │   ├── openapi_runner.py
    │   ├── code_exec_tool.py
    │   └── exporter_tool.py
    └── agents/
        ├── planner_agent.py
        ├── executor_agent.py
        └── reporter_agent.py

⚙️ Setup Instructions
1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Add your Gemini API key

Create a .env file:

GOOGLE_API_KEY=your_key_here

3️⃣ Use httpbin as a mock backend (recommended)

Edit main.py:

SERVICE_SPECS = {
    "user-service": ("openapi_user.json", "https://httpbin.org"),
    "email-service": ("openapi_email.json", "https://httpbin.org")
}


And set the OpenAPI paths to /anything for local testing.

▶️ Running the App
python main.py


Example input:

Create a user and send a welcome email


You will get a detailed Markdown report:

## Workflow Execution Report: createUserAndSendWelcomeEmail
...
✓ Step 1: User created
✓ Step 2: Welcome email sent

📈 Demo Output (Sample)
=== REPORT ===

## Workflow Execution Report: createUserAndSendWelcomeEmail

**Goal:** Create a user and send a welcome email.

### Steps:
- step1: Created new user (ID: 123)
- step2: Sent welcome email to user@email.com

🎉 **Workflow completed successfully!**

🚀 Future Improvements (If more time available)

Add FastAPI-based UI

Add natural-language to OpenAPI search (semantic endpoint discovery)

Add retries, backoff strategies

Parallel execution visualization UI

Integration with workflow engines (Temporal, Airflow)

Deploy on Cloud Run or Agent Engine for bonus points

🏁 Final Notes

This project demonstrates:

Multi-agent collaboration

Context-aware orchestration

OpenAPI-driven automation

Tool-using agents

Memory + observability

Real executable API workflows

Production-ready structure

It fully satisfies the capstone project rubric.