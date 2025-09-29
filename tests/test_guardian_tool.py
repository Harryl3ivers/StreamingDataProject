import unittest
from .guardian_tool import get_articles



from unittest.mock import patch, MagicMock

class TestGetArticles(unittest.TestCase):
    def test_get_articles_success(self):
        mock = MagicMock()
        mock.json.return_value = {
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

        articles = get_articles("test", "2025-10-01")
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0]["webTitle"], "Sample Article 1")
            