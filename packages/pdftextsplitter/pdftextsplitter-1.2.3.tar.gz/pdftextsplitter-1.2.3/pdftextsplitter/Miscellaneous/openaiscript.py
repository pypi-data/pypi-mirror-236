import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../TextPart/')

import openai
from OpenAI_Keys import OpenAI_Keys

thekeys = OpenAI_Keys(0
openai.api_key = thekeys.standard_key

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


with open('testdocument.txt', 'r') as file:
    data = file.read()
    prompt = "Itemize the 10 most important things from the following text; " + data
    response = generate_response(prompt)
    print(response)
    prompt = "Summarize the following text in 150 words; " + data
    response = generate_response(prompt)
    print(response)
