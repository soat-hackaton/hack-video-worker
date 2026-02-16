import os
from aiohttp import FormData
from loguru import logger


class VideoIIngestApiAPIClient:

    def __init__(self, session, ingest_api_url, result_url):
        self.session = session
        self.ingest_api_url = ingest_api_url

    async def update_status(self, task_id: str, status: str, user_email: str):
        logger.info("Updating status for task {}: {}", task_id, status)
        url = os.path.join(self.ingest_api_url, task_id)
        payload = {"status": status, "user_email": user_email}
        async with self.session.patch(url, json=payload) as resp:
            logger.info(
                "Received response from Ingest API with status: {}",
                resp.status,
            )
            resp.raise_for_status()