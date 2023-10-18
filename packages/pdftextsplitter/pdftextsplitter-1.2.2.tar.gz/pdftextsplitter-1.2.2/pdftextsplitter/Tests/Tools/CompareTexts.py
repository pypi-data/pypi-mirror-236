# import statements:
from thefuzz import fuzz

# Function definition:
def CompareTexts(text1: str, text2: str) -> float:
    """
    This function uses fuzzy string mathcing to compare two textual strings.
    This can then be used to test the quality of a ChatGPT-summary against
    a predefined outcome.
    
    # Parameters:
    text1: str: the first string to compare.
    text2: str: the second string to compare.
    # Return: float: the fuzz-ratio between the strings.
    """
    
    # ------------------------------------------------------------------------------------
    
    return fuzz.ratio(text1,text2)
