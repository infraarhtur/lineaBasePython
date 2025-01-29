import boto3
import json
import os

class SQSClient:
    def __init__(self, queue_url=None):
        self.sqs = boto3.client(
            'sqs',
            region_name=os.getenv("AWS_REGION", "us-east-1")
        )
        self.queue_url = queue_url or os.getenv("SQS_QUEUE_CLIENT_URL")

    def send_message(self, message):
        """Envía un mensaje a la cola SQS"""
        response = self.sqs.send_message(
            QueueUrl=self.queue_url,
            MessageBody=json.dumps(message)
        )
        return response['MessageId']

    def receive_messages(self, max_messages=1, wait_time=10):
        """Recibe mensajes de la cola SQS"""
        response = self.sqs.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=max_messages,
            WaitTimeSeconds=wait_time
        )
        return response.get('Messages', [])

    def delete_message(self, receipt_handle):
        """Elimina un mensaje de la cola después de procesarlo"""
        self.sqs.delete_message(
            QueueUrl=self.queue_url,
            ReceiptHandle=receipt_handle
        )
