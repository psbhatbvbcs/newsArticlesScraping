import requests
from bs4 import BeautifulSoup


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

        required_tags = [
            "og:url",
            "og:title",
            "og:description",
            "article:published_time",
        ]

        # Find and remove meta tags that are not in the required_tags list
        for meta_property in list(meta_properties.keys()):
            if meta_property not in required_tags:
                del meta_properties[meta_property]

        return meta_properties
