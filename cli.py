import argparse
import os
from dotenv import load_dotenv
from guardian_data_streamer.api_client import GuardianAPIClient
from guardian_data_streamer.message_broker import MessageBroker
from guardian_data_streamer.streamer import GuardianStreamer

load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Fetch and stream Guardian articles.")
    parser.add_argument("--search", required=True, help="Search term, e.g. 'machine learning'")
    parser.add_argument("--date-from", help="Filter articles from this date (YYYY-MM-DD)")
    parser.add_argument("--stream", help="Kinesis stream name (e.g., 'guardian_content')")
    parser.add_argument("--limit", type=int, default=10, help="Max number of articles to fetch (default 10)")

    args = parser.parse_args()

    api_client = GuardianAPIClient(os.getenv("GUARDIAN_API_KEY"))

    if args.stream:
        broker = MessageBroker(stream_name=args.stream)
    else:
        broker = None

    streamer = GuardianStreamer(api_client=api_client, broker=broker)
    streamer.run(args.search, args.date_from, args.limit)


if __name__ == "__main__":
    main()