import aiohttp
import pytest
from unittest.mock import AsyncMock, MagicMock
from settings import settings
from src.domain.entities.video_job import VideoJob
from src.application.usecases.process_video_job import ProcessVideoJobUseCase
from src.infrastructure.http.video_ingest_api_client import VideoIIngestApiAPIClient
from tests.helper import mock_aiohttp_post


@pytest.mark.asyncio
async def test_execute_success():

    storage = AsyncMock()
    api = AsyncMock()
    queue = AsyncMock()

    storage.download.return_value = b"video"
    api.process_video.return_value = "result123"
    api.download_result.return_value = b"zip"
    http_session = MagicMock()

    ingest_api_client = VideoIIngestApiAPIClient(
        http_session, settings.INGEST_API_URL
    )
    usecase = ProcessVideoJobUseCase(storage, api, queue, "bucket", ingest_api_client)

    job = VideoJob(filename="video.mp4", s3_path="input", user_email="test@example.com", task_id="task123")

    await usecase.execute(job, "receipt")

    storage.download.assert_called_once_with("bucket", "input")
    api.process_video.assert_called_once()
    api.download_result.assert_called_once_with("result123")
    storage.upload.assert_called_once()
    queue.ack.assert_called_once_with("receipt")


@pytest.mark.asyncio
async def test_execute_propagates_error_and_does_not_ack():

    storage = AsyncMock()
    api = AsyncMock()
    queue = AsyncMock()

    storage.download.side_effect = Exception("boom")

    http_session = MagicMock()
    ingest_api_client = VideoIIngestApiAPIClient(
        http_session, settings.INGEST_API_URL
    )

    usecase = ProcessVideoJobUseCase(storage, api, queue, "bucket", ingest_api_client)
    job = VideoJob(filename="video.mp4", s3_path="input", user_email="test@example.com", task_id="task123")

    with pytest.raises(Exception):
        await usecase.execute(job, "receipt")

    queue.ack.assert_not_called()
