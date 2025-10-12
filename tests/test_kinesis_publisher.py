from StreamingDataProject.kinesis_publisher import KinesisPublisher
from unittest.mock import patch, MagicMock
from botocore.exceptions import ClientError
import unittest


class TestKinesisPublisher(unittest.TestCase):
    @patch("StreamingDataProject.kinesis_publisher.boto3.client")
    def test_publish_to_kinesis_success(self, mock_boto_client):
        """Test successful publishing to Kinesis"""
        mock_kinesis = MagicMock()
        mock_boto_client.return_value = mock_kinesis

        # Mock describe_stream to simulate existing stream with proper structure
        mock_kinesis.describe_stream.return_value = {
            "StreamDescription": {
                "StreamStatus": "ACTIVE",
                "RetentionPeriodHours": 72,
                "Shards": [{"ShardId": "shard-001"}],
            }
        }

        test_articles = [
            {"webTitle": "Article 1", "webUrl": "http://example.com/1"},
            {"webTitle": "Article 2", "webUrl": "http://example.com/2"},
        ]

        # Create publisher with stream name only
        publisher = KinesisPublisher("test_stream")
        publisher.publish_articles(test_articles)

        # Verify put_record was called twice (once for each article)
        self.assertEqual(mock_kinesis.put_record.call_count, 2)

        # Verify the stream name was correct
        for call in mock_kinesis.put_record.call_args_list:
            self.assertEqual(call[1]["StreamName"], "test_stream")

    @patch("StreamingDataProject.kinesis_publisher.boto3.client")
    def test_publish_to_kinesis_empty_list(self, mock_boto_client):
        """Test publishing empty article list"""
        mock_kinesis = MagicMock()
        mock_boto_client.return_value = mock_kinesis

        # Mock describe_stream with proper structure
        mock_kinesis.describe_stream.return_value = {
            "StreamDescription": {
                "StreamStatus": "ACTIVE",
                "RetentionPeriodHours": 72,
                "Shards": [{"ShardId": "shard-001"}],
            }
        }

        publisher = KinesisPublisher("test_stream")
        publisher.publish_articles([])

        # Verify put_record was never called
        mock_kinesis.put_record.assert_not_called()

    @patch("StreamingDataProject.kinesis_publisher.boto3.client")
    def test_stream_creation_when_not_exists(self, mock_boto_client):
        """Test that stream is created if it doesn't exist"""
        mock_kinesis = MagicMock()
        mock_boto_client.return_value = mock_kinesis

        # First call raises ResourceNotFoundException, then return success
        error_response = {"Error": {"Code": "ResourceNotFoundException"}}
        mock_kinesis.describe_stream.side_effect = [
            ClientError(error_response, "DescribeStream"),
            {
                "StreamDescription": {
                    "StreamStatus": "ACTIVE",
                    "RetentionPeriodHours": 24,
                    "Shards": [{"ShardId": "shard-001"}],
                }
            },
        ]

        # Mock the waiter
        mock_waiter = MagicMock()
        mock_kinesis.get_waiter.return_value = mock_waiter

        publisher = KinesisPublisher("test_stream", shard_count=2)

        # Verify create_stream was called
        mock_kinesis.create_stream.assert_called_once_with(
            StreamName="test_stream", ShardCount=2
        )

        # Verify waiter was used
        mock_waiter.wait.assert_called()


if __name__ == "__main__":
    unittest.main()
