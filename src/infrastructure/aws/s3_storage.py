class S3Storage:

    def __init__(self, s3_client):
        self.s3 = s3_client

    async def download(self, bucket: str, key: str) -> bytes:
        obj = await self.s3.get_object(Bucket=bucket, Key=key)
        return await obj["Body"].read()

    async def upload(self, bucket: str, key: str, data: bytes):
        await self.s3.put_object(Bucket=bucket, Key=key, Body=data)
