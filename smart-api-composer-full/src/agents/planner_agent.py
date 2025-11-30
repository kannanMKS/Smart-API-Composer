# src/agents/planner_agent.py

import json
import uuid
from typing import List, Dict, Any

from src.client import get_client, MODEL_PLANNER
from src.core.models import WorkflowPlan, PlanStep, ExecutionMode
from src.core.memory import memory_bank
from src.core.observability import logger, timed_span


def _build_planner_prompt(goal: str, api_summaries: List[Dict[str, Any]]) -> str:
    return (
        "You are an API workflow planner. "
        "Given a high-level integration goal and a list of available API operations, "
        "design a workflow plan.\n\n"
        f"Goal:\n{goal}\n\n"
        "Available operations (JSON array):\n"
        f"{json.dumps(api_summaries, indent=2)}\n\n"
        "Return ONLY valid JSON with the following structure:\n"
        "{\n"
        '  \"plan_id\": \"string\",\n'
        '  \"execution_mode\": \"sequential\" | \"parallel\",\n'
        '  \"steps\": [\n'
        "    {\n"
        '      \"id\": \"string\",\n'
        '      \"name\": \"string\",\n'
        '      \"operation_id\": \"string\",\n'
        '      \"service\": \"string\",\n'
        '      \"inputs\": { \"param\": \"value-or-${var}\" },\n'
        '      \"requires_confirmation\": false\n'
        "    }\n"
        "  ]\n"
        "}\n"
    )


def generate_plan(goal: str, api_summaries: List[Dict[str, Any]]) -> WorkflowPlan:
    client = get_client()

    with timed_span("planner.generate_plan"):
        prompt = _build_planner_prompt(goal, api_summaries)

        # ✅ New google-genai SDK: contents can just be a string
        resp = client.models.generate_content(
            model=MODEL_PLANNER,
            contents=prompt,
        )

        raw_text = resp.candidates[0].content.parts[0].text.strip()

        # Strip ```json fences if the model adds them
        if raw_text.startswith("```"):
            raw_text = raw_text.strip("`")
            if "\n" in raw_text:
                raw_text = raw_text.split("\n", 1)[1]

        data = json.loads(raw_text)

        plan = WorkflowPlan(
            plan_id=data.get("plan_id") or str(uuid.uuid4()),
            goal=goal,
            execution_mode=ExecutionMode(data.get("execution_mode", "sequential")),
            steps=[PlanStep(**s) for s in data["steps"]],
        )

        memory_bank.save_workflow_summary(
            goal=goal,
            plan_summary=f"{len(plan.steps)} steps, mode={plan.execution_mode}",
            apis_used=", ".join(step.operation_id for step in plan.steps),
            status="planned",
        )

        logger.info(f"Generated plan {plan.plan_id} with {len(plan.steps)} steps")
        return plan
