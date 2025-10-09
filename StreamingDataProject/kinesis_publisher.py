import json
import boto3
import botocore


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
        """
        Initializes the KinesisPublisher with connection details.
        
        Works both for local Kinesis (Kinesalite/LocalStack) and real AWS Kinesis.
        
        :param stream_name: Name of the Kinesis stream
        :param region_name: AWS region name
        :param aws_access_key_id: AWS access key ID (optional for AWS, required for local)
        :param aws_secret_access_key: AWS secret access key (optional for AWS, required for local)
        :param endpoint_url: Optional endpoint URL (e.g., http://localhost:4567 for local using something like kinesalite)
        :param shard_count: Number of shards for the stream if creating
        """
        self.stream_name = stream_name
        self.shard_count = shard_count

        # Create Kinesis client
        client_params = {
            "region_name": region_name,
            "aws_access_key_id": aws_access_key_id,
            "aws_secret_access_key": aws_secret_access_key,
        }

        if endpoint_url:
            client_params["endpoint_url"] = endpoint_url

        self.kinesis = boto3.client("kinesis", **client_params)

        # Ensure the stream exists
        self._ensure_stream_exists()

    def publish_articles(self, articles):
        """
        Publishes a list of articles to the Kinesis stream.

        :param articles: List of dictionaries or objects to send to Kinesis
        """
        try:
            for article in articles:
                self.kinesis.put_record(
                    StreamName=self.stream_name,
                    Data=json.dumps(article),
                    PartitionKey="1",
                )
        except botocore.exceptions.ClientError as e:
            print(f"Error publishing to Kinesis: {e}")
            return
        print(f"Published {len(articles)} articles to Kinesis stream '{self.stream_name}'")

    def _ensure_stream_exists(self):
        """Creates the stream if it doesn't exist and waits until it's active."""
        try:
            response = self.kinesis.describe_stream(StreamName=self.stream_name)
            status = response["StreamDescription"]["StreamStatus"]
            if status != "ACTIVE":
                print(f"Waiting for stream '{self.stream_name}' to become ACTIVE...")
                waiter = self.kinesis.get_waiter("stream_exists")
                waiter.wait(StreamName=self.stream_name)
        except self.kinesis.exceptions.ResourceNotFoundException:
            print(f"Stream '{self.stream_name}' not found. Creating it...")
            self.kinesis.create_stream(
                StreamName=self.stream_name, ShardCount=self.shard_count
            )
            print(f"Waiting for stream '{self.stream_name}' to become ACTIVE...")
            waiter = self.kinesis.get_waiter("stream_exists")
            waiter.wait(StreamName=self.stream_name)
            print(f"Stream '{self.stream_name}' is now ACTIVE.")
