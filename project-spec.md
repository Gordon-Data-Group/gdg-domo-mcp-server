# Domo MCP Server — Project Spec

## Overview

Python-based MCP (Model Context Protocol) server that exposes Domo's internal APIs as callable tools. The server allows an AI assistant to read and write data in a Domo instance by calling tools that map to documented Domo API endpoints.

---

## Auth Strategy

**Header-based token auth on every request:**

```
X-DOMO-DEVELOPER-TOKEN: <token>
```

- Token is a Domo developer token obtained from the instance admin panel.
- Injected as a header on every HTTP request — no OAuth flow, no token refresh.
- The token is treated as a secret and loaded from an environment variable (`DOMO_DEVELOPER_TOKEN`).
- No per-endpoint auth variation; all endpoints use the same header.

---

## Base URL

```
{{instanceUrl}}/api
```

- `instanceUrl` is the full scheme + hostname of the Domo instance, e.g. `https://mycompany.domo.com`.
- Loaded from environment variable (`DOMO_INSTANCE_URL`).
- All endpoint paths in the definitions are relative to this base.
- Example full URL: `https://mycompany.domo.com/api/data/v3/datasources`

---

## Language & Stack

- **Language:** Python
- **HTTP client:** `httpx` (async-capable) or `requests`
- **MCP framework:** `mcp` (Python SDK)
- **Config:** environment variables via `python-dotenv`
- **API definitions source:** `api-definitions-md/` — one `.md` file per group

---

## Naming Conventions

### Tool naming
Tools are named `{group}_{action}` in snake_case, e.g.:
- `datasets_list` — list datasets
- `datasets_query` — run a SQL query against a dataset
- `users_search` — search users
- `pages_get` — get a page/dashboard

### Parameter naming
- Path variables use their original names from the URL (e.g., `:id` → `id`, `:datasetId` → `dataset_id` in Python snake_case)
- Query params passed as optional kwargs
- Request bodies passed as a `body` dict argument

### File layout
```
/
├── project-spec.md
├── api-definitions/          # Source JSON definitions
├── api-definitions-md/       # Converted markdown definitions (35 files)
├── server.py                 # MCP server entrypoint
├── tools/
│   ├── __init__.py
│   ├── accounts.py
│   ├── admin.py
│   ├── datasets.py
│   └── ...                   # One module per group
└── client.py                 # Shared HTTP client wrapper (auth header injection)
```

---

## Tool Groups

The 35 API definition files map to the following functional tool groups. Each group becomes a module under `tools/`.

| # | Group | Module | Description |
|---|-------|--------|-------------|
| 01 | Accounts | `accounts.py` | Data connectors, providers, OAuth configs, account credentials |
| 02 | Achievements | `achievements.py` | User achievement badges |
| 03 | Admin | `admin.py` | Activity logs, access tokens, sessions, company settings, OAuth clients |
| 04 | AI / Data Science | `ai_data_science.py` | AutoML, AI service layer (text-to-SQL, text gen, summarization, forecasting), Jupyter workspaces |
| 05 | Alerts | `alerts.py` | Alert creation, evaluation, subscriptions, sharing |
| 06 | AppDB | `appdb.py` | NoSQL document store (datastores, collections, documents) |
| 07 | Approvals | `approvals.py` | Approval workflow templates and requests (GraphQL) |
| 08 | App Studio | `app_studio.py` | Low-code app management, views, sharing |
| 09 | Brand Kit | `brand_kit.py` | Color palettes, email configs, login settings |
| 10 | Bricks / Pro-Code Apps | `bricks.py` | Custom app designs, instances, versions, file assets |
| 11 | Cards | `cards.py` | KPI/chart cards, sharing, drill paths, problems |
| 12 | Categories | `categories.py` | Certified attributes / entity category tags |
| 13 | Certification | `certification.py` | Content certification workflows (GraphQL) |
| 14 | Code Engine | `code_engine.py` | Serverless function packages and execution |
| 15 | Credits | `credits.py` | Credit usage reporting and contract details |
| 16 | DataFlows | `dataflows.py` | ETL/ELT flow management, execution, tags |
| 17 | DataSets & Streams | `datasets.py` | Dataset CRUD, queries, uploads, PDP policies, data repair, streams |
| 18 | Domo Everywhere | `domo_everywhere.py` | Publications and subscriber management |
| 19 | Elevation | `elevation.py` | OTP-based session elevation |
| 20 | Files | `files.py` | Binary file upload/management and file cards |
| 21 | FileSets | `filesets.py` | File collections with folder structure, search, AI query |
| 22 | Forms | `forms.py` | Form instances and submissions |
| 23 | Functions (Beast Modes) | `functions.py` | Calculated field (beast mode) CRUD |
| 24 | Groups | `groups.py` | User group management, membership, dynamic rules |
| 25 | Left Navigation | `left_navigation.py` | Nav pin management |
| 26 | Objectives (Goals) | `objectives.py` | OKR objectives, key results, periods, tags |
| 27 | Pages (Dashboards) | `pages.py` | Dashboard CRUD, layouts, filter views, sharing |
| 28 | Projects & Tasks | `projects_tasks.py` | Project/task management, lists, attachments |
| 29 | Reports | `reports.py` | Slideshow publication reports |
| 30 | Roles & Authorities | `roles.py` | Role definitions and authority/grant assignments |
| 31 | Sandbox | `sandbox.py` | Environment promotion, repositories, commit requests |
| 32 | Scheduled Reports | `scheduled_reports.py` | Report schedule CRUD, send-now, view management |
| 33 | Task Center | `task_center.py` | Queue-based human task routing and completion |
| 34 | Toolkit | `toolkit.py` | Scheduled job execution and triggers |
| 35 | Users | `users.py` | User CRUD, search, bulk ops, profile pictures |

---

## Full Endpoint Reference

Auth header applied to all: `X-DOMO-DEVELOPER-TOKEN: <token>`
Response shape: JSON (object or array) unless noted. Not formally documented in source definitions.

---

### Accounts
*See `api-definitions-md/01-accounts.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/data/v1/accounts` | — | — |
| POST | `{{instanceUrl}}/api/search/v1/query` | — | search body |
| GET | `{{instanceUrl}}/api/data/v1/accounts/templates/user/extended` | — | — |
| GET | `{{instanceUrl}}/api/data/v2/datasources/providers` | — | — |
| GET | `{{instanceUrl}}/api/data/v1/providers` | query: fields, filter, includeFederated | — |
| GET | `{{instanceUrl}}/api/data/v1/accounts/provider/:provider` | path: provider | — |
| GET | `{{instanceUrl}}/api/data/v1/accounts/:id` | path: id | — |
| GET | `{{instanceUrl}}/api/data/v1/providers/:provider/account/:id` | path: provider, id; query: unmask | — |
| GET | `{{instanceUrl}}/api/data/v1/providers/:provider` | path: provider; query: fields, country, language | — |
| GET | `{{instanceUrl}}/api/data/v1/providers/:provider/images/96.png` | path: provider | — |
| GET | `{{instanceUrl}}/api/connectors/appstore/v2/details/connector/:connector` | path: connector; query: fields, country, language | — |
| GET | `{{instanceUrl}}/api/data/v2/datasources/account/:id` | path: id | — |
| POST | `{{instanceUrl}}/api/data/v2/datasources/accounts` | — | `[accountId, ...]` |
| POST | `{{instanceUrl}}/api/data/v1/accounts/validators` | — | credentials object |
| POST | `{{instanceUrl}}/api/data/v1/accounts` | — | account object |
| PUT | `{{instanceUrl}}/api/data/v1/accounts/:id/name` | path: id | raw text name |
| PUT | `{{instanceUrl}}/api/data/v1/providers/:providerId/account/:id` | path: providerId, id | credentials object |
| PUT | `{{instanceUrl}}/api/data/v2/accounts/share/:id` | path: id | access object |
| DELETE | `{{instanceUrl}}/api/data/v1/accounts/:id` | path: id | — |

---

### Achievements
*See `api-definitions-md/02-achievements.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/content/v1/achievements/bulk` | query: limit, offset | — |
| GET | `{{instanceUrl}}/api/content/v1/achievements/:id` | path: id | — |
| GET | `{{instanceUrl}}/api/content/v1/achievements/:id/admins` | path: id | — |
| POST | `{{instanceUrl}}/api/content/v1/achievements` | — | achievement object |
| POST | `{{instanceUrl}}/api/content/v1/achievements/:achievementId/admins` | path: achievementId | admin object |
| PUT | `{{instanceUrl}}/api/content/v1/achievements/:id` | path: id | achievement object |
| DELETE | `{{instanceUrl}}/api/content/v1/achievements/:id` | path: id | — |
| DELETE | `{{instanceUrl}}/api/content/v1/achievements/:achievementId/admins/:adminId` | path: achievementId, adminId | — |

