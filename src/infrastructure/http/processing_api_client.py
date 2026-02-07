from aiohttp import FormData
from loguru import logger


class ProcessingAPIClient:

    def __init__(self, session, processing_url, result_url):
        self.session = session
        self.processing_url = processing_url
        self.result_url = result_url

    async def process_video(self, filename: str, bytes_data: bytes) -> str:
        logger.info("Sending video to Processing API: {}", filename)
        form = FormData()
        form.add_field(
            "video",
            bytes_data,
            filename=filename,
            content_type="video/mp4",
        )

        async with self.session.post(self.processing_url, data=form) as resp:
            logger.info(
                "Received response from Processing API with status: {}",
                resp.status,
            )
            resp.raise_for_status()
            data = await resp.json()
            logger.info("Processing API response data: {}", data)
            return data["zip_path"]

    async def download_result(self, result_id: str) -> bytes:
        async with self.session.get(f"{self.result_url}/{result_id}") as resp:
            logger.info(
                "Downloading result from Result API for result ID: {}",
                result_id,
            )
            resp.raise_for_status()
            return await resp.read()
