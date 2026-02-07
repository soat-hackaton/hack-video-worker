import pytest
from unittest.mock import AsyncMock
from src.infrastructure.aws.sqs_consumer import SQSMessageQueue


@pytest.mark.asyncio
async def test_ack():

    sqs = AsyncMock()
    queue = SQSMessageQueue(sqs, "url")

    await queue.ack("abc")

    sqs.delete_message.assert_called_once()
