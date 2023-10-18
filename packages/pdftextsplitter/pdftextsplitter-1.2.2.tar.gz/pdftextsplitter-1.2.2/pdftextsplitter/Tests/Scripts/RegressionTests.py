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
from cellar_hardcoded_content import hardcodedalineas_cellar
from Copernicus_hardcoded_content import hardcodedalineas_Copernicus
from Plan_Velo_FR_hardcoded_content import hardcodedalineas_Plan_Velo_FR
from Christiaan_PhD_Thesis_hardcoded_content import hardcodedalineas_Christiaan_PhD_Thesis
from Burgerlijk_wetboek_deel_1_hardcoded_content import hardcodedalineas_Burgerlijk_wetboek_deel_1

# Definition of paths:
inputpath = "../Regressie/"
outputpath = "../Calc_Outputs/"
truthpath = "../True_Outputs/"

# Definition of Regression tests:
def RegressionTest_a(use_dummy_summary: bool) -> bool:
    """
    # Regression test for documentsplitting using the textsplitter-class (58 calls).
    # Parameters:
    use_dummy_summary: bool: decides whether we call ChatGPT to actually make summaries, or use a dummy summarization function.
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    filename = "Copernicus"
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.standard_params()
    thetest.set_UseDummySummary(use_dummy_summary)
    thetest.set_ruleverbosity(1)
    thetest.set_verbosetextline("jfhjhfjhs")
    thetest.set_LanguageChoice("English")
    thetest.set_LanguageModel("gpt-3.5-turbo")
    thetest.process()
    print(" =====> " + str(thetest.callcounter) + " calls counted.")

    # Import the correct alineas:
    correctalineas = hardcodedalineas_Copernicus()
    
    # Compare whether we have the correct alineas:
    Answer = AlineasPresent(correctalineas,thetest.textalineas)

    # Check whether we obtain the correct header/footer boundaries (manual = 1000.0 & 55.0):
    if not ((thetest.footerboundary<55.0)and(thetest.footerboundary>50.0)): Answer = False
    if not (thetest.headerboundary>thetest.max_vert): Answer = False

    if not Answer:
        print("For " + filename + " we obtained headerboundary = " + str(thetest.headerboundary) + ", which should be close to 1000.0")
        print("For " + filename + " we obtained footerboundary = " + str(thetest.footerboundary) + ", which should be close to   55.0")
        print("For " + filename + " the full range of position = [" + str(thetest.min_vert) + "," + str(thetest.max_vert) + "]")
        Answer = False
    
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
        print("This is a regressiontest on Copernicus.pdf. It is supposed to fully pass!")
        print("If not, this means that more is going on then just a wrong html-visualization!")
        print("\n")
    
    # Done:
    return Answer

# Definition of Regression tests:
def RegressionTest_b(use_dummy_summary: bool) -> bool:
    """
    # Regression test for documentsplitting using the textsplitter-class (383 calls).
    # Parameters:
    use_dummy_summary: bool: decides whether we call ChatGPT to actually make summaries, or use a dummy summarization function.
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    filename = "cellar"
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.standard_params()
    thetest.set_UseDummySummary(use_dummy_summary)
    thetest.set_ruleverbosity(1)
    thetest.set_verbosetextline("jfhjhfjhs")
    thetest.set_LanguageChoice("Dutch")
    thetest.set_LanguageModel("gpt-3.5-turbo")
    thetest.process()
    print(" =====> " + str(thetest.callcounter) + " calls counted.")

    # Import the correct alineas:
    correctalineas = hardcodedalineas_cellar()
    
    # Compare whether we have the correct alineas:
    Answer = AlineasPresent(correctalineas,thetest.textalineas)

    # Check whether we obtain the correct header/footer boundaries (manual = 1000.0 & 55.0):
    if not ((thetest.footerboundary<40.0)and(thetest.footerboundary>thetest.min_vert)): Answer = False
    if not (thetest.headerboundary>thetest.max_vert): Answer = False

    if not Answer:
        print("For " + filename + " we obtained headerboundary = " + str(thetest.headerboundary) + ", which should be close to 1000.0")
        print("For " + filename + " we obtained footerboundary = " + str(thetest.footerboundary) + ", which should be close to   55.0")
        print("For " + filename + " the full range of position = [" + str(thetest.min_vert) + "," + str(thetest.max_vert) + "]")
        Answer = False
    
    # Check whether we have the correct number of alineas:
    if not (len(correctalineas)==len(thetest.textalineas)):
        Answer = False
        print("The code found some additional structure-elements that were not supposed to be found!")
        
    # Verify html-output:
    html_rapport = FileComparison(outputpath + filename + "_html_visualization.html", truthpath + filename + "_html_visualization.html","html")
    if not (html_rapport=="")and(use_dummy_summary==True):
        Answer = False
        print(" ==> HTML Comparison failed. Inspect the alinea-comparison and see if the true html should be adapted.")
        print(" ========== ATTENTION ===========> ")
        print("This is a regressiontest on cellar.pdf. It is supposed to fully pass!")
        print("If not, this means that more is going on then just a wrong html-visualization!")
        print("\n")
    
    # Done:
    return Answer

