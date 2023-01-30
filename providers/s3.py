import boto3
import io
import botocore.response as br
from abc import ABC, abstractmethod


class IS3(ABC):
    @abstractmethod
    def put_object(self, bucket: str, key: str, body: b'bytes'):
        raise NotImplementedError()

    @abstractmethod
    def get_object(self, bucket: str, key: str):
        raise NotImplementedError()

    @abstractmethod
    def delete_object(self, bucket: str, key: str):
        raise NotImplementedError()


class S3(IS3):
    """Wrapper class designed to interact with AWS S3.

    This class adheres to the abstract base class `IS3`.
    """

    # initialize with boto3 S3 client
    def __init__(self, client):
        self.client = client

    def put_object(self, bucket: str, key: str, body: b'bytes'):
        return self.client.put_object(Bucket=bucket, Key=key, Body=body)

    def get_object(self, bucket: str, key: str):
        return self.client.get_object(Bucket=bucket, Key=key)

    def delete_object(self, bucket: str, key: str):
        return self.client.delete_object(Bucket=bucket, Key=key)


class S3Mock(IS3):
    """Mock implementation of the `IS3` abstract base class.

    This class is designed to be used during dry runs or testing and will mock
    the implementation of AWS S3 and guarantees no network requests.

    """

    def __init__(self):
        self.buckets = {}

    def put_object(self, bucket: str, key: str, body: b'bytes'):
        if bucket in self.buckets:
            b = self.buckets[bucket]
            b[key] = body
        else:
            self.buckets[bucket] = {}
            self.buckets[bucket][key] = body

        return {'ResponseMetadata': {}}

    def get_object(self, bucket: str, key: str):
        if bucket in self.buckets:
            b = self.buckets[bucket]
            if key in b:
                f = b[key]
                buf = io.BytesIO(f)
                body = br.StreamingBody(raw_stream=buf, content_length=len(f))
                return {'Body': body, 'ContentLength': len(f)}

        raise boto3.S3.Client.exceptions.NoSuchKey()

    def delete_object(self, bucket: str, key: str):
        if bucket in self.buckets:
            if key in self.buckets[bucket]:
                del self.buckets[bucket][key]
                return {'ResponseMetadata': {}}

        raise boto3.S3.Client.exceptions.NoSuchKey()
