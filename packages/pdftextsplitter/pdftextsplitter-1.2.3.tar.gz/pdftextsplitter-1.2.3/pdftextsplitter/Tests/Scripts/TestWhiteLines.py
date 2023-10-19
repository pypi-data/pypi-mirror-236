import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from TextPart code:
sys.path.insert(1, '../../')
from TextPart.lineregion import lineregion
from TextPart.textsplitter import textsplitter

# Imports from Tools:
sys.path.insert(2, '../Tools/')
from FileComparison import FileComparison
from hardcodedlineregions import hardcodedlineregions_pdfminer_LineTest1
from hardcodedlineregions import hardcodedlineregions_pymupdf_LineTest1
from hardcodedfontregions import hardcodedfontregions_pdfminer_LineTest1
from hardcodedfontregions import hardcodedfontregions_pymupdf_LineTest1
from hardcodedlineregions import hardcodedlineregions_pdfminer_LineTest2
from hardcodedlineregions import hardcodedlineregions_pymupdf_LineTest2
from hardcodedfontregions import hardcodedfontregions_pdfminer_LineTest2
from hardcodedfontregions import hardcodedfontregions_pymupdf_LineTest2
from hardcoded_TOC_Elements import hardcoded_LineTest1_TOC_pdfminer
from hardcoded_TOC_Elements import hardcoded_LineTest1_TOC_pymupdf
from hardcoded_TOC_Elements import hardcoded_LineTest2_pdfminer_TOC
from hardcoded_TOC_Elements import hardcoded_LineTest2_pymupdf_TOC
from TOCElementsPresent import TOCElementsPresent

# Definition of paths:
inputpath = "../Inputs/"
outputpath = "../Calc_Outputs/"
truthpath = "../True_Outputs/"

