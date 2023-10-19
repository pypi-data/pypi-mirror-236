import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from Source code:
sys.path.insert(1, '../../')
from Source.GenerateTextFile import GenerateTextFile

# Imports from Tools:
sys.path.insert(2, '../Tools/')
from FileComparison import FileComparison
from Platformdetection import detectsystem
from Platformdetection import MySystem

# Definition of paths:
inputpath = "../Inputs/"
outputpath = "../Calc_Outputs/"
truthpath = "../True_Outputs/"

# Definition of filenames:
filename = "TextExtraction_001"

# Definition of unit tests:
def TextExtraction_001a() -> bool:
    """
    # Unit test for text extraction using the GenerateTextFile.py script.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    GenerateTextFile("pypdf2",inputpath,outputpath,filename)
    rapport = FileComparison(outputpath+filename,truthpath+filename,"txt")
    Answer = False
    if (rapport==""): Answer = True 
    else: print(" ==> TextExtraction_001|option a: pypdf2:\n\n" + rapport + "----------------------------------------------------")
    return Answer

def TextExtraction_001b() -> bool:
    """
    # Unit test for text extraction using the GenerateTextFile.py script.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    GenerateTextFile("pymupdf",inputpath,outputpath,filename)
    rapport = FileComparison(outputpath+filename,truthpath+filename,"txt")
    Answer = False
    if (rapport==""): Answer = True 
    else: print(" ==> TextExtraction_001|option b: pymupdf:\n\n" + rapport + "----------------------------------------------------")
    return Answer

def TextExtraction_001d() -> bool:
    """
    # Unit test for text extraction using the GenerateTextFile.py script.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    GenerateTextFile("estupido",inputpath,outputpath,filename)
    rapport = FileComparison(outputpath+filename,truthpath+filename+"_source_invalid","txt")
    Answer = False
    if (rapport==""): Answer = True 
    else: print(" ==> TextExtraction_001|option d: non-supported:\n\n" + rapport + "----------------------------------------------------")
    return Answer

def TextExtraction_001e() -> bool:
    """
    # Unit test for text extraction using the GenerateTextFile.py script.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    GenerateTextFile("shortcut",inputpath,outputpath,filename)
    rapport = FileComparison(outputpath+filename,truthpath+filename,"txt")
    Answer = False
    if (rapport==""): Answer = True 
    else: print(" ==> TextExtraction_001|option e: shortcut:\n\n" + rapport + "----------------------------------------------------")
    return Answer

def TextExtraction_001c() -> bool:
    """
    # Unit test for text extraction using the GenerateTextFile.py script.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    GenerateTextFile("shell",inputpath,outputpath,filename)
    # NOTE: the shell does a fundamentally different job then the other libraries,
    # For a very simple document like this one, the difference is understood, and
    # all we have to do is remve the last 2 whitelines. For more complex documents,
    # the difference is larger.
    fold = open(outputpath+filename+".txt", 'r')
    text = []
    for line in fold.readlines():
        text.append(line)
    fold.close()
    text = text[:-2]
    fnew = open(outputpath+filename+".txt", 'w')
    for line in text:
        fnew.write(line)
    fnew.close()
    
    # Now, continue with the test:
    rapport = FileComparison(outputpath+filename,truthpath+filename,"txt")
    Answer = False
    if (rapport==""): Answer = True 
    else: print(" ==> TextExtraction_001|option c: shell:\n\n" + rapport + "----------------------------------------------------")
    return Answer
    
# Definition of collection:    
def TextExtraction_001() -> bool:
    """
    # Collection-function of unit-tests.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    Answer = True
    if (TextExtraction_001a()==False): Answer=False
    if (TextExtraction_001b()==False): Answer=False
    if ((detectsystem()==MySystem.LINUX)and(TextExtraction_001c()==False)): Answer=False # shell option only works undr linux.
    if (TextExtraction_001d()==False): Answer=False
    if (TextExtraction_001e()==False): Answer=False
    return Answer

if __name__ == '__main__':
    if TextExtraction_001():
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
