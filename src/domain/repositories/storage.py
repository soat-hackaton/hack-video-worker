from abc import ABC, abstractmethod


class Storage(ABC):

    @abstractmethod
    async def download(self, bucket: str, key: str) -> bytes:
        pass

    @abstractmethod
    async def upload(self, bucket: str, key: str, data: bytes):
        pass