# Definition of Regression tests:
def RegressionTest_c(use_dummy_summary: bool) -> bool:
    """
    # Regression test for documentsplitting using the textsplitter-class (383 calls).
    # Parameters:
    use_dummy_summary: bool: decides whether we call ChatGPT to actually make summaries, or use a dummy summarization function.
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    filename = "Plan_Velo_FR"
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.standard_params()
    thetest.set_UseDummySummary(use_dummy_summary)
    thetest.set_ruleverbosity(1)
    thetest.set_verbosetextline("fldldkj")
    thetest.set_LanguageChoice("Dutch")
    thetest.set_LanguageModel("gpt-3.5-turbo")
    thetest.process()
    print(" =====> " + str(thetest.callcounter) + " calls counted.")
    
    # Import the correct alineas:
    correctalineas = hardcodedalineas_Plan_Velo_FR()
    
    # Compare whether we have the correct alineas:
    Answer = AlineasPresent(correctalineas,thetest.textalineas)

    # Check whether we obtain the correct header/footer boundaries (manual = 1000.0 & 21.0):
    if not ((thetest.footerboundary<22.0)and(thetest.footerboundary>thetest.min_vert)): Answer = False
    if not (thetest.headerboundary>thetest.max_vert): Answer = False

    if not Answer:
        print("For " + filename + " we obtained headerboundary = " + str(thetest.headerboundary) + ", which should be close to 1000.0")
        print("For " + filename + " we obtained footerboundary = " + str(thetest.footerboundary) + ", which should be close to   21.0")
        print("For " + filename + " the full range of position = [" + str(thetest.min_vert) + "," + str(thetest.max_vert) + "]")
        Answer = False
    
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
        print("This is a regressiontest on Plan_Velo_FR.pdf. It is supposed to fully pass!")
        print("If not, this means that more is going on then just a wrong html-visualization!")
        print("\n")
    
    # Done:
    return Answer

# Definition of Regression tests:
def RegressionTest_d(use_dummy_summary: bool) -> bool:
    """
    # Regression test for documentsplitting using the textsplitter-class (383 calls).
    # Parameters:
    use_dummy_summary: bool: decides whether we call ChatGPT to actually make summaries, or use a dummy summarization function.
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    filename = "eu_space"
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.standard_params()
    thetest.set_UseDummySummary(use_dummy_summary)
    thetest.set_ruleverbosity(1)
    thetest.set_verbosetextline("shjhfj")
    thetest.set_LanguageChoice("English")
    thetest.set_LanguageModel("gpt-3.5-turbo")
    thetest.process()
    print(" =====> " + str(thetest.callcounter) + " calls counted.")
    
    print("\n This Regression test (eu_space) is still under development ad, therefore, not to be trusted!\n")
    print("\n Manual boundaries for pdfminer were determined at 1000.0 & 55.0\n")
    
    # Done:
    return False

