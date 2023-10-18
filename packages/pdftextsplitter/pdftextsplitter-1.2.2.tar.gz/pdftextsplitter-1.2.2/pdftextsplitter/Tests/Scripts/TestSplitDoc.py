import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from TextPart code:
sys.path.insert(1, '../../')
from TextPart.textpart import textpart
from TextPart.fontregion import fontregion
from TextPart.textsplitter import textsplitter
from TextPart.textalinea import textalinea

# Imports from Tools:
sys.path.insert(2, '../Tools/')
from FileComparison import FileComparison
from hardcodedfontregions import hardcodedfontregions
from AlineasPresent import AlineasPresent
from hardcodedalineas import hardcodedalineas_SplitDoc
from hardcodedalineas import hardcodedalineas_TestTex
from hardcodedlineregions import hardcodedlineregions_pdfminer_SplitDoc
from hardcodedlineregions import hardcodedlineregions_pdfminer_TestTex
from hardcodedlineregions import hardcodedlineregions_pymupdf_SplitDoc
from hardcodedlineregions import hardcodedlineregions_pymupdf_TestTex

# Definition of paths:
inputpath = "../Inputs/"
outputpath = "../Calc_Outputs/"
truthpath = "../True_Outputs/"

# Definition of unit tests:
def TestSplitDoc_a(use_dummy_summary: bool) -> bool:
    """
    # Integration test for documentsplitting using the textsplitter-class.
    # Parameters: 
    use_dummy_summary: bool: decides whether we call ChatGPT to actually make summaries, or use a dummy summarization function.
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    filename = "SplitDoc"
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.set_labelname(filename)
    thetest.set_MaxSummaryLength(50)
    thetest.set_UseDummySummary(use_dummy_summary)
    thetest.set_summarization_threshold(50)
    thetest.set_LanguageChoice("Default")
    thetest.set_LanguageModel("gpt-3.5-turbo")
    thetest.set_LanguageTemperature(0.1)
    thetest.set_MaxCallRepeat(20) 
    thetest.document_metadata()
    thetest.read_native_toc("pdfminer")
    thetest.textgeneration("pdfminer")
    thetest.calculate_footerboundaries(0)
    thetest.export("default")
    thetest.fontsizehist()
    thetest.findfontregions()
    thetest.whitelinehist()
    thetest.findlineregions()
    thetest.passinfo()
    thetest.breakdown()
    thetest.shiftcontents()
    thetest.calculatetree()
    Num_Errors = thetest.layered_summary(1)
    thetest.exportdecisions()
    thetest.exportalineas("complete")
    thetest.alineas_to_html()
    
    # Next, calculate whether all required alineas exist:
    alineas_thatshouldbethere = hardcodedalineas_SplitDoc("pdfminer")
    
    Answer = AlineasPresent(alineas_thatshouldbethere,thetest.textalineas)
    
    # See if we get the correct answer for TOC-reading:
    if not (len(thetest.native_TOC)==0):
        Answer = False
        print("SplitDoc.pdf is not supposed to have an intrinsic TOC!")

    # Check whether we obtain the correct header/footer boundaries (manual for pdfminer: 625.0 & 40.0):
    if not ((thetest.footerboundary<40.0)and(thetest.footerboundary>thetest.min_vert)): Answer = False
    if not ((thetest.headerboundary>625.0)and(thetest.headerboundary<thetest.max_vert)): Answer = False

    # Generate an output report:
    if not Answer:
        print("For " + filename + " we obtained headerboundary = " + str(thetest.headerboundary) + ", which should be close to  625.0")
        print("For " + filename + " we obtained footerboundary = " + str(thetest.footerboundary) + ", which should be close to   40.0")
        print("For " + filename + " the full range of position = [" + str(thetest.min_vert) + "," + str(thetest.max_vert) + "]")
        Answer = False
    
    # Also compare calculated font regions:
    trueregions = hardcodedfontregions("pdfminer")
    index = 0
    if (len(thetest.fontregions)==len(trueregions)):
        for region in thetest.fontregions:
            if not region.compare(trueregions[index]):
                Answer = False
                print("Computed FONTregion "+str(index)+" deviated from its intended value:")
                region.printregion()
                trueregions[index].printregion()
                print("\n")
            index +=1
    else:
        Answer = False
        print("The number of computed FONTregions ("+str(len(thetest.fontregions))+") was different then what was expected ("+str(len(trueregions))+"):")
        for region in thetest.fontregions:
            region.printregion()
        print("\n")
        
    # Also compare calculated whiteline regions:
    truelineregions = hardcodedlineregions_pdfminer_SplitDoc()
    index = 0
    if (len(thetest.lineregions)==len(truelineregions)):
        for region in thetest.lineregions:
            if not region.compare(truelineregions[index]):
                Answer = False
                print("Computed LINEregion "+str(index)+" deviated from its intended value:")
                region.printregion()
                truelineregions[index].printregion()
                print("\n")
            index +=1
    else:
        Answer = False
        print("The number of computed LINEregions ("+str(len(thetest.lineregions))+") was different then what was expected ("+str(len(truelineregions))+"):")
        for region in thetest.lineregions:
            region.printregion()
        print("\n")
    
    # Find out if we actually added something in the summaries of the textalineas:
    LengthCheck = True
    for alinea in thetest.textalineas:
        sum_array = alinea.summary.split()
        lengthsum = len(sum_array)
        if (lengthsum<1)and(alinea.sum_CanbeEmpty==False): LengthCheck = False
    if not LengthCheck: 
        Answer = False
        print("Not enough words were added to some of the summaries of SplitDoc & pdfminer.")
    
    # Next, also check that we did not encounter errors during the layered_summary()-fase:
    if not (Num_Errors==0):
        Answer = False
        print("textsplitter.layered_summary() encountered " + str(Num_Errors) + "x a child with empty summary.")
        print("This should not be possible, so the test failed!")
    
    # Verify html-output:
    if use_dummy_summary: # Otherwise the output varies with ChatGPT and a fair comparison cannot be made.
        html_rapport = FileComparison(outputpath + filename + "_html_visualization.html", truthpath + filename + "_pdfminer_html_visualization.html","html")
        if not (html_rapport==""): 
            Answer = False
            print(" ==> HTML Comparison failed. Inspect the alinea-comparison and see if the true html should be adapted.")
            print(" ========== ATTENTION ===========> ")
            print("This is a integration test on SplitDoc.pdf & pdfminer. It is supposed to fully pass!")
            print("\n")
    
    # NOTE: We do NOT test for the content of the summaries. This would require the use of meaningful text 
    # (as was used in TestSummarize(), but is not used here) and a fuzzy match or another ChatGPT-call to verify,
    # or it would require the use of the dummy-mode according to TestLayeredSummary(). But then it would 
    # not be an integration test anymore. The idea is that this test can also run without the dummy-mode.
    # So we keep it like this.
    
    # Done:
    return Answer
    
# Definition of unit tests:
def TestSplitDoc_b(use_dummy_summary: bool) -> bool:
    """
    # Integration test for documentsplitting using the textsplitter-class.
    # Parameters: 
    use_dummy_summary: bool: decides whether we call ChatGPT to actually make summaries, or use a dummy summarization function.
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    filename = "TestTex"
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.set_labelname(filename)
    thetest.set_MaxSummaryLength(50)
    thetest.set_UseDummySummary(use_dummy_summary)
    thetest.set_summarization_threshold(50)
    thetest.set_LanguageChoice("Default")
    thetest.set_LanguageModel("gpt-3.5-turbo")
    thetest.set_LanguageTemperature(0.1)
    thetest.set_MaxCallRepeat(20) 
    thetest.document_metadata()
    thetest.read_native_toc("pdfminer")
    thetest.textgeneration("pdfminer")
    thetest.calculate_footerboundaries(0)
    thetest.export("default")
    thetest.fontsizehist()
    thetest.findfontregions()
    thetest.whitelinehist()
    thetest.findlineregions()
    thetest.passinfo()
    thetest.breakdown()
    thetest.shiftcontents()
    thetest.calculatetree()
    Num_Errors = thetest.layered_summary(1)
    thetest.exportdecisions()
    thetest.exportalineas("complete")
    thetest.alineas_to_html()
    
    # Next, calculate whether all required alineas exist:
    alineas_thatshouldbethere = hardcodedalineas_TestTex("pdfminer")
    Answer = AlineasPresent(alineas_thatshouldbethere,thetest.textalineas)
    
    # See if we get the correct answer for TOC-reading:
    if not (len(thetest.native_TOC)==0):
        Answer = False
        print("SplitDoc.pdf is not supposed to have an intrinsic TOC!")

    # Check whether we obtain the correct header/footer boundaries (manual pdfminer: 650.0 & 128.0):
    if not ((thetest.footerboundary<129.0)and(thetest.footerboundary>thetest.min_vert)): Answer = False
    if not (thetest.headerboundary>thetest.max_vert): Answer = False

    if not Answer:
        print("For " + filename + " we obtained headerboundary = " + str(thetest.headerboundary) + ", which should be close to  650.0")
        print("For " + filename + " we obtained footerboundary = " + str(thetest.footerboundary) + ", which should be close to  128.0")
        print("For " + filename + " the full range of position = [" + str(thetest.min_vert) + "," + str(thetest.max_vert) + "]")
        Answer = False
    
    # Also compare calculated whiteline regions:
    truelineregions = hardcodedlineregions_pdfminer_TestTex()
    
    index = 0
    if (len(thetest.lineregions)==len(truelineregions)):
        for region in thetest.lineregions:
            if not region.compare(truelineregions[index]):
                Answer = False
                print("Computed LINEregion "+str(index)+" deviated from its intended value:")
                region.printregion()
                truelineregions[index].printregion()
                print("\n")
            index +=1
    else:
        Answer = False
        print("The number of computed LINEregions ("+str(len(thetest.lineregions))+") was different then what was expected ("+str(len(truelineregions))+"):")
        for region in thetest.lineregions:
            region.printregion()
        print("\n")
    
    # Find out if we actually added something in the summaries of the textalineas:
    LengthCheck = True
    for alinea in thetest.textalineas:
        sum_array = alinea.summary.split()
        lengthsum = len(sum_array)
        if (lengthsum<1)and(alinea.sum_CanbeEmpty==False): LengthCheck = False
    if not LengthCheck: 
        Answer = False
        print("Not enough words were added to some of the summaries of TestTex & pdfminer.")
    
    # Next, also check that we did not encounter errors during the layered_summary()-fase:
    if not (Num_Errors==0):
        Answer = False
        print("textsplitter.layered_summary() encountered " + str(Num_Errors) + "x a child with empty summary.")
        print("This should not be possible, so the test failed!")
    
    # Verify html-output:
    if use_dummy_summary: # Otherwise the output varies with ChatGPT and a fair comparison cannot be made.
        html_rapport = FileComparison(outputpath + filename + "_html_visualization.html", truthpath + filename + "_pdfminer_html_visualization.html","html")
        if not (html_rapport==""): 
            Answer = False
            print(" ==> HTML Comparison failed. Inspect the alinea-comparison and see if the true html should be adapted.")
            print(" ========== ATTENTION ===========> ")
            print("This is a integration test on TestTex.pdf & pdfminer. It is supposed to fully pass!")
            print("\n")
    
    # NOTE: We do NOT test for the content of the summaries. This would require the use of meaningful text 
    # (as was used in TestSummarize(), but is not used here) and a fuzzy match or another ChatGPT-call to verify,
    # or it would require the use of the dummy-mode according to TestLayeredSummary(). But then it would 
    # not be an integration test anymore. The idea is that this test can also run without the dummy-mode.
    # So we keep it like this.
    
    # Done:
    return Answer

