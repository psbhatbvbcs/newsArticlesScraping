import requests
from bs4 import BeautifulSoup
import json


class IndianExpress(object):
    def __init__(self, url):
        self.url = url


    def parse_content(self):
        """Scrapes the details of the given webpage into respective keys.

        Args:
        url: The URL of the webpage.

        Returns:
        A dictionary containing the details of the webpage, as key-value pairs.
        """

        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Get the JSON-LD data from the webpage.
        json_ld_data = soup.find_all("script", type="application/ld+json")

        # Find the JSON-LD object with @type equal to NewsArticle.
        news_article_json_ld_object = None
        for json_ld_script in json_ld_data:
            json_ld_object = json.loads(json_ld_script.text)
            if json_ld_object["@type"] == "NewsArticle":
                news_article_json_ld_object = json_ld_object
                break

        # If no JSON-LD object with @type equal to NewsArticle is found, return an empty dictionary.
        if news_article_json_ld_object is None:
            return {}

        # Return the details of the news article.
        return news_article_json_ld_object['articleBody']
