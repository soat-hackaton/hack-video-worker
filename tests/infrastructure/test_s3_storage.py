import pytest
from unittest.mock import AsyncMock
from src.infrastructure.aws.s3_storage import S3Storage


@pytest.mark.asyncio
async def test_download():

    body = AsyncMock()
    body.read.return_value = b"data"

    s3 = AsyncMock()
    s3.get_object.return_value = {"Body": body}

    storage = S3Storage(s3)

    result = await storage.download("b", "k")

    assert result == b"data"


@pytest.mark.asyncio
async def test_upload():

    s3 = AsyncMock()
    storage = S3Storage(s3)

    await storage.upload("b", "k", b"x")

    s3.put_object.assert_called_once()
