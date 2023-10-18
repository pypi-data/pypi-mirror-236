import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from Source code:
sys.path.insert(1, '../../')
from Source.GenerateKeyWords import GenerateKeyWords

# Imports from Tools:
sys.path.insert(2, '../Tools/')
from FileComparison import FileComparison

# Definition of paths:
inputpath = "../Inputs/"
outputpath = "../Calc_Outputs/"
truthpath = "../True_Outputs/"

# Definition of filenames:
filename = "Keywords"

# Definition of unit tests:
def TestKeywords_a() -> bool:
    """
    # Unit test for text the script using the GenerateKeyWords.py script.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Generate the keywords-file:
    GenerateKeyWords(inputpath,outputpath,filename,"yake")
    
    # Compare to the correct output:
    rapport = FileComparison(outputpath+filename+"_Summary",truthpath+filename+"_Summary_yake","txt")
    
    # Find out the answer:
    Answer = False
    if (rapport==""): Answer = True 
    else: print(" ==> TestKeywords|DNN abstract with option=yake:\n\n" + rapport + "----------------------------------------------------")
    return Answer

def TestKeywords_b() -> bool:
    """
    # Unit test for text the script using the GenerateKeyWords.py script.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Generate the keywords-file:
    GenerateKeyWords(inputpath,outputpath,filename,"rake_nltk")
    
    # Compare to the correct output:
    rapport = FileComparison(outputpath+filename+"_Summary",truthpath+filename+"_Summary_rake","txt")
    
    # Find out the answer:
    Answer = False
    if (rapport==""): Answer = True 
    else: print(" ==> TestKeywords|DNN abstract with option=rake_nltk:\n\n" + rapport + "----------------------------------------------------")
    return Answer

# Definition of collection:    
def TestKeywords() -> bool:
    """
    # Collection-function of unit-tests.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    Answer = True
    if (TestKeywords_a()==False): Answer=False
    if (TestKeywords_b()==False): Answer=False
    # NOTE: We do not test the third option: openai.
    return Answer

if __name__ == '__main__':
    if TestKeywords():
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
