"""
Handles publishing messages to an AWS Kinesis stream. 
If the specified stream does not exist, it will be created.

This can also be used on local machine using Kinesalite by providing the endpoint_url parameter
to the KinesisPublisher class allowing you to test locally.
"""

import json
import boto3
import botocore
from logger import get_logger
logger = get_logger(__name__)



class KinesisPublisher:
    def __init__(
        self,
        stream_name,
        region_name="us-east-1",
        aws_access_key_id=None,
        aws_secret_access_key=None,
        endpoint_url=None,
        shard_count=1
    ):
        # Initialize the Kinesis client
        self.stream_name = stream_name
        self.shard_count = shard_count

        client_params = {"region_name": region_name}
        if aws_access_key_id and aws_secret_access_key:
            client_params["aws_access_key_id"] = aws_access_key_id
            client_params["aws_secret_access_key"] = aws_secret_access_key
        if endpoint_url:
            client_params["endpoint_url"] = endpoint_url

        self.kinesis = boto3.client("kinesis", **client_params)

        # Ensure the stream exists
        self._ensure_stream_exists()

    def publish_articles(self, articles):
        """Publish a list of articles to the Kinesis stream."""
        try:
            for article in articles:
                self.kinesis.put_record(
                    StreamName=self.stream_name,
                    Data=json.dumps(article),
                    PartitionKey="1",
                )
        except botocore.exceptions.ClientError as e:
            logger.error(f"Error publishing to Kinesis: {e}")
            return

        logger.info(f"Published {len(articles)} articles to Kinesis stream '{self.stream_name}'")

    def _ensure_stream_exists(self):
        """Ensure the stream exists and has at least 72-hour retention."""
        try:
            response = self.kinesis.describe_stream(StreamName=self.stream_name)
            status = response["StreamDescription"]["StreamStatus"]
            if status != "ACTIVE":
                logger.info(f"Waiting for stream '{self.stream_name}' to become ACTIVE...")
                waiter = self.kinesis.get_waiter("stream_exists")
                waiter.wait(StreamName=self.stream_name)

            # Increase retention if less than 72 hours
            current_retention = response["StreamDescription"].get("RetentionPeriodHours", 24)
            if current_retention < 72:
                logger.info(f"Updating stream '{self.stream_name}' retention to 3 days...")
                self.kinesis.increase_stream_retention_period(
                    StreamName=self.stream_name,
                    RetentionPeriodHours=72
                )

        except self.kinesis.exceptions.ResourceNotFoundException:
            # Stream doesn't exist, create it
            logger.info(f"Stream '{self.stream_name}' not found. Creating it...")
            self.kinesis.create_stream(
                StreamName=self.stream_name,
                ShardCount=self.shard_count
            )
            logger.info(f"Waiting for stream '{self.stream_name}' to become ACTIVE...")
            waiter = self.kinesis.get_waiter("stream_exists")
            waiter.wait(StreamName=self.stream_name)
            logger.info(f"Stream '{self.stream_name}' is now ACTIVE.")

            # Set retention to 72 hours directly
            logger.info(f"Setting stream '{self.stream_name}' retention to 3 days...")
            self.kinesis.increase_stream_retention_period(
                StreamName=self.stream_name,
                RetentionPeriodHours=72
            )
