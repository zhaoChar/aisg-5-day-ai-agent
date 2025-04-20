import google.generativeai as genai
from dotenv import load_dotenv
import os
import re

# Load environment variables from .env file
load_dotenv()

# Access the API key from the environment variable
api_key = os.getenv("SECRET_KEY")

# Configure the model
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

# Define the prompt
base_prompt = """
You cycle through Thought, Memorize, Recall, PAUSE, Observation. At the end of the loop you output a continuation of the conversation. Your final output should be specific to the observations you have from running
the actions.
1. Thought: describe your thoughts about the given prompt.
2. Memorize: add any important information into your memory.
3. PAUSE
4. Recall: return the conversation memory.
5. PAUSE
6. Observation: will be the result of the recall action.

Available actions:
- recallConvo: 
    E.g. recallConvo: null
    Returns the memorized chat history. No arguments needed.
- addToRecall:
    E.g. addToRecall: User stated name as "John Doe"
    Saves the given information to the chat history for future recall.

Example session:
User prompt: Hello, my name is John.
Thought: This is a greeting. The user has introduced themselves as John.
Memorize: Action: addToRecall: User greeted me. User's name is John.
PAUSE
Recall: Action: recallConvo: null
PAUSE

You will be called again with something like this:
Observation: "User greeted me. User's name is John."

Then you loop again:
Thought: I should return the greeting.

You'll then output:
Answer: <Hello, John.>
"""

# Chat history
chat_history = ""

# Dummy functions
def recallConvo(place=None):
    # Debug
    print ("DEBUG: recall called")
    return chat_history

def addToRecall(notes=None):
    print ("DEBUG: memorize called")
    chat_history += f'\n{notes}'
    return {}

available_functions = {
    "recallConvo": recallConvo,
    "addToRecall": addToRecall
}

# Regex for parsing actions
action_regex = r"^Action: (\w+): (.*)$"
answer_regex = r"^Answer: (.*)$"

# Initialize variables
observation = None
max_calls = 5

# Query
query = input()

# Start the loop
for i in range(max_calls):
    print(f"\n--- Call {i + 1} ---")
    
    # Build the dynamic prompt
    if observation:
        full_prompt = f"{base_prompt}\n\nUser: {query}\nAssistant: {observation}\n\nUser:"
    else:
        full_prompt = f"{base_prompt}\n\nUser: {query}\nAssistant:"

    # Generate response from the model
    response = model.generate_content(full_prompt)
    response_text = response.parts[0].text.strip()
    print(f"Response:\n{response_text}")

    # Split response text into lines
    response_lines = response_text.split("\n")
    
    # Find the action string in the response
    found_action_str = next((line for line in response_lines if re.match(action_regex, line)), None)
   
    for line in response_lines:
        if re.match(answer_regex, line):
            i = max_calls
            break
        if re.match(action_regex, line):
            # Parse the action and arguments
            actions = re.match(action_regex, line)
            if actions:
                action, action_arg = actions.groups()
                if action in available_functions:
                    # Execute the action
                    observation = available_functions[action](action_arg)
                else:
                    print(f"Invalid action: {action}")
