import json
import boto3
import base64

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
    prefix = body.get('prefix', '').strip('/')  # optional
    filename = body.get('filename')
    content_b64 = body.get('content_base64')

    if not bucket or not filename or content_b64 is None:
        return {
            "statusCode": 400,
            "body": json.dumps({"ok": False, "error": "Body debe incluir 'bucket', 'filename' y 'content_base64'"})
        }

    key = f"{prefix}/{filename}" if prefix else filename

    try:
        data = base64.b64decode(content_b64)
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"ok": False, "error": f"content_base64 inválido: {e}"})
        }

    try:
        s3.put_object(Bucket=bucket, Key=key, Body=data)
        return {
            "statusCode": 200,
            "body": json.dumps({"ok": True, "message": f"Archivo subido a s3://{bucket}/{key}"})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"ok": False, "error": str(e)})
        }