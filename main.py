import re
from newspapers.main import ParseNewspapers
import csv
import os


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


def main():
    # Get the link to the news article from the user
    link = input("Enter the link to the news article: ")

    # Identify the news website from the given link
    news_website = identify_news_website(link)

    # Parse the news article and get the meta-properties and text content
    parseNewspaper = ParseNewspapers(news_website, link)

    parseNewspaper.perform_meta_analysis()
    parseNewspaper.call_respective_function()

    # Create or append to the CSV file
    meta_properties = parseNewspaper.meta_properties
    text_content = parseNewspaper.text_content
    print(meta_properties)

    if os.path.isfile("news_articles.csv"):
        append_to_csv_file(
            "news_articles.csv",
            [
                meta_properties["og:url"],
                meta_properties["article:published_time"],
                meta_properties["og:title"],
                meta_properties["og:description"],
                text_content,
            ],
        )
    else:
        create_csv_file(
            "news_articles.csv",
            [
                "Url",
                "Published_time",
                "Title",
                "Description",
                "Article Body",
            ],
        )
        append_to_csv_file(
            "news_articles.csv",
            [
                meta_properties["og:url"],
                meta_properties["article:published_time"],
                meta_properties["og:title"],
                meta_properties["og:description"],
                text_content,
            ],
        )


if __name__ == "__main__":
    main()
