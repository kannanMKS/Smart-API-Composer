import httpx
import yaml
import json
from pathlib import Path
from typing import Any, Dict
from pydantic import BaseModel

class OpenAPISpec(BaseModel):
    raw: Dict[str, Any]
    base_url: str

def load_openapi_spec(path: str, base_url: str) -> OpenAPISpec:
    p = Path(path)
    text = p.read_text()
    if path.endswith(".yaml") or path.endswith(".yml"):
        raw = yaml.safe_load(text)
    else:
        raw = json.loads(text)
    return OpenAPISpec(raw=raw, base_url=base_url)

def find_operation(spec: OpenAPISpec, operation_id: str):
    for path, methods in spec.raw.get("paths", {}).items():
        for method, details in methods.items():
            if details.get("operationId") == operation_id:
                return method.upper(), path, details
    raise ValueError(f"operationId {operation_id} not found")

async def call_operation(
    spec: OpenAPISpec,
    operation_id: str,
    params: Dict[str, Any],
) -> httpx.Response:
    method, path, _details = find_operation(spec, operation_id)
    url = spec.base_url.rstrip("/") + path

    async with httpx.AsyncClient(timeout=10) as client:
        if method in ("GET", "DELETE"):
            return await client.request(method, url, params=params)
        else:
            return await client.request(method, url, json=params)
