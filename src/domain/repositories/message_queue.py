from abc import ABC, abstractmethod


class MessageQueue(ABC):

    @abstractmethod
    async def ack(self, receipt_handle: str):
        pass
