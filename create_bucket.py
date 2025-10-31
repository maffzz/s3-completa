import json
import boto3
import os

s3 = boto3.client('s3')

def _json_body(event):
    body = event.get('body')
    if isinstance(body, str):
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return {}
    return body or {}

def lambda_handler(event, context):
    body = _json_body(event)
    bucket = body.get('bucket')
    region = os.environ.get('AWS_REGION') or os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')

    if not bucket:
        return {
            "statusCode": 400,
            "body": json.dumps({"ok": False, "error": "Falta 'bucket' en el body"})
        }

    try:
        params = {"Bucket": bucket}
        if region != "us-east-1":
            params["CreateBucketConfiguration"] = {"LocationConstraint": region}
        s3.create_bucket(**params)
        return {
            "statusCode": 200,
            "body": json.dumps({"ok": True, "message": f"Bucket '{bucket}' creado en {region}"})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"ok": False, "error": str(e)})
        }