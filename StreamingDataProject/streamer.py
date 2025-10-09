"""
Handles the overall streaming process.
Fetches articles from The Guardian API and publishes them to an AWS Kinesis stream.
"""

from StreamingDataProject.guardian_client import GuardianAPIClient
from StreamingDataProject.kinesis_publisher import publish_to_kinesis
from logger import get_logger
logger = get_logger(__name__)

class GuardianStreamer:
    def __init__(self, api_key):
        self.client = GuardianAPIClient(api_key)

    def run(self, search_term, date_from, stream_name):
        articles = self.client.get_articles(search_term, date_from)
        if articles:
            publish_to_kinesis(articles, stream_name)
            logger.info(f" Published {len(articles)} articles to {stream_name}")
        else:
            logger.info(f"No articles found.")