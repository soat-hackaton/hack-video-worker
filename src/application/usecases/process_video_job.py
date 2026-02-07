import os

from loguru import logger

from src.domain.entities.video_job import VideoJob


class ProcessVideoJobUseCase:

    def __init__(self, storage, processing_api, message_queue, bucket: str):
        self.storage = storage
        self.processing_api = processing_api
        self.message_queue = message_queue
        self.bucket = bucket

    async def execute(self, job: VideoJob, receipt_handle: str):
        logger.info("Processing job for file: {}", job.filename)
        input_path = os.path.join(job.s3_path, job.filename)

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

        await self.message_queue.ack(receipt_handle)
        logger.info("Job completed and ACK sent for file: {}", job.filename)
