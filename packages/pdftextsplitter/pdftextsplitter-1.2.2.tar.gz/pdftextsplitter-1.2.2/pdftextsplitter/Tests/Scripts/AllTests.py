# Motherscript to call for running all tests.
import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Set proper parameters:
use_dummy_summary = True

# All Test-imports:
from TextExtraction_001 import TextExtraction_001
from TextExtraction_002 import TextExtraction_002
from TestSplitting import TestSplitting
from TestCountries import TestCountries
from TestTitleLines import TestTitleLines
from TestOpenAI import TestOpenAI
from TestKeywords import TestKeywords
from TestWordCloud import TestWordCloud
from TestTextPart import TestTextPart
from TestTextSplitter import TestTextSplitter
from TestSplitDoc import TestSplitDoc
from TestFontSizeHist import TestFontSizeHist
from TestFontRegions import TestFontRegions
from TestStringMatch import TestStringMatch
from TestRegex import TestRegex
from TestRules import TestRules
from TestExports import TestExports
from TestPassInfo import TestPassInfo
from TestBreakDown import TestBreakDown
from TestShifting import TestShifting
from TestMasterRule import TestMasterRule
from TestTreeStructure import TestTreeStructure
from TestSummarize import TestSummarize
from TestLayeredSummary import TestLayeredSummary
from TestHTMLPrint import TestHTMLconversion
from TestWhiteLines import TestWhiteLines
from TestTOCExtraction import TestTOCExtraction
from TestWhiteLineHist import TestWhiteLineHist
from TestLineRegions import TestLineRegions
from TestFontStyleRecognition import TestFontStyleRecognition
from TestTwoColumns import TestTwoColumns
from RegressionTests import RegressionTests
from TestEnumerations import TestEnumerations
from TestCalculateBoundaries import TestCalculateBoundaries
# NOTE: Add new tests here:

