import azure.functions as func
import uuid
import json
import logging
from storage import table_client

app = func.FunctionApp()

@app.route(route="CreateTask", auth_level=func.AuthLevel.ANONYMOUS)
def create_task(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return func.HttpResponse(
            status_code=200,
            headers={
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            }
        )

    try:
        logging.info("CreateTask function processed a request")
        data = req.get_json()
        title = data.get("title")
        if not title:
            return func.HttpResponse(
                json.dumps({"error": "Missing 'title'"}),
                mimetype="application/json",
                status_code=400,
                headers={'Access-Control-Allow-Origin': '*'}
            )

        task = {
            "PartitionKey": "todo",
            "RowKey": str(uuid.uuid4()),
            "title": title
        }
        table_client.create_entity(task)
        logging.info(f"Created task with id {task['RowKey']}")
        
        return func.HttpResponse(
            json.dumps({"status": "created", "id": task["RowKey"]}),
            mimetype="application/json",
            status_code=200,
            headers={'Access-Control-Allow-Origin': '*'}
        )
    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON in request body"}),
            mimetype="application/json",
            status_code=400
        )
    except Exception as e:
        logging.error(f"Error in CreateTask: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500,
            headers={'Access-Control-Allow-Origin': '*'}
        )

@app.route(route="ListTasks", auth_level=func.AuthLevel.ANONYMOUS)
def list_tasks(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "OPTIONS":
        return func.HttpResponse(
            status_code=200,
            headers={
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            }
        )

    try:
        logging.info("ListTasks function processed a request")
        tasks = list(table_client.query_entities("PartitionKey eq 'todo'"))
        result = [{"id": t["RowKey"], "title": t["title"]} for t in tasks]
        logging.info(f"Retrieved {len(result)} tasks")
        
        return func.HttpResponse(
            json.dumps(result),
            mimetype="application/json",
            status_code=200,
            headers={'Access-Control-Allow-Origin': '*'}
        )
    except Exception as e:
        logging.error(f"Error in ListTasks: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500,
            headers={'Access-Control-Allow-Origin': '*'}
        )