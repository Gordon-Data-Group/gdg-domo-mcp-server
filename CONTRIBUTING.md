# Contributing to Domo MCP Server

Thanks for your interest in contributing. This project is in alpha, so the most valuable contributions right now are bug reports, corrections to tool signatures, and filling coverage gaps against the Domo API.

## Before You Start

You'll need:
- Python 3.11+
- A Domo instance with admin access (to generate a developer token)
- A developer token from **Admin > Security > Access Tokens**

## Local Setup

```bash
git clone https://github.com/your-org/gdg-domo-mcp-server.git
cd gdg-domo-mcp-server
pip install -e .
cp .env.example .env
# Edit .env with your DOMO_INSTANCE_URL and DOMO_DEVELOPER_TOKEN
```

## Branching

- Branch off `development`, not `main`
- Use short descriptive branch names: `fix/datasets-query-params`, `feat/missing-alerts-tools`
- `main` is release-only — PRs directly to `main` will not be accepted

## Making Changes

**Project structure:**

| Path | Purpose |
|------|---------|
| `src/auth.py` | HTTP helpers; injects auth header on every request |
| `src/app.py` | FastMCP server instance |
| `src/server.py` | Imports all tool modules to register them |
| `src/tools/{group}.py` | One file per API group — this is where tools live |
| `api-definitions-md/` | Authoritative endpoint reference per group |

**Tool naming convention:** `{group}_{action}` in snake_case — e.g. `datasets_query`, `users_search`.

**Adding or fixing a tool:**
1. Find the relevant module in `src/tools/`
2. Cross-reference the endpoint in `api-definitions-md/`
3. Follow the existing patterns in that file for path params, query params, and request bodies
4. Keep docstrings short — one line describing what the tool does

**One module per PR** — changes spanning multiple tool groups are hard to review and harder to revert.

## Verifying Your Changes

There is no automated test suite. Before opening a PR, verify your changes against a real Domo instance:
- Call the affected tools and confirm the response matches the Domo API docs
- Check both the happy path and common error cases (missing required fields, invalid IDs)
- Note which tools you tested in your PR description

## Commit Style

Use plain, descriptive commit messages in the imperative mood:

```
Fix datasets_query missing limit param
Add missing tools to alerts module
Correct path param name in cards_get
```

## Pull Request Checklist

- [ ] Branched from `development`
- [ ] Tested against a live Domo instance
- [ ] Listed which tools were verified in the PR description
- [ ] No new dependencies added
- [ ] Follows existing naming and code conventions

## What We're Not Looking For Right Now

- New dependencies
- Refactors to `auth.py` or server infrastructure
- Auto-generated or untested tools
- Changes to `main` directly

## Questions

Open a GitHub issue — no question is too small.
