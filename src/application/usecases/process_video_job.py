import os

from loguru import logger

from src.domain.entities.video_job import VideoJob


class ProcessVideoJobUseCase:

    def __init__(self, storage, processing_api, message_queue, bucket, ingest_api_client):
        self.storage = storage
        self.processing_api = processing_api
        self.message_queue = message_queue
        self.bucket = bucket
        self.ingest_api_client = ingest_api_client

    async def execute(self, job: VideoJob, receipt_handle: str):
        logger.info("Processing job for file: {}", job.filename)
        await self.ingest_api_client.update_status(job.task_id, "PROCESSING", job.user_email)

        input_path = job.s3_path

        logger.info("Downloading video from S3: {}", input_path)

        video_bytes = await self.storage.download(self.bucket, input_path)

        result_id = await self.processing_api.process_video(
            job.filename,
            video_bytes,
        )
        logger.info("Processing complete, result ID: {}", result_id)

        processed_video = await self.processing_api.download_result(result_id)

        output_path = f"results/{result_id}"
        logger.info("Uploading processed video to S3: {}", output_path)

        await self.storage.upload(self.bucket, output_path, processed_video)

        await self.ingest_api_client.update_status(job.task_id, "DONE", job.user_email)
        await self.message_queue.ack(receipt_handle)
        logger.info("Job completed and ACK sent for file: {}", job.filename)
