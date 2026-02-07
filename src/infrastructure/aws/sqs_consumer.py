class SQSMessageQueue:

    def __init__(self, sqs_client, queue_url: str):
        self.sqs = sqs_client
        self.queue_url = queue_url

    async def ack(self, receipt_handle: str):
        await self.sqs.delete_message(
            QueueUrl=self.queue_url,
            ReceiptHandle=receipt_handle,
        )
