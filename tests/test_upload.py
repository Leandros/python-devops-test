import boto3
import freezegun
import subcommands

from moto import mock_s3
from subcommands import upload


@mock_s3
def test_upload_content(tmp_path):
    tmp_file = str(tmp_path) + "tmpfile.txt"
    with open(tmp_file, 'w') as f:
        f.write('this is a test')
    s3 = boto3.resource('s3')
    s3.create_bucket(Bucket="hardcoded-bucket")
    with freezegun.freeze_time("2023-01-01"):
        subcommands.upload.upload(tmp_file)
    obj = s3.Object("hardcoded-bucket", "1672531200.txt")
    content = obj.get()['Body'].read().decode('utf-8')
    assert "this is a test" == content
