import requests

GUARDIAN_API_URL = "https://content.guardianapis.com/search"


class GuardianAPIClient:
    """Client to fetch articles from the Guardian Open Platform API."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("Guardian API key is required")

    def fetch_articles(self, query: str, date_from: str = None, limit: int = 10):
        """Fetch up to 'limit' articles from the Guardian API."""
        params = {
            "q": query,
            "api-key": self.api_key,
            "show-fields": "trailText,bodyText",
            "order-by": "newest",
            "page-size": limit,
        }
        if date_from:
            params["from-date"] = date_from

        response = requests.get(GUARDIAN_API_URL, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        results = data.get("response", {}).get("results", [])
        articles = []

        for r in results[:limit]:
            fields = r.get("fields", {})
            articles.append({
                "id": r.get("id"),
                "type": r.get("type"),
                "section": r.get("sectionName"),
                "publication_date": r.get("webPublicationDate"),
                "title": r.get("webTitle"),
                "url": r.get("webUrl"),
                "content_preview": fields.get("bodyText", "")[:1000],
            })

        return articles