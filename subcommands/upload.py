import boto3
import os

from providers.s3 import S3
from time import time

BUCKET = "hardcoded-bucket"


def file_extension(filepath):
    base, ext = os.path.splitext(
        os.path.basename(filepath))
    return ext


def upload(filepath, s3_class=S3):
    with open(filepath, "rb") as fh:
        body = bytes(fh.read())
    key = f"{int(time())}{file_extension(filepath)}"
    s3_client = boto3.client('s3')
    s3 = s3_class(s3_client)
    s3.put_object(bucket=BUCKET, key=key, body=body)
    return key
