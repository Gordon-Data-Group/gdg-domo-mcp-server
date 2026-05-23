# AI/Data Science

## AutoML

### List Models on DataSet
`GET {{instanceUrl}}/api/dataprocessing/v1/ml/:datasetId/automl/job`
- Path: `:datasetId`
- Query: `includeDetails`

### Get Model
`GET {{instanceUrl}}/api/dataprocessing/v1/ml/:datasetId/automl/job/:modelId`
- Path: `:datasetId`, `:modelId`
- Query: `includeCandidates`

### Get Model Schema
`GET {{instanceUrl}}/api/dataprocessing/v1/ml/automl/job/:modelId/schema`
- Path: `:modelId`

### Explain Model
`GET {{instanceUrl}}/api/dataprocessing/v1/ml/automl/job/:modelId/explain`
- Path: `:modelId`

### Add Model to DataSet
`POST {{instanceUrl}}/api/dataprocessing/v1/ml/:id/model`
- Path: `:id`
- Body: `{"automlJobId":123,"candidateName":"<string>","displayName":"<string>"}`

## AI Models and Projects (User Generated)/Models

### List/Search Models
`POST {{instanceUrl}}/api/datascience/ml/v1/search/models`
- Body:
  ```json
  {
    "limit": 50,
    "sortFieldMap": {
      "CREATED": "DESC"
    },
    "searchFieldMap": {
      "NAME": ""
    },
    "filters": [
      {
        "type": "OWNER",
        "values": [
          1234
        ]
      },
      {
        "type": "ML_PROJECT_ID",
        "values": [
          "00000000-0000-0000-0000-000000000000"
        ]
      }
    ],
    "metricFilters": {},
    "dateFilters": {
      "CREATED": {
        "startDate": "2025-01-01T12:00:00Z",
        "endDate": null,
        "not": false
      }
    },
    "sortMetricMap": {}
  }
  ```

### Get Model
`GET {{instanceUrl}}/api/datascience/ml/v1/models/:id`
- Path: `:id`

### Update Model
`PUT {{instanceUrl}}/api/datascience/ml/v1/models/:id`
- Path: `:id`
- Body:
  ```json
  {
    "type": "AUTOML",
    "id": "00000000-0000-0000-0000-000000000000",
    "projectIds": [
      "00000000-0000-0000-0000-000000000000"
    ],
    "name": "<string>",
    "description": "<string>",
    "owner": "123456",
    "tasks": [
      {
        "task": "REGRESSION",
        "input": {
          "schema": {
            "dataSourceId": "<dataset_id>",
            "dataSourceName": "schema",
            "columns": [
              {
                "name": "Date Column",
                "type": "DATE"
              },
              {
                "name": "String Column",
                "type": "STRING"
              }
            ]
          },
          "type": "CSV",
          "mediaType": "text/csv"
        },
        "output": {
          "schema": {
            "dataSourceId": "<dataset_id>",
            "dataSourceName": "<string>",
            "columns": [
              {
                "name": "predicted_label",
                "type": "DOUBLE"
              }
            ]
          },
          "type": "CSV",
          "mediaType": "text/csv"
        }
      }
    ],
    "executionTypes": [
      "DATAFLOW",
      "ENDPOINT"
    ],
    "training": {
      "metrics": {
        "train:mae": {
          "name": "train:mae",
          "value": 123,
          "standardDeviation": null,
          "timestamp": "2025-02-05T00:59:05Z"
        },
        "train:mse": {
          "name": "train:mse",
          "value": 123,
          "standardDeviation": null,
          "timestamp": "2025-02-05T00:59:05Z"
        },
        "train:rmse": {
          "name": "train:rmse",
          "value": 123,
          "standardDeviation": null,
          "timestamp": "2025-02-05T00:59:05Z"
        },
        "validation:r2": {
          "name": "validation:r2",
          "value": 123,
          "standardDeviation": null,
          "timestamp": "2025-02-05T00:59:05Z"
        },
        "validation:mae": {
          "name": "validation:mae",
          "value": 123,
          "standardDeviation": null,
          "timestamp": "2025-02-05T00:59:05Z"
        },
        "validation:mse": {
          "name": "validation:mse",
          "value": 123,
          "standardDeviation": null,
          "timestamp": "2025-02-05T00:59:05Z"
        },
        "ObjectiveMetric": {
          "name": "ObjectiveMetric",
          "value": 123,
          "standardDeviation": null,
          "timestamp": "2025-02-05T00:59:05Z"
        },
        "validation:rmse": {
          "name": "validation:rmse",
          "value": 123,
          "standardDeviation": null,
          "timestamp": "2025-02-05T00:59:05Z"
        }
      },
      "hyperparameters": {
        "eta": "<decimal>",
        "alpha": "<decimal>",
        "gamma": "<decimal>",
        "lambda": "<decimal>",
        "max_depth": "<integer>",
        "num_round": "<integer>",
        "objective": "reg:squarederror",
        "subsample": "1.0",
        "eval_metric": "mse,mae,rmse,r2",
        "colsample_bytree": "<decimal>",
        "min_child_weight": "<decimal>",
        "_tuning_objective_metric": "validation:mse",
        "save_model_on_termination": "true"
      },
      "algorithm": "XGBoost"
    },
    "created": "2025-02-05T20:13:32.776643Z",
    "updated": "2025-02-05T20:13:32.776643Z",
    "autoMLModelContext": {
      "dataSourceId": "00000000-0000-0000-0000-000000000000",
      "autoMLJobId": 123,
      "automlModelId": 123,
      "targetColumn": "<column_name>"
    },
    "endpointStatus": "UNKNOWN",
    "permissionLevel": "ADMIN"
  }
  ```

