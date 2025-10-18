import os
import sys
import json
import boto3
from dotenv import load_dotenv


def read_kinesis_stream(
    stream_name,
    region_name,
    aws_access_key_id,
    aws_secret_access_key,
    endpoint_url=None,
    limit=10,
):
    """
    Reads records from a Kinesis stream.
    """
    client_params = {"region_name": region_name}
    if aws_access_key_id and aws_secret_access_key:
        client_params["aws_access_key_id"] = aws_access_key_id
        client_params["aws_secret_access_key"] = aws_secret_access_key
    if endpoint_url:
        client_params["endpoint_url"] = endpoint_url

    kinesis = boto3.client("kinesis", **client_params)

    # Get the first shard ID
    response = kinesis.describe_stream(StreamName=stream_name)
    shards = response["StreamDescription"]["Shards"]
    if not shards:
        print(f"No shards found in stream '{stream_name}'")
        return
    shard_id = shards[0]["ShardId"]

    # Get shard iterator
    shard_iterator = kinesis.get_shard_iterator(
        StreamName=stream_name,
        ShardId=shard_id,
        ShardIteratorType="TRIM_HORIZON",
    )["ShardIterator"]

    # Fetch records
    records_response = kinesis.get_records(ShardIterator=shard_iterator, Limit=limit)
    records = records_response["Records"]

    if not records:
        print(f"No records found in stream '{stream_name}'.")
        return

    print(f"Records from stream '{stream_name}':")
    for record in records:
        data = record["Data"].decode("utf-8")
        print(data)


if __name__ == "__main__":
    # Check if stream name is provided as argument
    if len(sys.argv) < 2:
        print("Usage: python read_kinesis_stream.py <stream_name>")
        sys.exit(1)

    stream_name = sys.argv[1]

    load_dotenv()

    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    REGION_NAME = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    LOCAL_KINESIS_ENDPOINT_URL = os.getenv("LOCAL_KINESIS_ENDPOINT_URL")

    read_kinesis_stream(
        stream_name=stream_name,
        region_name=REGION_NAME,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        endpoint_url=LOCAL_KINESIS_ENDPOINT_URL,
    )
