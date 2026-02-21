import pytest
from unittest.mock import AsyncMock, MagicMock
from settings import settings
from src.domain.entities.video_job import VideoJob
from src.application.usecases.process_video_job import ProcessVideoJobUseCase
from src.infrastructure.http.video_ingest_api_client import VideoIIngestApiAPIClient


@pytest.mark.asyncio
async def test_output_path_is_correct():

    storage = AsyncMock()
    api = AsyncMock()
    queue = AsyncMock()

    storage.download.return_value = b"x"
    api.process_video.return_value = {"success": True, "result_id": "result.zip"}
    api.download_result.return_value = b"zip"

    http_session = MagicMock()
    ingest_api_client = VideoIIngestApiAPIClient(
        http_session, settings.INGEST_API_URL
    )

    usecase = ProcessVideoJobUseCase(storage, api, queue, "bucket", ingest_api_client)

    job = VideoJob(filename="video.mp4", s3_path="input", user_email="test@example.com", task_id="task123")

    await usecase.execute(job, "r")

    storage.upload.assert_called_once_with(
        "bucket",
        "results/task123.zip",
        b"zip"
    )
