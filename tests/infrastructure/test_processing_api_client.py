import pytest
from unittest.mock import AsyncMock, MagicMock
from src.infrastructure.http.processing_api_client import ProcessingAPIClient


@pytest.mark.asyncio
async def test_process_video():

    session = MagicMock()

    response_ctx = AsyncMock()
    response = AsyncMock()

    response_ctx.__aenter__.return_value = response
    response.raise_for_status.return_value = None
    response.json.return_value = {"zip_path": "123"}

    session.post.return_value = response_ctx

    api = ProcessingAPIClient(session, "upload", "download")

    result = await api.process_video("a.mp4", b"bytes")

    assert result == "123"


@pytest.mark.asyncio
async def test_download_result():

    session = MagicMock()

    response_ctx = AsyncMock()
    response = AsyncMock()

    response_ctx.__aenter__.return_value = response
    response.raise_for_status.return_value = None
    response.read.return_value = b"zip"

    session.get.return_value = response_ctx

    api = ProcessingAPIClient(session, "upload", "download")

    result = await api.download_result("123")

    assert result == b"zip"
