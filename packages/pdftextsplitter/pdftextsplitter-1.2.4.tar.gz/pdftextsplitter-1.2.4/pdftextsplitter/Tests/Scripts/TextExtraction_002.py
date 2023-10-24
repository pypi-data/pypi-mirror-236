import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from Source code:
sys.path.insert(1, '../../')
from Source.GenerateTextFile import GenerateTextFile

# Imports from Tools:
sys.path.insert(2, '../Tools/')
from FileComparison import FileComparison

# Definition of paths:
inputpath = "../Inputs/"
outputpath = "../Calc_Outputs/"
truthpath = "../True_Outputs/"

# Definition of filenames:
filename = "TextExtraction_002"

# Definition of parameters:
keywordextractor = "yake"
method = "pymupdf"

# Definition of unit tests:
def TextExtraction_002a() -> bool:
    """
    # Unit test for text extraction using the GenerateTextFile.py script.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    GenerateTextFile("pypdf2",inputpath,outputpath,filename)
    rapport = FileComparison(outputpath+filename,truthpath+filename,"txt")
    Answer = False
    if (rapport==""): Answer = True 
    else: print(" ==> TextExtraction_002|option a: pypdf2:\n\n" + rapport + "----------------------------------------------------")
    return Answer

def TextExtraction_002b() -> bool:
    """
    # Unit test for text extraction using the GenerateTextFile.py script.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    GenerateTextFile("pymupdf",inputpath,outputpath,filename)
    rapport = FileComparison(outputpath+filename,truthpath+filename,"txt")
    Answer = False
    if (rapport==""): Answer = True 
    else: print(" ==> TextExtraction_002|option b: pymupdf:\n\n" + rapport + "----------------------------------------------------")
    return Answer
    
# Definition of collection:    
def TextExtraction_002() -> bool:
    """
    # Collection-function of unit-tests.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    Answer = True
    #NOTE: The shell will do a fundamentally different job then the others.
    if (TextExtraction_002a()==False): Answer=False
    if (TextExtraction_002b()==False): Answer=False
    return Answer

if __name__ == '__main__':
    if TextExtraction_002():
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
