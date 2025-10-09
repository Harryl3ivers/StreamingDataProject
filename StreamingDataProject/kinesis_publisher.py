from api_client import GuardianAPIClient
from kinesis_publisher import publish_to_kinesis

class GuardianStreamer:
    """Coordinates fetching articles and publishing to Kinesis."""
    def __init__(self, api_key):
        self.client = GuardianAPIClient(api_key)

    def run(self, search_term, date_from, stream_name):
        articles = self.client.get_articles(search_term, date_from)
        if articles:
            publish_to_kinesis(articles, stream_name)
            print(f" Published {len(articles)} articles to {stream_name}")
        else:
            print("No articles found.")