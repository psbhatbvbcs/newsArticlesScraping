import requests
from bs4 import BeautifulSoup


class theHindu(object):
    def __init__(self, url):
        self.url = url

    def parse_content(self, itemprop, stop_div_class):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")

        div_tag = soup.find("div", itemprop=itemprop)

        # Find the `<div>` tag to stop scraping at.
        stop_div_tag = soup.find("div", class_=stop_div_class)

        # Remove all `<div>` tags with class `also-read`.

        for also_read_div in soup.find_all("div", class_="also-read"):
            also_read_div.extract()

        # Get all text content inside the `<div>` tag, up to the stop `<div>` tag.
        text_content = ""
        for child in div_tag.children:
            # print(child.text)
            if child == stop_div_tag:
                break
            text_content += child.text

        return text_content


# Example usage:
