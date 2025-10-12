import os
import requests
from datetime import datetime
from StreamingDataProject.logger import get_logger

logger = get_logger(__name__)


class GuardianAPIClient:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GUARDIAN_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key not found. Please set GUARDIAN_API_KEY as an environment variable."
            )

    def get_articles(self, search_term, date_from=None):
        if date_from:
            try:
                datetime.strptime(date_from, "%Y-%m-%d")
            except ValueError:
                logger.error("Incorrect date format, should be YYYY-MM-DD")
                return []

        url = "https://content.guardianapis.com/search"
        params = {
            "api-key": self.api_key,
            "q": search_term,
            "type": "article",
            "page-size": 10,
            "show-fields": "bodyText",
        }

        if date_from:
            params["from-date"] = date_from

        try:
            r = requests.get(url, params=params, timeout=5)
            r.raise_for_status()
            data = r.json()
            results = data.get("response", {}).get("results", [])

            articles = []
            for i in results:
                articles.append(
                    {
                        "webPublicationDate": i.get("webPublicationDate"),
                        "webTitle": i.get("webTitle"),
                        "webUrl": i.get("webUrl"),
                        "content preview": i.get("fields", {}).get("bodyText", "")[
                            :1000
                        ],
                    }
                )
            return articles

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching articles: {e}")
            return []
