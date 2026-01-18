"""REST API server for the WiFi router simulation."""

from __future__ import annotations

import json
from typing import Any

from fastapi import Body, FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

from wifi_router_mcp.server import (
    call_tool,
    get_prompt,
    list_prompts,
    list_resources,
    list_tools,
    read_resource,
)


def create_fastapi_app() -> FastAPI:
    """Create a FastAPI app that serves RESTful endpoints."""
    resource_uri_map = {
        "devices": "router://devices",
        "stats": "router://stats",
        "config": "router://config",
        "logs": "router://logs",
        "networks": "router://networks",
    }

    def normalize_model(item: Any) -> Any:
        if hasattr(item, "model_dump"):
            return item.model_dump()
        if hasattr(item, "dict"):
            return item.dict()
        return item

    def parse_json_maybe(value: str) -> Any:
        if not isinstance(value, str):
            return value
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value

    app_instance = FastAPI()

    @app_instance.get("/health")
    async def health_check() -> dict[str, str]:
        return {"status": "ok"}

    @app_instance.get("/resources")
    async def list_resources_endpoint() -> list[dict[str, Any]]:
        resources = await list_resources()
        return [normalize_model(resource) for resource in resources]

    @app_instance.get("/resources/{resource_id}")
    async def read_resource_endpoint(resource_id: str) -> Any:
        uri = resource_uri_map.get(resource_id, resource_id)
        try:
            payload = await read_resource(uri)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return parse_json_maybe(payload)

    @app_instance.get("/tools")
    async def list_tools_endpoint() -> list[dict[str, Any]]:
        tools = await list_tools()
        return [normalize_model(tool) for tool in tools]

    @app_instance.post("/tools/{tool_name}")
    async def call_tool_endpoint(
        tool_name: str,
        arguments: dict[str, Any] = Body(default_factory=dict),
    ) -> Any:
        try:
            contents = await call_tool(tool_name, arguments)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        if not contents:
            return {}
        return parse_json_maybe(contents[0].text)

    @app_instance.get("/prompts")
    async def list_prompts_endpoint() -> list[dict[str, Any]]:
        prompts = await list_prompts()
        return [normalize_model(prompt) for prompt in prompts]

    @app_instance.post("/prompts/{prompt_name}")
    async def get_prompt_endpoint(
        prompt_name: str,
        arguments: dict[str, str] | None = Body(default=None),
    ) -> dict[str, Any]:
        try:
            prompt_result = await get_prompt(prompt_name, arguments)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        prompt_payload = normalize_model(prompt_result)
        if "messages" in prompt_payload:
            for message in prompt_payload["messages"]:
                if isinstance(message, dict) and "content" in message:
                    message["content"] = normalize_model(message["content"])
        return prompt_payload

    app_instance.router.redirect_slashes = False
    app_instance.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app_instance
