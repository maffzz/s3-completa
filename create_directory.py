import json
import boto3

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
    prefix = body.get('prefix')
    if not bucket or not prefix:
        return {
            "statusCode": 400,
            "body": json.dumps({"ok": False, "error": "Body debe incluir 'bucket' y 'prefix'"})
        }

    if not prefix.endswith('/'):
        prefix += '/'

    try:
        s3.put_object(Bucket=bucket, Key=prefix, Body=b"")
        return {
            "statusCode": 200,
            "body": json.dumps({"ok": True, "message": f"Directorio '{prefix}' creado en bucket '{bucket}'"})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"ok": False, "error": str(e)})
        }