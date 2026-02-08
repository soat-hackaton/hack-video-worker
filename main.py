import asyncio

import aioboto3
import aiohttp
from loguru import logger

from settings import settings
from src.application.usecases.process_video_job import ProcessVideoJobUseCase
from src.infrastructure.aws.s3_storage import S3Storage
from src.infrastructure.aws.sqs_consumer import SQSMessageQueue
from src.infrastructure.http.processing_api_client import ProcessingAPIClient
from src.interfaces.worker.sqs_worker import SQSWorker


async def main():

    session = aioboto3.Session(region_name=settings.AWS_REGION)
    timeout = aiohttp.ClientTimeout(total=30)

    async with (
        session.client("sqs") as sqs,
        session.client("s3") as s3,
        aiohttp.ClientSession(timeout=timeout) as http_session,
    ):
        storage = S3Storage(s3)
        queue = SQSMessageQueue(sqs, settings.QUEUE_URL)
        api = ProcessingAPIClient(
            http_session, settings.PROCESSING_API_URL, settings.RESULT_API_URL
        )

        usecase = ProcessVideoJobUseCase(storage, api, queue, settings.BUCKET)

        semaphore = asyncio.Semaphore(settings.SEMAPHORE_LIMIT)

        logger.info(
            "Worker started with semaphore limit: {}", settings.SEMAPHORE_LIMIT
        )
        logger.info("Listening to SQS queue: {}", settings.QUEUE_URL)
        logger.info("Using Processing API: {}", settings.PROCESSING_API_URL)
        logger.info("Using Result API: {}", settings.RESULT_API_URL)
        logger.info("Using S3 Bucket: {}", settings.BUCKET)

        worker = SQSWorker(sqs, settings.QUEUE_URL, usecase, semaphore)

        await worker.poll()


if __name__ == "__main__":
    asyncio.run(main())
