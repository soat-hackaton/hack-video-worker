import pytest
from unittest.mock import AsyncMock
from src.domain.entities.video_job import VideoJob
from src.application.usecases.process_video_job import ProcessVideoJobUseCase


@pytest.mark.asyncio
async def test_output_path_is_correct():

    storage = AsyncMock()
    api = AsyncMock()
    queue = AsyncMock()

    storage.download.return_value = b"x"
    api.process_video.return_value = "result.zip"
    api.download_result.return_value = b"zip"

    usecase = ProcessVideoJobUseCase(storage, api, queue, "bucket")

    job = VideoJob(filename="video.mp4", s3_path="input")

    await usecase.execute(job, "r")

    storage.upload.assert_called_once_with(
        "bucket",
        "results/result.zip",
        b"zip"
    )
