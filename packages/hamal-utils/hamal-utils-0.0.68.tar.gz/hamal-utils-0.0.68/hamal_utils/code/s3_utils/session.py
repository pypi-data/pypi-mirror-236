import boto3

from hamal_utils.code.prefect_utils.access_manager import s3_access_data

region_name, access_key_id, secret_access_key = s3_access_data()
if access_key_id and secret_access_key:
    aws_session = boto3.Session(aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
else:
    aws_session = boto3.Session()
