import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from TextPart code:
sys.path.insert(1, '../../')
from TextPart.textsplitter import textsplitter
from TextPart.textalinea import textalinea

# Imports from Tools:
sys.path.insert(2, '../Tools/')
from FileComparison import FileComparison
from AlineasPresent import AlineasPresent
from Plan_Velo_FR_page5_hardcoded_content import hardcodedalineas_Plan_Velo_FR_page5

# Definition of paths:
inputpath = "../Inputs/"
outputpath = "../Calc_Outputs/"
truthpath = "../True_Outputs/"

# Definition of Regression tests:
def TestTwoColumns_a(use_dummy_summary: bool) -> bool:
    """
    # Integration test test for documentsplitting using a 2-column page from plan_Velo.
    # Parameters:
    use_dummy_summary: bool: decides whether we call ChatGPT to actually make summaries, or use a dummy summarization function.
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    filename = "Plan_Velo_FR_page5"
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.standard_params()
    thetest.set_ruleverbosity(0)
    thetest.set_verbosetextline("17 millions")
    thetest.set_UseDummySummary(use_dummy_summary)
    thetest.process()
    
    # Import the correct alineas:
    correctalineas = hardcodedalineas_Plan_Velo_FR_page5()
    
    # Compare whether we have the correct alineas:
    Answer = AlineasPresent(correctalineas,thetest.textalineas)
    
    # Check whether we have the correct number of alineas:
    if not (len(correctalineas)==len(thetest.textalineas)):
        Answer = False
        print("The code found some additional structure-elements that were not supposed to be found!")
        
    # Next, verify html-output:
    html_rapport = FileComparison(outputpath + filename + "_html_visualization.html", truthpath + filename + "_html_visualization.html","html")
    if not (html_rapport=="")and(use_dummy_summary==True): 
        Answer = False
        print(" ==> HTML Comparison failed. Inspect the alinea-comparison and see if the true html should be adapted.")
        print(" ========== ATTENTION ===========> ")
        print("This is an integration test on Plan_Velo_FR_page5.pdf. It is supposed to fully pass!")
        print("\n")
    
    # Done:
    return Answer
    
# Definition of collection:    
def TestTwoColumns(use_dummy_summary: bool) -> bool:
    """
    # Collection-function of Regression-tests.
    # Parameters:
    use_dummy_summary: bool: decides whether we call ChatGPT to actually make summaries, or use a dummy summarization function.
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    Answer = True
    #"""
    
    if not TestTwoColumns_a(use_dummy_summary): Answer=False 
    print("TestTwoColumns_a()...")
    
    return Answer

if __name__ == '__main__':
    
    # Identify parameters:
    use_dummy_summary = False
    if (len(sys.argv)>1):
        if (sys.argv[1]=="dummy"):
            use_dummy_summary = True

    if TestTwoColumns(use_dummy_summary):
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