# Definition of Regression tests:
def RegressionTest_e(use_dummy_summary: bool) -> bool:
    """
    # Regression test for documentsplitting using the textsplitter-class (383 calls).
    # Parameters:
    use_dummy_summary: bool: decides whether we call ChatGPT to actually make summaries, or use a dummy summarization function.
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    filename = "Internationale_Klimaatstrategie"
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.standard_params()
    thetest.set_UseDummySummary(use_dummy_summary)
    thetest.set_ruleverbosity(1)
    thetest.set_verbosetextline("shjhfj")
    thetest.set_LanguageChoice("Dutch")
    thetest.set_LanguageModel("gpt-3.5-turbo")
    thetest.process()
    print(" =====> " + str(thetest.callcounter) + " calls counted.")
    
    print("\n This Regression test (Internationale_Klimaatstrategie) is still under development ad, therefore, not to be trusted!\n")
    print("\n Manual boundaries for pdfminer were determined at 1000.0 & 30.0\n")
    
    # Done:
    return False

# Definition of Regression tests:
def RegressionTest_f(use_dummy_summary: bool) -> bool:
    """
    # Regression test for documentsplitting using the textsplitter-class (383 calls).
    # Parameters:
    use_dummy_summary: bool: decides whether we call ChatGPT to actually make summaries, or use a dummy summarization function.
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    filename = "InnovatieAgendaRWS"
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.standard_params()
    thetest.set_UseDummySummary(use_dummy_summary)
    thetest.set_ruleverbosity(1)
    thetest.set_verbosetextline("shjhfj")
    thetest.set_LanguageChoice("Dutch")
    thetest.set_LanguageModel("gpt-3.5-turbo")
    thetest.process()
    print(" =====> " + str(thetest.callcounter) + " calls counted.")
    
    print("\n This Regression test (Innovatie Agenda RWS 2023) is still under development ad, therefore, not to be trusted!\n")
    print("\n Manual boundaries for pdfminer were determined at 1000.0 & 30.0\n")
    
    # Done:
    return False

# Definition of Regression tests:
def RegressionTest_g(use_dummy_summary: bool) -> bool:
    """
    # Regression test for documentsplitting using the textsplitter-class (383 calls).
    # Parameters:
    use_dummy_summary: bool: decides whether we call ChatGPT to actually make summaries, or use a dummy summarization function.
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    filename = "STEP"
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.standard_params
    thetest.set_UseDummySummary(use_dummy_summary)
    thetest.set_ruleverbosity(1)
    thetest.set_verbosetextline("shjhfj")
    thetest.set_LanguageChoice("English")
    thetest.set_LanguageModel("gpt-3.5-turbo")
    thetest.process()
    print(" =====> " + str(thetest.callcounter) + " calls counted.")
    
    print("\n This Regression test (STEP) is still under development ad, therefore, not to be trusted!\n")
    print("\n Manual boundaries for pdfminer were determined at 1000.0 & 55.0\n")
    
    # Done:
    return False

# Definition of Regression tests:
def RegressionTest_t(use_dummy_summary: bool) -> bool:
    """
    # Regression test for documentsplitting using the textsplitter-class (383 calls).
    # Parameters:
    use_dummy_summary: bool: decides whether we call ChatGPT to actually make summaries, or use a dummy summarization function.
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    filename = "Christiaan PhD Thesis"
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.standard_params()
    thetest.set_UseDummySummary(use_dummy_summary)
    thetest.set_ruleverbosity(1)
    thetest.set_verbosetextline("kdkdjd")
    thetest.set_LanguageChoice("English")
    thetest.set_LanguageModel("gpt-3.5-turbo")
    thetest.process()
    print(" =====> " + str(thetest.callcounter) + " calls counted.")
    
    # Import the correct alineas:
    correctalineas = hardcodedalineas_Christiaan_PhD_Thesis()
    
    # Compare whether we have the correct alineas:
    Answer = AlineasPresent(correctalineas,thetest.textalineas)

    # Check whether we obtain the correct header/footer boundaries (manual determined at 625.0 & 40.0):
    if not ((thetest.footerboundary<40.0)and(thetest.footerboundary>thetest.min_vert)): Answer = False
    if not ((thetest.headerboundary>625.0)and(thetest.headerboundary<thetest.max_vert)): Answer = False

    if not Answer:
        print("For " + filename + " we obtained headerboundary = " + str(thetest.headerboundary) + ", which should be close to  625.0")
        print("For " + filename + " we obtained footerboundary = " + str(thetest.footerboundary) + ", which should be close to   40.0")
        print("For " + filename + " the full range of position = [" + str(thetest.min_vert) + "," + str(thetest.max_vert) + "]")
        Answer = False
    
    # Check whether we have the correct number of alineas.
    # NOTE: In this case we will not do that, as we deliberately do not test
    # on the list of figures, tables, etc. There is too much complicated
    # stuff in there to try to make sense of it. It will hold future improvements back.
        
    # Next, verify html-output:
    html_rapport = FileComparison(outputpath + filename + "_html_visualization.html", truthpath + filename + "_html_visualization.html","html")
    if not (html_rapport=="")and(use_dummy_summary==True): 
        Answer = False
        print(" ==> HTML Comparison failed. Inspect the alinea-comparison and see if the true html should be adapted.")
        print(" ========== ATTENTION ===========> ")
        print("This is a regressiontest on Christiaan PhD Thesis.pdf. It is supposed to fully pass!")
        print("If not, this means that more is going on then just a wrong html-visualization!")
        print("\n")
    
    # Done:
    return Answer

