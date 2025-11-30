# src/core/models.py

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class PlanStep(BaseModel):
    id: str
    name: str
    operation_id: str
    service: str
    inputs: Dict[str, Any] = {}
    requires_confirmation: bool = False


class ExecutionMode(str, Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"


class WorkflowPlan(BaseModel):
    plan_id: str
    goal: str
    steps: List[PlanStep]
    execution_mode: ExecutionMode = Field(default=ExecutionMode.SEQUENTIAL)


class StepResult(BaseModel):
    step_id: str
    success: bool
    status_code: Optional[int] = None
    data: Any = None
    error: Optional[str] = None
    duration_ms: Optional[float] = None


class ExecutionSummary(BaseModel):
    plan_id: str
    goal: str
    results: List[StepResult]
    success: bool