---

### Admin
*See `api-definitions-md/03-admin.md`*

**Access Tokens**

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/data/v1/accesstokens` | — | — |
| DELETE | `{{instanceUrl}}/api/data/v1/accesstokens/:id` | path: id | — |

**Activity Log**

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/audit/v1/user-audits/objectTypes` | — | — |
| GET | `{{instanceUrl}}/api/audit/v1/user-audits` | query: start, end, offset, limit, objectType | — |

**Company Settings**

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/query/v1/datasources/customer-stats` | — | — |
| GET | `{{instanceUrl}}/api/dataprocessing/v1/dataflows/timezones` | — | — |
| GET | `{{instanceUrl}}/api/companysettings` | — | — |
| GET | `{{instanceUrl}}/api/content/v1/customer-states/locale` | query: ignoreCache | — |
| GET | `{{instanceUrl}}/api/content/v1/customer-states/:customerState` | path: customerState; query: ignoreCache | — |
| GET | `{{instanceUrl}}/api/content/v1/customer-states` | query: ignoreCache, stateName | — |
| GET | `{{instanceUrl}}/api/customer/v1/properties/:property` | path: property | — |
| GET | `{{instanceUrl}}/api/content/v1/licenses/total/current` | — | — |
| GET | `{{instanceUrl}}/api/datascience/v1/settings` | — | — |
| GET | `{{instanceUrl}}/api/metrics/v1/usage/credits/contract/current/summary` | — | — |
| GET | `{{instanceUrl}}/api/content/v1/landings/customer` | — | — |
| PUT | `{{instanceUrl}}/api/content/v1/customer-states/:customerState` | path: customerState | state object |
| PUT | `{{instanceUrl}}/api/customer/v1/properties/:property` | path: property | value |

**OAuth API Clients**

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/identity/v1/developer-tokens` | — | — |

**Session Management**

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/sessions/v1/admin` | query: limit | — |
| DELETE | `{{instanceUrl}}/api/sessions/v1/admin/:id` | path: id | — |

---

### AI / Data Science
*See `api-definitions-md/04-ai-data-science.md`*

**AutoML**

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/dataprocessing/v1/ml/:datasetId/automl/job` | path: datasetId; query: includeDetails | — |
| GET | `{{instanceUrl}}/api/dataprocessing/v1/ml/:datasetId/automl/job/:modelId` | path: datasetId, modelId; query: includeCandidates | — |
| GET | `{{instanceUrl}}/api/dataprocessing/v1/ml/automl/job/:modelId/schema` | path: modelId | — |
| GET | `{{instanceUrl}}/api/dataprocessing/v1/ml/automl/job/:modelId/explain` | path: modelId | — |
| POST | `{{instanceUrl}}/api/dataprocessing/v1/ml/:id/model` | path: id | model config |

**AI Models & Projects**

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| POST | `{{instanceUrl}}/api/datascience/ml/v1/search/models` | — | search body |
| GET | `{{instanceUrl}}/api/datascience/ml/v1/models/:id` | path: id | — |
| PUT | `{{instanceUrl}}/api/datascience/ml/v1/models/:id` | path: id | model object |
| POST | `{{instanceUrl}}/api/datascience/ml/v1/models/:id/ownership` | path: id | owner object |
| DELETE | `{{instanceUrl}}/api/datascience/ml/v1/models/:modelId` | path: modelId | — |
| POST | `{{instanceUrl}}/api/datascience/ml/v1/search/projects` | — | search body |
| GET | `{{instanceUrl}}/api/datascience/ml/v1/projects/:projectId` | path: projectId | — |
| PUT | `{{instanceUrl}}/api/datascience/ml/v1/projects/:id` | path: id | project object |
| POST | `{{instanceUrl}}/api/datascience/ml/v1/projects/:id/ownership` | path: id | owner object |
| DELETE | `{{instanceUrl}}/api/datascience/ml/v1/projects/:id` | path: id | — |

**AI Service Layer**

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/ai/v1/settings/services/sql/models` | — | — |
| GET | `{{instanceUrl}}/api/ai/v1/settings/services/sql/models/default` | — | — |
| POST | `{{instanceUrl}}/api/ai/v1/text/sql` | — | prompt body |
| GET | `{{instanceUrl}}/api/ai/v1/settings/services/generation/models` | — | — |
| GET | `{{instanceUrl}}/api/ai/v1/settings/services/generation/models/default` | — | — |
| POST | `{{instanceUrl}}/api/ai/v1/text/generation` | — | prompt body |
| GET | `{{instanceUrl}}/api/ai/v1/settings/services/beastmode/models` | — | — |
| GET | `{{instanceUrl}}/api/ai/v1/settings/services/beastmode/models/default` | — | — |
| POST | `{{instanceUrl}}/api/ai/v1/text/beastmode` | — | prompt body |
| GET | `{{instanceUrl}}/api/ai/v1/settings/services/summarization/models` | — | — |
| GET | `{{instanceUrl}}/api/ai/v1/settings/services/summarization/models/default` | — | — |
| POST | `{{instanceUrl}}/api/ai/v1/text/summarize` | — | prompt body |
| GET | `{{instanceUrl}}/api/ai/v1/settings/services/forecasting/models` | — | — |
| GET | `{{instanceUrl}}/api/ai/v1/settings/services/forecasting/models/default` | — | — |
| POST | `{{instanceUrl}}/api/query/v1/execute/:datasetId` | path: datasetId | query body |
| GET | `{{instanceUrl}}/api/ai/v1/settings/services/image/models` | — | — |
| GET | `{{instanceUrl}}/api/ai/v1/settings/services/image/models/default` | — | — |
| POST | `{{instanceUrl}}/api/ai/v1/image/text` | — | image body |
| GET | `{{instanceUrl}}/api/ai/v1/settings/general` | — | — |
| GET | `{{instanceUrl}}/api/ai/v1/sessions/:sessionId` | path: sessionId | — |
| GET | `{{instanceUrl}}/api/ai/v1/sessions/:sessionId/context` | path: sessionId | — |
| POST | `{{instanceUrl}}/api/ai/v1/assistant/toolkits/DOMO_BASIC_ASSISTANT/execute/streaming` | — | chat body |

**Jupyter Workspaces**

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/fileshare/v1/shares` | — | — |
| GET | `{{instanceUrl}}/api/fileshare/v1/shares/:id/permissions` | path: id | — |
| POST | `{{instanceUrl}}/api/fileshare/v1/shares` | — | share object |
| PUT | `{{instanceUrl}}/api/fileshare/v1/shares/:id` | path: id | share object |
| POST | `{{instanceUrl}}/api/fileshare/v1/shares/:id/permissions` | path: id | permissions object |
| DELETE | `{{instanceUrl}}/api/fileshare/v1/shares/:id` | path: id | — |
| POST | `{{instanceUrl}}/api/datascience/v1/search/workspaces` | — | search body |
| GET | `{{instanceUrl}}/api/datascience/v1/workspaces/:id` | path: id | — |
| PUT | `{{instanceUrl}}/api/datascience/v1/workspaces/:id/ownership` | path: id | owner object |

---

### Alerts
*See `api-definitions-md/05-alerts.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/social/v4/alerts` | query: all, fields, limit, offset | — |
| GET | `{{instanceUrl}}/api/messaging/v3/subscriptions/schedule/primary/immediate` | — | — |
| GET | `{{instanceUrl}}/api/messaging/v3/preferences/immediate/user/current/alert_triggered` | — | — |
| POST | `{{instanceUrl}}/api/search/v1/query` | — | search body |
| POST | `{{instanceUrl}}/api/social/v4/alerts/ids` | query: all, subscriberId, fields, limit, offset | alert IDs array |
| GET | `{{instanceUrl}}/api/social/v4/alerts/:id` | path: id | — |
| GET | `{{instanceUrl}}/api/social/v4/alerts/:alertId/actions/:actionId` | path: alertId, actionId | — |
| GET | `{{instanceUrl}}/api/social/v4/alerts/:id/evaluations` | path: id | — |
| POST | `{{instanceUrl}}/api/social/v4/alerts` | — | alert object |
| POST | `{{instanceUrl}}/api/social/v4/alerts/:id/share` | path: id | share object |
| PATCH | `{{instanceUrl}}/api/social/v4/alerts/:id` | path: id | partial alert object |
| PUT | `{{instanceUrl}}/api/social/v4/alerts/:id` | path: id | alert rules |
| PUT | `{{instanceUrl}}/api/social/v4/alerts/:id/message-template` | path: id | template object |
| DELETE | `{{instanceUrl}}/api/social/v4/alerts/:id` | path: id | — |
| DELETE | `{{instanceUrl}}/api/social/v4/alerts/:id/subscriptions` | path: id; query: subscriberId, type | — |

