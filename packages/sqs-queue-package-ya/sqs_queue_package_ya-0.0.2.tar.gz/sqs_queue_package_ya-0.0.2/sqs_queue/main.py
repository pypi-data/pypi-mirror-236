import boto3
import os
from dotenv import dotenv_values

env_path = os.getcwd().replace('/src', '') + '/.env'
Env = dotenv_values(env_path)

os.environ['AWS_ACCESS_KEY_ID'] = Env["AWS_ACCESS_KEY_ID"]
os.environ['AWS_SECRET_ACCESS_KEY'] = Env["AWS_SECRET_ACCESS_KEY"]


class SQSQueue:
    client = None

    def __init__(self, _endpoint_url: str):
        self.client = boto3.client(
            service_name=Env["QUEUE_SERVICE_NAME"],
            endpoint_url=_endpoint_url,
            region_name=Env["QUEUE_REGION"]
        )

    def send_message(self, _queue_name, _queue_msg):
        queue_url = self.client.create_queue(
            QueueName=_queue_name
        ).get('QueueUrl')

        return self.client.send_message(
            QueueUrl=queue_url,
            MessageBody=_queue_msg,
        )

    def get_messages(self, _queue_name):
        queue_url = self.client.create_queue(
            QueueName=_queue_name
        ).get('QueueUrl')

        return self.client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,
            VisibilityTimeout=1200,
            WaitTimeSeconds=10
        ).get('Messages')

    def delete_message(self, _queue_name, _recept):
        queue_url = self.client.create_queue(
            QueueName=_queue_name
        ).get('QueueUrl')

        return self.client.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=_recept
        )

    def delete_all_messages(self, _queue_name):
        queue_url = self.client.create_queue(
            QueueName=_queue_name
        ).get('QueueUrl')

        return self.client.purge_queue(
            QueueUrl=queue_url
        )
