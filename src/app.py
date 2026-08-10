"""Shared FastMCP application instance.

Kept in its own module so both server.py and tool modules can import `mcp`
without creating a circular dependency.
"""
from __future__ import annotations

from functools import partial

from mcp.server.fastmcp import FastMCP
from mcp.server.lowlevel.server import NotificationOptions

mcp = FastMCP(
    "domo-mcp-server",
    instructions=(
        "MCP server for the Domo analytics platform. "
        "Provides tools to read and write datasets, cards, pages, users, groups, "
        "dataflows, alerts, and all other Domo resources. "
        "All tools require DOMO_INSTANCE_URL and DOMO_DEVELOPER_TOKEN to be set. "
        "By default the server is read-only (DOMO_READ_ONLY=1) and exposes every "
        "toolset up front; set DOMO_DYNAMIC_TOOLSETS=1 to instead start with only "
        "list_toolsets/enable_toolset and register other toolsets on demand."
    ),
)

# FastMCP always calls create_initialization_options() with no notification
# options, which advertises tools.listChanged=False — but src/toolsets.py's
# enable_toolset can register new tools mid-session and needs to notify
# clients when it does. Default that capability to on for every session.
mcp._mcp_server.create_initialization_options = partial(
    mcp._mcp_server.create_initialization_options,
    notification_options=NotificationOptions(tools_changed=True),
)