# Definition of unit tests:
def TestWhiteLines_a(use_dummy_summary: bool) -> bool:
    """
    # Integration test for analyzing whitelines using the textsplitter-class.
    # NOTE: We will also use this one as an intergartion test form the standard_params & process test
    # Parameters: 
    use_dummy_summary: bool: decides whether we call ChatGPT to actually make summaries, or use a dummy summarization function.
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    filename = "LineTest1"
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.standard_params()
    Num_Errors = thetest.process()
    
    # Declare the answer:
    Answer = True

    # Check whether we obtain the correct header/footer boundaries (manual: 1000.0 & 55.0):
    if not ((thetest.footerboundary<40.0)and(thetest.footerboundary>thetest.min_vert)): Answer = False
    if not (thetest.headerboundary>thetest.max_vert): Answer = False

    if not Answer:
        print("For " + filename + " we obtained headerboundary = " + str(thetest.headerboundary) + ", which should be close to 1000.0")
        print("For " + filename + " we obtained footerboundary = " + str(thetest.footerboundary) + ", which should be close to   55.0")
        print("For " + filename + " the full range of position = [" + str(thetest.min_vert) + "," + str(thetest.max_vert) + "]")
        Answer = False
    
    # Test whether all required alineas are there:
    TOClist = hardcoded_LineTest1_TOC_pdfminer()
    if not TOCElementsPresent(TOClist,thetest.textalineas): Answer = False
    
    # See if we get the correct answer for TOC-reading:
    if not (len(thetest.native_TOC)==0):
        Answer = False
        print("LineTest1.pdf is not supposed to have an intrinsic TOC!")
    
    # Also compare calculated font regions:
    truefontregions = hardcodedfontregions_pdfminer_LineTest1()
    index = 0
    if (len(thetest.fontregions)==len(truefontregions)):
        for region in thetest.fontregions:
            if not region.compare(truefontregions[index]):
                Answer = False
                print("Computed FONTregion "+str(index)+" deviated from its intended value:")
                region.printregion()
                truefontregions[index].printregion()
                print("\n")
            index +=1
    else:
        Answer = False
        print("The number of computed FONTregions ("+str(len(thetest.fontregions))+") was different then what was expected ("+str(len(truefontregions))+"):")
        for region in thetest.fontregions:
            region.printregion()
        print("\n")
        
    # Also compare calculated lineregions:
    truelineregions = hardcodedlineregions_pdfminer_LineTest1()
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
        print("Not enough words were added to so of the summaries of LineTest1 & pdfminer.")
    
    # Next, also check that we did not encounter errors during the layered_summary()-fase:
    if (Num_Errors>0):
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
            print("This is a integration test on LineTest1.pdf & pdfminer. It is supposed to fully pass!")
            print("\n")
    
    # NOTE: We do NOT test for the content of the summaries. This would require the use of meaningful text 
    # (as was used in TestSummarize(), but is not used here) and a fuzzy match or another ChatGPT-call to verify,
    # or it would require the use of the dummy-mode according to TestLayeredSummary(). But then it would 
    # not be an integration test anymore. The idea is that this test can also run without the dummy-mode.
    # So we keep it like this.
  
    # Done:
    return Answer

def TestWhiteLines_b(use_dummy_summary: bool) -> bool:
    """
    # Integration test for analyzing whitelines using the textsplitter-class.
    # Parameters: 
    use_dummy_summary: bool: decides whether we call ChatGPT to actually make summaries, or use a dummy summarization function.
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    filename = "LineTest2"
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
    thetest.set_ruleverbosity(1)
    thetest.set_verbosetextline("sjkhfjh")
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
    
    # Declare the answer:
    Answer = True

    # Check whether we obtain the correct header/footer boundaries (manual: 1000.0 & 55.0):
    if not ((thetest.footerboundary<55.0)and(thetest.footerboundary>50.0)): Answer = False
    if not (thetest.headerboundary>thetest.max_vert): Answer = False

    if not Answer:
        print("For " + filename + " we obtained headerboundary = " + str(thetest.headerboundary) + ", which should be close to 1000.0")
        print("For " + filename + " we obtained footerboundary = " + str(thetest.footerboundary) + ", which should be close to   55.0")
        print("For " + filename + " the full range of position = [" + str(thetest.min_vert) + "," + str(thetest.max_vert) + "]")
        Answer = False
    
    # Test whether all required alineas are there:
    TOClist = hardcoded_LineTest2_pdfminer_TOC()
    if not TOCElementsPresent(TOClist,thetest.textalineas): Answer = False
    
    # See if we get the correct answer for TOC-reading:
    if not (len(thetest.native_TOC)==0):
        Answer = False
        print("LineTest2.pdf is not supposed to have an intrinsic TOC!")
    
    # Also compare calculated font regions:
    truefontregions = hardcodedfontregions_pdfminer_LineTest2()
    index = 0
    if (len(thetest.fontregions)==len(truefontregions)):
        for region in thetest.fontregions:
            if not region.compare(truefontregions[index]):
                Answer = False
                print("Computed FONTregion "+str(index)+" deviated from its intended value:")
                region.printregion()
                truefontregions[index].printregion()
                print("\n")
            index +=1
    else:
        Answer = False
        print("The number of computed FONTregions ("+str(len(thetest.fontregions))+") was different then what was expected ("+str(len(truefontregions))+"):")
        for region in thetest.fontregions:
            region.printregion()
        print("\n")
        
    # Also compare calculated lineregions:
    truelineregions = hardcodedlineregions_pdfminer_LineTest2()
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
        print("Not enough words were added to so of the summaries of LineTest2 & pdfminer.")
    
    # Next, also check that we did not encounter errors during the layered_summary()-fase:
    if (Num_Errors>0):
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
            print("This is a integration test on LineTest2.pdf & pdfminer. It is supposed to fully pass!")
            print("\n")
    
    # NOTE: We do NOT test for the content of the summaries. This would require the use of meaningful text 
    # (as was used in TestSummarize(), but is not used here) and a fuzzy match or another ChatGPT-call to verify,
    # or it would require the use of the dummy-mode according to TestLayeredSummary(). But then it would 
    # not be an integration test anymore. The idea is that this test can also run without the dummy-mode.
    # So we keep it like this.
  
    # Done:
    return Answer

