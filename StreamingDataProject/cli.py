"""
Script to fetch articles from The Guardian API and publish them to AWS Kinesis.
This python script is designed to fetch artciles from the Guardian Api based on a relevant search term
and a date provided by the user. These articles are then published to an AWS Kinesis stream for further processing.

This tool is specifically designed to retrive up to 10 articles at a time whilst maching the search criteria
provided by the user

How to use locally:
    python guardian_tool.py <search_term> <date_from - YYY-MM-DD> <stream_name>

Example usage:
    python guardian_tool.py "A.I" "2023-01-01" "my_kinesis_stream"
"""

import argparse
from guardian_client import GuardianAPIClient
from kinesis_publisher import KinesisPublisher
import os
from dotenv import load_dotenv
 
def main():
    load_dotenv()
    GUARDIAN_API_KEY = os.getenv("GUARDIAN_API_KEY")
    GUARDIAN_API_KEY= os.getenv("GUARDIAN_API_KEY")
    AWS_ACCESS_KEY_ID= os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY= os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION= os.getenv("AWS_REGION")
    LOCAL_KINESIS_ENDPOINT_URL = os.getenv("LOCAL_KINESIS_ENDPOINT_URL")
    KINESS_SHARD_COUNT = int(os.getenv("KINESS_SHARD_COUNT", 1))


    if not GUARDIAN_API_KEY:
        raise ValueError(
            "API key not found. Please set the 'api_key' environment variable."
        )
        """checks if  the guradian api is found, if not, it raises an error ."""     


    parser = argparse.ArgumentParser(description="Fetch articles from The Guardian API and publish to AWS Kinesis.")
    parser.add_argument("search_term", type=str, help="Search term for fetching articles.")
    parser.add_argument("date_from", type=str, help="Start date for fetching articles in YYYY-MM-DD format.")
    parser.add_argument("stream_name", type=str, help="Name of the AWS Kinesis stream.") #
    args = parser.parse_args() # parses the arguments from the command line

    try:
        client = GuardianAPIClient(GUARDIAN_API_KEY)
        articles = client.get_articles(args.search_term, args.date_from)  # fetches articles using the api client
        if articles:
            publisher = KinesisPublisher(
                stream_name=args.stream_name,
                region_name=AWS_REGION,
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                endpoint_url=LOCAL_KINESIS_ENDPOINT_URL,
                shard_count=KINESS_SHARD_COUNT
            )

            publisher.publish_articles(articles)
        else:
            print("No articles found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
     