# Function definition: simply call all unit tests:
def AllTests(use_dummy_summary: bool) -> bool:
    """
    Collection-function of all imported tests.
    Parameters: 
    use_dummy_summary: bool: decides whether we actually call ChatGPT during the tests, or use a dummy-function for summarization.
    # Returns (bool): succes of the text.
    
    NOTE: We do use an Answer-boolian as an in-between, because we do want all tests 
    to run (and give a full report), not that it breaks down at the first fail.
    """
    
    # ---------------------------------------------------------
    
    # Definition of the final outcome variable:
    Answer = True
    
    #############################################################
    ####################### Unit Tests ##########################
    #############################################################
    
    # These are tests that only execute a single piece of code
    # or function. The same script may contain multiple unit tests.
    # In that case, the same code piece is tested for different
    # scenario's (like the use of different methods/libraries
    # for the same task: reading tekst from PDF's)
    
    # Unit tests for the function to identify country names in a given string. Multple tests; one for each world-part and one for no country at all.
    if TestCountries(): print(" ==>        ==> TestCountries() successful.")
    else: 
        Answer = False
        print(" ==>        ==> TestCountries() FAILED!!!!.")

    # Unit test for keyword extraction. Multiple tests: one for each extractor (rake_nltk and yake).
    if TestKeywords(): print(" ==>        ==> TestKeywords() successful.")
    else: 
        Answer = False
        print(" ==>        ==> TestKeywords() FAILED!!!!.")
    
    # Unit test for cmmunication-script with ChatGPT. Multiple tests: asking ChatGPT different questions.
    # For dummy summaries, it is meaningless to test this. Also, the dummy is meant for when the ChatGPT-connection
    # does not work, so then it would be pointless to specifically test this connection, which is what TestOpenAI() does.
    if not use_dummy_summary:
        if TestOpenAI(): print(" ==>        ==> TestOpenAI() successful.")
        else: 
            Answer = False
            print(" ==>        ==> TestOpenAI() FAILED!!!!.")
    
    # Unit test for reading text from PDF's. Multiple tests; one for each library we use (tested against the same 'true' output).
    if TextExtraction_001(): print(" ==>        ==> TextExtraction_001() successful.")
    else: 
        Answer = False
        print(" ==>        ==> TextExtraction_001() FAILED!!!!.")

    # Unit test for reading text from PDF's. Multiple tests; same as TextExtraction_001 but with a different source-file.
    if TextExtraction_002(): print(" ==>        ==> TextExtraction_002() successful.")
    else: 
        Answer = False
        print(" ==>        ==> TextExtraction_002() FAILED!!!!.")

    # Unit test for the function that returns the lines to find the title of a document (hard-coded). Multiple tests; one for each doc.
    if TestTitleLines(): print(" ==>        ==> TestTitleLines() successful.")
    else: 
        Answer = False
        print(" ==>        ==> TestTitleLines() FAILED!!!!.")
    
    # Unit test for generation of a wordcloud from a given .txt-file.
    if TestWordCloud(): print(" ==>        ==> TestWordCloud() successful.")
    else: 
        Answer = False
        print(" ==>        ==> TestWordCloud() FAILED!!!!.")
    
    # Unit test for basic functionality of the textpart-class. Multiple tests, like testing get/set, export, load, etc.
    if TestTextPart(): print(" ==>        ==> TestTextPart() successful.")
    else: 
        Answer = False
        print(" ==>        ==> TestTextPart() FAILED!!!!.")
        
    # Unit test for basic functionality of the textsplitter-class. Multiple tests, like testing get/set, process, etc.
    if TestTextSplitter(): print(" ==>        ==> TestTextSplitter() successful.")
    else: 
        Answer = False
        print(" ==>        ==> TestTextSplitter() FAILED!!!!.")
        
    # Unit test for the creation of font size histograms:
    if TestFontSizeHist(): print(" ==>        ==> TestFontSizeHist() successful.")
    else: 
        Answer = False
        print(" ==>        ==> TestFontSizeHist() FAILED!!!!.")
    
    # Unit test for basic functionality of fontregion-class & unit tests for findfontregions() in textpart-class.
    if TestFontRegions(): print(" ==>        ==> TestFontRegions() successful.")
    else: 
        Answer = False
        print(" ==>        ==> TestFontRegions() FAILED!!!!.")
    
    # Unit test for stringmatch-function that can compare different strings on a scale 0.0-1.0
    if TestStringMatch(): print(" ==>        ==> TestStringMatch() successful.")
    else: 
        Answer = False
        print(" ==>        ==> TestStringMatch() FAILED!!!!.")
    
    # Unit test for the various regex-expressions in regex_expressions.py
    if TestRegex(): print(" ==>        ==> TestRegex() successful.")
    else: 
        Answer = False
        print(" ==>        ==> TestRegex() FAILED!!!!.")
    
    # Unit test for the various selection rules of the different children from textpart.
    if TestRules(): print(" ==>        ==> TestRules() successful.")
    else: 
        Answer = False
        print(" ==>        ==> TestRules() FAILED!!!!.")
    
    # Unit test for various export functions (to write to .txt-files) of the textsplitter class.
    if TestExports(): print(" ==>        ==> TestExports() successful.")
    else: 
        Answer = False
        print(" ==>        ==> TestExports() FAILED!!!!.")
    
    # Unit test for the passinfo-function in the textsplitter-class that makes sure all the elements in textsplitter have access to basic info.
    if TestPassInfo(): print(" ==>        ==> TestPassInfo() successful.")
    else: 
        Answer = False
        print(" ==>        ==> TestPassInfo() FAILED!!!!.")
    
    # Unit test for the breadown-function in the textsplitter-class. This function is the one that actually performs the document splitting.
    if TestBreakDown(): print(" ==>        ==> TestBreakDown() successful.")
    else: 
        Answer = False
        print(" ==>        ==> TestBreakDown() FAILED!!!!.")
        
    # Unit test for the shiftcontents-function in the textsplitter-class. This function rearranges content for signed letters, so that the right content belongs to the right politician.
    if TestShifting(): print(" ==>        ==> TestShifting() successful.")
    else: 
        Answer = False
        print(" ==>        ==> TestShifting() FAILED!!!!.")
    
    # Unit test for the masterrule-function in the textsplitter-class. This function takes the dependencies into account between selection rules.
    if TestMasterRule(): print(" ==>        ==> TestMasterRule() successful.")
    else: 
        Answer = False
        print(" ==>        ==> TestMasterRule() FAILED!!!!.")
        
    # Unit test for the calculatetree()-function of the textsplitter-class that identifies parentID's & horizontal orderings.
    if TestTreeStructure(): print(" ==>        ==> TestTreeStructure() successful.")
    else: 
        Answer = False
        print(" ==>        ==> TestTreeStructure() FAILED!!!!.")
    
    # Unit test for the summarize()-function of textsplitter that summarizes text using ChatGPT. We test for general parameters like length of the summary.
    if TestSummarize(use_dummy_summary): print(" ==>        ==> TestSummarize() successful.")
    else: 
        Answer = False
        print(" ==>        ==> TestSummarize() FAILED!!!!.")
    
    # Unit test for the layered_summary()-function of textsplitter that uses the summary()-function to provide a layered summary for all textalinea-elements in the document.
    if TestLayeredSummary(): print(" ==>        ==> TestLayeredSummary() successful.")
    else: 
        Answer = False
        print(" ==>        ==> TestLayeredSummary() FAILED!!!!.")
        
    # Unit test for HTML-conversion of the textalineas-structure. The html-visualization can be viewed with any browser.
    if TestHTMLconversion(): print(" ==>        ==> TestHTMLConversion() successful.")
    else:
        Answer = False
        print(" ==>        ==> TestHTMLConversion() FAILED!!!!.")
        
    # Unit test for extraction of the native Table Of Contents (TOC) from a PDF.
    if TestTOCExtraction(): print(" ==>        ==> TestTOCExtraction() successful.")
    else:
        Answer = False
        print(" ==>        ==> TestTOCExtraction() FAILED!!!.")
    
    # Unit test for creating data & histograms on whitelines between textual lines in PDF documents.
    if TestWhiteLineHist(): print(" ==>        ==> TestWhiteLineHist() successful.")
    else:
        Answer = False
        print(" ==>        ==> TestWhiteLineHist() FAILED!!!.")
    
    # Unit test for finding line regions and searching in them.
    if TestLineRegions(): print(" ==>        ==> TestLineRegions() successful.")
    else:
        Answer = False
        print(" ==>        ==> TestLineRegions() FAILED!!!.")

    # Unit test for font style recognition, multiple tests; one for each method and font style aspect
    if TestFontStyleRecognition(): print(" ==>        ==> TestFontStyleRecognition() successful.")
    else:
        Answer = False
        print(" ==>        ==> TestFontStyleRecognition() FAILED!!!.")

    # Unit test for the calculation of header & footer boundaries from hardcoded textlines of SplitDoc.
    if TestCalculateBoundaries(): print(" ==>        ==> TestCalculateBoundaries() successful.")
    else:
        Answer = False
        print(" ==>        ==> TestCalculateBoundaries() FAILED!!!.")

    # NOTE: Add new unit tests here

    #############################################################
    ####################### Integration Tests ###################
    #############################################################
    
    # These are tests that multiple pieces of code at the same time.
    # The same script may contain multiple integration tests.
    # In that case, the same code piece is tested for different
    # scenario's (like the use of different methods/libraries
    # for the same task: reading tekst from PDF's)
    
    # Integration test for splitting documents. The document contains chapters, sections, headers and footers, that all have to be identified.
    if TestSplitDoc(use_dummy_summary): print(" ==>        ==> TestSplitDoc() successful.")
    else: 
        Answer = False
        print(" ==>        ==> TestSplitDoc() FAILED!!!!.")
    
    # Integration test for the initial rule-based splitting of textfiles. It applies all rules at once to an actual doc (not a small test-doc).
    if TestSplitting(): print(" ==>        ==> TestSplitting() successful.")
    else: 
        Answer = False
        print(" ==>        ==> TestSplitting() FAILED!!!!.")

    # Integration test for testing if complex enumerations are appointed correctly.
    if TestEnumerations(): print(" ==>        ==> TestEnumerations() successful.")
    else: 
        Answer = False
        print(" ==>        ==> TestEnumerations() FAILED!!!!.")
    
    # Integration test for the whitelines-analysis of documents. The documents contain a small selection of actual EU-text, so that a realistic sample
    # of different whitelines is used.
    if TestWhiteLines(use_dummy_summary): print(" ==>        ==> TestWhiteLines() successful.")
    else: 
        Answer = False
        print(" ==>        ==> TestWhiteLines() FAILED!!!!.")
    
    # Integration test for handling a 2-column page with highlighted text.
    if TestTwoColumns(use_dummy_summary): print(" ==>        ==> TestTwoColumns() successful.")
    else: 
        Answer = False
        print(" ==>        ==> TestTwoColumns() FAILED!!!!.")
     
    # NOTE: Add new integration tests here
    
    #############################################################
    
    #############################################################
    ####################### Regression Tests ####################
    #############################################################
    
    # These are different from integration tests in the sense that
    # they use complete documents, not just toy docs meant to trigger
    # a specific type of behaviour.
    
    # ATTENTION: We made a team decision to not add regression tests to test_collection.py
    # so that code coverage will not measure it. A regression test will probably cover 
    # almost all code, so then code coverage would become meaningless. For integration tests,
    # the situation is different, as those work with small toy-docs designed to trigger
    # only a specific behavious; regression tests work with full documents from the users.
    
    # Regression test for splitting documents. The document contains chapters, sections, headers and footers, that all have to be identified.
    # NOTE: We will always do this in dummy-mode; as a test run should not burn incredible amounts of ChatGPT-calls.
    
    if RegressionTests(True): print(" ==>        ==> RegressionTests() successful.")
    else: 
        Answer = False
        print(" ==>        ==> RegressionTests() FAILED!!!!.")
    
    # NOTE: Add new regression tests here
    
    return Answer

# Actually run the tests:
if __name__ == '__main__':
    
    # Identify parameters:
    use_dummy_summary = False
    if (len(sys.argv)>1):
        if (sys.argv[1]=="dummy"):
            use_dummy_summary = True
    
    # Perform the test:
    if AllTests(use_dummy_summary):
        print("\n\n ==> CONGRATULATIONS!!! All tests were successful! <==\n\n")
    else:
        print("\n\n ==> ERROR!!! Some tests failed!             <==\n ==> ERROR!!! Please investigate the report. <==\n\n")
