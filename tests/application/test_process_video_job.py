import pytest
from unittest.mock import AsyncMock
from src.domain.entities.video_job import VideoJob
from src.application.usecases.process_video_job import ProcessVideoJobUseCase


@pytest.mark.asyncio
async def test_execute_success():

    storage = AsyncMock()
    api = AsyncMock()
    queue = AsyncMock()

    storage.download.return_value = b"video"
    api.process_video.return_value = "result123"
    api.download_result.return_value = b"zip"

    usecase = ProcessVideoJobUseCase(storage, api, queue, "bucket")

    job = VideoJob(filename="video.mp4", s3_path="input")

    await usecase.execute(job, "receipt")

    storage.download.assert_called_once_with("bucket", "input/video.mp4")
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

    usecase = ProcessVideoJobUseCase(storage, api, queue, "bucket")
    job = VideoJob(filename="video.mp4", s3_path="input")

    with pytest.raises(Exception):
        await usecase.execute(job, "receipt")

    queue.ack.assert_not_called()
