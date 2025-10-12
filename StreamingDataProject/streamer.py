"""
Handles the overall streaming process.
Fetches articles from The Guardian API and publishes them to an AWS Kinesis stream.
"""

from StreamingDataProject.guardian_client import GuardianAPIClient
from StreamingDataProject.kinesis_publisher import KinesisPublisher
from StreamingDataProject.logger import get_logger


logger = get_logger(__name__)


class GuardianStreamer:
    def __init__(
        self,
        api_key,
        region_name="us-east-1",
        aws_access_key_id=None,
        aws_secret_access_key=None,
        endpoint_url=None,
        shard_count=1,
    ):
        self.client = GuardianAPIClient(api_key)
        self.region_name = region_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.endpoint_url = endpoint_url
        self.shard_count = shard_count

    def run(self, search_term, date_from, stream_name):
        articles = self.client.get_articles(search_term, date_from)

        if articles:
            publisher = KinesisPublisher(
                stream_name=stream_name,
                region_name=self.region_name,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                endpoint_url=self.endpoint_url,
                shard_count=self.shard_count,
            )
            publisher.publish_articles(articles)
            logger.info(f"Published {len(articles)} articles to {stream_name}")
        else:
            logger.info("No articles found.")
