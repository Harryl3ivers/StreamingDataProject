import requests
from datetime import datetime


class GuardianAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("API key not found. Please set the 'api_key' environment variable.")

    def get_articles(self, search_term, date_from=None):
        """Fetch articles from The Guardian API

        Args:
            search_term (str): The term to search for articles.
            date_from (str, optional): The start date for the search in YYYY-MM-DD format.
        """
        if date_from:
            try:
                datetime.strptime(date_from, "%Y-%m-%d")  # checks if the date is in the correct format
            except ValueError:
                print("Incorrect date format, should be YYYY-MM-DD")
                return []

        url = "https://content.guardianapis.com/search"  # sets the url for the guardian api
        parameters = {
            "api-key": self.api_key,
            "q": search_term,  # q is for query, it's like the search box on the guardian website
            "type": "article",
            "page-size": 10,
            "show-fields": "bodyText",  # extension to show the body text of the article
        }

        # This is a dictionary of query parameters that get attached to the URL when you make the request.
        if date_from:
            parameters["from-date"] = date_from  # adds the from-date parameter if date_from is provided

        try:
            r = requests.get(url, params=parameters)  # makes a get request to the url with the parameters
            r.raise_for_status()  # raise exception for bad response
            data = r.json()  # parses the response to json format
            results = data.get("response", {}).get("results", [])  # navigates to the results part of the json response

            articles = []  # list to hold the articles
            for i in results:  # loops through the results and appends the relevant information to the articles list
                articles.append(
                    {
                        "webPublicationDate": i.get("webPublicationDate"),
                        "webTitle": i.get("webTitle"),
                        "webUrl": i.get("webUrl"),
                        "content preview": i.get("fields", {}).get("bodyText", "")[:1000],  # Get first 1000 characters
                    }
                )

            return articles

        except requests.exceptions.RequestException as e:
            print(f"Error fetching articles: {e}")
            return []