# Definition of unit tests:
def TestSplitDoc_c(use_dummy_summary: bool) -> bool:
    """
    # Integration test for documentsplitting using the textsplitter-class.
    # Parameters: 
    use_dummy_summary: bool: decides whether we call ChatGPT to actually make summaries, or use a dummy summarization function.
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    filename = "SplitDoc"
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.set_labelname(filename)
    thetest.set_MaxSummaryLength(50)
    thetest.set_UseDummySummary(use_dummy_summary)
    thetest.set_summarization_threshold(50)
    thetest.set_LanguageChoice("Default")
    thetest.set_LanguageModel("gpt-3.5-turbo")
    thetest.set_LanguageTemperature(0.1)
    thetest.set_MaxCallRepeat(20) 
    thetest.document_metadata()
    thetest.read_native_toc("pymupdf")
    thetest.textgeneration("pymupdf")
    thetest.calculate_footerboundaries(0) # manual: 625.0 & 40.0 for pymupdf
    thetest.export("default")
    thetest.fontsizehist()
    thetest.findfontregions()
    thetest.whitelinehist()
    thetest.findlineregions()
    thetest.passinfo()
    thetest.breakdown()
    thetest.shiftcontents()
    thetest.calculatetree()
    Num_Errors = thetest.layered_summary(1)
    thetest.exportdecisions()
    thetest.exportalineas("complete")
    thetest.alineas_to_html()
   
    # Next, calculate whether all required alineas exist:
    alineas_thatshouldbethere = hardcodedalineas_SplitDoc("pymupdf")
    Answer = AlineasPresent(alineas_thatshouldbethere,thetest.textalineas)
    
    # See if we get the correct answer for TOC-reading:
    if not (len(thetest.native_TOC)==0):
        Answer = False
        print("SplitDoc.pdf is not supposed to have an intrinsic TOC!")
    
    # Also compare calculated font regions:
    trueregions = hardcodedfontregions("pymupdf")
    index = 0
    if (len(thetest.fontregions)==len(trueregions)):
        for region in thetest.fontregions:
            if not region.compare(trueregions[index]): # Because pymupdf gives slightly different freqs then pdfminer, which is where the hardcodedfontregions match to.
                Answer = False
                print("Computed FONTregion "+str(index)+" deviated from its intended value:")
                region.printregion()
                trueregions[index].printregion()
                print("\n")
            index +=1
    else:
        Answer = False
        print("The number of computed FONTregions ("+str(len(thetest.fontregions))+") was different then what was expected ("+str(len(trueregions))+"):")
        for region in thetest.fontregions:
            region.printregion()
        print("\n")
    
    # Also compare calculated whiteline regions:
    truelineregions = hardcodedlineregions_pymupdf_SplitDoc()
    index = 0
    if (len(thetest.lineregions)==len(truelineregions)):
        for region in thetest.lineregions:
            if not region.compare(truelineregions[index]):
                Answer = False
                print("Computed LINEregion "+str(index)+" deviated from its intended value:")
                region.printregion()
                truelineregions[index].printregion()
                print("\n")
            index +=1
    else:
        Answer = False
        print("The number of computed LINEregions ("+str(len(thetest.lineregions))+") was different then what was expected ("+str(len(truelineregions))+"):")
        for region in thetest.lineregions:
            region.printregion()
        print("\n")
    
    # Find out if we actually added something in the summaries of the textalineas:
    LengthCheck = True
    for alinea in thetest.textalineas:
        sum_array = alinea.summary.split()
        lengthsum = len(sum_array)
        if (lengthsum<1)and(alinea.sum_CanbeEmpty==False): LengthCheck = False
    if not LengthCheck: 
        Answer = False
        print("Not enough words were added to some of the summaries of SplitDoc & pymupdf.")
    
    # Next, also check that we did not encounter errors during the layered_summary()-fase:
    if not (Num_Errors==0):
        Answer = False
        print("textsplitter.layered_summary() encountered " + str(Num_Errors) + "x a child with empty summary.")
        print("This should not be possible, so the test failed!")
    
    # Verify html-output:
    if use_dummy_summary: # Otherwise the output varies with ChatGPT and a fair comparison cannot be made.
        html_rapport = FileComparison(outputpath + filename + "_html_visualization.html", truthpath + filename + "_pymupdf_html_visualization.html","html")
        if not (html_rapport==""): 
            Answer = False
            print(" ==> HTML Comparison failed. Inspect the alinea-comparison and see if the true html should be adapted.")
            print(" ========== ATTENTION ===========> ")
            print("This is a integration test on SplitDoc.pdf & pymupdf. It is supposed to fully pass!")
            print("\n")
    
    # NOTE: We do NOT test for the content of the summaries. This would require the use of meaningful text 
    # (as was used in TestSummarize(), but is not used here) and a fuzzy match or another ChatGPT-call to verify,
    # or it would require the use of the dummy-mode according to TestLayeredSummary(). But then it would 
    # not be an integration test anymore. The idea is that this test can also run without the dummy-mode.
    # So we keep it like this.
    
    # Done:
    return Answer
    
# Definition of unit tests:
def TestSplitDoc_d(use_dummy_summary: bool) -> bool:
    """
    # Integration test for documentsplitting using the textsplitter-class.
    # Parameters: 
    use_dummy_summary: bool: decides whether we call ChatGPT to actually make summaries, or use a dummy summarization function.
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    filename = "TestTex"
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.set_labelname(filename)
    thetest.set_MaxSummaryLength(50)
    thetest.set_UseDummySummary(use_dummy_summary)
    thetest.set_summarization_threshold(50)
    thetest.set_LanguageChoice("Default")
    thetest.set_LanguageModel("gpt-3.5-turbo")
    thetest.set_LanguageTemperature(0.1)
    thetest.set_MaxCallRepeat(20) 
    thetest.document_metadata()
    thetest.read_native_toc("pymupdf")
    thetest.textgeneration("pymupdf")
    thetest.calculate_footerboundaries(0) # manual 496.0 & -32.0 for pymupdf
    thetest.export("default")
    thetest.fontsizehist()
    thetest.findfontregions()
    thetest.whitelinehist()
    thetest.findlineregions()
    thetest.passinfo()
    thetest.breakdown()
    thetest.shiftcontents()
    thetest.calculatetree()
    Num_Errors = thetest.layered_summary(1)
    thetest.exportdecisions()
    thetest.exportalineas("complete")
    thetest.alineas_to_html()
    
    # Next, calculate whether all required alineas exist:
    alineas_thatshouldbethere = hardcodedalineas_TestTex("pymupdf")
    Answer = AlineasPresent(alineas_thatshouldbethere,thetest.textalineas)
    
    # See if we get the correct answer for TOC-reading:
    if not (len(thetest.native_TOC)==0):
        Answer = False
        print("SplitDoc.pdf is not supposed to have an intrinsic TOC!")
    
    # Also compare calculated whiteline regions:
    truelineregions = hardcodedlineregions_pymupdf_TestTex()
    index = 0
    if (len(thetest.lineregions)==len(truelineregions)):
        for region in thetest.lineregions:
            if not region.compare(truelineregions[index]):
                Answer = False
                print("Computed LINEregion "+str(index)+" deviated from its intended value:")
                region.printregion()
                truelineregions[index].printregion()
                print("\n")
            index +=1
    else:
        Answer = False
        print("The number of computed LINEregions ("+str(len(thetest.lineregions))+") was different then what was expected ("+str(len(truelineregions))+"):")
        for region in thetest.lineregions:
            region.printregion()
        print("\n")
    
    # Find out if we actually added something in the summaries of the textalineas:
    LengthCheck = True
    for alinea in thetest.textalineas:
        sum_array = alinea.summary.split()
        lengthsum = len(sum_array)
        if (lengthsum<1)and(alinea.sum_CanbeEmpty==False): LengthCheck = False
    if not LengthCheck: 
        Answer = False
        print("Not enough words were added to some of the summaries of TestTex & pymupdf.")
    
    # Next, also check that we did not encounter errors during the layered_summary()-fase:
    if not (Num_Errors==0):
        Answer = False
        print("textsplitter.layered_summary() encountered " + str(Num_Errors) + "x a child with empty summary.")
        print("This should not be possible, so the test failed!")
    
    # Verify html-output:
    if use_dummy_summary: # Otherwise the output varies with ChatGPT and a fair comparison cannot be made.
        html_rapport = FileComparison(outputpath + filename + "_html_visualization.html", truthpath + filename + "_pymupdf_html_visualization.html","html")
        if not (html_rapport==""): 
            Answer = False
            print(" ==> HTML Comparison failed. Inspect the alinea-comparison and see if the true html should be adapted.")
            print(" ========== ATTENTION ===========> ")
            print("This is a integration test on TestTex.pdf & pymupdf. It is supposed to fully pass!")
            print("\n")
    
    # NOTE: We do NOT test for the content of the summaries. This would require the use of meaningful text 
    # (as was used in TestSummarize(), but is not used here) and a fuzzy match or another ChatGPT-call to verify,
    # or it would require the use of the dummy-mode according to TestLayeredSummary(). But then it would 
    # not be an integration test anymore. The idea is that this test can also run without the dummy-mode.
    # So we keep it like this.
    
    # Return the Answer:
    return Answer
    
