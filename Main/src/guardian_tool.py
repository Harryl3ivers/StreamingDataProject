import argparse
import boto3
import requests
from dotenv import load_dotenv
import os
import botocore

load_dotenv()
GUARDIAN_API_KEY = os.getenv("GUARDIAN_API_KEY")

if not GUARDIAN_API_KEY:
    raise ValueError(
        "API key not found. Please set the 'api_key' environment variable."
    )
 
 


def get_articles(search_term, date_from):
    url = "https://content.guardianapis.com/search"
    parameters = {
        "api-key": GUARDIAN_API_KEY,
        "q": search_term,  #q is for querey its like the search box on the guardian website
        "type": "article",
        "from-date": date_from,
        "page-size": 10,
    }

    try:
        r = requests.get(url, params=parameters)
        r.raise_for_status()  # raise exception for bad response
        data = r.json()
        results = data.get("response", {}).get("results", [])

        articles = []
        for i in results:
            articles.append(
                {
                    "webPublicationDate": i.get("webPublicationDate"),
                    "webTitle": i.get("webTitle"),
                    "webUrl": i.get("webUrl"),
                }
            )

        return articles

    except requests.exceptions.RequestException as e:
        print(f"Error fetching articles: {e}")
        return []


def publish_to_kinesis(articles,stream_name):  #takes articles as input
    kinesis = boto3.client("kinesis")
    try:
        for i in articles:
         kinesis.put_record(
            StreamName=stream_name,
            Data=str(i), #kinesis only takes string data maybe better to convert to json?
            PartitionKey="partitionkey",
        )
    except botocore.exceptions.ClientError as e:
        print(f"Error publishing to Kinesis: {e}")
        return
    print(f"Published {len(articles)} articles to Kinesis stream '{stream_name}'")
    

def lambda_handler(event,context):
    pass


def main():
    parser = argparse.ArgumentParser(description="Fetch articles from The Guardian API")
    parser.add_argument("search_term", type=str, help="Search term for the Guardian API")
    parser.add_argument(
        "date_from", type=str, help="enter the date you are interested in..(YYYY-MM-DD)"
    )
    parser.add_argument("stream_name", type=str, help="Name of the message broker stream")

    args = parser.parse_args()
    search_term = args.search_term
    date_from = args.date_from
    stream_name = args.stream_name
    
    
    articles = get_articles(search_term, date_from)
    if articles:
        publish_to_kinesis(articles, stream_name)
        print(f"Successfully fetched and published {len(articles)} articles")
    else:
        print("No articles found or an error occurred")


# Only run when script is executed directly
if __name__ == "__main__":
    main()

  