import boto3
from botocore.exceptions import ClientError


class S3Service:
	"""Minimal S3 helper for upload/download/list operations.

	Usage:
		svc = S3Service(bucket_name)
		svc.upload_bytes('path/key.json', b'data')
		data = svc.download_bytes('path/key.json')
		keys = svc.list_keys(prefix='path/')
	"""

	def __init__(self, bucket_name: str, region_name: str | None = None):
		self.bucket = bucket_name
		self.s3 = boto3.client("s3", region_name=region_name)

	def upload_bytes(self, key: str, data: bytes, content_type: str = "application/octet-stream") -> None:
		self.s3.put_object(Bucket=self.bucket, Key=key, Body=data, ContentType=content_type)

	def download_bytes(self, key: str) -> bytes | None:
		try:
			resp = self.s3.get_object(Bucket=self.bucket, Key=key)
			return resp["Body"].read()
		except ClientError:
			return None

	def list_keys(self, prefix: str = "") -> list:
		paginator = self.s3.get_paginator("list_objects_v2")
		keys: list = []
		for page in paginator.paginate(Bucket=self.bucket, Prefix=prefix):
			for obj in page.get("Contents", []) or []:
				keys.append(obj["Key"])
		return keys

