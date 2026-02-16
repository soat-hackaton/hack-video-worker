import pytest
from unittest.mock import AsyncMock
import asyncio
from src.interfaces.worker.sqs_worker import SQSWorker


@pytest.mark.asyncio
async def test_handle_message_when_usecase_fails_does_not_raise():

    sqs = AsyncMock()
    usecase = AsyncMock()
    usecase.execute.side_effect = Exception("boom")

    worker = SQSWorker(
        sqs_client=sqs,
        queue_url="url",
        usecase=usecase,
        semaphore=asyncio.Semaphore(1),
    )

    message = {
        "Body": '{"filename":"a.mp4","s3_path":"input", "user_email":"test@example.com", "task_id":"task123"}',
        "ReceiptHandle": "abc"
    }

    # Não deve propagar exceção
    await worker.handle_message(message)

    usecase.execute.assert_called_once()


@pytest.mark.asyncio
async def test_handle_message_with_invalid_json():

    sqs = AsyncMock()
    usecase = AsyncMock()

    worker = SQSWorker(
        sqs_client=sqs,
        queue_url="url",
        usecase=usecase,
        semaphore=asyncio.Semaphore(1),
    )

    message = {
        "Body": "invalid-json",
        "ReceiptHandle": "abc"
    }

    await worker.handle_message(message)

    usecase.execute.assert_not_called()


@pytest.mark.asyncio
async def test_handle_message_with_missing_field():

    sqs = AsyncMock()
    usecase = AsyncMock()

    worker = SQSWorker(
        sqs_client=sqs,
        queue_url="url",
        usecase=usecase,
        semaphore=asyncio.Semaphore(1),
    )

    message = {
        "Body": '{"filename":"a.mp4"}',
        "ReceiptHandle": "abc"
    }

    await worker.handle_message(message)

    usecase.execute.assert_not_called()
