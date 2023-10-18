import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from TextPart code:
sys.path.insert(1, '../../')
from TextPart.textsplitter import textsplitter

# Imports from Tools:
sys.path.insert(2, '../Tools/')
from Platformdetection import detectsystem
from Platformdetection import MySystem

# Definition of paths:
inputpath = "../Inputs/"
outputpath = "../Calc_Outputs/"
truthpath = "../True_Outputs/"

# Definition of unit tests:
def textsplitter_basetest() -> bool:
    """
    # Unit test for the basic functionality of the textsplitter-class:
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Create the testclass:
    thetest = textsplitter()
    Answer = True
    
    # Check default values of parameters:
    if not(thetest.get_labelname()=="TextSplitter"):
        Answer = False
        print("Testing the default-value for textsplitter.labelname failed.")
    if not(thetest.get_histogramsize()==100):
        Answer = False
        print("Testing the default-value for textsplitter.histogramsize failed.")
    if not(thetest.get_MaxSummaryLength()==50):
        Answer = False
        print("Testing the default-value for textsplitter.MaxSummaryLength failed.")
    if not(thetest.get_summarization_threshold()==50):
        Answer = False
        print("Testing the default-value for textsplitter.summarization_threshold failed.")
    if not(thetest.get_LanguageModel()=="gpt-3.5-turbo"):
        Answer = False
        print("Testing the default-value for textsplitter.LanguageModel failed.")
    if not(thetest.get_LanguageChoice()=="Default"):
        Answer = False
        print("Testing the default-value for textsplitter.LanguageChoice failed.")
    if not(thetest.get_UseDummySummary()==True):
        Answer = False
        print("Testing the default-value for textsplitter.UseDummySummary failed.")
    if (abs(thetest.get_LanguageTemperature()-0.1)>1e-3):
        Answer = False
        print("Testing the default-value for textsplitter.LanguageTemperature failed.")
    if not(thetest.get_MaxCallRepeat()==20):
        Answer = False
        print("Testing the default-value for textsplitter.MaxCallRepeat failed.")

    # Use the setters:
    thetest.set_labelname("SomeLabel")
    thetest.set_histogramsize(200)
    thetest.set_MaxSummaryLength(60)
    thetest.set_summarization_threshold(70)
    thetest.set_LanguageModel("text-davinci-003")
    thetest.set_LanguageChoice("English")
    thetest.set_UseDummySummary(True)
    thetest.set_LanguageTemperature(0.23)
    thetest.set_MaxCallRepeat(18) 
    
    # Check the values again:
    if not(thetest.get_labelname()=="SomeLabel"):
        Answer = False
        print("Testing the manually setted value for textsplitter.labelname failed.")
    if not(thetest.get_histogramsize()==200):
        Answer = False
        print("Testing the manually setted value for textsplitter.histogramsize failed.")
    if not(thetest.get_MaxSummaryLength()==60):
        Answer = False
        print("Testing the manually setted value for textsplitter.MaxSummaryLength failed.")
    if not(thetest.get_summarization_threshold()==70):
        Answer = False
        print("Testing the manually setted value for textsplitter.summarization_threshold failed.")
    if not(thetest.get_LanguageModel()=="text-davinci-003"):
        Answer = False
        print("Testing the manually setted value for textsplitter.LanguageModel failed.")
    if not(thetest.get_LanguageChoice()=="English"):
        Answer = False
        print("Testing the manually setted value for textsplitter.LanguageChoice failed.")
    if not(thetest.get_UseDummySummary()==True):
        Answer = False
        print("Testing the manually setted value for textsplitter.UseDummySummary failed.")
    if (abs(thetest.get_LanguageTemperature()-0.23)>1e-3):
        Answer = False
        print("Testing the manually setted value for textsplitter.LanguageTemperature failed.")
    if not(thetest.get_MaxCallRepeat()==18):
        Answer = False
        print("Testing the manually setted value for textsplitter.MaxCallRepeat failed.")
    
    # Next, use the standard-params function:
    thetest.standard_params()
    
    # And check the values:
    if not(thetest.get_labelname()=="TextSplitter"):
        Answer = False
        print("Testing the standard_params-value for textsplitter.labelname failed.")
    if not(thetest.get_histogramsize()==100):
        Answer = False
        print("Testing the standard_params-value for textsplitter.histogramsize failed.")
    if not(thetest.get_MaxSummaryLength()==50):
        Answer = False
        print("Testing the standard_params-value for textsplitter.MaxSummaryLength failed.")
    if not(thetest.get_summarization_threshold()==50):
        Answer = False
        print("Testing the standard_params-value for textsplitter.summarization_threshold failed.")
    if not(thetest.get_LanguageModel()=="gpt-3.5-turbo"):
        Answer = False
        print("Testing the standard_params-value for textsplitter.LanguageModel failed.")
    if not(thetest.get_LanguageChoice()=="Default"):
        Answer = False
        print("Testing the standard_params-value for textsplitter.LanguageChoice failed.")
    if not(thetest.get_UseDummySummary()==True):
        Answer = False
        print("Testing the standard_params-value for textsplitter.UseDummySummary failed.")
    if (abs(thetest.get_LanguageTemperature()-0.1)>1e-3):
        Answer = False
        print("Testing the standard_params-value for textsplitter.LanguageTemperature failed.")
    if not(thetest.get_MaxCallRepeat()==20):
        Answer = False
        print("Testing the standard_params-value for textsplitter.MaxCallRepeat failed.")
    
    # That's it. So complete the test:
    return Answer

def textsplitter_processtest() -> bool:
    """
    # Unit test for the process-functionality of the textsplitter-class:
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Simply create a textsplitter-class and make it run (in dummy-mode)
    # on an extremely simple textfile:
    
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname("TextExtraction_001")
    thetest.set_outputpath(outputpath)
    thetest.standard_params()
    thetest.set_UseDummySummary(True) # we don't want this to change even if standard_params is adapted.
    thetest.set_ruleverbosity(0)
    thetest.set_verbosetextline("a small test")
    thetest.process()
    
    return True

