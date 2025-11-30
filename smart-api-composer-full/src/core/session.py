from typing import Dict
from .models import WorkflowPlan, ExecutionSummary

class SessionService:
    """
    Simple in-memory session store.
    Replace with Redis/DB for production.
    """
    def __init__(self):
        self._plans: Dict[str, WorkflowPlan] = {}
        self._summaries: Dict[str, ExecutionSummary] = {}

    def save_plan(self, plan: WorkflowPlan):
        self._plans[plan.plan_id] = plan

    def get_plan(self, plan_id: str) -> WorkflowPlan:
        return self._plans[plan_id]

    def save_execution_summary(self, summary: ExecutionSummary):
        self._summaries[summary.plan_id] = summary

    def get_execution_summary(self, plan_id: str) -> ExecutionSummary:
        return self._summaries[plan_id]

session_service = SessionService()
