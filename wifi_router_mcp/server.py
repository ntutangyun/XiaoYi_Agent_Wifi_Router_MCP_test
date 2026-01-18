"""WiFi Router MCP Server - Simulates a home WiFi router."""

import asyncio
import json
from contextlib import asynccontextmanager
from typing import Any, Optional

import mcp.server.stdio
from mcp.server import Server
from mcp.server.fastmcp.server import StreamableHTTPASGIApp
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from mcp.types import (
    GetPromptResult,
    Prompt,
    PromptMessage,
    Resource,
    TextContent,
    Tool,
)
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from starlette.routing import Route

from wifi_router_shared.router import (
    call_tool_data,
    get_prompt_data,
    list_prompts_data,
    list_resources_data,
    list_tools_data,
    read_resource_data,
    router_state,
)


app = Server("wifi-router-mcp-server")


@app.list_resources()
async def list_resources() -> list[Resource]:
    """List available router resources."""
    return [Resource(**resource) for resource in list_resources_data()]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read a specific router resource."""
    payload = read_resource_data(uri)
    if isinstance(payload, str):
        return payload
    return json.dumps(payload, indent=2)


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available router tools."""
    return [Tool(**tool) for tool in list_tools_data()]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Execute a router tool."""
    result = call_tool_data(name, arguments)
    return [TextContent(type="text", text=json.dumps(result, indent=2))]


@app.list_prompts()
async def list_prompts() -> list[Prompt]:
    """List available router prompts."""
    return [Prompt(**prompt) for prompt in list_prompts_data()]


@app.get_prompt()
async def get_prompt(name: str, arguments: dict[str, str] | None) -> GetPromptResult:
    """Get a specific router prompt."""
    prompt_payload = get_prompt_data(name, arguments)
    messages = []
    for message in prompt_payload.get("messages", []):
        content = message.get("content", {})
        messages.append(
            PromptMessage(
                role=message.get("role", "user"),
                content=TextContent(type="text", text=content.get("text", "")),
            )
        )
    return GetPromptResult(description=prompt_payload["description"], messages=messages)


async def main():
    """Main entry point for the WiFi router MCP server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


def create_streamable_http_app() -> Starlette:
    """Create a Starlette app that serves MCP over Streamable HTTP."""
    session_manager = StreamableHTTPSessionManager(app)
    streamable_http_asgi = StreamableHTTPASGIApp(session_manager)

    async def health_check(_request):
        return JSONResponse({"status": "ok"})

    @asynccontextmanager
    async def lifespan(_app: Starlette):
        async with session_manager.run():
            yield

    app_instance = Starlette(
        routes=[
            Route("/sse", endpoint=streamable_http_asgi),
            Route("/sse/", endpoint=streamable_http_asgi),
            Route("/health", endpoint=health_check, methods=["GET"]),
        ],
        lifespan=lifespan,
    )
    app_instance.router.redirect_slashes = False

    app_instance.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app_instance


if __name__ == "__main__":
    asyncio.run(main())
