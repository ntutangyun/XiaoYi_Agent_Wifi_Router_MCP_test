#!/usr/bin/env python3
"""Entry point for the WiFi Router FastAPI Server."""

import argparse
import os

import uvicorn

from wifi_router_mcp.server import create_fastapi_app


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="WiFi Router FastAPI Server")
    parser.add_argument(
        "--host",
        default=os.getenv("FASTAPI_HOST", "127.0.0.1"),
        help="Host for FastAPI server (default: 127.0.0.1).",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("FASTAPI_PORT", "8000")),
        help="Port for FastAPI server (default: 8000).",
    )
    parser.add_argument(
        "--log-level",
        default=os.getenv("FASTAPI_LOG_LEVEL", "info"),
        help="Uvicorn log level (default: info).",
    )
    return parser.parse_args()


def run_fastapi(host: str, port: int, log_level: str) -> None:
    app = create_fastapi_app()
    uvicorn.run(app, host=host, port=port, log_level=log_level)


if __name__ == "__main__":
    args = parse_args()
    run_fastapi(args.host, args.port, args.log_level)