# Definition of Regression tests:
def RegressionTest_w(use_dummy_summary: bool) -> bool:
    """
    # Regression test for documentsplitting using the textsplitter-class (383 calls).
    # Parameters:
    use_dummy_summary: bool: decides whether we call ChatGPT to actually make summaries, or use a dummy summarization function.
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    filename = "Burgerlijk wetboek deel 1"
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.standard_params
    thetest.set_UseDummySummary(use_dummy_summary)
    thetest.set_ruleverbosity(1)
    thetest.set_verbosetextline("jdhdj")
    thetest.set_LanguageChoice("Dutch")
    thetest.set_LanguageModel("gpt-3.5-turbo")
    thetest.process()
    print(" =====> " + str(thetest.callcounter) + " calls counted.")
    
    # Import the correct alineas:
    correctalineas = hardcodedalineas_Burgerlijk_wetboek_deel_1()
    
    # Compare whether we have the correct alineas:
    Answer = AlineasPresent(correctalineas,thetest.textalineas)

    # Check whether we obtain the correct header/footer boundaries (manually determined at 1000.0 & -100.0):
    if not (thetest.footerboundary<thetest.min_vert): Answer = False
    if not (thetest.headerboundary>thetest.max_vert): Answer = False

    if not Answer:
        print("For " + filename + " we obtained headerboundary = " + str(thetest.headerboundary) + ", which should be close to 1000.0")
        print("For " + filename + " we obtained footerboundary = " + str(thetest.footerboundary) + ", which should be close to -100.0")
        print("For " + filename + " the full range of position = [" + str(thetest.min_vert) + "," + str(thetest.max_vert) + "]")
        Answer = False
    
    # Check whether we have the correct number of alineas:
    if not (len(correctalineas)==len(thetest.textalineas)):
        Answer = False
        print("The code found some additional structure-elements that were not supposed to be found!")
    
    # Note: This one has thousands of structural elements. Comapring html-files
    # would be too expensive in terms of CPU-power. We skip it.
    
    # Done:
    return Answer
    
# Definition of collection:    
def RegressionTests(use_dummy_summary: bool) -> bool:
    """
    # Collection-function of Regression-tests.
    # Parameters:
    use_dummy_summary: bool: decides whether we call ChatGPT to actually make summaries, or use a dummy summarization function.
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    Answer = True
    
    if not RegressionTest_a(use_dummy_summary): Answer=False
    print("RegressionTest_a()...")
    if not RegressionTest_b(use_dummy_summary): Answer=False
    print("RegressionTest_b()...")
    if not RegressionTest_c(use_dummy_summary): Answer=False
    print("RegressionTest_c()...")
    if not RegressionTest_t(use_dummy_summary): Answer=False 
    print("RegressionTest_t()...")
    if not RegressionTest_w(use_dummy_summary): Answer=False 
    print("RegressionTest_w()...")

    # --------------------------------------------------------
    
    #if not RegressionTest_d(use_dummy_summary): Answer=False
    #print("RegressionTest_d()...")
    #if not RegressionTest_e(use_dummy_summary): Answer=False
    #print("RegressionTest_e()...")
    #if not RegressionTest_f(use_dummy_summary): Answer=False
    #print("RegressionTest_f()...")
    #if not RegressionTest_g(use_dummy_summary): Answer=False
    #print("RegressionTest_g()...")

    return Answer

if __name__ == '__main__':
    
    # Identify parameters:
    use_dummy_summary = False
    if (len(sys.argv)>1):
        if (sys.argv[1]=="dummy"):
            use_dummy_summary = True

    if RegressionTests(use_dummy_summary):
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")

        # Provide handle for git pipeline:
        exit(1)
