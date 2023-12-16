import google.generativeai as palm
import os


class PalmAI(object):
    def __init__(self, text_content):
        self.text_content = text_content
        palm.configure(api_key=os.environ["GoogleApiKey"])
        self.generated_summary = ""

    def GenerateSummary(self):
        request = f"Generate a factually right heading in about 200 to 250 words and also give a short summary of the most important takeaways of article in 10 bullet points for the given text content below preserving all important details. Text Content: {self.text_content}"
        response = palm.generate_text(prompt=request)
        print(response.result)
