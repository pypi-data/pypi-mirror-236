import boto3
import os

region = os.environ.get("REGION")
access_key_id = os.environ.get("ACCESS_KEY")
secret_access_key = os.environ.get("SECRET_ACCESS_KEY")

if access_key_id and secret_access_key:
    aws_session = boto3.Session(
        region_name=region, aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
else:
    aws_session = boto3.Session()
