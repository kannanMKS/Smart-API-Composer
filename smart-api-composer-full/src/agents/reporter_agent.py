# src/agents/reporter_agent.py

import json

from src.client import get_client, MODEL_REPORTER
from src.core.models import ExecutionSummary
from src.core.memory import memory_bank
from src.core.observability import logger, timed_span


def build_report(summary: ExecutionSummary) -> str:
    client = get_client()

    with timed_span(f"reporter.build_report[{summary.plan_id}]"):
        summary_json = summary.model_dump()

        prompt = (
            "You are a reporting assistant. Given this workflow execution summary, "
            "write a concise Markdown report for engineers and product managers.\n\n"
            "Highlight:\n"
            "- Goal\n"
            "- Each step and whether it succeeded or failed\n"
            "- Important IDs or values\n"
            "- Any errors\n"
            "- Recommended next actions\n\n"
            f"SUMMARY_JSON:\n{json.dumps(summary_json, indent=2)}"
        )

        # ✅ New SDK usage – just pass a string
        resp = client.models.generate_content(
            model=MODEL_REPORTER,
            contents=prompt,
        )

        text = resp.candidates[0].content.parts[0].text

        status = "success" if summary.success else "partial_or_failed"

        memory_bank.save_workflow_summary(
            goal=summary.goal,
            plan_summary=f"{len(summary.results)} executed steps",
            apis_used="N/A",
            status=status,
        )

        logger.info("Generated report for %s", summary.plan_id)
        return text
