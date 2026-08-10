# Domo MCP Server

> **Alpha Release (v0.0.2)** — This is an independent, community-built project. It is not affiliated with, endorsed by, or supported by Domo. APIs, tool signatures, and behavior may change without notice.

MCP server exposing Domo internal APIs as tools. 527 tools across 35 API groups.

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
| `src/auth.py` | HTTP helpers; injects `X-DOMO-DEVELOPER-TOKEN` on every request |
| `src/app.py` | FastMCP server instance |
| `src/server.py` | Imports all tool modules to register them, then calls `mcp.run()` |
| `src/tools/*.py` | 35 modules, one per API group |

The server uses stdio transport (standard for MCP clients). No port binding required.

## Tool Groups

| # | Module | Tools |
|---|--------|-------|
| 01 | accounts | 19 |
| 02 | achievements | 8 |
| 03 | admin | 16 |
| 04 | ai_data_science | 46 |
| 05 | alerts | 15 |
| 06 | appdb | 23 |
| 07 | approvals | 7 |
| 08 | app_studio | 13 |
| 09 | brand_kit | 5 |
| 10 | bricks | 15 |
| 11 | cards | 32 |
| 12 | categories | 5 |
| 13 | certification | 11 |
| 14 | code_engine | 9 |
| 15 | credits | 3 |
| 16 | dataflows | 27 |
| 17 | datasets | 58 |
| 18 | domo_everywhere | 13 |
| 19 | elevation | 3 |
| 20 | files | 7 |
| 21 | filesets | 19 |
| 22 | forms | 6 |
| 23 | functions | 9 |
| 24 | groups | 11 |
| 25 | left_navigation | 3 |
| 26 | objectives | 25 |
| 27 | pages | 22 |
| 28 | projects_tasks | 19 |
| 29 | reports | 4 |
| 30 | roles | 5 |
| 31 | sandbox | 15 |
| 32 | scheduled_reports | 16 |
| 33 | task_center | 13 |
| 34 | toolkit | 8 |
| 35 | users | 16 |
| | **Total** | **526** |
