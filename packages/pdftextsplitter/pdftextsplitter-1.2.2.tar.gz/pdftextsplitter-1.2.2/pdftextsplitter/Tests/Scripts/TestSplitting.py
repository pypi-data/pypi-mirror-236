import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from Source code:
sys.path.insert(1, '../../')
from Source.GenerateTextFile import GenerateTextFile
from Source.PrepareTextFile import PrepareTextFile

# Imports from Tools:
sys.path.insert(2, '../Tools/')
from FileComparison import FileComparison
from Platformdetection import detectsystem
from Platformdetection import MySystem

# Definition of paths:
inputpath = "../Inputs/"
outputpath = "../Calc_Outputs/"
truthpath = "../True_Outputs/"

# Definition of unit tests:
def TestSplitting_linux() -> str:
    """
    # Linux-part for the integration test of PrepareTextFile.py
    # Parameters: none; # Returns: the name of the file used to test on this platform.
    # Author: christiaan Douma
    """
    
    # Generate the .txt-file using the shell, as that is what the PrepareTextFile was designed for:
    filename = "CADouma_DNN_Publication"
    GenerateTextFile("shell",inputpath,outputpath,filename)
    
    # retun the filename taht we need later on:
    return filename

def TestSplitting_windows() -> str:
    """
    # Windows-part for the integration test of PrepareTextFile.py
    # Parameters: none; # Returns: the name of the file used to test on this platform.
    # Author: christiaan Douma
    """
    
    # First, begin by reporting that the windows-test is less reliable:
    print("\n")
    print(" ==> WARNING: windows has trouble recognising math-symbols in .txt-files. As such, the")
    print(" ==> WARNING: integration test TestSplitting() for PrepareTextFile.py uses a different")
    print(" ==> WARNING: test document, whcih is much less complex. The test is, therefore, LESS RELIABLE!!!")
    print("\n")
    
    # Generate the .txt-file using pymupdf, as windows does not support the shell-option.
    filename = "Windows_SplittingTest" # replacement for CADouma_DNN_Publication, as windows struggles with the math-symbols in there.
    GenerateTextFile("pymupdf",inputpath,outputpath,filename)
    
    # retun the filename taht we need later on:
    return filename

def TestSplitting() -> bool:
    """
    # Integration-test of the full script PrepareTextFile.py
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Begin with the generation of the source .txt-file. This is different for different platforms:
    thesystem = detectsystem()
    filename = ""
    
    if thesystem==MySystem.LINUX:
        filename = TestSplitting_linux()
    elif thesystem==MySystem.WINDOWS:
        filename = TestSplitting_windows()
    else:
        print("The platform <"+str(platform.system())+"> was not supported in TestSplitting()!\n")
        return False # then it is pointless to continue.
    
    # Next, execute the splitting of .txt-files:
    PrepareTextFile(inputpath,outputpath,filename)
    
    # Compare outputs:
    rapport_abstract  = FileComparison(outputpath+filename+"_Abstract",truthpath+filename+"_Abstract","txt")
    rapport_captions  = FileComparison(outputpath+filename+"_Captions",truthpath+filename+"_Captions","txt")
    rapport_headlines = FileComparison(outputpath+filename+"_Headlines",truthpath+filename+"_Headlines","txt")
    rapport_keywords  = FileComparison(outputpath+filename+"_KeyWords",truthpath+filename+"_KeyWords","txt")
    rapport_title     = FileComparison(outputpath+filename+"_Title",truthpath+filename+"_Title","txt")
    # NOTE: It is meaningless to compare the other quantities: Body, Authors, Garbich, Remain. 
    # For those, the output one would expect changes with the definition of the rules, so testing
    # against a standard output is meaningless. But for these 5, the output should, regardless
    # of the rules, always be the same.
    
    # Add rapports together:
    rapport = ""
    if (not(rapport_abstract=="")):  rapport =         "========= ABSTRACT  ===========\n"+rapport_abstract
    if (not(rapport_captions=="")):  rapport = rapport+"========= CAPTIONS  ===========\n"+rapport_captions
    if (not(rapport_headlines=="")): rapport = rapport+"========= HEADLINES ===========\n"+rapport_headlines
    if (not(rapport_keywords=="")):  rapport = rapport+"========= KEYWORDS  ===========\n"+rapport_keywords
    if (not(rapport_title=="")):     rapport = rapport+"========= TITLE     ===========\n"+rapport_title
    
    # Find out the answer:
    Answer = False
    if (rapport==""): Answer = True 
    else: print(" ==> TestSplitting_linux|DNN publication with option=shell:\n\n" + rapport + "----------------------------------------------------")
    return Answer

if __name__ == '__main__':
    if TestSplitting():
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
