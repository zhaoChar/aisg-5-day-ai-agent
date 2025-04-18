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

    # mock functions 
    def getLocation(self):
        """Get the user's current location. (mock API).
              parameters: {
                            type: "object",
                            properties: {}
                        }
        Returns:
            A string representing the current location of the user.

        """


    def getWeather(self):
        """Returns the user's current weather based on their location. (mock API).
              parameters: {
                            type: "object",
                            properties: {}
                        }

        Returns:
            A string representing the current weather at the user's location.
        """
        # Returning mock weather information

    def call_model(self):
        # Mock functions
        mock_functions = [
           self.getLocation,
           self.getWeather
        ]
        
        try:
            model = genai.GenerativeModel("gemini-2.0-flash", tools=mock_functions)
            response = model.generate_content(self.full_prompt)
                        
            # Print and return the response
            if response:
                txt_response = response.parts[0].text.strip()
                print(txt_response)
            else:
                print("Error: No response from the model.")
        except Exception as e:
            print(f"An error occurred: {e}")