def TestWhiteLines_c(use_dummy_summary: bool) -> bool:
    """
    # Integration test for analyzing whitelines using the textsplitter-class.
    # Parameters: 
    use_dummy_summary: bool: decides whether we call ChatGPT to actually make summaries, or use a dummy summarization function.
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    filename = "LineTest1"
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
    thetest.set_ruleverbosity(1)
    thetest.set_verbosetextline("djfbh")
    thetest.document_metadata()
    thetest.read_native_toc("pymupdf")
    thetest.textgeneration("pymupdf")
    thetest.calculate_footerboundaries(0) # Manual: 1000.0 & -107.0 for pymupdf
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
    
    # Declare the answer:
    Answer = True
    
    # Test whether all required alineas are there:
    TOClist = hardcoded_LineTest1_TOC_pymupdf()
    if not TOCElementsPresent(TOClist,thetest.textalineas): Answer = False
    
    # See if we get the correct answer for TOC-reading:
    if not (len(thetest.native_TOC)==0):
        Answer = False
        print("LineTest1.pdf is not supposed to have an intrinsic TOC!")
    
    # Also compare calculated font regions:
    truefontregions = hardcodedfontregions_pymupdf_LineTest1()
    index = 0
    if (len(thetest.fontregions)==len(truefontregions)):
        for region in thetest.fontregions:
            if not region.compare(truefontregions[index]):
                Answer = False
                print("Computed FONTregion "+str(index)+" deviated from its intended value:")
                region.printregion()
                truefontregions[index].printregion()
                print("\n")
            index +=1
    else:
        Answer = False
        print("The number of computed FONTregions ("+str(len(thetest.fontregions))+") was different then what was expected ("+str(len(truefontregions))+"):")
        for region in thetest.fontregions:
            region.printregion()
        print("\n")
        
    # Also compare calculated lineregions:
    truelineregions = hardcodedlineregions_pymupdf_LineTest1()
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
        print("Not enough words were added to so of the summaries of LineTest1 & pymupdf.")
    
    # Next, also check that we did not encounter errors during the layered_summary()-fase:
    if (Num_Errors>0):
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
            print("This is a integration test on LineTest1.pdf & pymupdf. It is supposed to fully pass!")
            print("\n")
    
    # NOTE: We do NOT test for the content of the summaries. This would require the use of meaningful text 
    # (as was used in TestSummarize(), but is not used here) and a fuzzy match or another ChatGPT-call to verify,
    # or it would require the use of the dummy-mode according to TestLayeredSummary(). But then it would 
    # not be an integration test anymore. The idea is that this test can also run without the dummy-mode.
    # So we keep it like this.
  
    # Done:
    return Answer

def TestWhiteLines_d(use_dummy_summary: bool) -> bool:
    """
    # Integration test for analyzing whitelines using the textsplitter-class.
    # Parameters: 
    use_dummy_summary: bool: decides whether we call ChatGPT to actually make summaries, or use a dummy summarization function.
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    filename = "LineTest2"
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
    thetest.set_ruleverbosity(1)
    thetest.set_verbosetextline("sjahfj")
    thetest.document_metadata()
    thetest.read_native_toc("pymupdf")
    thetest.textgeneration("pymupdf")
    thetest.calculate_footerboundaries(0) # Manual: 1000.0 & -107.0 for pymupdf.
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
   
    # Declare the answer:
    Answer = True
    
    # Test whether all required alineas are there:
    TOClist = hardcoded_LineTest2_pymupdf_TOC()
    if not TOCElementsPresent(TOClist,thetest.textalineas): Answer = False
    
    # See if we get the correct answer for TOC-reading:
    if not (len(thetest.native_TOC)==0):
        Answer = False
        print("LineTest2.pdf is not supposed to have an intrinsic TOC!")
    
    # Also compare calculated font regions:
    truefontregions = hardcodedfontregions_pymupdf_LineTest2()
    index = 0
    if (len(thetest.fontregions)==len(truefontregions)):
        for region in thetest.fontregions:
            if not region.compare(truefontregions[index]):
                Answer = False
                print("Computed FONTregion "+str(index)+" deviated from its intended value:")
                region.printregion()
                truefontregions[index].printregion()
                print("\n")
            index +=1
    else:
        Answer = False
        print("The number of computed FONTregions ("+str(len(thetest.fontregions))+") was different then what was expected ("+str(len(truefontregions))+"):")
        for region in thetest.fontregions:
            region.printregion()
        print("\n")
        
    # Also compare calculated lineregions:
    truelineregions = hardcodedlineregions_pymupdf_LineTest2()
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
        print("Not enough words were added to so of the summaries of LineTest2 & pymupdf.")
    
    # Next, also check that we did not encounter errors during the layered_summary()-fase:
    if (Num_Errors>0):
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
            print("This is a integration test on LineTest2.pdf & pymupdf. It is supposed to fully pass!")
            print("\n")
    
    # NOTE: We do NOT test for the content of the summaries. This would require the use of meaningful text 
    # (as was used in TestSummarize(), but is not used here) and a fuzzy match or another ChatGPT-call to verify,
    # or it would require the use of the dummy-mode according to TestLayeredSummary(). But then it would 
    # not be an integration test anymore. The idea is that this test can also run without the dummy-mode.
    # So we keep it like this.
  
    # Done:
    return Answer

# Definition of collection:    
def TestWhiteLines(use_dummy_summary: bool, test_run=0) -> bool:
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
        TestWhiteLines_a(use_dummy_summary)
        TestWhiteLines_b(use_dummy_summary)
        return Answer
    
    elif (test_run==2):
        
        # Then we only run pymupdf:
        TestWhiteLines_c(use_dummy_summary)
        TestWhiteLines_d(use_dummy_summary)
        return Answer
    
    else:
        
        # Then, we run all:
        if (TestWhiteLines_a(use_dummy_summary)==False): Answer=False 
        print("TestWhiteLines_a()...")
        if (TestWhiteLines_b(use_dummy_summary)==False): Answer=False 
        print("TestWhiteLines_b()...")
        if (TestWhiteLines_c(use_dummy_summary)==False): Answer=False 
        print("TestWhiteLines_c()...")
        if (TestWhiteLines_d(use_dummy_summary)==False): Answer=False 
        print("TestWhiteLines_d()...")
    
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
    
    if TestWhiteLines(use_dummy_summary,test_run):
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
