# Changelog

All notable changes to this project will be documented in this file.

## [0.0.4] - 2026-10-14

### Added
- Multi-instance support: one server process can serve several Domo instances via `DOMO_INSTANCES` + `DOMO_<ALIAS>_INSTANCE_URL` / `DOMO_<ALIAS>_DEVELOPER_TOKEN` (optional `DOMO_<ALIAS>_READ_ONLY`, `DOMO_DEFAULT_INSTANCE`). Every tool gains an `instance` argument when more than one is configured. The single-instance `DOMO_INSTANCE_URL` / `DOMO_DEVELOPER_TOKEN` form still works unchanged.
- `DOMO_MAX_RESPONSE_CHARS` (default 50000) caps tool output; `DOMO_STRIP_NULLS` (default on) drops null fields from results.
- `.mcp.json.example` client config template (multi-instance, dynamic toolsets).
- Gordon Data Group attribution in the README.

### Changed
- Tool results are compact JSON instead of 2-space-indented JSON.
- Input schemas no longer carry auto-generated `title`s, `default: null`, or `anyOf [X, null]` wrappers.
- Consolidated 22 tools (529 → 507):
  - `ai_text_sql_*`, `ai_text_generation_*`, `ai_text_beastmode_*`, `ai_text_summarize_*`, `ai_forecasting_*`, `ai_image_to_text_*` (18 tools) → `ai_services_list_models`, `ai_services_get_default_model`, `ai_services_run` with a `service` argument. `ai_forecasting_run` was a plain SQL query; use `datasets_query`.
  - `datasets_query` + `datasets_query_sql` → `datasets_query(sql=… | query=…)`, which now also returns only `columns`, `rows`, `numRows`.
  - `datasets_list_data_versions_v2` → `datasets_list_data_versions(api_version="v2")`.
  - `datasets_bulk_update_owners_v1` → `datasets_bulk_update_owners(group_id=…)`.
  - `users_get_v2` / `users_get_v3` → `users_get(api=…)`; `users_list_v3` → `users_list(api="content_v3")`; `users_update_v3` → `users_update(full_user=…)`.

### Fixed
- Parameter descriptions were silently dropped from every tool's schema (`Annotated[T, "text"]` is ignored by Pydantic); they are now sent as JSON-schema descriptions.
- 54 read-only tools backed by POST or PUT endpoints (search, query, bulk-get, card render/definition) were blocked by the write guard under the default `DOMO_READ_ONLY=1`. They now use the unguarded `auth.post_read` / `auth.put_read` verbs.

## [0.0.3] - 2026-08-10

### Added
- `DOMO_READ_ONLY` (default on): write tools are not registered, and mutating HTTP verbs are blocked again in `auth.py` regardless of tool tagging.
- `DOMO_DYNAMIC_TOOLSETS` (default off): start with only `list_toolsets` / `enable_toolset` and register a toolset's tools on demand (with a `tools/list_changed` notification). `DOMO_DEFAULT_TOOLSETS` pre-enables specific toolsets.
- Every tool is tagged read-only or write via the `domo_tool(toolset, read_only)` decorator.
- `datasets_export` and `dataflows_export` write export data (dataset CSV/XLSX, dataflow JSON) to a local file under the user's home directory instead of returning it through the MCP connection.

### Removed
- `cards_get_problems`: duplicate of `cards_get` (identical endpoint).

### Fixed
- `categories` and `filesets` tools were never imported by the server and were unreachable.
- README / CLAUDE.md tool counts reconciled with what is actually implemented.

### Security
- `datasets_upload_file` only reads from `~/Downloads`, `~/Documents`, `~/Desktop`, and `/tmp`, preventing path traversal.
- `DomoHTTPError` strips query strings from URLs in error messages.
- `DOMO_INSTANCE_URL` must be a `*.domo.com` host, so the developer token can't be sent to another server.

## [0.0.2] - 2026-06-02

### Added
- `cards_create_notebook` for rich-text / section-header cards.
- `datasets_upload_file`: create a PUSH dataset from a local CSV or XLSX file (schema inferred, uploaded via the 3-step upload API). Adds the `openpyxl` dependency and the `auth.post_multipart` helper.

### Changed
- `cards_create` / `cards_update`: corrected column format (mapping only, `groupBy` as an object list), verified chart-type list, `badge_singlevalue` KPI pattern, and `series_N_color` override (hex without `#`).
- `cards_update` body must match `cards_create`'s shape (`variables: true`, object-form `formulas` / `annotations` / `conditionalFormats`, `controls: []`, `dynamicTitle`, `dynamicDescription`).
- Page tool docs: `layoutId` comes from `pages_get_with_cards`, not the create response; `pages_get_layout` may return empty; clarified `virtual` / `virtualAppendix` / `children` in `pages_update_layout`.

### Fixed
- `orderBy` entries must include `order` (ASCENDING / DESCENDING); omitting it caused a 500 on card render even though the save succeeded.

## [0.0.1] - 2026-05-22

### Initial Release

Full MCP server implementation exposing Domo internal APIs as tools across 35 modules.

**542 tools across the following modules:**

- `accounts` (19 tools) — account management, credentials, OAuth providers
- `achievements` (8 tools) — achievements and admin management
- `admin` (20 tools) — access tokens, activity logs, customer settings, sessions
- `ai_data_science` (46 tools) — AutoML, Jupyter workspaces, text/image/forecasting AI models
- `alerts` (15 tools) — alert creation, sharing, rules, and evaluations
- `appdb` (23 tools) — datastores, collections, and document CRUD
- `approvals` (7 tools) — approval templates and workflows (GraphQL)
- `app_studio` (13 tools) — App Studio apps, views, and access management
- `brand_kit` (5 tools) — color palettes, email configs, login settings
- `bricks` (17 tools) — Bricks app designs, instances, and versions
- `cards` (32 tools) — card creation, updates, sharing, drill paths, and problems
- `categories` (5 tools) — category listing and entity associations
- `certification` (11 tools) — certification templates and workflows (GraphQL)
- `code_engine` (9 tools) — package deployment, versioning, and function execution
- `credits` (3 tools) — usage reports, subscription details, balance
- `dataflows` (28 tools) — MagicETL/SQL dataflow creation, execution, tagging, and versioning
- `datasets` (65 tools) — dataset CRUD, PDP policies, uploads, streams, data versions, wrangle
- `domo_everywhere` (13 tools) — publications, subscriptions, and invites
- `elevation` (3 tools) — elevation settings and OTP authentication
- `files` (7 tools) — file revisions, cards, and uploads
- `filesets` (19 tools) — fileset management, AI querying, file upload/download
- `forms` (6 tools) — form instances and submissions
- `functions` (11 tools) — Beast Mode function management and locking
- `groups` (11 tools) — group membership, permissions, and dynamic rules
- `left_navigation` (3 tools) — navigation pin management
- `objectives` (25 tools) — OKRs, key results, tags, and periods
- `pages` (22 tools) — dashboard pages, layouts, filter views, and writelocks
- `projects_tasks` (19 tools) — projects, task lists, and task assignments
- `reports` (4 tools) — report scheduling CRUD
- `roles` (5 tools) — role listing and authority management
- `sandbox` (15 tools) — repository commits, promotions, and instance management
- `scheduled_reports` (16 tools) — scheduled report delivery and history
- `task_center` (13 tools) — task queues, assignment, progress, and completion
- `toolkit` (8 tools) — Toolkit job management and triggers
- `users` (16 tools) — user CRUD, profile management, and bulk operations
