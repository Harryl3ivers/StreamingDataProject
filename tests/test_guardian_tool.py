import unittest
import pytest
from unittest.mock import patch, MagicMock
from Main.src.guardian_tool import get_articles
import requests

class TestGetArticles(unittest.TestCase):
    @patch('Main.src.guardian_tool.requests.get')  # Mock requests.get
    def test_get_one_articles_success(self, mock_get):
        # Create mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "response": {
                "results": [
                    {
                        "webPublicationDate": "2025-10-01T12:00:00Z",
                        "webTitle": "Sample Article 1",
                        "webUrl": "https://www.theguardian.com/sample-article-1"
                    },
                ]
            }
        }
        mock_response.raise_for_status = MagicMock()  # Mock this method
        
        # Make requests.get return our mock response
        mock_get.return_value = mock_response
        
        # Call the function
        articles = get_articles("test", "2025-10-01")
        
        # Assertions
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0]["webTitle"], "Sample Article 1")
        self.assertEqual(articles[0]["webUrl"], "https://www.theguardian.com/sample-article-1")
        self.assertEqual(articles[0]["webPublicationDate"], "2025-10-01T12:00:00Z")
        
        # Verify requests.get was called
        mock_get.assert_called_once()
    
    @patch("Main.src.guardian_tool.requests.get")
    def test_get_articles_no_results(self, mock_get):
        # Mock response with no results
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "response": {"results": []}
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        articles = get_articles("nonexistent", " ")

        self.assertEqual(len(articles), 0)
        mock_get.assert_called_once()

    @patch("Main.src.guardian_tool.requests.get")
    def test_get_articles_api_error(self, mock_get):
        mock_response = MagicMock()
        mock_response.side_effect = requests.exceptions.RequestException("API error")
        articles = get_articles("test", "2025-10-01")
        self.assertEqual(articles, [])
        mock_get.assert_called_once()
