# Python import commands:
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# Main function definition:
def GenerateWordCloud(filepath: str, outputpath: str, filename: str, number_of_words: int):
    '''
    This function generates a summary .txt-file from the splitted
    .txt-files based on title, headlines and keyword extraction.
    
    Parameters:
    filepath (str): absolute path to where the .txt file is located to create a wordcloud on.
    outputpath (str): absolute path to where the resulted cloud as .png file will be stored.
    filename (str): name of the specific .txt file to be transformed.
                    NB: Without the .txt-extension.
    number_of_words (int): maximum number of words the wordcloud will show.
    
    Return:
    -- Nothing ---    
    The returned object is the .png-file.
    '''

    # ------------------------------------------------------------------

    # Open the text-file a word-cloud has to be generated from:
    f = open(filepath + filename + ".txt", "r")

    # Merge all body lines into one:
    lines = [line.rstrip() for line in f]
    text = "".join(lines)
    # Create a WordCloud object
    wordcloud = WordCloud(width=800, height=800,
                          max_words=number_of_words, # Number of words in the file that is taken along in generating the file.
                          background_color='white',  # background color of the resulting picture.
                          stopwords=set(STOPWORDS),  # Stopwords for wordcloud generation
                          min_font_size=10,          # Smallest word appearence in the picture
                          random_state=20            # fixes random seed to cause unique outcome when iteratively executed
                          ).generate(text)

    # Create a plot for the WordCloud image
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    # Save the plot:
    plt.savefig(outputpath + filename + ".png")
    plt.close()

    # Done.
