import requests
from bs4 import BeautifulSoup
from newspaper import Article


class CommonModule:
    def __init__(self, url):
        self.url = url

    def get_meta_properties(self):
        """Gets the meta properties from the given URL.

        Args:
        url: The URL of the website.

        Returns:
        A dictionary containing the meta properties, as key-value pairs.
        """

        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")

        meta_properties = {}
        for meta_tag in soup.find_all("meta"):
            if "property" in meta_tag.attrs:
                meta_property = meta_tag["property"]
                meta_content = meta_tag["content"]
                meta_properties[meta_property] = meta_content

            # if "name" in meta_tag.attrs:
            #     meta_property = meta_tag["name"]
            #     if (meta_tag["content"]):
            #         meta_content = meta_tag["content"]
            #         meta_properties[meta_property] = meta_content
            #     else:
            #         meta_properties[meta_property] = ""

        required_tags = [
            "og:site_name",
            "og:url",
            "og:title",
            "og:description",
            "article:published_time",
            "og:keywords",
            "keywords",
        ]

        # Find and remove meta tags that are not in the required_tags list
        for meta_property in list(meta_properties.keys()):
            if meta_property not in required_tags:
                del meta_properties[meta_property]

        return meta_properties

    def common_paper_scraper(self):
        article = Article(self.url, language="en")  # en for English

        # To download the article
        article.download()

        # To parse the article
        article.parse()

        # To extract text
        print("Article's Text:")
        print(article.text)
        print("n")

        return article.text
