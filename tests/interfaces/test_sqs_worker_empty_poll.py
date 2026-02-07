import pytest
from unittest.mock import AsyncMock
import asyncio
from src.interfaces.worker.sqs_worker import SQSWorker


@pytest.mark.asyncio
async def test_poll_with_no_messages():

    sqs = AsyncMock()
    usecase = AsyncMock()

    sqs.receive_message.side_effect = [
        {"Messages": []},
        asyncio.CancelledError()
    ]

    worker = SQSWorker(
        sqs_client=sqs,
        queue_url="url",
        usecase=usecase,
        semaphore=asyncio.Semaphore(1),
    )

    with pytest.raises(asyncio.CancelledError):
        await worker.poll()

    assert not usecase.execute.called
