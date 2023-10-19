import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from TextPart code:
sys.path.insert(1, '../../')
from TextPart.textpart import textpart
from TextPart.textsplitter import textsplitter
from TextPart.fontregion import fontregion
from TextPart.lineregion import lineregion
from TextPart.CurrentLine import CurrentLine
from TextPart.textalinea import textalinea

# Imports from Tools:
sys.path.insert(2, '../Tools/')
from hardcodedalineas import hardcodedalineas_SplitDoc
from hardcodedalineas import hardcodedalineas_TestTex
from hardcoded_TOC_Elements import hardcoded_DNN_TOC
from hardcoded_TOC_Elements import hardcoded_cellar_TOC
from FileComparison import FileComparison
from TOCElementsPresent import TOCElementsPresent
from AlineasPresent import AlineasPresent
from CompareImages import CompareImages

# Definition of paths:
inputpath = "../Inputs/"
outputpath = "../Calc_Outputs/"
truthpath = "../True_Outputs/"

# Definition of unit tests:
def TestPrints() -> bool:
    """
    # This script executes the print-functions in classes in the code.
    # Normally, we would not do this, but for the purpose of code
    # coverage, we will run them once here. As such, this function is 
    # NOT added to AllTests.py, but it is added to test_collection.py
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Begin by the executing print statements of fontregion:
    testregion1 = fontregion()
    testregion1.printregion()
    testregion1.printcode()
    
    # Next, do lineregion:
    testregion2 = lineregion()
    testregion2.printregion()
    testregion2.printcode()
    
    # Next, do textalinea:
    alineas = hardcodedalineas_SplitDoc("pdfminer")
    alineas[0].printalinea()
    
    # Do a Native-TOC element:
    Correct_TOC_elements = hardcoded_DNN_TOC()
    Correct_TOC_elements[0].print_TOC_element()
    Correct_TOC_elements[0].printcode()
    
    # Do a CurrentLine element:
    test_textline = CurrentLine()
    test_textline.printcode()
    
    # Next, do it for verbose summarization:
    thetest = textsplitter()
    print(thetest.alineas_to_html())
    thetest.set_labelname("VerboseSummarizationTest")
    thetest.set_documentname("Musk_wordcloud")
    thetest.set_documentpath(inputpath)
    thetest.set_outputpath(outputpath)
    thetest.set_UseDummySummary(False)
    thetest.set_MaxSummaryLength(50)
    thetest.load()
    thetest.textalineas = alineas
    thetest.printcode()
    
    # Next, do an unsupported TOC-extraction:
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname("CADouma_DNN_Publication")
    thetest.set_outputpath(outputpath)
    thetest.set_labelname("DNN_TOCTest")
    thetest.read_native_toc("estupido")
    thetest.set_LanguageModel("estupido") # on purpose; not important here.
    
    # Next, do some file comparisons:
    r1 = FileComparison(truthpath+"TextExtraction_001",truthpath+"TextExtraction_002","txt")
    r2 = FileComparison(truthpath+"TextExtraction_001",truthpath+"TextExtraction_001_wrong","txt")
    r3 = FileComparison(truthpath+"TextExtraction_001",truthpath+"TextExtraction_002","estupido")
    print(r1)
    print(r2)
    print(r3)
    
    # And some TOC & alinea comparison:
    alineas_TestTex = hardcodedalineas_TestTex("pdfminer")
    alineas_TestTex_scrambled = hardcodedalineas_TestTex("pdfminer")
    alineas_TestTex_scrambled[0].texttitle = "nonsense"
    Correct_TOC_elements[0].title = "###" # To trigger a fuzz-ration==0 case.
    outcome1 = TOCElementsPresent(Correct_TOC_elements,alineas)
    ourcome2 = AlineasPresent(alineas,alineas_TestTex)
    ourcome3 = AlineasPresent(alineas_TestTex,alineas_TestTex_scrambled)
    percentage = CompareImages(truthpath+"Musk_wordcloud_Linux.png",truthpath+"HistTest_Fontsizes_allcharacters.png")
    
    # Some other stuff:
    xx = hardcodedalineas_SplitDoc("estupido")
    yy = hardcodedalineas_TestTex("estupido")
    
    # Add some verbosity-tracking:
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname("SplitDoc")
    thetest.set_outputpath(outputpath)
    thetest.standard_params()
    thetest.set_UseDummySummary(True) # we don want this to change even if standard_params is adapted.
    thetest.set_ruleverbosity(1)
    thetest.set_verbosetextline("a small test")
    thetest.process(1000)

    # Again for a different document:
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname("LineTest2")
    thetest.set_outputpath(outputpath)
    thetest.standard_params()
    thetest.set_UseDummySummary(True) # we don want this to change even if standard_params is adapted.
    thetest.set_ruleverbosity(1)
    thetest.set_verbosetextline("a small test")
    thetest.process(1000)

    # And again:
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname("TextExtraction_001")
    thetest.set_outputpath(outputpath)
    thetest.standard_params()
    thetest.set_UseDummySummary(True) # we don want this to change even if standard_params is adapted.
    thetest.set_ruleverbosity(1)
    thetest.set_verbosetextline("a small test")
    thetest.process(1000)
    
    # When we get this far, the test is succesful:
    return True
    
if __name__ == '__main__':
    if TestPrints():
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
