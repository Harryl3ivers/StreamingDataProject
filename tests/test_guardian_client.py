from unittest.mock import patch, MagicMock
import requests
import unittest

from StreamingDataProject.guardian_client import GuardianAPIClient


class TestGuardianApi(unittest.TestCase):
    @patch("StreamingDataProject.guardian_client.requests.get")
    def test_get_one_articles_success(self, mock_get):
        """Test successful retrieval of one article"""
        # Create mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "response": {
                "results": [
                    {
                        "webPublicationDate": "2025-10-01T12:00:00Z",
                        "webTitle": "Sample Article 1",
                        "webUrl": "https://www.theguardian.com/sample-article-1",
                        "fields": {"bodyText": "This is some example article text."},
                    },
                ]
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # Call the function
        client = GuardianAPIClient("fake-api-key")
        articles = client.get_articles("test", "2025-10-01")

        # Assertions
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0]["webTitle"], "Sample Article 1")
        self.assertEqual(
            articles[0]["webUrl"],
            "https://www.theguardian.com/sample-article-1",
        )
        self.assertEqual(articles[0]["webPublicationDate"], "2025-10-01T12:00:00Z")
        self.assertIn("content_preview", articles[0])

        # Verify requests.get was called with correct parameters
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        self.assertEqual(call_args[0][0], "https://content.guardianapis.com/search")

    @patch("StreamingDataProject.guardian_client.requests.get")
    def test_get_articles_no_results(self, mock_get):
        """Test handling of empty results"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": {"results": []}}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        client = GuardianAPIClient("fake-api-key")
        articles = client.get_articles("nonexistent", "2025-10-01")

        self.assertEqual(len(articles), 0)
        mock_get.assert_called_once()

    @patch("StreamingDataProject.guardian_client.requests.get")
    def test_get_articles_api_error(self, mock_get):
        """Test handling of API errors"""
        mock_get.side_effect = requests.exceptions.RequestException("API error")

        client = GuardianAPIClient("fake-api-key")
        articles = client.get_articles("test", "2025-10-01")

        self.assertEqual(articles, [])
        mock_get.assert_called_once()

    @patch("StreamingDataProject.guardian_client.logger")
    def test_invalid_date_format(self, mock_logger):
        """Test that invalid date format is handled"""
        client = GuardianAPIClient("fake-api-key")
        # This should return empty list due to date validation
        articles = client.get_articles("test", "invalid-date")
        mock_logger.error.assert_called_with(
            "Incorrect date format, should be YYYY-MM-DD"
        )
        self.assertEqual(articles, [])

    def test_missing_api_key(self):
        """Test that missing API key raises error"""
        with self.assertRaises(ValueError) as context:
            GuardianAPIClient("")
        self.assertIn("API key not found", str(context.exception))


if __name__ == "__main__":
    unittest.main()