---

### AppDB
*See `api-definitions-md/06-appdb.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| POST | `{{instanceUrl}}/api/datastores/v1/collections/query` | — | query body |
| POST | `{{instanceUrl}}/api/datastores/v2/collections/:id/documents/query` | path: id; query: limit, offset, count, avg, sum, max, min, orderby, groupby | query body |
| GET | `{{instanceUrl}}/api/datastores/v1` | — | — |
| GET | `{{instanceUrl}}/api/datastores/v1/collections` | — | — |
| GET | `{{instanceUrl}}/api/datastores/v1/:id` | path: id | — |
| GET | `{{instanceUrl}}/api/datastores/v1/:id/collections` | path: id | — |
| GET | `{{instanceUrl}}/api/datastores/v1/collections/:id` | path: id | — |
| GET | `{{instanceUrl}}/api/datastores/v1/collections/:collectionId/documents` | path: collectionId | — |
| GET | `{{instanceUrl}}/api/datastores/v1/collections/:id/permission` | path: id | — |
| POST | `{{instanceUrl}}/api/datastores/v1` | — | datastore object |
| POST | `{{instanceUrl}}/api/datastores/v1/:datastoreId/collections/` | path: datastoreId | collection object |
| POST | `{{instanceUrl}}/api/datastores/v1/collections` | — | collection + datastore object |
| POST | `{{instanceUrl}}/api/datastores/v1/collections/:collectionId/documents` | path: collectionId | document object |
| POST | `{{instanceUrl}}/api/datastores/v1/collections/:collectionId/documents/bulk` | path: collectionId | documents array |
| PUT | `{{instanceUrl}}/api/datastores/v1/collections/:id` | path: id | collection object |
| PUT | `{{instanceUrl}}/api/datastores/v1/collections/:collectionId/permission/:entityType/:entityId` | path: collectionId, entityType, entityId; query: overwrite, permissions | — |
| PUT | `{{instanceUrl}}/api/datastores/v2/collections/:collectionId/documents/:documentId` | path: collectionId, documentId | document object |
| PUT | `{{instanceUrl}}/api/datastores/v2/collections/:collectionId/documents/bulk` | path: collectionId | documents array |
| DELETE | `{{instanceUrl}}/api/datastores/v1/:id` | path: id | — |
| DELETE | `{{instanceUrl}}/api/datastores/v1/collections/:id` | path: id | — |
| DELETE | `{{instanceUrl}}/api/datastores/v1/collections/:collectionId/permission/:entityType/:entityId` | path: collectionId, entityType, entityId | — |
| DELETE | `{{instanceUrl}}/api/datastores/v2/collections/:collectionId/documents/:documentId` | path: collectionId, documentId | — |
| DELETE | `{{instanceUrl}}/api/datastores/v2/collections/:collectionId/documents/bulk` | path: collectionId; query: ids | — |

---

### Approvals
*See `api-definitions-md/07-approvals.md`*

All operations POST to `{{instanceUrl}}/api/synapse/approval/graphql` with a GraphQL body.

| Operation | Body |
|-----------|------|
| Search Templates | GraphQL query |
| Search Approvals | GraphQL query |
| List Templates | GraphQL query |
| Get Template | GraphQL query |
| Get Approval | GraphQL query |
| Replace Approver | GraphQL mutation |
| Update Template | GraphQL mutation |

---

### App Studio
*See `api-definitions-md/08-app-studio.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/content/v1/dataapps` | query: parts, includeHiddenViews, authoring | — |
| POST | `{{instanceUrl}}/api/content/v1/dataapps/adminsummary` | query: limit, skip | filter body |
| GET | `{{instanceUrl}}/api/content/v1/dataapps/:appId` | path: appId | — |
| GET | `{{instanceUrl}}/api/content/v1/dataapps/:appId/adminsummary` | path: appId | — |
| GET | `{{instanceUrl}}/api/content/v1/dataapps/:appId/access` | path: appId | — |
| POST | `{{instanceUrl}}/api/content/v1/dataapps/share` | query: sendEmail | share object |
| POST | `{{instanceUrl}}/api/content/v1/dataapps/:appId/views` | path: appId | view object |
| PUT | `{{instanceUrl}}/api/content/v1/dataapps/bulk/owners` | — | owners array |
| PUT | `{{instanceUrl}}/api/content/v1/dataapps/:appId/duplicate` | path: appId | duplicate options |
| PUT | `{{instanceUrl}}/api/content/v1/dataapps/:appId/duplicate/synchronous` | path: appId | duplicate options |
| DELETE | `{{instanceUrl}}/api/content/v1/dataapps/:appId` | path: appId | — |
| DELETE | `{{instanceUrl}}/api/content/v1/dataapps/:appId/views/:viewId` | path: appId, viewId | — |
| POST | `{{instanceUrl}}/api/content/v1/dataapps/bulk/owners/remove` | — | owners array |

---

### Brand Kit
*See `api-definitions-md/09-brand-kit.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/brandkit/v1/chartColorPalettes/all` | — | — |
| GET | `{{instanceUrl}}/api/messaging/v1/email/configurations` | — | — |
| GET | `{{instanceUrl}}/api/content/v1/login-settings/v1` | — | — |
| GET | `{{instanceUrl}}/api/messaging/v1/email/configurations/template` | — | — |
| GET | `{{instanceUrl}}/api/messaging/v1/email/configurations/backlink` | — | — |

---

### Bricks / Pro-Code Apps
*See `api-definitions-md/10-bricks-and-pro-code-apps.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/apps/v1/designs` | query: checkAdminAuthority, creator, deleted, order, direction, limit, offset, search, withPermission, parts | — |
| GET | `{{instanceUrl}}/api/domoapps/apps/v2/:id` | path: id | — |
| GET | `{{instanceUrl}}/api/apps/v1/designs/:id` | path: id; query: parts | — |
| GET | `{{instanceUrl}}/api/v1/designs/:designId/versions/:versionNumber/assets` | path: designId, versionNumber; query: path | — |
| GET | `{{instanceUrl}}/api/v1/designs/:designId/versions/:versionNumber` | path: designId, versionNumber | — |
| GET | `{{instanceUrl}}/api/domoapps/apps/v2/contexts/:contextId` | path: contextId | — |
| GET | `{{instanceUrl}}/api/apps/v1/designs/count` | query: checkAdminAuthority, creator, deleted, search, withPermission | — |
| POST | `{{instanceUrl}}/api/apps/v1/instances` | query: temporary | instance object |
| POST | `{{instanceUrl}}/api/apps/v1/designs/:id/permissions/:permissions` | path: id, permissions | permissions body |
| POST | `{{instanceUrl}}/api/domoapps/designs/:id/release` | path: id; query: version | — |
| POST | `{{instanceUrl}}/api/apps/v1/designs/:designId/versions/:versionNumber/assets` | path: designId, versionNumber; query: path | file content |
| PUT | `{{instanceUrl}}/api/apps/v1/instances/:instanceId` | path: instanceId | instance object |
| PUT | `{{instanceUrl}}/api/domoapps/apps/v2/contexts/:id` | path: id | context object |
| DELETE | `{{instanceUrl}}/api/domoapps/designs/:id` | path: id | — |
| DELETE | `{{instanceUrl}}/api/apps/v1/designs/:designId` | path: designId | — |
| DELETE | `{{instanceUrl}}/api/apps/v1/instances/:instanceId` | path: instanceId | — |
| PUT | `{{instanceUrl}}/api/apps/v1/designs/:designId/undelete` | path: designId | — |

---

### Cards
*See `api-definitions-md/11-cards.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| POST | `{{instanceUrl}}/api/search/v1/query` | — | search body |
| POST | `{{instanceUrl}}/api/content/v2/cards/adminsummary` | query: limit, skip | filter body |
| GET | `{{instanceUrl}}/api/content/v1/cards` | query: urns, parts, includeFiltered | — |
| GET | `{{instanceUrl}}/api/content/v1/cards/notebook/:id` | path: id | — |
| GET | `{{instanceUrl}}/api/content/v1/cards/:id/link` | path: id | — |
| PUT | `{{instanceUrl}}/api/content/v1/analytics/views/cards/counts` | — | card urns array |
| GET | `{{instanceUrl}}/api/content/v1/share/accesslist/badge/:id` | path: id; query: expandUsers | — |
| GET | `{{instanceUrl}}/api/content/v1/cards/:id/details` | path: id | — |
| GET | `{{instanceUrl}}/api/content/v1/datasources/:id/cards` | path: id; query: drill | — |
| GET | `{{instanceUrl}}/api/content/v1/cards/minmaxdates` | query: urns | — |
| GET | `{{instanceUrl}}/api/content/v1/access/users/:id/cards` | path: id; query: limit, offset | — |
| GET | `{{instanceUrl}}/api/content/v1/cards/kpi/:chartType/options` | path: chartType | — |
| GET | `{{instanceUrl}}/api/content/v1/cards/kpi/palette` | — | — |
| GET | `{{instanceUrl}}/api/content/v1/cards/kpi/:cardId/comparemove/:datasetId` | path: cardId, datasetId | — |
| PUT | `{{instanceUrl}}/api/content/v3/cards/kpi/definition` | — | card def body |
| PUT | `{{instanceUrl}}/api/content/v1/cards/kpi/:id/render` | path: id; query: parts | render body |
| PUT | `{{instanceUrl}}/api/content/v3/cards/kpi` | query: pageId, parentUrn | card definition |
| POST | `{{instanceUrl}}/api/content/v1/share` | query: sendEmail | share body |
| POST | `{{instanceUrl}}/api/kpis/:id/history` | path: id | history entry |
| PUT | `{{instanceUrl}}/api/content/v3/cards/kpi/:id` | path: id | card definition |
| PUT | `{{instanceUrl}}/api/content/v1/cards/:id` | path: id | lock object |
| PUT | `{{instanceUrl}}/api/content/v1/cards/bulk/pages` | — | cards + pages mapping |
| PUT | `{{instanceUrl}}/api/content/v1/cards/:id/pages` | path: id | pages array |
| PUT | `{{instanceUrl}}/api/content/v1/analytics/views/cards/increment` | — | card URN object |
| POST | `{{instanceUrl}}/api/content/v1/cards/owners/:action` | path: action | owners body |
| POST | `{{instanceUrl}}/api/kpis/:id/remove` | path: id; query: pageid | — |
| DELETE | `{{instanceUrl}}/api/content/v1/share/bulk/badge/:type/:id` | path: type, id; query: resourceIds | — |
| DELETE | `{{instanceUrl}}/api/content/v1/cards/bulk` | query: cardIds | — |
| DELETE | `{{instanceUrl}}/api/kpis/:cardId/drillPath/:drillNumber/drillView/:drillPathId` | path: cardId, drillNumber, drillPathId | — |
| GET | `{{instanceUrl}}/api/content/v1/cards` | query: urns, parts (problems) | — |
| POST | `{{instanceUrl}}/api/content/v1/badges/:cardId/problems` | path: cardId | problem object |
| PUT | `{{instanceUrl}}/api/content/v1/badges/:cardId/problems/:problemId/states` | path: cardId, problemId | state object |

