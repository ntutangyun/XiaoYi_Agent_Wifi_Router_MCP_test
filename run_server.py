#!/usr/bin/env python3
"""Entry point for the WiFi Router MCP Server."""

from wifi_router_mcp.server import main
import asyncio

if __name__ == "__main__":
    asyncio.run(main())
