# Left Navigation

### Get Pins
`GET {{instanceUrl}}/api/nav/v1/pins`

### Create Pin
`POST {{instanceUrl}}/api/nav/v1/pins/append`
- Body: `{"action":{"id":"automate_workflow","type":"feature","newTab":false},"icon":"workflow","iconColor":"#FFFFFFB3","iconBackgroundColor":"#FFFFFF00","label":"<string>","userId":1234}`

### Update Pins
`POST {{instanceUrl}}/api/nav/v1/pins/append`
- Body:
  ```json
  [
    {
      "id": 1,
      "userId": 1234,
      "order": 0,
      "icon": "database",
      "iconColor": "#FFFFFFB3",
      "iconBackgroundColor": "#FFFFFF00",
      "label": "DataSets",
      "action": {
        "type": "feature",
        "id": "data_etl_datasources",
        "newTab": false
      }
    },
    {
      "id": 2,
      "userId": 1234,
      "order": 1,
      "icon": "dataflow",
      "iconColor": "#FFFFFFB3",
      "iconBackgroundColor": "#FFFFFF00",
      "label": "DataFlows",
      "action": {
        "type": "feature",
        "id": "data_etl_dataflows",
        "newTab": false
      }
    }
  ]
  ```