---

### Categories (Certified Attributes)
*See `api-definitions-md/12-categories-certified-attributes-.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/entity/v1/properties/category` | — | — |
| GET | `{{instanceUrl}}/api/entity/v1/properties/category/usage` | — | — |
| GET | `{{instanceUrl}}/api/entity/v1/properties/entity/:type/:id` | path: type, id | — |
| POST | `{{instanceUrl}}/api/entity/v1/properties/category` | — | category object |
| PUT | `{{instanceUrl}}/api/entity/v1/properties/entity/:type/:id` | path: type, id | categories array |

---

### Certification
*See `api-definitions-md/13-certification.md`*

All operations POST to `{{instanceUrl}}/api/synapse/approval/graphql` with a GraphQL body.

| Operation |
|-----------|
| List Certifications |
| List Certification Templates |
| List Certified Entities |
| Get Certification |
| Get Certification Template |
| Get Certification ID from Approval ID |
| Get Entity Access |
| Get Waiting on Me Count |
| Create Certification |
| Remove Certification |

Also: `GET {{instanceUrl}}/api/customer/v1/properties/:type` — Get Certification Expire on Edit [path: type]

---

### Code Engine
*See `api-definitions-md/14-code-engine.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| POST | `{{instanceUrl}}/api/search/v1/query` | — | search body |
| GET | `{{instanceUrl}}/api/codeengine/v2/packages/:id` | path: id; query: parts | — |
| GET | `{{instanceUrl}}/api/codeengine/v2/packages/:id/versions/:version` | path: id, version; query: parts | — |
| GET | `{{instanceUrl}}/api/codeengine/v2/packages/:id/permissions` | path: id | — |
| POST | `{{instanceUrl}}/api/codeengine/v2/packages/:id/versions/:version/functions/:function` | path: id, version, function | function args |
| POST | `{{instanceUrl}}/api/codeengine/v2/packages/:id/versions/:version/release` | path: id, version | — |
| POST | `{{instanceUrl}}/api/codeengine/v2/packages` | — | package object |
| PUT | `{{instanceUrl}}/api/codeengine/v2/packages/:id` | path: id | owner object |
| POST | `{{instanceUrl}}/api/codeengine/v2/packages/:id/permissions` | path: id | permissions object |

---

### Credits
*See `api-definitions-md/15-credits.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/metrics/v1/usage/credits/reports/usage` | query: startDate, endDate | — |
| GET | `{{instanceUrl}}/api/metrics/v1/usage/credits/reports/subscription` | — | — |
| GET | `{{instanceUrl}}/api/metrics/v1/usage/credits/reports/balance` | — | — |

---

### DataFlows
*See `api-definitions-md/16-dataflows.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| POST | `{{instanceUrl}}/api/search/v1/query` | — | search body |
| GET | `{{instanceUrl}}/api/dataprocessing/v2/dataflows` | query: limit, offset, orderBy | — |
| GET | `{{instanceUrl}}/api/dataprocessing/v1/dataflows/:id/versions` | path: id | — |
| GET | `{{instanceUrl}}/api/dataprocessing/v2/dataflows/:id` | path: id | — |
| GET | `{{instanceUrl}}/api/dataprocessing/v2/dataflows/:dataflowId/versions/:versionId` | path: dataflowId, versionId | — |
| GET | `{{instanceUrl}}/api/dataprocessing/v3/dataflows/:dataflowId/versions/:versionNumber` | path: dataflowId, versionNumber | — |
| GET | `{{instanceUrl}}/api/dataprocessing/v1/dataflows/:id/executions` | path: id; query: limit, offset | — |
| GET | `{{instanceUrl}}/api/dataprocessing/v1/dataflows/:dataflowId/executions/:executionId` | path: dataflowId, executionId | — |
| GET | `{{instanceUrl}}/api/dataprocessing/v1/dataflows/:id/subscription` | path: id | — |
| GET | `{{instanceUrl}}/api/search/v1/saved` | query: queryProfile | — |
| GET | `{{instanceUrl}}/api/dataprocessing/v1/dataflows/timezones` | — | — |
| GET | `{{instanceUrl}}/api/dataprocessing/v1/expression-docs` | — | — |
| GET | `{{instanceUrl}}/api/dataprocessing/v2/dataflows/filters/dataflowType` | — | — |
| POST | `{{instanceUrl}}/api/dataprocessing/v1/dataflows/:id/executions` | path: id; query: activationTypeOverride, createPendingExecution | — |
| POST | `{{instanceUrl}}/api/dataprocessing/v1/dataflows/bulk/execute` | — | dataflow IDs array |
| POST | `{{instanceUrl}}/api/dataprocessing/v1/dataflows/previews/run` | — | preview body |
| POST | `{{instanceUrl}}/api/dataprocessing/v1/dataflows` | — | dataflow object |
| POST | `{{instanceUrl}}/api/dataprocessing/v1/dataflows/:id/tags` | path: id | tag object |
| PUT | `{{instanceUrl}}/api/dataprocessing/v1/dataflows/bulk/tag` | — | bulk tag body |
| PUT | `{{instanceUrl}}/api/dataprocessing/v1/dataflows/:id` | path: id | dataflow object |
| PUT | `{{instanceUrl}}/api/dataprocessing/v1/dataflows/:id/patch` | path: id | patch object |
| PUT | `{{instanceUrl}}/api/dataprocessing/v1/dataflows/bulk/patch` | — | bulk patch body |
| DELETE | `{{instanceUrl}}/api/dataprocessing/v1/dataflows/:id` | path: id | — |
| PUT | `{{instanceUrl}}/api/dataprocessing/v1/dataflows/bulk/delete` | — | IDs array |
| DELETE | `{{instanceUrl}}/api/dataprocessing/v1/dataflows/:id/tags` | path: id | — |
| DELETE | `{{instanceUrl}}/api/dataprocessing/v1/dataflows/:id/tags/:tag` | path: id, tag | — |
| PUT | `{{instanceUrl}}/api/dataprocessing/v1/dataflows/bulk/tag/delete` | — | bulk tag IDs |

