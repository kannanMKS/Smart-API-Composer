import asyncio
from src.core.session import session_service
from src.tools.openapi_runner import load_openapi_spec
from src.agents.planner_agent import generate_plan
from src.agents.executor_agent import execute_plan, register_spec
from src.agents.reporter_agent import build_report

# For demo: paths & base URLs hard-coded
SERVICE_SPECS = {
    "user-service": ("openapi_user.json", "https://httpbin.org"),
    "email-service": ("openapi_email.json", "https://httpbin.org"),
}



def load_specs():
    for service, (path, base_url) in SERVICE_SPECS.items():
        spec = load_openapi_spec(path, base_url)
        register_spec(service, spec)

async def main():
    load_specs()

    goal = input("Enter integration goal: ")
    # For now, we fake API summaries (you can build real ones from OpenAPI)
    api_summaries = [
        {"service": "user-service", "operation_id": "createUser", "description": "Create a new user"},
        {"service": "email-service", "operation_id": "sendWelcomeEmail", "description": "Send welcome email"},
    ]

    plan = generate_plan(goal, api_summaries)
    session_service.save_plan(plan)

    summary = await execute_plan(plan)
    report = build_report(summary)

    print("\n=== REPORT ===\n")
    print(report)

if __name__ == "__main__":
    asyncio.run(main())
