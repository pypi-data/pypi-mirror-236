import sys

# Python import commands:
import yake
import openai
import tiktoken
from rake_nltk import Rake

# Imports from TextPart code:
sys.path.insert(1, '../')
from TextPart.OpenAI_Keys import OpenAI_Keys

# Function to connect to free ChatGPT account:
TheKeys = OpenAI_Keys()
openai.api_key = TheKeys.standard_key
use_tokens_in_prompt = 3000
use_tokens_in_response = 1000


def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=use_tokens_in_response,
        n=1,
        stop=None,
        temperature=0.5,
    )
    
    return response.choices[0].text.strip()


# Main function definition:
def GenerateKeyWords(filepath: str, outputpath: str, filename: str, keywordextractor: str):
    '''
    This function generates a summary .txt-file from the splitted
    .txt-files based on title, headlines and keyword extraction.
    
    Parameters:
    filepath (str): absolute path to where the splitted .txt file is located.
    outputpath (str): absolute path to where the summary .txt file will be stored.
    filename (str): name of the specific .txt file to be transformed.
                    NB: Without the .txt-extension and without the _Body, _Title, etc.
    keywordextractor (str): name of the keyword extractor to be used. yake or rake_nltk
    
    Return:
    -- Nothing ---    # Add     # Add the title to the textfile:
the title to the textfile:

    '''

    # ------------------------------------------------------------------

    # Open the Body-text-file generated from the PDF:
    f = open(filepath + filename + "_Body.txt", "r")

    # Merge all body lines into one:
    lines = [line.rstrip() for line in f]
    text = "".join(lines)

    # Generate output file:
    summary = open(outputpath + filename + '_Summary.txt', 'w')
    Title = open(filepath + filename + "_Title.txt", "r")
    Headlines = open(filepath + filename + "_Headlines.txt", "r")

    # Add the title to the textfile:
    for jj in Title.readlines():
        summary.write("".join(jj))

    summary.write("\n")
    summary.write("--- Table of Contents ---\n")

    # Add the headlines to the textfile:
    for jj in Headlines.readlines():
        summary.write("".join(jj))

    summary.write("\n")
    summary.write("--- Extracted Keywords from Textbody ---\n")

    # ------------------------------------------------------------------

    # perform keyword extraction with different engines:
    if keywordextractor == "yake":

        # Define parameters of yake keyword extraction:
        # lan=language, n= max #words in keyword phrase, dedupLim= duplication limit from 0.0 to 1.0, top= max. number of phrases you want.
        nKeywords = 10
        kw_extractor1 = yake.KeywordExtractor(lan='en', n=3, dedupLim=0.9, top=nKeywords, features=None)
        kw_extractor2 = yake.KeywordExtractor(lan='en', n=4, dedupLim=0.9, top=nKeywords, features=None)

        # Actually perform the extraction:
        keywords1 = kw_extractor1.extract_keywords(text)
        keywords2 = kw_extractor2.extract_keywords(text)

        # Add Keywords to the summary textfile:
        for k in range(0, nKeywords):
            summary.write("".join(str(keywords1[k][0]) + "\n"))
            summary.write("".join(str(keywords2[k][0]) + "\n"))

    elif keywordextractor == "rake_nltk":

        # Perform keyword extraction:
        nKeyWords = 20
        rake_nltk_var = Rake()
        rake_nltk_var.extract_keywords_from_text(text)
        keyword_extracted = rake_nltk_var.get_ranked_phrases()[:nKeyWords]

        # Add the Keywords to the textfile:
        for kw in keyword_extracted:
            summary.write("".join(str(kw) + "\n"))

    elif keywordextractor == "openai":
        
        # Count tokens & terminate tekst:
        encoding = tiktoken.get_encoding("gpt2")
        # encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        # encoding = tiktoken.get_encoding("cl100k_base")
        # encoding = tiktoken.get_encoding("p50k_base")
        tokens = encoding.encode(text)
        Number_of_tokens = len(tokens)
        first_tokens = tokens[0:use_tokens_in_prompt]
        Broken_Text = encoding.decode(first_tokens)

        prompt = "Summarize the following text in 100 words or less; " + Broken_Text
        response = generate_response(prompt)
        summary.write(response)

    else:

        # then the user did not properly specify an extractor:
        summary.write("==> The function was called with an unsupported keyword extractor!")
        summary.write("==> Therefore, no keywords were added.")