### Update Owner
`POST {{instanceUrl}}/api/datascience/ml/v1/models/:id/ownership`
- Path: `:id`
- Body: `{"userId":1234}`

### Delete Model
`DELETE {{instanceUrl}}/api/datascience/ml/v1/models/:modelId`
- Path: `:modelId`

## AI Models and Projects (User Generated)/Projects

### List/Search Projects
`POST {{instanceUrl}}/api/datascience/ml/v1/search/projects`
- Body:
  ```json
  {
    "limit": 50,
    "sortFieldMap": {
      "CREATED": "DESC"
    },
    "searchFieldMap": {
      "NAME": ""
    },
    "filters": [
      {
        "type": "TYPE",
        "values": [
          "JUPYTER"
        ]
      },
      {
        "type": "OWNER",
        "values": [
          "1234"
        ]
      }
    ],
    "dateFilters": {
      "CREATED": {
        "startDate": "2025-01-01T12:00:00Z",
        "endDate": null,
        "not": false
      }
    }
  }
  ```

### List/Search Associated AutoML Models
`POST {{instanceUrl}}/api/datascience/ml/v1/search/models`
- Body:
  ```json
  {
    "limit": 50,
    "sortFieldMap": {
      "CREATED": "DESC"
    },
    "searchFieldMap": {
      "NAME": ""
    },
    "filters": [
      {
        "type": "ML_PROJECT_ID",
        "values": [
          "00000000-0000-0000-0000-000000000000"
        ]
      }
    ],
    "metricFilters": {},
    "dateFilters": {},
    "sortMetricMap": {}
  }
  ```

### Get Project
`GET {{instanceUrl}}/api/datascience/ml/v1/projects/:projectId`
- Path: `:projectId`

### Update Project
`PUT {{instanceUrl}}/api/datascience/ml/v1/projects/:id`
- Path: `:id`
- Body:
  ```json
  {
    "type": "CUSTOM",
    "id": "00000000-0000-0000-0000-000000000000",
    "name": "<string>",
    "description": "<string>",
    "owner": "1234",
    "created": "2025-01-01T12:00:00Z",
    "updated": "2025-01-01T12:00:00Z",
    "modelCount": 0,
    "autoMLProjectContext": {
      "dataSourceId": "11111111-1111-1111-1111-111111111111",
      "targetColumn": "<string>"
    },
    "permissionLevel": null,
    "customProjectContext": {}
  }
  ```

### Update Owner
`POST {{instanceUrl}}/api/datascience/ml/v1/projects/:id/ownership`
- Path: `:id`
- Body: `{"userId":1234}`

### Delete Project
`DELETE {{instanceUrl}}/api/datascience/ml/v1/projects/:id`
- Path: `:id`

## AI Service Layer/Text to SQL

### List Models
`GET {{instanceUrl}}/api/ai/v1/settings/services/sql/models`

### Get Default Model
`GET {{instanceUrl}}/api/ai/v1/settings/services/sql/models/default`