---

### DataSets & Streams
*See `api-definitions-md/17-datasets-and-streams.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| POST | `{{instanceUrl}}/api/data/ui/v3/datasources/search` | — | search body |
| GET | `{{instanceUrl}}/api/data/v3/datasources` | query: limit, offset, part, includeHidden, orderBy, ownerId, displayType, type, dataProviderType, nameLike, createdSince | — |
| GET | `{{instanceUrl}}/api/data/ui/v3/datasources/search/tags/all` | — | — |
| POST | `{{instanceUrl}}/api/data/v3/datasources/bulk` | query: includePrivate, includeAllDetails | dataset IDs array |
| POST | `{{instanceUrl}}/api/data/ui/v3/datasources/ownedBy` | — | owner filter |
| GET | `{{instanceUrl}}/api/data/v3/datasources/:id` | path: id; query: includeAllDetails, part | — |
| GET | `{{instanceUrl}}/api/data/v1/streams/:id` | path: id; query: fields | — |
| GET | `{{instanceUrl}}/api/data/v1/streams/:id/executions` | path: id | — |
| GET | `{{instanceUrl}}/api/data/v1/streams/:streamId/executions/:executionId` | path: streamId, executionId | — |
| GET | `{{instanceUrl}}/api/data/v1/lineage/DATA_SOURCE/:id` | path: id; query: traverseUp, traverseDown, requestEntities, maxDepth | — |
| GET | `{{instanceUrl}}/api/data/v1/impacts/DATA_SOURCE/:id` | path: id | — |
| GET | `{{instanceUrl}}/api/query/v1/datasources/:id/schema/indexed` | path: id; query: includeHidden | — |
| GET | `{{instanceUrl}}/api/query/v1/datasources/:id/wrangle` | path: id | — |
| POST | `{{instanceUrl}}/api/query/v1/execute/:id` | path: id | SQL/query body |
| POST | `{{instanceUrl}}/api/query/v1/views/query-preview` | — | preview body |
| POST | `{{instanceUrl}}/api/data/v1/streams` | — | stream + dataset object |
| POST | `{{instanceUrl}}/api/query/v1/views` | — | view object |
| POST | `{{instanceUrl}}/api/data/v1/ui/bulk/tag` | — | bulk tag body |
| POST | `{{instanceUrl}}/api/data/v1/streams/:id/executions` | path: id | — |
| POST | `{{instanceUrl}}/api/data/ui/v3/datasources/:id/defrost` | path: id | — |
| POST | `{{instanceUrl}}/api/data/v3/datasources/:id/share` | path: id | share body |
| POST | `{{instanceUrl}}/api/iot/v1/webhook/data/:id` | path: id | — |
| POST | `{{instanceUrl}}/api/query/v1/datasources/:id/wrangle` | path: id | wrangle body |
| PUT | `{{instanceUrl}}/api/data/v1/streams/:id` | path: id | stream object |
| PUT | `{{instanceUrl}}/api/data/v3/datasources/:id/properties` | path: id | name/description object |
| PUT | `{{instanceUrl}}/api/data/v2/datasources/:id/responsibleUsers` | path: id | owner object |
| PUT | `{{instanceUrl}}/api/data/v2/datasources/responsible-user/:userId` | path: userId | dataset IDs |
| POST | `{{instanceUrl}}/api/data/v1/ui/bulk/reassign` | — | reassign body |
| POST | `{{instanceUrl}}/api/data/v1/ui/bulk/delete` | — | IDs array |
| POST | `{{instanceUrl}}/api/data/ui/v3/datasources/:id/tags` | path: id | tags array |
| PUT | `{{instanceUrl}}/api/query/v1/byos/accounts/:cloudId/polling/refresh` | path: cloudId | — |
| DELETE | `{{instanceUrl}}/api/data/v3/datasources/:id` | path: id; query: deleteMethod | — |
| POST | `{{instanceUrl}}/api/data/v1/ui/bulk/delete/check` | — | IDs array |
| PUT | `{{instanceUrl}}/api/data/v1/streams/:streamId/executions/:executionId` | path: streamId, executionId | abort body |

**AI Readiness / Data Dictionary**

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/ai/readiness/v1/data-dictionary/dataset/:id` | path: id | — |
| POST | `{{instanceUrl}}/api/ai/readiness/v1/data-dictionary/dataset/:datasetId` | path: datasetId | dictionary object |
| PUT | `{{instanceUrl}}/api/ai/readiness/v1/data-dictionary/dataset/:id` | path: id | dictionary object |

**Data Repair**

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/data/v3/datasources/:datasetId/dataversions/details` | path: datasetId | — |
| GET | `{{instanceUrl}}/api/data/v2/datasources/:datasetId/dataversions` | path: datasetId | — |
| GET | `{{instanceUrl}}/api/data/v2/datasources/:datasetId/dataversions/:versionId` | path: datasetId, versionId; query: excludeAppendedData, rowLimit | — |
| POST | `{{instanceUrl}}/api/data/v3/datasources/:datasetId/dataversions` | path: datasetId; query: repairDataVersionId, repairAction | — |
| DELETE | `{{instanceUrl}}/api/data/v2/datasources/:datasetId/dataversions` | path: datasetId | version IDs array |

**PDP (Row & Column)**

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/query/v2/data-control/:datasetId/policy-group` | path: datasetId | — |
| GET | `{{instanceUrl}}/api/query/v2/data-control/:datasetId/column-policy-mapping` | path: datasetId | — |
| POST | `{{instanceUrl}}/api/query/v2/data-control/:datasetId/policy-group` | path: datasetId | policy object |
| POST | `{{instanceUrl}}/api/query/v2/data-control/:datasetId/column-policy-mapping` | path: datasetId | mapping object |
| PUT | `{{instanceUrl}}/api/query/v2/data-control/:datasetId/policy-group/:policyId` | path: datasetId, policyId | policy object |
| PUT | `{{instanceUrl}}/api/query/v2/data-control/:datasetId/column-policy-mapping/:columnPdpPolicyMappingId` | path: datasetId, columnPdpPolicyMappingId | mapping object |
| DELETE | `{{instanceUrl}}/api/query/v2/data-control/:datasetId/policy-group/:policyId` | path: datasetId, policyId | — |
| DELETE | `{{instanceUrl}}/api/query/v2/data-control/:datasetId/column-policy-mapping/:columnPdpPolicyMappingId` | path: datasetId, columnPdpPolicyMappingId | — |
| GET | `{{instanceUrl}}/api/query/v1/data-control/:datasetId/filter-groups` | path: datasetId; query: options | — |
| POST | `{{instanceUrl}}/api/query/v1/data-control/:datasetId/filter-groups` | path: datasetId | policy object |
| PUT | `{{instanceUrl}}/api/query/v1/data-control/:datasetId/filter-groups/:policyId` | path: datasetId, policyId | policy object |
| DELETE | `{{instanceUrl}}/api/query/v1/data-control/:datasetId/filter-groups/:policyId` | path: datasetId, policyId | — |
| GET | `{{instanceUrl}}/api/query/v2/data-control/:datasetId` | path: datasetId | — |
| GET | `{{instanceUrl}}/api/data/v3/datasources/:datasetId/impacted-resources` | path: datasetId | — |
| PUT | `{{instanceUrl}}/api/query/v1/data-control/:datasetId` | path: datasetId | enable/disable body |

**Uploads (multi-part)**

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| POST | `{{instanceUrl}}/api/data/v3/datasources/:datasetId/uploads` | path: datasetId | upload metadata |
| PUT | `{{instanceUrl}}/api/data/v3/datasources/:datasetId/uploads/:uploadId/parts/:partNumber` | path: datasetId, uploadId, partNumber | CSV/data chunk |
| PUT | `{{instanceUrl}}/api/data/v3/datasources/:datasetId/uploads/:uploadId/commit` | path: datasetId, uploadId | commit options |

