import os
from aiohttp import FormData
import logging

logger = logging.getLogger(__name__)


class VideoIIngestApiAPIClient:

    def __init__(self, session, ingest_api_url):
        self.session = session
        self.ingest_api_url = ingest_api_url

    async def update_status(self, task_id: str, status: str, user_email: str):
        logger.info("Atualizando status para a task %s: %s", task_id, status)
        url = os.path.join(self.ingest_api_url, task_id)
        payload = {"status": status, "user_email": user_email}
        async with self.session.patch(url, json=payload) as resp:
            logger.info(
                "Resposta recebida da Ingest API com status: %s",
                resp.status,
            )
            resp.raise_for_status()