### Run Model
`POST {{instanceUrl}}/api/ai/v1/text/sql`
- Body:
  ```json
  {
    "input": "<query>",
    "system": "You are a SQL database expert that generates SQL queries for data visualization purposes. Your goal is to provide the most accurate and efficient solution to the problem at hand.\n\nPlease adhere to the following guidelines and restrictions:\n\n1. Always use column aliases <if var=\"locale\">(in ${locale})</if> for aggregations, calculations, and functions.<if var=\"disallowsList\">\n\n2. The following types of statements are not allowed: </if><if var=\"disallowCommonTableExpressions\">\n - Common Table Expressions, also known as WITH queries.</if><if var=\"disallowJoins\">\n - Joins</if><if var=\"disallowSubqueries\"> (except for Calendar() joins)\n - Subqueries</if><if var=\"disallowUnions\">\n - Unions</if><if var=\"disallowCorrelatedSubqueries\">\n\n3. Never use a correlated subquery, as this can negatively impact SQL query performance. Use an alternative method to achieve the solution, like using joins or window functions.</if>\n\n4. Include only the columns necessary to clearly answer your question, keeping the chart visually appealing by avoiding excessive series or data elements.\n\n<if var=\"max_columns\">5. It is critical that the number of select items in the provided sql query is between ${min_columns} and ${max_columns}. Do not use any more columns than absolutely necessary to answer the question.</if>\nDo not add any labels, comments, or brackets to the SQL query.\nOutput the answer in <SQL></SQL> XML tags. Skip any preamble.\n<if var=\"fiscalYear\">${fiscalYear}</if>\n<if var=\"locale\">The user's locale is ${locale}. Query aliases should be in ${locale}.</if>\n",
    "promptTemplate": {
      "template": "<if var=\"today\">\n  <current_date>Today's date is: ${today}</current_date>\n  Use today's date for calculating relative time frames such as \"the past thirty days\" or \"last year,\" if specified.\n  Otherwise, do not make assumptions about dates unless additional date-related instructions are given.\n</if>\n<if var=\"sql_examples\">\n  <examples>\n  ${sql_examples}\n  </examples>\n</if>\n${commentToken} ${dialect}\n${dataSourceSchemas}\n${commentToken} Generate a query to answer the following:\n${commentToken} ${input}\n"
    },
    "model": "domo.domo_ai.domogpt-sql-v1.1:anthropic",
    "dataSourceSchemas": [
      {
        "dataSourceName": "<string>",
        "columns": [
          {
            "name": "Date Column",
            "type": "DATE"
          },
          {
            "name": "String Column",
            "type": "STRING"
          }
        ]
      }
    ]
  }
  ```

## AI Service Layer/Text Generation

### List Models
`GET {{instanceUrl}}/api/ai/v1/settings/services/generation/models`

### Get Default Model
`GET {{instanceUrl}}/api/ai/v1/settings/services/generation/models/default`

### Run Model
`POST {{instanceUrl}}/api/ai/v1/text/generation`
- Body: `{"input":"<query>","promptTemplate":{"template":"${input}"},"model":"domo.domo_ai.domogpt-chat-medium-v1.1:anthropic"}`

## AI Service Layer/Text to Beast Mode

### List Models
`GET {{instanceUrl}}/api/ai/v1/settings/services/beastmode/models`

### Get Default Model
`GET {{instanceUrl}}/api/ai/v1/settings/services/beastmode/models/default`

### Run Model
`POST {{instanceUrl}}/api/ai/v1/text/beastmode`
- Body:
  ```json
  {
    "input": "<query>",
    "system": "You are a SQL database expert that generates SQL queries. Your goal is to create a SQL statement that includes a calculation to address the request.\nYou should follow the guidelines below:\n\nThese are only partial queries, meant to be used in a situation with existing context about the table and available columns. As such, do not include a SELECT keywork or a FROM clause. Also, do not us AS to rename the calculation.\n\nInstead of filtering data using a WHERE clause, use a CASE statement.\n\nDon't worry about processing any NULL values.\n\nIf asked for something \"fixed\", follow the documentation found here: https://domo-support.domo.com/s/article/4408174643607?language=en_US\n\nOutput the answer in <SQL></SQL> XML tags. Skip any preamble.\n",
    "promptTemplate": {
      "template": "# SQL\n# ${dataSourceSchema}\n# Generate a query to answer the following:\n# ${input}"
    },
    "model": "domo.domo_ai.domogpt-sql-v1.1:anthropic",
    "dataSourceSchema": {
      "dataSourceName": "<string>",
      "columns": [
        {
          "name": "Date Column",
          "type": "DATE"
        },
        {
          "name": "String Column",
          "type": "STRING"
        }
      ]
    }
  }
  ```

## AI Service Layer/Text Summarization

### List Models
`GET {{instanceUrl}}/api/ai/v1/settings/services/summarization/models`

### Get Default Model
`GET {{instanceUrl}}/api/ai/v1/settings/services/summarization/models/default`

