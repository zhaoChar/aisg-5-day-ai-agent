import google.generativeai as genai
import google.generativeai as genai
from dotenv import load_dotenv
import os
from sumbot import SumBot
from reddit import RedditTool

# Load environment variables from .env file
load_dotenv()

# Access the API key from the environment variable
api_key = os.getenv('SECRET_KEY')

# Configure the model
genai.configure(api_key=api_key)

class Agent:
    def __init__(self):
        # init tools
        self.rt = RedditTool()
        self.sb = SumBot()

        # init agent model
        self.name = 'Turing'
        self.prompt = (
            f'You are a sassy AI assistant named {self.name}. The user will ask you for summaries of different news subreddits. '
            'You have access to the subreddits '
            'r/news -- a general mostly US focused news subreddit; '
            'r/worldnews -- a general global news subreddit; '
            'r/nottheonion -- a news subreddit focusing on asinine, egregious, or comical news stories; '
            'and r/thescoop -- a news subreddit that may feature less mainstream news. '
            'Each subreddit has 4 channels '
            'Hot -- for currently trending stories; '
            'Top -- for the most popular and biggest stories; '
            'New -- for the latest stories; and '
            'Rising -- for new stories that are gaining popularity. '
            'Given an initial prompt from the user you must determine which subreddit and channel to source articles from and how many articles to source. '
            'You must output your answer in the format:\n'
            'source:<subreddit key>\n'
            'channel:<channel key>'
            'n_articles:<number of articles to source>\n'
            'Valid subreddit keys: r_news, r_worldnews, r_nottheonion, r_thescoop. '
            'Valid channel keys: getHot, getTop, getNew, getRising. '
            'Default to either 5 or 10 articles if the user shows no preference in the number of articles. '
            'If you cannot parse the user\'s prompt, return a failure message beginning with the exact string \'FAILURE\''
            'and followed by a message to the user in the format:\n'
            'FAILURE\n'
            '<message to the user>\n'
        )
        self.full_prompt = self.prompt
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    # query model
    def queryModel(self, query):
        self.query = query
        self.full_prompt = self.prompt + self.query
    
    # summerize new article from url
    def getSummary(self, url):
        return self.sb.call_model(url)
    
    # get reddit posts
    def getRedditPosts(self, key, sreddit, nposts):
        ret = []
        if key == 'getHot':
            ret = self.rt.getHot(sub_name=sreddit, lim=nposts)
        elif key == 'getTop':
            ret = self.rt.getTop(sub_name=sreddit, lim=nposts)
        elif key == 'getNew':
            ret = self.rt.getNew(sub_name=sreddit, lim=nposts)
        elif key == 'getRising':
            ret = self.rt.getRising(sub_name=sreddit, lim=nposts)
        
        return ret

    def handleResponse(self, args):
        if args == None or len(args) == 0:
            return -1
        if args[0] == 'FAILURE':
            print (args[1])
            return -1
        
        try:
            for i in range(len(args)):
                args[i] = args[i].split(':')[1]

            posts = self.getRedditPosts(key=args[1], sreddit=args[0], nposts=int(args[2]))
            for p in posts:
                print (self.sb.call_model(p['url']), '\n')
            
        except Exception as e:
            print(f'An error occured: {e}')

    def call_model(self, query):
        self.queryModel(query)
            
        try:
            response = self.model.generate_content(self.full_prompt)
                        
            # Print and return the response
            if response:
                txt_response = response.parts[0].text.strip()
                args = txt_response.split('\n')
                self.handleResponse(args)
            else:
                print('Error: No response from the model.')
        except Exception as e:
            print(f'An error occurred: {e}')
