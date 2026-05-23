# Admin

## Access Tokens

### List Access Tokens
`GET {{instanceUrl}}/api/data/v1/accesstokens`

### Delete/Revoke Access Token
`DELETE {{instanceUrl}}/api/data/v1/accesstokens/:id`
- Path: `:id`

## Activity Log

### List Object Types
`GET {{instanceUrl}}/api/audit/v1/user-audits/objectTypes`

### Get Events
`GET {{instanceUrl}}/api/audit/v1/user-audits`
- Query: `start`, `end`, `offset`, `limit`, `objectType`

## Company

### List Customer Stats
`GET {{instanceUrl}}/api/query/v1/datasources/customer-stats`

### List Time Zones
`GET {{instanceUrl}}/api/dataprocessing/v1/dataflows/timezones`

### Get Settings
`GET {{instanceUrl}}/api/companysettings`

### Get Locale
`GET {{instanceUrl}}/api/content/v1/customer-states/locale`
- Query: `ignoreCache`

### Get Customer State
`GET {{instanceUrl}}/api/content/v1/customer-states/:customerState`
- Path: `:customerState`
- Query: `ignoreCache`

### Get Customer States
`GET {{instanceUrl}}/api/content/v1/customer-states`
- Query: `ignoreCache`, `stateName`, `stateName`

### Get Property
`GET {{instanceUrl}}/api/customer/v1/properties/:property`
- Path: `:property`

### Get Licenses
`GET {{instanceUrl}}/api/content/v1/licenses/total/current`

### Get Jupyter Settings
`GET {{instanceUrl}}/api/datascience/v1/settings`

### Get Credits
`GET {{instanceUrl}}/api/metrics/v1/usage/credits/contract/current/summary`

### Get Default Landing Page
`GET {{instanceUrl}}/api/content/v1/landings/customer`

### Update Customer State
`PUT {{instanceUrl}}/api/content/v1/customer-states/:customerState`
- Path: `:customerState`
- Body: `{"name":"domo.policy.multifactor.maxCodeAttempts","value":"5"}`

### Update Property
`PUT {{instanceUrl}}/api/customer/v1/properties/:property`
- Path: `:property`
- Body: `{"keyspace":"domo","issuer":"DEFAULT_VALUE","entityId":"<string>","key":"card.hide_share_email_ui","value":"true","values":["true"]}`

## OAuth API Clients

### List OAuth API Clients
`GET {{instanceUrl}}/api/identity/v1/developer-tokens`

## Session Management

### List Sessions
`GET {{instanceUrl}}/api/sessions/v1/admin`
- Query: `limit`

### Delete Session
`DELETE {{instanceUrl}}/api/sessions/v1/admin/:id`
- Path: `:id`
