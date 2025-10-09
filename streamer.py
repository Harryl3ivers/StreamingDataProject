from guardian_data_streamer.api_client import GuardianAPIClient
from guardian_data_streamer.message_broker import MessageBroker


class GuardianStreamer:
    """Coordinates fetching Guardian articles and sending them to the broker."""

    def __init__(self, api_client=None, broker=None):
        self.api_client = api_client or GuardianAPIClient()
        self.broker = broker

    def run(self, search_term: str, date_from: str = None, limit: int = 10):
        print(f"Searching for '{search_term}' (from {date_from or 'any date'})...")
        articles = self.api_client.fetch_articles(search_term, date_from, limit)

        if not articles:
            print("No articles found.")
            return

        if not self.broker:
            print("No message broker provided. Printing JSON locally:")
            import json
            print(json.dumps(articles, indent=2))
            return

        self.broker.publish(articles)