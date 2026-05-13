"""Shared FastMCP application instance.

Kept in its own module so both server.py and tool modules can import `mcp`
without creating a circular dependency.
"""
from __future__ import annotations

from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    "domo-mcp-server",
    instructions=(
        "MCP server for the Domo analytics platform. "
        "Provides tools to read and write datasets, cards, pages, users, groups, "
        "dataflows, alerts, and all other Domo resources. "
        "All tools require DOMO_INSTANCE_URL and DOMO_DEVELOPER_TOKEN to be set."
    ),
)