def textsplitter_metadatatest() -> bool:
    """
    # Unit test for the metadata-functionality of the textsplitter-class:
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Simply create a textsplitter-class and make it run (in dummy-mode)
    # on an extremely simple textfile:
    
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname("TextExtraction_001")
    thetest.set_outputpath(outputpath)
    thetest.document_metadata()
    
    # Test that we have a creation-date:
    Answer = False
    if not (thetest.doc_metadata_creationdate=="None"):
        Answer = True
    
    # Return the Answer:
    return Answer

def textsplitter_readingspacestest_a() -> bool:
    """
    # Unit test test for text reading with lots of spaces.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname("Spaces")
    thetest.set_outputpath(outputpath)
    thetest.standard_params()
    thetest.textgeneration("pdfminer")
    
    outcome = ["This is some text with spaces","and more","even more so.",""]
    Answer = True
    if not (len(thetest.textcontent)==4):
        Answer = False
        print("We failed to extract the correct amount of textlines.")
    else:
        index = 0
        for textline in thetest.textcontent:
            if not (textline==outcome[index]):
                print("Expected = <"+outcome[index]+"> while we got <"+textline+">")
                Answer = False
            index = index + 1
    
    # Done:
    return Answer

def textsplitter_readingspacestest_b() -> bool:
    """
    # Unit test test for text reading with lots of spaces.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname("Spaces")
    thetest.set_outputpath(outputpath)
    thetest.standard_params()
    thetest.textgeneration("pymupdf")
    
    outcome = ["This is some text with spaces","and more","even more so.",""]
    Answer = True
    if not (len(thetest.textcontent)==4):
        Answer = False
        print("We failed to extract the correct amount of textlines.")
    else:
        index = 0
        for textline in thetest.textcontent:
            if not (textline==outcome[index]):
                print("Expected = <"+outcome[index]+"> while we got <"+textline+">")
                Answer = False
            index = index + 1
    
    # Done:
    return Answer

# Definition of collection:    
def TestTextSplitter() -> bool:
    """
    # Collection-function of unit-tests.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    
    Answer = True
    
    if (textsplitter_basetest()==False): 
        Answer=False
        print('\n==> Basetest for textsplitter-class failed!\n')
    if (textsplitter_metadatatest()==False):
        Answer = False
        print('\n==> document_metadata unit-test for textsplitter-class failed!\n')
    if (textsplitter_processtest()==False): 
        Answer=False
        print('\n==> process unit-test for textsplitter-class failed!\n')
    if (textsplitter_readingspacestest_a()==False): 
        Answer=False
        print('\n==> textsplitter_readingspacestest_a unit-test for textsplitter-class failed!\n')
    if (textsplitter_readingspacestest_b()==False): 
        Answer=False
        print('\n==> textsplitter_readingspacestest_b unit-test for textsplitter-class failed!\n')

    return Answer

if __name__ == '__main__':
    if TestTextSplitter():
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