**Webforms**

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/data/v2/webforms/:datasetId/grid` | path: datasetId | — |
| PUT | `{{instanceUrl}}/api/data/v2/webforms/:streamId` | path: streamId | grid data |

---

### Domo Everywhere
*See `api-definitions-md/18-domo-everywhere.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/publish/v2/publications` | — | — |
| GET | `{{instanceUrl}}/api/publish/v2/publications/summaries` | query: public, limit, offset, searchTerm, sort | — |
| GET | `{{instanceUrl}}/api/publish/v2/publications/:id` | path: id | — |
| GET | `{{instanceUrl}}/api/publish/v2/publications/summaries/:publicationId` | path: publicationId | — |
| GET | `{{instanceUrl}}/api/publish/v2/publications/status` | — | — |
| GET | `{{instanceUrl}}/api/publish/v2/subscriptions/summaries` | query: searchTerm, limit, offset | — |
| GET | `{{instanceUrl}}/api/publish/v2/automatic-subscriptions` | — | — |
| GET | `{{instanceUrl}}/api/publish/v2/automatic-subscriptions/shares/v1` | — | — |
| GET | `{{instanceUrl}}/api/publish/v2/subscriptions/invites` | query: searchTerm, limit, offset | — |
| GET | `{{instanceUrl}}/api/publish/v2/subscriptions/summaries/counts` | query: searchTerm | — |
| GET | `{{instanceUrl}}/api/publish/v2/subscriptions/invites/counts` | query: searchTerm | — |
| GET | `{{instanceUrl}}/api/publish/v2/subscriptions/:subscriptionId/share` | path: subscriptionId | — |
| PUT | `{{instanceUrl}}/api/publish/v2/subscriptions/:subscriptionId` | path: subscriptionId | subscription object |

---

### Elevation
*See `api-definitions-md/19-elevation.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/customer/v1/properties/authentication.otp_elevation` | — | — |
| PUT | `{{instanceUrl}}/api/identity/v1/authentication/elevations/:userId` | path: userId | OTP body |
| PUT | `{{instanceUrl}}/api/customer/v1/properties/authentication.otp_elevation` | — | setting value |

---

### Files
*See `api-definitions-md/20-files.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/data/v1/data-files/:fileId/revisions/:revisionId` | path: fileId, revisionId; query: fileName | — |
| GET | `{{instanceUrl}}/api/data/v1/data-files/:fileId/revisions/:revisionId/details` | path: fileId, revisionId | — |
| GET | `{{instanceUrl}}/api/data/v1/data-files/:id/details` | path: id; query: expand | — |
| POST | `{{instanceUrl}}/api/data/v1/data-files` | query: name, public | file binary |
| POST | `{{instanceUrl}}/api/content/v1/cards` | query: pageId | card object |
| PUT | `{{instanceUrl}}/api/data/v1/data-files/:id` | path: id; query: public, description | file binary |
| PUT | `{{instanceUrl}}/api/content/v1/cards/:id` | path: id | card object |

---

### FileSets
*See `api-definitions-md/21-filesets.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| POST | `{{instanceUrl}}/api/files/v1/filesets/search` | query: limit, offset | search body |
| POST | `{{instanceUrl}}/api/files/v1/filesets/:filesetId/files/search` | path: filesetId; query: directoryPath, immediateChildren, limit, next | search body |
| POST | `{{instanceUrl}}/api/files/v1/filesets/:id/query` | path: id | AI query body |
| GET | `{{instanceUrl}}/api/files/v1/filesets/:id` | path: id | — |
| GET | `{{instanceUrl}}/api/files/v1/filesets/:filesetId/files/:fileId` | path: filesetId, fileId | — |
| GET | `{{instanceUrl}}/api/files/v1/filesets/:filesetId/path` | path: filesetId; query: path | — |
| GET | `{{instanceUrl}}/api/files/v1/filesets/:id/access` | path: id | — |
| GET | `{{instanceUrl}}/api/files/v1/filesets/:id/stats` | path: id | — |
| GET | `{{instanceUrl}}/api/files/v1/filesets/:filesetId/files/:fileId/download` | path: filesetId, fileId | — |
| GET | `{{instanceUrl}}/api/files/v1/filesets/:filesetId/path/download` | path: filesetId; query: path | — |
| POST | `{{instanceUrl}}/api/files/v1/filesets` | — | fileset object |
| POST | `{{instanceUrl}}/api/files/v1/filesets/:filesetId/files` | path: filesetId | folder object |
| POST | `{{instanceUrl}}/api/files/v1/filesets/:id/files` | path: id | file binary |
| POST | `{{instanceUrl}}/api/files/v1/filesets/:id` | path: id | fileset object |
| POST | `{{instanceUrl}}/api/files/v1/filesets/:id/access` | path: id | access object |
| POST | `{{instanceUrl}}/api/files/v1/filesets/:id/ownership` | path: id | owner object |
| DELETE | `{{instanceUrl}}/api/files/v1/filesets/:id` | path: id | — |
| DELETE | `{{instanceUrl}}/api/files/v1/filesets/:filesetId/files/:fileId` | path: filesetId, fileId | — |
| DELETE | `{{instanceUrl}}/api/files/v1/filesets/:filesetId/path` | path: filesetId; query: path | — |

---

### Forms
*See `api-definitions-md/22-forms.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| POST | `{{instanceUrl}}/api/search/v1/query` | — | search body |
| GET | `{{instanceUrl}}/api/forms/v1/:id` | path: id | — |
| POST | `{{instanceUrl}}/api/forms/v1/instances` | — | instance object |
| POST | `{{instanceUrl}}/api/forms/v1/instances/:id/submission` | path: id | submission object |
| PUT | `{{instanceUrl}}/api/forms/v1/instances/:id` | path: id | instance object |
| POST | `{{instanceUrl}}/api/forms/v1/:id/hydration` | path: id | fields object |

---

### Functions (Beast Modes & Variables)
*See `api-definitions-md/23-functions-beast-modes-and-variables-.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| POST | `{{instanceUrl}}/api/query/v1/functions/search` | — | search body |
| POST | `{{instanceUrl}}/api/query/v1/functions/list/id` | — | IDs array |
| GET | `{{instanceUrl}}/api/query/v1/functions/template/:id` | path: id; query: hidden | — |
| GET | `{{instanceUrl}}/api/content/v2/cards/formulausage` | query: datasourceId, formulaId | — |
| POST | `{{instanceUrl}}/api/query/v1/functions/template` | query: strict | function object |
| POST | `{{instanceUrl}}/api/query/v1/functions/bulk/template` | — | functions array |
| PUT | `{{instanceUrl}}/api/query/v1/functions/template/:id` | path: id; query: strict | function object |
| DELETE | `{{instanceUrl}}/api/query/v1/functions/template/:id` | path: id | — |

---

### Groups
*See `api-definitions-md/24-groups.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/content/v2/groups/grouplist` | query: ascending, sort, limit, offset, includeFullMembership, owner, ownerType, groupType, createdAfter, createdBefore, members, isManageable, search | — |
| POST | `{{instanceUrl}}/api/content/v2/groups/get` | query: includeActive, includeUsers | group IDs array |
| GET | `{{instanceUrl}}/api/content/v2/groups/:id` | path: id | — |
| GET | `{{instanceUrl}}/api/content/v2/groups/:id/permissions` | path: id; query: checkOwnership, includeUsers | — |
| GET | `{{instanceUrl}}/api/content/v1/avatar/GROUP/:id` | path: id; query: size, defaultBackground, defaultForeground, defaultText | — |
| POST | `{{instanceUrl}}/api/content/v2/groups` | — | group object |
| PUT | `{{instanceUrl}}/api/content/v2/groups/access` | — | access body |
| PUT | `{{instanceUrl}}/api/content/v2/groups` | — | dynamic rules object |
| DELETE | `{{instanceUrl}}/api/content/v2/groups/:id` | path: id | — |
| DELETE | `{{instanceUrl}}/api/content/v2/groups` | — | group IDs array |

---

### Left Navigation
*See `api-definitions-md/25-left-navigation.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/nav/v1/pins` | — | — |
| POST | `{{instanceUrl}}/api/nav/v1/pins/append` | — | pin object |

---

