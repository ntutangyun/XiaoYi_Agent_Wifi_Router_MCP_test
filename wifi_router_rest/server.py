"""REST API server for the WiFi router simulation."""

from __future__ import annotations

from typing import Any

from fastapi import Body, FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

from wifi_router_shared.router import (
    call_tool_data,
    get_prompt_data,
    list_prompts_data,
    list_resources_data,
    list_tools_data,
    read_resource_data,
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

    app_instance = FastAPI()

    @app_instance.get("/health")
    async def health_check() -> dict[str, str]:
        return {"status": "ok"}

    @app_instance.get("/resources")
    async def list_resources_endpoint() -> list[dict[str, Any]]:
        return [normalize_model(resource) for resource in list_resources_data()]

    @app_instance.get("/resources/{resource_id}")
    async def read_resource_endpoint(resource_id: str) -> Any:
        uri = resource_uri_map.get(resource_id, resource_id)
        try:
            return read_resource_data(uri)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app_instance.get("/tools")
    async def list_tools_endpoint() -> list[dict[str, Any]]:
        return [normalize_model(tool) for tool in list_tools_data()]

    @app_instance.post("/tools/{tool_name}")
    async def call_tool_endpoint(
        tool_name: str,
        arguments: dict[str, Any] = Body(default_factory=dict),
    ) -> Any:
        try:
            return call_tool_data(tool_name, arguments)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app_instance.get("/prompts")
    async def list_prompts_endpoint() -> list[dict[str, Any]]:
        return [normalize_model(prompt) for prompt in list_prompts_data()]

    @app_instance.post("/prompts/{prompt_name}")
    async def get_prompt_endpoint(
        prompt_name: str,
        arguments: dict[str, str] | None = Body(default=None),
    ) -> dict[str, Any]:
        try:
            return normalize_model(get_prompt_data(prompt_name, arguments))
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    app_instance.router.redirect_slashes = False
    app_instance.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app_instance
