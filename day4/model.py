import google.generativeai as genai
import google.generativeai as genai
from dotenv import load_dotenv
import os
from sumbot import SumBot
from reddit import RedditTool

# Load environment variables from .env file
load_dotenv()

# Access the API key from the environment variable
api_key = os.getenv("SECRET_KEY")

# Configure the model
genai.configure(api_key=api_key)

class Agent:
    def __init__(self):
        # init tools
        self.rt = RedditTool()
        self.sb = SumBot()

        # init agent model
        self.name = "Turing"
        self.prompt = (
            f"You are a sassy AI assistant named {self.name}. The user will ask you for summaries of different news subreddits. "
            "You have access to the subreddits r/news, r/worldnews, r/nottheonion, and r/thescoop and can access linked news articles. "
            "\n"
        )
        self.full_prompt = self.prompt

    # query model
    def queryModel(self, query):
        self.query = query
        self.full_prompt = self.prompt + self.query
    
    # summerize new article from url
    def getSummary(self, url):
        return self.sb.call_model(url)
    
    # get reddit posts
    def getRedditPosts(self, key, sreddit, nposts):
        ret = ''
        if key == 'getHot':
            ret = self.rt.getHot(sub_name=sreddit, lim=nposts)
        elif key == 'getTop':
            ret = self.rt.getTop(sub_name=sreddit, lim=nposts)
        elif key == 'getNew':
            ret = self.rt.getNew(sub_name=sreddit, lim=nposts)
        elif key == 'getRising':
            ret = self.rt.getRising(sub_name=sreddit, lim=nposts)
        
        return ret

    def call_model(self, query):
        self.queryModel(query)
        
        # Helper functions
        helper_functions = [
           self.getSummary,
           self.getRedditPosts
        ]
        
        try:
            model = genai.GenerativeModel("gemini-2.0-flash", tools=helper_functions)
            response = model.generate_content(self.full_prompt)
                        
            # Print and return the response
            if response:
                txt_response = response.parts[0].text.strip()
                print(txt_response)
            else:
                print("Error: No response from the model.")
        except Exception as e:
            print(f"An error occurred: {e}")
