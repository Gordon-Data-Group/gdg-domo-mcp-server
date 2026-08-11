# Domo MCP Server

> **Alpha Release (v0.0.3)** — This is an independent, community-built project. It is not affiliated with, endorsed by, or supported by Domo. APIs, tool signatures, and behavior may change without notice.

MCP server exposing Domo internal APIs as tools. 529 tools across 35 API groups — 281 read-only, 248 that create/update/delete data.

By default the server is **read-only** and loads **every** toolset up front. Two independent knobs trade safety and token footprint against capability:

- `DOMO_READ_ONLY` (default `1`) — write tools are not registered, and blocked at the HTTP layer even if called directly. Set to `0` to unlock them.
- `DOMO_DYNAMIC_TOOLSETS` (default `0`) — when `1`, the server starts with just two tools, `list_toolsets` and `enable_toolset`, instead of all 35 groups. Call `enable_toolset("datasets")` (etc.) to register a group's tools on demand. Use `DOMO_DEFAULT_TOOLSETS` (comma-separated) to pre-register specific groups at startup under this mode.

## Requirements

- Python 3.11+
- A Domo developer token (Admin → Security → Access Tokens)

## Setup

**1. Install dependencies**

```bash
pip install -e .
```

**2. Configure credentials**

```bash
cp .env.example .env
```

Edit `.env`:

```
DOMO_INSTANCE_URL=https://yourcompany.domo.com
DOMO_DEVELOPER_TOKEN=your_developer_token_here

# Optional — see .env.example for details
# DOMO_READ_ONLY=1
# DOMO_DYNAMIC_TOOLSETS=0
# DOMO_DEFAULT_TOOLSETS=
```

## Running

```bash
# via module
python -m src.server

# via entry point (after pip install -e .)
domo-mcp-server
```

## Connect to Claude Desktop

Add to `~/.claude/claude_desktop_config.json`:

```json
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
```

## Connect to Claude Code

Add to `.mcp.json` (project) or `~/.claude/mcp.json` (global):

```json
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
```

---

## Architecture

| File | Purpose |
|------|---------|
| `src/auth.py` | HTTP helpers; injects `X-DOMO-DEVELOPER-TOKEN` on every request; blocks writes when `DOMO_READ_ONLY` is on |
| `src/app.py` | FastMCP server instance |
| `src/toolsets.py` | Toolset registry — the `domo_tool` decorator every tool uses instead of `@mcp.tool()`; implements `DOMO_READ_ONLY` / `DOMO_DYNAMIC_TOOLSETS` gating and the `list_toolsets` / `enable_toolset` meta-tools |
| `src/server.py` | Imports all tool modules to populate the registry, then calls `mcp.run()` |
| `src/tools/*.py` | 35 modules, one per API group — each Domo toolset name matches its module name |

The server uses stdio transport (standard for MCP clients). No port binding required.

Each tool is tagged `read_only=True` or `read_only=False` when it's defined (`@domo_tool(toolset="datasets", read_only=True)`). That tag drives both gates above — see `src/toolsets.py` for the registration logic and `src/auth.py` for the HTTP-layer enforcement.

## Tool Groups

Toolset name = module name, and is what you pass to `enable_toolset` under `DOMO_DYNAMIC_TOOLSETS=1`.

| # | Toolset | Tools | Read-only | Write |
|---|---------|-------|-----------|-------|
| 01 | accounts | 19 | 14 | 5 |
| 02 | achievements | 8 | 3 | 5 |
| 03 | admin | 16 | 12 | 4 |
| 04 | ai_data_science | 46 | 27 | 19 |
| 05 | alerts | 15 | 8 | 7 |
| 06 | appdb | 23 | 9 | 14 |
| 07 | approvals | 7 | 5 | 2 |
| 08 | app_studio | 13 | 5 | 8 |
| 09 | brand_kit | 5 | 5 | 0 |
| 10 | bricks | 15 | 7 | 8 |
| 11 | cards | 32 | 16 | 16 |
| 12 | categories | 5 | 3 | 2 |
| 13 | certification | 11 | 9 | 2 |
| 14 | code_engine | 9 | 4 | 5 |
| 15 | credits | 3 | 3 | 0 |
| 16 | dataflows | 28 | 15 | 13 |
| 17 | datasets | 60 | 29 | 31 |
| 18 | domo_everywhere | 13 | 12 | 1 |
| 19 | elevation | 3 | 1 | 2 |
| 20 | files | 7 | 3 | 4 |
| 21 | filesets | 19 | 10 | 9 |
| 22 | forms | 6 | 2 | 4 |
| 23 | functions | 9 | 4 | 5 |
| 24 | groups | 11 | 5 | 6 |
| 25 | left_navigation | 3 | 1 | 2 |
| 26 | objectives | 25 | 12 | 13 |
| 27 | pages | 22 | 7 | 15 |
| 28 | projects_tasks | 19 | 10 | 9 |
| 29 | reports | 4 | 1 | 3 |
| 30 | roles | 5 | 5 | 0 |
| 31 | sandbox | 15 | 10 | 5 |
| 32 | scheduled_reports | 16 | 7 | 9 |
| 33 | task_center | 13 | 5 | 8 |
| 34 | toolkit | 8 | 3 | 5 |
| 35 | users | 16 | 9 | 7 |
| | **Total** | **529** | **281** | **248** |
