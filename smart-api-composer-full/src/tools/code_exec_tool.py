# src/tools/code_exec_tool.py

from __future__ import annotations

from typing import Any, Dict


def run_python_snippet(code: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """
    Execute a small Python snippet in a restricted environment.

    The snippet can read and modify the `ctx` dict.
    Example code:

        total = sum(item["value"] for item in ctx["items"])
        ctx["total_value"] = total

    :param code: Python code to execute.
    :param context: Initial context dictionary (will be mutated).
    :return: Updated context dict.
    """
    ctx: Dict[str, Any] = dict(context or {})

    # Very restricted globals: no builtins, no imports.
    safe_globals = {
        "__builtins__": {},
    }

    # Locals will expose ctx
    local_vars = {"ctx": ctx}

    exec(code, safe_globals, local_vars)

    # ctx may have been mutated
    return ctx