### Objectives (Goals)
*See `api-definitions-md/26-objectives-goals-.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/social/v1/objectives/search` | query: filterKeyResults, periodId, query | — |
| GET | `{{instanceUrl}}/api/social/v2/objectives/profile` | query: filterKeyResults, includeSampleGoal, ownerId, periodId, type | — |
| GET | `{{instanceUrl}}/api/social/v2/objectives/teams-profile` | query: filterKeyResults, ownerId, periodId | — |
| GET | `{{instanceUrl}}/api/social/v1/objectives/periods` | query: all | — |
| GET | `{{instanceUrl}}/api/social/v1/objectives/events` | — | — |
| GET | `{{instanceUrl}}/api/social/v1/objectives/tags` | query: all | — |
| GET | `{{instanceUrl}}/api/social/v1/objectives/tags/categories` | query: all | — |
| GET | `{{instanceUrl}}/api/social/v1/objectives/needs-update` | query: filterKeyResults, periodId, userId | — |
| GET | `{{instanceUrl}}/api/social/v2/objectives/draft` | query: filterKeyResults, periodId, userId | — |
| GET | `{{instanceUrl}}/api/social/v2/objectives/report` | query: filterKeyResults, periodId, type | — |
| GET | `{{instanceUrl}}/api/social/v1/objectives/key-results/:id/chart` | path: id | — |
| GET | `{{instanceUrl}}/api/social/v1/objectives/key-results/:id/values` | path: id | — |
| POST | `{{instanceUrl}}/api/social/v1/objectives` | — | objective object |
| POST | `{{instanceUrl}}/api/social/v1/objectives/key-results` | — | key result object |
| POST | `{{instanceUrl}}/api/social/v1/objectives/tags` | — | tag object |
| POST | `{{instanceUrl}}/api/social/v1/objectives/tags/categories` | — | category object |
| PUT | `{{instanceUrl}}/api/social/v1/objectives/:id` | path: id; query: periodId | objective object |
| PUT | `{{instanceUrl}}/api/social/v1/objectives/key-results/:id` | path: id | key result object |
| PUT | `{{instanceUrl}}/api/social/v1/objectives/key-results/:id/tags` | path: id; query: periodId | tags array |
| PUT | `{{instanceUrl}}/api/social/v1/objectives/tags/:id` | path: id | tag object |
| PUT | `{{instanceUrl}}/api/social/v1/objectives/tags/categories/:id` | path: id | category object |
| DELETE | `{{instanceUrl}}/api/social/v1/objectives/:id` | path: id | — |
| DELETE | `{{instanceUrl}}/api/social/v1/objectives/key-results/:id` | path: id | — |
| DELETE | `{{instanceUrl}}/api/social/v1/objectives/tags/:id` | path: id | — |
| DELETE | `{{instanceUrl}}/api/social/v1/objectives/tags/categories/:id` | path: id | — |

---

### Pages (Dashboards)
*See `api-definitions-md/27-pages-dashboards-.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| POST | `{{instanceUrl}}/api/content/v1/pages/adminsummary` | query: limit, skip | filter body |
| GET | `{{instanceUrl}}/api/content/v3/stacks/:id` | path: id; query: parts, includeV4PageLayouts, stackLoadContextId, stackLoadContext, stackLoadTrigger | — |
| GET | `{{instanceUrl}}/api/content/v3/stacks/:id/cards` | path: id; query: parts, includeV4PageLayouts | — |
| GET | `{{instanceUrl}}/api/content/v1/share/accesslist/page/:id` | path: id; query: filter, limit, expandUsers | — |
| GET | `{{instanceUrl}}/api/content/v2/pages/navigation` | query: includeStartPage, elevateSharedPage, includeHidden | — |
| POST | `{{instanceUrl}}/api/content/v1/pages` | — | page object |
| POST | `{{instanceUrl}}/api/content/v1/share` | query: sendEmail | share body |
| PUT | `{{instanceUrl}}/api/content/v1/pages/bulk/move` | — | move body |
| PUT | `{{instanceUrl}}/api/content/v1/pages/pageorder` | — | page order array |
| PUT | `{{instanceUrl}}/api/content/v1/pages/:id` | path: id | page object |
| PUT | `{{instanceUrl}}/api/content/v1/pages/:pageId/duplicate` | path: pageId; query: doNotDuplicateCards | duplicate options |
| PUT | `{{instanceUrl}}/api/content/v1/pages/:pageId/duplicateAsync` | path: pageId; query: doNotDuplicateCards | duplicate options |
| DELETE | `{{instanceUrl}}/api/content/v1/pages/:id` | path: id | — |
| DELETE | `{{instanceUrl}}/api/content/v1/share/bulk/page/:type/:id` | path: type, id; query: resourceIds | — |
| POST | `{{instanceUrl}}/api/content/v1/pages/bulk/owners/remove` | — | owners array |

**Layouts**

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/content/v4/pages/layouts/:layoutId` | path: layoutId | — |
| PUT | `{{instanceUrl}}/api/content/v4/pages/layouts/:layoutId/writelock` | path: layoutId | — |
| PUT | `{{instanceUrl}}/api/content/v4/pages/layouts/:layoutId` | path: layoutId | layout object |
| DELETE | `{{instanceUrl}}/api/content/v4/pages/layouts/:id/writelock` | path: id | — |

**Filter Views**

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/content/v3/pages/:pageId/analyzer/named` | path: pageId | — |
| PUT | `{{instanceUrl}}/api/content/v3/pages/:pageId/analyzer` | path: pageId | filter view object |
| DELETE | `{{instanceUrl}}/api/content/v3/pages/analyzer/:filterViewId` | path: filterViewId | — |

---

### Projects & Tasks
*See `api-definitions-md/28-projects-and-tasks.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/content/v1/projects` | query: limit, offset, status | — |
| GET | `{{instanceUrl}}/api/content/v1/tags` | query: q | — |
| GET | `{{instanceUrl}}/api/content/v2/users/:userId/projects` | path: userId; query: limit, offset, status | — |
| GET | `{{instanceUrl}}/api/content/v1/projects/:projectId/tasks` | path: projectId; query: search, archived, assignedToOwnerId | — |
| GET | `{{instanceUrl}}/api/content/v1/projects/:projectId/lists/:listId/tasks` | path: projectId, listId; query: fields | — |
| GET | `{{instanceUrl}}/api/content/v2/users/:userId/tasks/assignments` | path: userId; query: limit, offset, status | — |
| GET | `{{instanceUrl}}/api/content/v1/projects/:projectId/lists` | path: projectId; query: archived | — |
| GET | `{{instanceUrl}}/api/content/v1/projects/:projectId/tags` | path: projectId; query: archived | — |
| GET | `{{instanceUrl}}/api/content/v1/projects/:projectId` | path: projectId | — |
| GET | `{{instanceUrl}}/api/content/v1/tasks/:taskId` | path: taskId | — |
| POST | `{{instanceUrl}}/api/v1/projects` | — | project object |
| POST | `{{instanceUrl}}/api/content/v1/projects/:projectId/lists/:listId/tasks` | path: projectId, listId | task object |
| POST | `{{instanceUrl}}/api/content/v2/users/:userId/tasks` | path: userId | task object |
| POST | `{{instanceUrl}}/api/content/v1/projects/:projectId/lists` | path: projectId | list object |
| POST | `{{instanceUrl}}/api/content/v1/tasks/:taskId/attachments` | path: taskId | attachment object |
| PUT | `{{instanceUrl}}/api/content/v1/projects/:projectId` | path: projectId | project object |
| PUT | `{{instanceUrl}}/api/content/v1/tasks/:taskId` | path: taskId | task object |
| PUT | `{{instanceUrl}}/api/content/v1/projects/:projectId/lists/:listId` | path: projectId, listId | list object |
| DELETE | `{{instanceUrl}}/api/content/v1/projects/:projectId` | path: projectId | — |

---

### Reports (Slideshow Publications)
*See `api-definitions-md/29-reports-slideshow-publications-.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/content/v1/reports` | — | — |
| POST | `{{instanceUrl}}/api/content/v1/reports` | — | report object |
| PUT | `{{instanceUrl}}/api/content/v1/reports/:id` | path: id | report object |
| DELETE | `{{instanceUrl}}/api/content/v1/reports/:id` | path: id | — |

---

### Roles & Authorities (Grants)
*See `api-definitions-md/30-roles-and-authorities-grants-.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/authorization/v1/roles` | — | — |
| GET | `{{instanceUrl}}/api/authorization/v1/authorities` | — | — |
| GET | `{{instanceUrl}}/api/content/v1/typeahead` | query: authorities, limit, type, filter, fields | — |
| GET | `{{instanceUrl}}/api/authorization/v1/roles/:id` | path: id | — |
| GET | `{{instanceUrl}}/api/authorization/v1/roles/:id/authorities` | path: id | — |

---

### Sandbox
*See `api-definitions-md/31-sandbox.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| POST | `{{instanceUrl}}/api/version/v1/repositories/search` | — | search body |
| POST | `{{instanceUrl}}/api/version/v1/promotions/search` | — | search body |
| POST | `{{instanceUrl}}/api/version/v1/commitRequests/search` | — | search body |
| GET | `{{instanceUrl}}/api/version/v1/authorizations` | query: limit | — |
| GET | `{{instanceUrl}}/api/version/v1/repositories/:repositoryId` | path: repositoryId | — |
| GET | `{{instanceUrl}}/api/version/v1/repositories/:repositoryId/commits` | path: repositoryId | — |
| GET | `{{instanceUrl}}/api/version/v1/repositories/:repositoryId/commitRequests` | path: repositoryId | — |
| GET | `{{instanceUrl}}/api/version/v1/repositories/:repositoryId/permissions` | path: repositoryId | — |
| GET | `{{instanceUrl}}/api/version/v1/repositories/:repositoryId/access` | path: repositoryId | — |
| GET | `{{instanceUrl}}/api/version/v1/settings` | — | — |
| POST | `{{instanceUrl}}/api/version/v1/repositories/:repositoryId/deployments/:deploymentId/promoteAndSeed` | path: repositoryId, deploymentId | promote body |
| POST | `{{instanceUrl}}/api/version/v1/repositories/:repositoryId/commitRequests` | path: repositoryId | commit body |
| POST | `{{instanceUrl}}/api/version/v1/repositories/:repositoryId/permissions` | path: repositoryId | permissions body |
| POST | `{{instanceUrl}}/api/version/v1/authorizations/aliases` | — | alias body |

