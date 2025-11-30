import asyncio
import time
from typing import Dict, Any, List
from src.tools.openapi_runner import OpenAPISpec, call_operation
from src.core.models import WorkflowPlan, StepResult, ExecutionSummary
from src.core.session import session_service
from src.core.observability import logger, timed_span

# for now: register specs manually
OPENAPI_SPECS: Dict[str, OpenAPISpec] = {}

def register_spec(service_name: str, spec: OpenAPISpec):
    OPENAPI_SPECS[service_name] = spec

async def _execute_step(step, context: Dict[str, Any]) -> StepResult:
    # Resolve inputs (simple variable interpolation)
    params = {}
    for key, value in step.inputs.items():
        if isinstance(value, str) and value.startswith("${"):
            # e.g. ${ctx.user_id}
            expr = value.strip("${}")
            params[key] = context.get(expr)
        else:
            params[key] = value

    spec = OPENAPI_SPECS[step.service]

    start = time.time()
    try:
        resp = await call_operation(spec, step.operation_id, params)
        duration = (time.time() - start) * 1000
        data = None
        try:
            data = resp.json()
        except Exception:
            data = resp.text

        success = resp.status_code < 400
        if success:
            # store some fields into context if needed
            # convention: if response has "id", store ctx.<step.name>_id
            if isinstance(data, dict) and "id" in data:
                context[f"{step.name}_id"] = data["id"]

        return StepResult(
            step_id=step.id,
            success=success,
            status_code=resp.status_code,
            data=data,
            duration_ms=duration,
            error=None if success else str(data),
        )
    except Exception as exc:
        duration = (time.time() - start) * 1000
        logger.exception("Error executing step %s", step.id)
        return StepResult(
            step_id=step.id,
            success=False,
            status_code=None,
            data=None,
            duration_ms=duration,
            error=str(exc),
        )

async def execute_plan(plan: WorkflowPlan) -> ExecutionSummary:
    with timed_span(f"executor.execute_plan[{plan.plan_id}]"):
        context: Dict[str, Any] = {}
        results: List[StepResult] = []

        if plan.execution_mode == "sequential":
            for step in plan.steps:
                # For brevity, skipping pause/confirm here; you can extend.
                res = await _execute_step(step, context)
                results.append(res)
                if not res.success:
                    break
        else:
            # naive parallel: execute all
            tasks = [_execute_step(step, context) for step in plan.steps]
            results = await asyncio.gather(*tasks)

        success = all(r.success for r in results)
        summary = ExecutionSummary(
            plan_id=plan.plan_id,
            goal=plan.goal,
            results=results,
            success=success,
        )
        session_service.save_execution_summary(summary)
        return summary
