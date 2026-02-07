from abc import ABC, abstractmethod


class ProcessingAPI(ABC):

    @abstractmethod
    async def process_video(self, filename: str, bytes_data: bytes) -> str:
        pass

    @abstractmethod
    async def download_result(self, result_id: str) -> bytes:
        pass
