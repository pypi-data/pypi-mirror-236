import sys
import openai

# Imports from TextPart code:
sys.path.insert(1, '../')
from TextPart.OpenAI_Keys import OpenAI_Keys

# Function to connect to free ChatGPT account:
TheKeys = OpenAI_Keys()
openai.api_key = TheKeys.standard_key

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()
