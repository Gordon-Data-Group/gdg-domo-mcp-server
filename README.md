# Domo MCP Server

> **Alpha Release (v0.0.4)** — This is an independent, community-built project. It is not affiliated with, endorsed by, or supported by Domo. APIs, tool signatures, and behavior may change without notice.

MCP server exposing Domo internal APIs as tools. 507 tools across 35 API groups — 266 read-only, 241 that create/update/delete data. One server process can serve several Domo instances.

Built and maintained by [Gordon Data Group](https://gordondatagroup.com), a data and analytics consulting firm. Need help with a Domo implementation, custom tooling, or AI integration? [Get in touch](https://gordondatagroup.com).

By default the server is **read-only** and loads **every** toolset up front. Two independent knobs trade safety and token footprint against capability:

- `DOMO_READ_ONLY` (default `1`) — write tools are not registered, and blocked at the HTTP layer even if called directly. Set to `0` to unlock them (or per instance with `DOMO_<ALIAS>_READ_ONLY`, see below).
- `DOMO_DYNAMIC_TOOLSETS` (default `0`) — when `1`, the server starts with just two tools, `list_toolsets` and `enable_toolset`, instead of all 35 groups. Call `enable_toolset("datasets")` (etc.) to register a group's tools on demand. Use `DOMO_DEFAULT_TOOLSETS` (comma-separated) to pre-register specific groups at startup under this mode.
- `DOMO_MAX_RESPONSE_CHARS` (default `50000`, `0` = unlimited) — tool results are returned as compact JSON with null fields removed (`DOMO_STRIP_NULLS=0` keeps them), and cut off at this length with a note telling the model to narrow the request.

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
# DOMO_MAX_RESPONSE_CHARS=50000
```

### Multiple Domo instances

Instead of running one server per instance, list aliases in `DOMO_INSTANCES` and give each its own URL and token. Every tool then takes an optional `instance` argument (an enum of your aliases, defaulting to `DOMO_DEFAULT_INSTANCE` or the first alias), and the server instructions tell the model which alias points at which URL.

```
DOMO_INSTANCES=prod,sandbox
DOMO_DEFAULT_INSTANCE=prod
DOMO_PROD_INSTANCE_URL=https://yourcompany.domo.com
DOMO_PROD_DEVELOPER_TOKEN=...
DOMO_SANDBOX_INSTANCE_URL=https://yourcompany-sandbox.domo.com
DOMO_SANDBOX_DEVELOPER_TOKEN=...
DOMO_SANDBOX_READ_ONLY=0   # optional per-instance override of DOMO_READ_ONLY
```

Write tools are registered if any instance allows writes; each call is still blocked at the HTTP layer unless the instance it targets is writable.

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

Add to `.mcp.json` (project) or `~/.claude/mcp.json` (global). See `.mcp.json.example` for a multi-instance config with dynamic toolsets.

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
| `src/auth.py` | Instance configuration and HTTP helpers; injects the active instance's `X-DOMO-DEVELOPER-TOKEN` on every request; blocks writes when that instance is read-only |
| `src/app.py` | FastMCP server instance |
| `src/toolsets.py` | Toolset registry — the `domo_tool` decorator every tool uses instead of `@mcp.tool()`; implements `DOMO_READ_ONLY` / `DOMO_DYNAMIC_TOOLSETS` gating, the `list_toolsets` / `enable_toolset` meta-tools, the `instance` argument, schema slimming, and compact result formatting |
| `src/server.py` | Imports all tool modules to populate the registry, then calls `mcp.run()` |
| `src/tools/*.py` | 35 modules, one per API group — each Domo toolset name matches its module name |

The server uses stdio transport (standard for MCP clients). No port binding required.

Each tool is tagged `read_only=True` or `read_only=False` when it's defined (`@domo_tool(toolset="datasets", read_only=True)`). That tag drives both gates above — see `src/toolsets.py` for the registration logic and `src/auth.py` for the HTTP-layer enforcement. Read-only tools whose endpoint is a POST or PUT (search, query, bulk-get) call `auth.post_read` / `auth.put_read`, which are the only non-GET verbs exempt from that enforcement.

## Tool Groups

Toolset name = module name, and is what you pass to `enable_toolset` under `DOMO_DYNAMIC_TOOLSETS=1`.

| # | Toolset | Tools | Read-only | Write |
|---|---------|-------|-----------|-------|
| 01 | accounts | 19 | 14 | 5 |
| 02 | achievements | 8 | 3 | 5 |
| 03 | admin | 16 | 12 | 4 |
| 04 | ai_data_science | 31 | 17 | 14 |
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
| 17 | datasets | 57 | 27 | 30 |
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
| 35 | users | 12 | 6 | 6 |
| | **Total** | **507** | **266** | **241** |

---

## About Gordon Data Group

This project is maintained by [Gordon Data Group](https://gordondatagroup.com), a consulting firm specializing in Domo implementations, data engineering, and AI-driven tooling. If your team needs help getting more out of Domo — custom integrations, dataflow architecture, governance, or projects like this one — [reach out](https://gordondatagroup.com).
