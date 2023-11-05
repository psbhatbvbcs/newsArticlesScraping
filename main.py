import re
from newspapers.main import ParseNewspapers
import csv
import os
from palmTextSummary.main import PalmAI


def identify_news_website(link):
    """Identifies the news website from the given link.

    Args:
      link: The URL of the news article.

    Returns:
      The name of the news website, or None if the news website is not recognized.
    """

    match = re.search(r"https?://(?:www\.)?([^\.]+)\.com", link)
    if match:
        news_website = match.group(1)
        return news_website
    else:
        return None


def create_csv_file(file_name, headings):
    if not os.path.isfile(file_name):
        with open(file_name, "w") as f:
            writer = csv.writer(f)
            writer.writerow(headings)


def append_to_csv_file(file_name, data):
    with open(file_name, "a") as f:
        writer = csv.writer(f)
        writer.writerow(data)


def checkKeywords(meta_properties):
    if "og:keywords" in meta_properties:
        return meta_properties["og:keywords"]
    elif "keywords" in meta_properties:
        return meta_properties["keywords"]
    else:
        return ""


def parse_news_article(link):
    """Parses the news article and gets the meta-properties and text content.

    Args:
    link: The URL of the news article.

    Returns:
    A dictionary containing the meta-properties and text content of the news article.
    """

    news_website = identify_news_website(link)
    parseNewspaper = ParseNewspapers(news_website, link)

    parseNewspaper.perform_meta_analysis()
    parseNewspaper.call_respective_function()

    meta_properties = parseNewspaper.meta_properties
    text_content = parseNewspaper.text_content

    print(f"Scraping {meta_properties['og:site_name']} article...")

    return {
        # Check if the key is present in the meta_properties dictionary. If it is not, return an empty string.
        "site_name": meta_properties["og:site_name"]
        if "og:site_name" in meta_properties
        else "",
        "url": meta_properties["og:url"] if "og:url" in meta_properties else "",
        "published_time": meta_properties["article:published_time"]
        if "article:published_time" in meta_properties
        else "",
        "title": meta_properties["og:title"] if "og:title" in meta_properties else "",
        "description": meta_properties["og:description"]
        if "og:description" in meta_properties
        else "",
        "text_content": text_content,
        "keywords": checkKeywords(meta_properties),
    }


def parse_multiple_news_articles(links):
    """Parses multiple news articles and returns a list of dictionaries containing the meta-properties and text content of each article.

    Args:
    links: A list of URLs to the news articles.

    Returns:
    A list of dictionaries containing the meta-properties and text content of each news article.
    """

    articles = []
    for link in links:
        article = parse_news_article(link)
        articles.append(article)

    return articles


def main():
    # Get the link to the news article from the user
    links = input("Enter a list of links to the news articles, separated by commas: ")
    links = links.split(",")

    # Parse the news articles and get the meta-properties and text content
    articles = parse_multiple_news_articles(links)

    for article in articles:
        if os.path.isfile("news_articles.csv"):
            csv_row = []
            for key in [
                "site_name",
                "url",
                "published_time",
                "title",
                "description",
                "text_content",
                "keywords",
            ]:
                if key in article:
                    csv_row.append(article[key])
                else:
                    csv_row.append("")
            append_to_csv_file("news_articles.csv", csv_row)
        else:
            create_csv_file(
                "news_articles.csv",
                [
                    "Site Name",
                    "Url",
                    "Published_time",
                    "Title",
                    "Description",
                    "Article Body",
                    "Keywords",
                ],
            )
            csv_row = []
            for key in [
                "site_name",
                "url",
                "published_time",
                "title",
                "description",
                "text_content",
                "keywords",
            ]:
                if key in article:
                    csv_row.append(article[key])
                else:
                    csv_row.append("")
            append_to_csv_file("news_articles.csv", csv_row)

    summaryGenerator = PalmAI(articles[0]["text_content"])
    summaryGenerator.GenerateSummary()


if __name__ == "__main__":
    os.environ["GoogleApiKey"] = "AIzaSyA2yFp-ajPIO_MPOedcuEdRFAA7dv7XoJ0"
    main()
