"""Domo MCP server — entry point.

Run locally:
    python -m src.server

Run via entry point (after pip install -e .):
    domo-mcp-server

Claude Desktop config (~/.claude/claude_desktop_config.json):
    {
      "mcpServers": {
        "domo": {
          "command": "domo-mcp-server",
          "env": {
            "DOMO_INSTANCE_URL": "https://yourcompany.domo.com",
            "DOMO_DEVELOPER_TOKEN": "your_token"
          }
        }
      }
    }
"""
from __future__ import annotations

import sys

from dotenv import load_dotenv

# load_dotenv must run before any tool module is imported, because auth.py
# reads env vars lazily at call time — but FastMCP needs the instance URL
# to be available by the time tools are registered.
load_dotenv()

from src import auth              # noqa: E402
from src.app import mcp           # noqa: E402
from src import toolsets          # noqa: E402

# Importing every tool module runs its @domo_tool-decorated functions, which
# populate the toolset registry in src/toolsets.py. Whether each tool is
# actually attached to `mcp` depends on DOMO_READ_ONLY / DOMO_DYNAMIC_TOOLSETS
# — see that module for the gating logic. Import order doesn't matter; it's
# cheap (no I/O), so every module is always imported regardless of mode.
from src.tools import accounts          # 01
from src.tools import achievements      # 02
from src.tools import admin             # 03
from src.tools import ai_data_science   # 04
from src.tools import alerts            # 05
from src.tools import appdb             # 06
from src.tools import approvals         # 07
from src.tools import app_studio        # 08
from src.tools import brand_kit         # 09
from src.tools import bricks            # 10
from src.tools import cards             # 11
from src.tools import categories        # 12
from src.tools import certification     # 13
from src.tools import code_engine       # 14
from src.tools import credits           # 15
from src.tools import dataflows         # 16
from src.tools import datasets          # 17
from src.tools import domo_everywhere   # 18
from src.tools import elevation         # 19
from src.tools import files             # 20
from src.tools import filesets          # 21
from src.tools import forms             # 22
from src.tools import functions         # 23
from src.tools import groups            # 24
from src.tools import left_navigation   # 25
from src.tools import objectives        # 26
from src.tools import pages             # 27
from src.tools import projects_tasks    # 28
from src.tools import reports           # 29
from src.tools import roles             # 30
from src.tools import sandbox           # 31
from src.tools import scheduled_reports # 32
from src.tools import task_center       # 33
from src.tools import toolkit           # 34
from src.tools import users             # 35

if toolsets.dynamic_toolsets_enabled():
    toolsets.register_meta_tools()


def _startup_summary() -> str:
    summary = toolsets.toolsets_summary()
    total = sum(t["tool_count"] for t in summary)
    registered = sum(t["registered_tool_count"] for t in summary)
    lines = [
        "domo-mcp-server starting",
        f"  DOMO_READ_ONLY={'on' if auth.read_only_mode() else 'off'} "
        f"({'write tools suppressed' if auth.read_only_mode() else 'write tools active — set DOMO_READ_ONLY=1 to disable'})",
        f"  DOMO_DYNAMIC_TOOLSETS={'on' if toolsets.dynamic_toolsets_enabled() else 'off'}",
        f"  tools registered at startup: {registered}/{total} "
        f"across {sum(1 for t in summary if t['enabled'])}/{len(summary)} toolsets "
        f"({sum(1 for t in summary if t['fully_enabled'])} fully enabled)",
    ]
    return "\n".join(lines)


def main() -> None:
    # Tool registration is settled by the time every module above has been
    # imported. stderr only — stdout is reserved for the MCP stdio protocol.
    print(_startup_summary(), file=sys.stderr)
    mcp.run()


if __name__ == "__main__":
    main()
