#!/usr/bin/env python3
"""Entry point for the WiFi Router MCP Server."""

import argparse
import asyncio
import os

import uvicorn

from wifi_router_mcp.server import create_streamable_http_app, main


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="WiFi Router MCP Server")
    parser.add_argument(
        "--transport",
        default=os.getenv("MCP_TRANSPORT", "stdio"),
        choices=["stdio", "streamable-http"],
        help="Transport type to use (default: stdio).",
    )
    parser.add_argument(
        "--host",
        default=os.getenv("MCP_HTTP_HOST", "127.0.0.1"),
        help="Host for streamable HTTP server (default: 127.0.0.1).",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("MCP_HTTP_PORT", "3001")),
        help="Port for streamable HTTP server (default: 3001).",
    )
    parser.add_argument(
        "--log-level",
        default=os.getenv("MCP_HTTP_LOG_LEVEL", "info"),
        help="Uvicorn log level (default: info).",
    )
    return parser.parse_args()


def run_stdio() -> None:
    asyncio.run(main())


def run_streamable_http(host: str, port: int, log_level: str) -> None:
    app = create_streamable_http_app()
    uvicorn.run(app, host=host, port=port, log_level=log_level)


if __name__ == "__main__":
    args = parse_args()
    if args.transport == "streamable-http":
        run_streamable_http(args.host, args.port, args.log_level)
    else:
        run_stdio()