---

### Scheduled Reports
*See `api-definitions-md/32-scheduled-reports.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/content/v1/reportschedules` | query: filter, isAscending, orderBy | — |
| GET | `{{instanceUrl}}/api/content/v1/reportschedules/resources` | query: limit, skip | — |
| GET | `{{instanceUrl}}/api/content/v1/reportschedules/:id` | path: id | — |
| GET | `{{instanceUrl}}/api/content/v1/reportschedules/:id/history` | path: id; query: limit, skip | — |
| GET | `{{instanceUrl}}/api/content/v1/reportschedules/resources/:resourceType/:resourceId` | path: resourceType, resourceId; query: skip, limit, showAll | — |
| GET | `{{instanceUrl}}/api/content/v2/views/:id` | path: id | — |
| POST | `{{instanceUrl}}/api/content/v1/reportschedules/history/search` | query: limit, skip | search body |
| POST | `{{instanceUrl}}/api/content/v1/reportschedules/:id/sendnow` | path: id | send body |
| POST | `{{instanceUrl}}/api/content/v1/reportschedules` | — | schedule object |
| POST | `{{instanceUrl}}/api/content/v2/views` | — | view object |
| PUT | `{{instanceUrl}}/api/content/v1/reportschedules/:id` | path: id | schedule object |
| PUT | `{{instanceUrl}}/api/content/v1/reportschedules/:id/enabled` | path: id | enabled flag |
| PUT | `{{instanceUrl}}/api/content/v2/views/:id` | path: id | view object |
| DELETE | `{{instanceUrl}}/api/content/v1/reportschedules/:id` | path: id | — |
| DELETE | `{{instanceUrl}}/api/content/v1/reportschedules/:id/unsubscribe/recipient` | path: id | — |
| POST | `{{instanceUrl}}/api/content/v1/reportschedules/:id/unsubscribe` | path: id | — |

---

### Task Center
*See `api-definitions-md/33-task-center.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/queues/v1` | query: combineAttributes, archived | — |
| POST | `{{instanceUrl}}/api/search/v1/query` | — | search body |
| POST | `{{instanceUrl}}/api/queues/v1/tasks/list` | query: limit, offset, render, renderParts, direction, orderBy | filter body |
| GET | `{{instanceUrl}}/api/queues/v1/:queueId` | path: queueId | — |
| GET | `{{instanceUrl}}/api/queues/v1/:queueId/tasks/:taskId` | path: queueId, taskId; query: render | — |
| PUT | `{{instanceUrl}}/api/queues/v1/:queueId/tasks/:taskId/outputs` | path: queueId, taskId | outputs object |
| POST | `{{instanceUrl}}/api/queues/v1/:queueId/tasks/:taskId/complete` | path: queueId, taskId; query: version | completion body |
| PUT | `{{instanceUrl}}/api/queues/v1/:currentQueueId/tasks/:taskId/move` | path: currentQueueId, taskId; query: targetQueueId | — |
| PUT | `{{instanceUrl}}/api/queues/v1/:queueId/tasks/:taskId/assign` | path: queueId, taskId | assignee body |
| POST | `{{instanceUrl}}/api/queues/v1/:queueId/tasks/:taskId/void` | path: queueId, taskId | — |
| POST | `{{instanceUrl}}/api/queues/v1/:queueId/tasks` | path: queueId | task object |
| POST | `{{instanceUrl}}/api/queues/v1/:queueId/permissions` | path: queueId | permissions object |
| PUT | `{{instanceUrl}}/api/queues/v1/:queueId/owner/:ownerId` | path: queueId, ownerId | — |

---

### Toolkit
*See `api-definitions-md/34-toolkit.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| GET | `{{instanceUrl}}/api/executor/v1/applications` | — | — |
| GET | `{{instanceUrl}}/api/executor/v2/applications/:applicationId/jobs` | path: applicationId; query: limit, offset | — |
| GET | `{{instanceUrl}}/api/executor/v1/applications/:applicationId/jobs/:jobId` | path: applicationId, jobId | — |
| POST | `{{instanceUrl}}/api/executor/v1/applications/:applicationId/jobs/:jobId/executions` | path: applicationId, jobId | execution body |
| PUT | `{{instanceUrl}}/api/executor/v1/applications/:applicationId/jobs/:jobId/share` | path: applicationId, jobId | share body |
| POST | `{{instanceUrl}}/api/executor/v1/applications/:appId/jobs/:jobId/triggers` | path: appId, jobId | trigger object |
| PUT | `{{instanceUrl}}/api/executor/v1/applications/:appId/jobs/:jobId` | path: appId, jobId | job object |
| DELETE | `{{instanceUrl}}/api/executor/v1/applications/:appId/jobs/:jobId` | path: appId, jobId | — |

---

### Users
*See `api-definitions-md/35-users.md`*

| Method | Endpoint | Params | Body |
|--------|----------|--------|------|
| POST | `{{instanceUrl}}/api/identity/v1/users/search` | query: explain, cacheBuster | search body |
| GET | `{{instanceUrl}}/api/identity/v1/users/` | query: limit, offset, attributes | — |
| GET | `{{instanceUrl}}/api/content/v3/users/` | query: limit, offset, active | — |
| GET | `{{instanceUrl}}/api/users/index` | query: cvUserIds | — |
| GET | `{{instanceUrl}}/api/identity/v1/users/:id` | path: id; query: attributes, parts | — |
| GET | `{{instanceUrl}}/api/content/v2/users/:id` | path: id | — |
| GET | `{{instanceUrl}}/api/content/v3/users/:id` | path: id | — |
| GET | `{{instanceUrl}}/api/content/v2/users/attributeTypeahead/EMPLOYEELOCATION` | query: limit, offset, search | — |
| GET | `{{instanceUrl}}/api/content/v2/users/:id/state` | path: id; query: keys | — |
| POST | `{{instanceUrl}}/api/content/v3/users` | query: sendInvite | user object |
| PATCH | `{{instanceUrl}}/api/identity/v1/users/:id` | path: id | partial user object |
| PUT | `{{instanceUrl}}/api/content/v3/users` | — | user object |
| PUT | `{{instanceUrl}}/api/content/v2/users/bulk` | — | users array |
| POST | `{{instanceUrl}}/api/content/v1/avatar/bulk` | — | avatars array |
| PUT | `{{instanceUrl}}/api/content/v1/landings/target/:type/entity/PAGE/id/:pageId/:userId` | path: type, pageId, userId | — |
| DELETE | `{{instanceUrl}}/api/identity/v1/users/:id` | path: id | — |

---

## Response Shapes

Response schemas are not formally documented in the source API definitions. In general:

- **List endpoints** return a JSON array or a paginated object with a `data`/`results` array.
- **Get endpoints** return a JSON object.
- **Create/Update endpoints** return the created/updated object.
- **Delete endpoints** return `204 No Content` or an empty body.
- **GraphQL endpoints** (`/api/synapse/approval/graphql`) return `{ "data": { ... } }`.
- **Search endpoints** (`/api/search/v1/query`) return `{ "hits": [...], "total": N }`.

Actual field names should be inferred from the request body examples in `api-definitions-md/` or discovered empirically.

---

## Environment Variables

```env
DOMO_INSTANCE_URL=https://yourcompany.domo.com
DOMO_DEVELOPER_TOKEN=your_developer_token_here
```
