import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from TextPart code:
sys.path.insert(1, '../../')
from TextPart.textsplitter import textsplitter
from TextPart.textalinea import textalinea

# Imports from Tools:
sys.path.insert(2, '../Tools/')
from Opsomming_hardcoded_content import hardcodedalineas_Opsomming
from AlineasPresent import AlineasPresent
from FileComparison import FileComparison

# Definition of paths:
inputpath = "../Inputs/"
outputpath = "../Calc_Outputs/"
truthpath = "../True_Outputs/"

def TestEnumerations_a() -> bool:
    """
    # Integration test for testing correct enumerations of the textsplitter-class:
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Run the textsplitter on the specific enumeration we like to test.
    # NOTE: This toy doc is specifically designed to provoke 1. versus 2.
    # chapter/enumeration discrepancies and artikel lid 1. 2. etc. situations.
    filename = "Opsomming"
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.standard_params()
    thetest.set_UseDummySummary(True)
    thetest.set_ruleverbosity(0)
    thetest.set_verbosetextline("jhdjd")
    thetest.process()
    
    # Get the correct alineas:
    correctalineas = hardcodedalineas_Opsomming()
    
    # Compare whether we have the correct alineas:
    Answer = AlineasPresent(correctalineas,thetest.textalineas)
    
    # Verify html-output:
    html_rapport = FileComparison(outputpath + filename + "_html_visualization.html", truthpath + filename + "_html_visualization.html","html")
    if not (html_rapport==""): 
        Answer = False
        print(" ==> HTML Comparison failed. Inspect the alinea-comparison and see if the true html should be adapted.")
        print(" ========== ATTENTION ===========> ")
        print("This is a integration test on Opsomming.pdf & pdfminer. It is supposed to fully pass!")
        print("\n")
    
    # Return the answer:
    return Answer

# Definition of collection:    
def TestEnumerations() -> bool:
    """
    # Collection-function of integration-tests.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    Answer = True
    
    if (TestEnumerations_a()==False): 
        Answer=False
        print('\n==> TestEnumerations_a failed!\n')
     
    return Answer

if __name__ == '__main__':
    if TestEnumerations():
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