### Run Model
`POST {{instanceUrl}}/api/ai/v1/text/summarize`
- Body:
  ```json
  {
    "input": "The old lighthouse keeper, Silas, squinted at the churning sea.  The storm, which had begun as a mere grumble on the horizon, had escalated into a furious beast, whipping the waves into a frenzy and clawing at the rocky cliffs.  He'd seen countless storms in his seventy years, more than half of which had been spent tending this lonely beacon, but this one felt different.  There was a malevolence in the wind, a raw, untamed power that made the hairs on his neck stand on end.\n\nHe adjusted the wick of the lamp, the flame flickering nervously in the draft that whistled through the tower's narrow windows.  The rhythmic pulse of the light, a constant reassurance to ships navigating the treacherous coastline, was his responsibility, his sacred duty.  He knew that somewhere out there, sailors were relying on that beam, trusting it to guide them through the tempest's dark embrace.\n\nSilas remembered his grandfather, a seasoned sailor himself, telling him stories of ships lost at sea, swallowed by the unforgiving waves.  He'd recounted tales of heroic rescues and heartbreaking tragedies, of the sea's capricious nature, capable of both breathtaking beauty and devastating cruelty.  These stories had instilled in Silas a deep respect for the ocean, a healthy fear mingled with an undeniable fascination.\n\nHe climbed the winding stairs to the lantern room, the wind howling like a banshee outside.  The glass panes rattled in their frames, threatened by the relentless onslaught of the storm.  He checked the lens, a magnificent Fresnel lens, painstakingly crafted to amplify the light's intensity, ensuring its visibility for miles across the turbulent waters.  It was a marvel of engineering, a testament to human ingenuity in the face of nature's might.\n\nLooking out at the tempestuous sea, Silas felt a pang of loneliness.  His wife, Martha, had passed away five years ago, leaving him with only the company of the gulls and the relentless rhythm of the waves.  He missed her dearly, her warm smile and gentle voice a distant memory, a comforting echo in the silence of the lighthouse.\n\nHe thought of the young couple he'd seen earlier that day, picnicking on the beach below, oblivious to the approaching storm.  They were so full of life, so carefree, their laughter carried on the wind.  He hoped they'd found shelter, that they were safe from the storm's fury.\n\nAs the night deepened, the storm intensified.  The waves crashed against the rocks with renewed vigor, sending plumes of spray high into the air, drenching the lighthouse in a salty mist.  Silas remained vigilant, his eyes fixed on the sea, his ears attuned to the sounds of the storm.  He knew that his duty was to keep the light burning, to be a beacon of hope in the darkness.\n\nHe brewed a pot of strong tea, the warmth spreading through his chilled bones.  He sipped it slowly, savoring the familiar taste, a small comfort in the midst of the chaos.  He thought about Martha, about her love for the sea, her understanding of his devotion to the lighthouse.  He imagined her beside him, her hand resting on his shoulder, offering silent support.\n\nThe storm raged on, its fury unabated.  But Silas remained steadfast, his resolve unwavering.  He was the keeper of the light, the guardian of the coast, and he would not abandon his post, not even in the face of the most fearsome storm.  He knew that the lives of sailors depended on him, on the unwavering beam of light that pierced the darkness, guiding them safely through the treacherous waters.  And as long as he had breath in his body, he would keep that light burning, a symbol of hope in the heart of the storm.  The lighthouse, a solitary sentinel against the raging sea, stood firm, its light a beacon of hope in the vast, dark expanse.\n",
    "system": "You are a helpful assistant that writes concise summaries.\n",
    "promptTemplate": {
      "template": "Write a ${outputWordLength} summary of the following text ${outputStyle}. ```${input}``` CONCISE SUMMARY:"
    },
    "model": "domo.domo_ai.domogpt-summarize-v1:anthropic"
  }
  ```

## AI Service Layer/Forecasting

### List Models
`GET {{instanceUrl}}/api/ai/v1/settings/services/forecasting/models`

### Get Default Model
`GET {{instanceUrl}}/api/ai/v1/settings/services/forecasting/models/default`

### Run Model
`POST {{instanceUrl}}/api/query/v1/execute/:datasetId`
- Path: `:datasetId`
- Body: `{"sql":"SELECT DATE_FORMAT(`Date` ,'%Y-%m')  as \"Date\", Sum(`Column`) as \"Alias\" FROM `<dataset_id>` group by DATE_FORMAT(`Date` ,'%Y-%m')  order by `Date` ASC"}`

## AI Service Layer/Image to Text

### List Models
`GET {{instanceUrl}}/api/ai/v1/settings/services/image/models`

### Get Default Model
`GET {{instanceUrl}}/api/ai/v1/settings/services/image/models/default`

