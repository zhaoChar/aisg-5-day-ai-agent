import google.generativeai as genai
import google.generativeai as genai
from dotenv import load_dotenv
import os
from newspaper import Article

# Load environment variables from .env file
load_dotenv()

# Access the API key from the environment variable
api_key = os.getenv("SECRET_KEY")

# Configure the model
genai.configure(api_key=api_key)

class SumBot:
    def __init__(self):
        self.base_prompt = (
            'You are a news article summary bot. You will be given the url, author names, publish date, keywords, and body text of a news article. '
            'You will use this data to generate a specific, accurate, and concise summary of the article. Do not leave out any important information. '
            'Prioritize accuracy over concision. The output must be formatted as:\n'
            'URL: <url>\n'
            'Authors: <author names>; <news source>; Published: <publish time>, <publish date>\n'
            '<headline on a new line>\n'
            '<summary on a new line>\n'
            'e.g.\n'
            'Authors: Huckleberry Finn; CNN; Published: 9:46 PM EDT, October 13, 2022\n'
            'headline here...\n'
            'summary here...\n'
        )
        
    def setURL(self, url):
        # print ('set url called')
        self.article = Article(url)
        # print ('article initialized')
        self.article.download()
        # print ('article downloaded')
        self.article.parse()
        # print ('article parsed')
        
        self.query = f'URL:{url}\nAUTHORS:{self.article.authors}\nPUBLISH_DATE:{self.article.publish_date}\nKEYWORDS:{self.article.keywords}\nTEXT:{self.article.text}'
        # print (self.query)
        self.full_prompt = self.base_prompt + self.query
        
    def call_model(self, url):
        self.setURL(url)
        
        try:
            model = genai.GenerativeModel("gemini-2.0-flash", tools=[])
            response = model.generate_content(self.full_prompt)
                        
            # Print and return the response
            if response:
                txt_response = response.parts[0].text.strip()
                return txt_response
            else:
                print("Error: No response from the model.")
                return -1
        except Exception as e:
            print(f"An error occurred: {e}")
            return -1

# sb = SumBot()
# print (sb.call_model('https://www.npr.org/2025/04/20/g-s1-60984/germany-deportation-protesters'))