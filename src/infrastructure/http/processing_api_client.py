from aiohttp import FormData, ClientError
import asyncio
import logging

logger = logging.getLogger(__name__)


class ProcessingAPIClient:

    def __init__(self, session, processing_url, result_url):
        self.session = session
        self.processing_url = processing_url
        self.result_url = result_url

    async def process_video(self, task_id: str, filename: str, bytes_data: bytes) -> dict:
        logger.info("Enviando vídeo para Processing API: %s (task_id: %s)", filename, task_id)
        form = FormData()
        form.add_field("task_id", task_id)
        form.add_field(
            "video",
            bytes_data,
            filename=filename,
            content_type="video/mp4",
        )

        try:
            async with self.session.post(self.processing_url, data=form, timeout=300) as resp:
                logger.info(
                    "Resposta recebida da Processing API com status: %s",
                    resp.status,
                )
                resp.raise_for_status()
                data = await resp.json()
                logger.info("Dados de resposta da Processing API: %s", data)
                return {"success": True, "result_id": data["zip_path"]}
        except asyncio.TimeoutError:
            logger.error("Timeout ao contactar a Processing API")
            return {"success": False, "message": "Timeout ao contactar a Processing API"}
        except ClientError as e:
            logger.error("Erro de rede ao contactar a Processing API: %s", e)
            return {"success": False, "message": "Erro de rede ao contactar a Processing API"}

    async def download_result(self, result_id: str) -> bytes:
        async with self.session.get(f"{self.result_url}/{result_id}") as resp:
            logger.info(
                "Baixando resultado da Result API para o ID do resultado: %s",
                result_id,
            )
            resp.raise_for_status()
            return await resp.read()
