import json
import boto3
import os
from utils import response

# Initialize DynamoDB
dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.getenv("TABLE_NAME", "ItemsTable")
table = dynamodb.Table(TABLE_NAME)

def get_items(event, context):
    """Fetch all items from DynamoDB"""
    try:
        result = table.scan()
        return response(200, result.get("Items", []))
    except Exception as e:
        return response(500, str(e))

def create_item(event, context):
    """Create a new item"""
    try:
        body = json.loads(event["body"])
        item_id = body["id"]
        name = body["name"]

        table.put_item(Item={"id": item_id, "name": name})
        return response(201, {"message": "Item created"})
    except Exception as e:
        return response(500, str(e))

def get_item(event, context):
    """Get an item by ID"""
    try:
        item_id = event["pathParameters"]["id"]
        result = table.get_item(Key={"id": item_id})

        if "Item" in result:
            return response(200, result["Item"])
        return response(404, {"message": "Item not found"})
    except Exception as e:
        return response(500, str(e))

def delete_item(event, context):
    """Delete an item"""
    try:
        item_id = event["pathParameters"]["id"]
        table.delete_item(Key={"id": item_id})
        return response(200, {"message": "Item deleted"})
    except Exception as e:
        return response(500, str(e))
