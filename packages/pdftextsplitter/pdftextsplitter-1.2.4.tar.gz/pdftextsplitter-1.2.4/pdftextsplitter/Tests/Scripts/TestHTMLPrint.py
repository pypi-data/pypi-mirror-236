import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from TextPart code:
sys.path.insert(1, '../../')
from TextPart.textsplitter import textsplitter

# Imports from Tools:
sys.path.insert(2, '../Tools/')
from FileComparison import FileComparison
from hardcodedalineas import hardcodedalineas_SplitDoc

# Definition of paths:
outputpath = "../Calc_Outputs/"
truthpath = "../True_Outputs/"
filename = "alineas_to_html"

def TestHTMLconversion() -> bool:
    """
    # Unit test for the function alineas_to_html() that converts the summarized document
    # to a hmtl layout.
    # Parameters: None.
    # Return: bool: the success of the test.
    # Author: Remco van groesen
    """
    
    # Create a textsplitter class for testing purposes:
    filename = "TestHTMLconversion"
    thetest = textsplitter()
    thetest.set_documentpath("/not/important/here/")
    thetest.set_outputpath(outputpath)
    thetest.set_documentname(filename)
    thetest.set_labelname(filename)
    
    # Next, gather the alineas we want to use in the html visualization:
    thetest.textalineas = hardcodedalineas_SplitDoc("pdfminer")
    
    # Perform the test:
    thetest.alineas_to_html()
 
    # Next, compare the outputs:
    rapport = FileComparison(outputpath + filename + "_html_visualization.html", truthpath + filename + "_html_visualization.html","html")
    Answer = False
    if (rapport==""): Answer = True 
    else: 
        Answer = False
        print(" ==> HTML Comparison failed for TestHTMLconversion_html_visualization.html")
        print(" ========== ATTENTION ===========> ")
        print("This is a unit test on html parsing. It is supposed to fully pass!")
        print("\n")
    
    # Return Answer:
    return Answer

if __name__ == '__main__':
    if TestHTMLconversion():
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