### Run Model
`POST {{instanceUrl}}/api/ai/v1/image/text`
- Body:
  ```json
  {
    "input": "<instructions>",
    "system": "You are an AI assistant tasked with performing Optical Character Recognition (OCR) on an image. Your goal is to accurately identify and transcribe any text present in the image by analyzing the image carefully and extract all visible text.\n\nFollow these steps to perform OCR on the image\n\n1. Examine the entire image thoroughly, paying attention to all areas where text might be present.\n2. Identify any visible text, including numbers, letters, symbols, and punctuation marks.\n3. Transcribe the text exactly as it appears in the image, maintaining the original spelling, capitalization, and punctuation.\n4. If the text is arranged in multiple lines or paragraphs, preserve this structure in your transcription.\n\nRemember, your task is to transcribe the text as accurately as possible without interpreting or summarizing its content. Focus solely on the text visible in the image.\n\nBefore responding think about your response step by step. Provide your final transcription within <answer> tags. For example\n<example>\n<answer>\nHello World\n</answer>\n</example>\n",
    "promptTemplate": {
      "template": "${input}"
    },
    "model": "domo.domo_ai.domogpt-chat-medium-v1.1:anthropic",
    "image": {
      "mediaType": "image/png",
      "type": "base64",
      "data": "<base64>"
    }
  }
  ```

## AI Service Layer

### Get Settings
`GET {{instanceUrl}}/api/ai/v1/settings/general`

### Get Session
`GET {{instanceUrl}}/api/ai/v1/sessions/:sessionId`
- Path: `:sessionId`

### Get Session Context
`GET {{instanceUrl}}/api/ai/v1/sessions/:sessionId/context`
- Path: `:sessionId`

### Ask Chat
`POST {{instanceUrl}}/api/ai/v1/assistant/toolkits/DOMO_BASIC_ASSISTANT/execute/streaming`
- Body:
  ```json
  {
    "input": "<query>",
    "sessionId": "00000000-0000-0000-0000-000000000000",
    "aiAssistantContext": {
      "dataSourceIds": [
        "00000000-0000-0000-0000-000000000000"
      ],
      "cardIds": [],
      "pageIds": [],
      "filters": [],
      "ignorableDataSourceIds": []
    },
    "agentType": "REACT"
  }
  ```

## Jupyter Workspaces/File Shares

### List File Shares
`GET {{instanceUrl}}/api/fileshare/v1/shares`

### Get File Share Permissions
`GET {{instanceUrl}}/api/fileshare/v1/shares/:id/permissions`
- Path: `:id`

### Create File Share
`POST {{instanceUrl}}/api/fileshare/v1/shares`
- Body: `{"name":"<string>","description":"<string>","defaultMountPoint":"<string>"}`

### Update File Share
`PUT {{instanceUrl}}/api/fileshare/v1/shares/:id`
- Path: `:id`
- Body: `{"name":"<string>","description":"<string>","defaultMountPoint":"<string>","fileshareType":"SHARED","lifecycleOwner":"1234","lifecycleOwnerType":"USER","permissionLevel":null}`

### Update File Share Permissions
`POST {{instanceUrl}}/api/fileshare/v1/shares/:id/permissions`
- Path: `:id`
- Body: `{"share":[{"entityId":1234,"permissionLevel":"ADMIN","entityType":"USER"}],"unshare":[{"entityId":2345,"entityType":"USER"}]}`

### Delete File Share
`DELETE {{instanceUrl}}/api/fileshare/v1/shares/:id`
- Path: `:id`

## Jupyter Workspaces

### List Jupyter Workspaces
`POST {{instanceUrl}}/api/datascience/v1/search/workspaces`
- Body: `{"filters":[{"type":"OWNER","values":[1234]}],"limit":50,"offset":0,"sortFieldMap":{"LAST_RUN":"DESC"},"searchFieldMap":{}}`

### List User AI Models
`POST {{instanceUrl}}/api/datascience/ml/v1/search/models`
- Body: `{"limit":50,"sortFieldMap":{"METRIC":"DESC"},"searchFieldMap":{"NAME":""},"filters":[{"type":"METRIC","values":[]}],"metricFilters":{},"dateFilters":{},"sortMetricMap":{"ObjectiveMetric":"DESC"}}`

### Get Jupyter Workspace
`GET {{instanceUrl}}/api/datascience/v1/workspaces/:id`
- Path: `:id`

### Update Owner
`PUT {{instanceUrl}}/api/datascience/v1/workspaces/:id/ownership`
- Path: `:id`
- Body: `{"newOwnerId":1234}`

### Update
`GET {{instanceUrl}}/api`
