import pytest
from unittest.mock import AsyncMock, patch
import asyncio
from src.interfaces.worker.sqs_worker import SQSWorker


@pytest.mark.asyncio
async def test_handle_message_calls_usecase():

    sqs = AsyncMock()
    usecase = AsyncMock()

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

    await worker.handle_message(message)

    usecase.execute.assert_called_once()


@pytest.mark.asyncio
async def test_poll_receives_and_dispatches():

    sqs = AsyncMock()
    usecase = AsyncMock()

    sqs.receive_message.side_effect = [
        {
            "Messages": [
                {"Body": '{"filename":"a.mp4","s3_path":"input", "user_email":"test@example.com", "task_id":"task123"}', "ReceiptHandle": "1"}
            ]
        },
        asyncio.CancelledError(),
    ]

    worker = SQSWorker(
        sqs_client=sqs,
        queue_url="url",
        usecase=usecase,
        semaphore=asyncio.Semaphore(1),
    )

    with pytest.raises(asyncio.CancelledError):
        await worker.poll()

    await asyncio.sleep(0)

    assert usecase.execute.called
