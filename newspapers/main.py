from .CommonModule import CommonModule
from .thehindu import theHindu
from .indianExpress import IndianExpress


class ParseNewspapers(object):
    def __init__(self, newspaper_name, newspaper_link):
        self.newspaper_name = newspaper_name
        self.newspaper_link = newspaper_link

        self.meta_properties = {}
        self.text_content = ""

    def perform_meta_analysis(self):
        commonModule = CommonModule(self.newspaper_link)
        self.meta_properties = commonModule.get_meta_properties()
        #print(meta_properties)

    def call_respective_function(self):
        """Calls the respective function to scrape the text content from the given newspaper_link, depending on the news website.

        Args:
        newspaper_name: The name of the news website.
        newspaper_link: The URL of the news article.
        """

        if self.newspaper_name == "thehindu":
            print("Scraping the Hindu article...")
            hindu_instance = theHindu(self.newspaper_link)

            self.text_content = hindu_instance.parse_content(
                "articleBody", "articleblock-container"
            )
            #print(self.text_content)

        elif self.newspaper_name == "indianexpress":
            print("Scraping the Indian Express article...")

            indianExpress_instance = IndianExpress(self.newspaper_link)
            self.text_content = indianExpress_instance.parse_content()
            #print(self.text_content)

        elif self.newspaper_name == "bbc":
            print("Scraping the BBC article...")
            # scrape_bbc_article(newspaper_link)

        else:
            print("News website not recognized.")
