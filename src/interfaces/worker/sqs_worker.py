import asyncio
import json

import logging

from src.infrastructure.logging.context import set_correlation_id
from src.domain.entities.video_job import VideoJob

logger = logging.getLogger(__name__)


class SQSWorker:

    def __init__(self, sqs_client, queue_url, usecase, semaphore):
        self.sqs = sqs_client
        self.queue_url = queue_url
        self.usecase = usecase
        self.semaphore = semaphore

    async def handle_message(self, message):

        async with self.semaphore:
            try:
                payload = json.loads(message["Body"])
                job = VideoJob(**payload)

                set_correlation_id(job.task_id)

                await self.usecase.execute(job, message["ReceiptHandle"])

            except Exception as e:
                logger.error("⚠️ Falha ao processar mensagem do SQS: %s", e)

    async def poll(self):

        tasks = set()

        while True:
            logger.info("Starting worker...")

            response = await self.sqs.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=20,
                VisibilityTimeout=300,
            )

            logger.info(
                "Received %s messages from SQS",
                len(response.get("Messages", [])),
            )

            for msg in response.get("Messages", []):
                task = asyncio.create_task(self.handle_message(msg))
                tasks.add(task)
                task.add_done_callback(tasks.discard)
