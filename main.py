import asyncio

import aioboto3
import aiohttp
import logging

from settings import settings
from src.application.usecases.process_video_job import ProcessVideoJobUseCase
from src.infrastructure.aws.s3_storage import S3Storage
from src.infrastructure.aws.sqs_consumer import SQSMessageQueue
from src.infrastructure.http.processing_api_client import ProcessingAPIClient
from src.infrastructure.http.video_ingest_api_client import VideoIIngestApiAPIClient
from src.interfaces.worker.sqs_worker import SQSWorker

from src.infrastructure.logging.setup import setup_logging

logger = logging.getLogger(__name__)

async def main():

    setup_logging()
    
    session = aioboto3.Session(region_name=settings.AWS_REGION)
    timeout = aiohttp.ClientTimeout(total=None)

    async with (
        session.client("sqs") as sqs,
        session.client("s3") as s3,
        aiohttp.ClientSession(timeout=timeout) as http_session,
    ):
        storage = S3Storage(s3)
        queue = SQSMessageQueue(sqs, settings.QUEUE_URL)
        processing_api = ProcessingAPIClient(
            http_session, settings.PROCESSING_API_URL, settings.RESULT_API_URL
        )
        ingest_api_client = VideoIIngestApiAPIClient(
            http_session, settings.INGEST_API_URL
        )

        usecase = ProcessVideoJobUseCase(storage, processing_api, queue, settings.BUCKET, ingest_api_client)

        semaphore = asyncio.Semaphore(settings.SEMAPHORE_LIMIT)

        logger.info(
            "Worker started with semaphore limit: %s", settings.SEMAPHORE_LIMIT
        )
        logger.info("Listening to SQS queue: %s", settings.QUEUE_URL)
        logger.info("Using Processing API: %s", settings.PROCESSING_API_URL)
        logger.info("Using Result API: %s", settings.RESULT_API_URL)
        logger.info("Using S3 Bucket: %s", settings.BUCKET)

        worker = SQSWorker(sqs, settings.QUEUE_URL, usecase, semaphore)

        await worker.poll()


if __name__ == "__main__":
    asyncio.run(main())