# Definition of collection:    
def TestSplitDoc(use_dummy_summary: bool, test_run=0) -> bool:
    """
    # Collection-function of Integration-tests.
    # Parameters: 
    use_dummy_summary: bool: decides whether we call ChatGPT to actually make summaries, or use a dummy summarization function.
    test_run: decides which tests we run; by default it is 0 (all tests)
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    Answer = True
    
    if (test_run==1):
        
        # Then we only run pdfminer:
        TestSplitDoc_a(use_dummy_summary)
        TestSplitDoc_b(use_dummy_summary)
        return Answer
    
    elif (test_run==2):
        
        # Then we only run pymupdf:
        TestSplitDoc_c(use_dummy_summary)
        TestSplitDoc_d(use_dummy_summary)
        return Answer
    
    else:
        
        # Then, we run all:
        if (TestSplitDoc_a(use_dummy_summary)==False): Answer=False 
        print("TestSplitDoc_a()...")
        if (TestSplitDoc_b(use_dummy_summary)==False): Answer=False
        print("TestSplitDoc_b()...")
        if (TestSplitDoc_c(use_dummy_summary)==False): Answer=False
        print("TestSplitDoc_c()...")
        if (TestSplitDoc_d(use_dummy_summary)==False): Answer=False
        print("TestSplitDoc_d()...")
        
        # Now, return an actual Answer:
        return Answer

if __name__ == '__main__':
    
    # Identify parameters:
    use_dummy_summary = False
    test_run = 0
    
    if (len(sys.argv)>1):
        if (sys.argv[1]=="dummy"):
            use_dummy_summary = True
        if (sys.argv[1]=="pdfminer"):
            use_dummy_summary = True
            test_run = 1
        if (sys.argv[1]=="pymupdf"):
            use_dummy_summary = True
            test_run = 2
    
    if TestSplitDoc(use_dummy_summary,test_run):
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
