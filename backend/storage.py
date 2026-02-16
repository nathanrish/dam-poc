import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minio",
    aws_secret_access_key="minio123"
)

BUCKET_NAME = "media"

def _ensure_bucket_exists():
    try:
        s3_client.head_bucket(Bucket=BUCKET_NAME)
    except ClientError:
        s3_client.create_bucket(Bucket=BUCKET_NAME)

_ensure_bucket_exists()

def upload_file(file_bytes, object_name):
    s3_client.put_object(Body=file_bytes, Bucket=BUCKET_NAME, Key=object_name)

def download_file(object_name):
    response = s3_client.get_object(Bucket=BUCKET_NAME, Key=object_name)
    return response['Body'].read()

def get_file_url(object_name):
    return f"http://localhost:9000/{BUCKET_NAME}/{object_name}"
