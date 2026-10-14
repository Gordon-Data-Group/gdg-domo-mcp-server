"""Shared FastMCP application instance.

Kept in its own module so both server.py and tool modules can import `mcp`
without creating a circular dependency.
"""
from __future__ import annotations

from functools import partial

import os

from mcp.server.fastmcp import FastMCP
from mcp.server.lowlevel.server import NotificationOptions

from src import auth


def _instructions() -> str:
    text = (
        "MCP server for the Domo analytics platform: datasets, cards, pages, "
        "users, groups, dataflows, alerts, and other Domo resources. "
        "Tools that change Domo data are only available on instances where "
        "read-only mode has been turned off."
    )
    configured = auth.instances()
    if len(configured) > 1:
        default = auth.default_alias()
        listing = "; ".join(
            f"{alias} = {os.environ.get(inst.env_prefix + 'INSTANCE_URL', '?')}"
            f"{' (default)' if alias == default else ''}"
            f"{'' if inst.read_only else ', writable'}"
            for alias, inst in configured.items()
        )
        text += (
            f" Several Domo instances are connected — every tool takes an "
            f"`instance` argument selecting one: {listing}. "
            "Pass `instance` explicitly whenever the user names an instance or "
            "you are working with data from a non-default one."
        )
    return text


# load_dotenv() has already run by the time src/server.py imports this module.
mcp = FastMCP("domo-mcp-server", instructions=_instructions())

# FastMCP always calls create_initialization_options() with no notification
# options, which advertises tools.listChanged=False — but src/toolsets.py's
# enable_toolset can register new tools mid-session and needs to notify
# clients when it does. Default that capability to on for every session.
mcp._mcp_server.create_initialization_options = partial(
    mcp._mcp_server.create_initialization_options,
    notification_options=NotificationOptions(tools_changed=True),
)
