import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from TextPart code:
sys.path.insert(1, '../../')
from TextPart.textpart import textpart
from TextPart.fontregion import fontregion
from TextPart.textsplitter import textsplitter

# Imports from Tools:
sys.path.insert(2, '../Tools/')
from FileComparison import FileComparison
from hardcodedfontregions import hardcodedfontregions
from hardcodedfontsizehist import hardcodedfontsizehist
from hardcodedalineas import hardcodedalineas_SplitDoc
from hardcodedalineas import hardcodedalineas_TestTex

# Definition of paths:
inputpath = "../Inputs/"
outputpath = "../Calc_Outputs/"
truthpath = "../True_Outputs/"

# Definition of unit tests:
def TestPassInfo_body() -> bool:
    """
    # Unit test for the passinfo-function of the textsplitter-class.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Begin by creating a textsplitter-object:
    thetest = textsplitter()
    thetest.set_documentpath("/some/input/path")
    thetest.set_documentname("Some document name")
    thetest.set_outputpath("/some/output/path")
    thetest.set_labelname("/some/input/path")
    thetest.set_histogramsize(100.0)
    
    # Put in some hard-coded information:
    thetest.fontsizeHist_perline = hardcodedfontsizehist()
    thetest.fontsizeHist_percharacter = hardcodedfontsizehist()
    thetest.fontregions = hardcodedfontregions("pdfminer")
    thetest.textalineas = hardcodedalineas_SplitDoc("pdfminer")
    thetest.headerboundary = 432.0
    thetest.footerboundary = 123.0
    
    # Now, call the passinfo function:
    thetest.passinfo()
    
    # And check if all the information correctly came through.
    # NOTE: In this function, we only test the body-object.
    Answer = True
    
    if not (thetest.histogramsize==thetest.body.histogramsize): Answer = False
    if not (thetest.documentpath==thetest.body.documentpath): Answer = False
    if not (thetest.documentname==thetest.body.documentname): Answer = False
    if not (thetest.outputpath==thetest.body.outputpath): Answer = False
    if not (thetest.headerboundary==thetest.body.headerboundary): Answer = False
    if not (thetest.footerboundary==thetest.body.footerboundary): Answer = False
    
    if not Answer: print("Passing the single-arguments to the body-class failed!")
    
    index = 0
    for region in thetest.fontregions:
        if not region.compare(thetest.body.fontregions[index]): Answer = False
        index = index + 1
    if not Answer: print("Passing the fontregions to the body-class failed!")
    
    index = 0
    for number in thetest.fontsizeHist_perline[0]:
        if (abs(number-thetest.body.fontsizeHist_perline[0][index])>1e-3): Answer = False
        index = index + 1
    if not Answer: print("Passing the fontsizeHist_perline-content to the body-class failed!")
    
    index = 0
    for number in thetest.fontsizeHist_perline[1]:
        if (abs(number-thetest.body.fontsizeHist_perline[1][index])>1e-3): Answer = False
        index = index + 1
    if not Answer: print("Passing the fontsizeHist_perline-bins to the body-class failed!")
    
    index = 0
    for number in thetest.fontsizeHist_percharacter[0]:
        if (abs(number-thetest.body.fontsizeHist_percharacter[0][index])>1e-3): Answer = False
        index = index + 1
    if not Answer: print("Passing the fontsizeHist_percharacter-content to the body-class failed!")
    
    index = 0
    for number in thetest.fontsizeHist_percharacter[1]:
        if (abs(number-thetest.body.fontsizeHist_percharacter[1][index])>1e-3): Answer = False
        index = index + 1
    if not Answer: print("Passing the fontsizeHist_percharacter-bins to the body-class failed!")

    # Done:
    return Answer

def TestPassInfo_title() -> bool:
    """
    # Unit test for the passinfo-function of the textsplitter-class.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Begin by creating a textsplitter-object:
    thetest = textsplitter()
    thetest.set_documentpath("/some/input/path")
    thetest.set_documentname("Some document name")
    thetest.set_outputpath("/some/output/path")
    thetest.set_labelname("/some/input/path")
    thetest.set_histogramsize(100.0)
    
    # Put in some hard-coded information:
    thetest.fontsizeHist_perline = hardcodedfontsizehist()
    thetest.fontsizeHist_percharacter = hardcodedfontsizehist()
    thetest.fontregions = hardcodedfontregions("pdfminer")
    thetest.textalineas = hardcodedalineas_SplitDoc("pdfminer")
    thetest.headerboundary = 432.0
    thetest.footerboundary = 123.0
    
    # Now, call the passinfo function:
    thetest.passinfo()
    
    # And check if all the information correctly came through.
    # NOTE: In this function, we only test the title-object.
    Answer = True
    
    if not (thetest.histogramsize==thetest.title.histogramsize): Answer = False
    if not (thetest.documentpath==thetest.title.documentpath): Answer = False
    if not (thetest.documentname==thetest.title.documentname): Answer = False
    if not (thetest.outputpath==thetest.title.outputpath): Answer = False
    if not (thetest.headerboundary==thetest.title.headerboundary): Answer = False
    if not (thetest.footerboundary==thetest.title.footerboundary): Answer = False
    
    if not Answer: print("Passing the single-arguments to the title-class failed!")
    
    index = 0
    for region in thetest.fontregions:
        if not region.compare(thetest.title.fontregions[index]): Answer = False
        index = index + 1
    if not Answer: print("Passing the fontregions to the title-class failed!")
    
    index = 0
    for number in thetest.fontsizeHist_perline[0]:
        if (abs(number-thetest.title.fontsizeHist_perline[0][index])>1e-3): Answer = False
        index = index + 1
    if not Answer: print("Passing the fontsizeHist_perline-content to the title-class failed!")
    
    index = 0
    for number in thetest.fontsizeHist_perline[1]:
        if (abs(number-thetest.title.fontsizeHist_perline[1][index])>1e-3): Answer = False
        index = index + 1
    if not Answer: print("Passing the fontsizeHist_perline-bins to the title-class failed!")
    
    index = 0
    for number in thetest.fontsizeHist_percharacter[0]:
        if (abs(number-thetest.title.fontsizeHist_percharacter[0][index])>1e-3): Answer = False
        index = index + 1
    if not Answer: print("Passing the fontsizeHist_percharacter-content to the title-class failed!")
    
    index = 0
    for number in thetest.fontsizeHist_percharacter[1]:
        if (abs(number-thetest.title.fontsizeHist_percharacter[1][index])>1e-3): Answer = False
        index = index + 1
    if not Answer: print("Passing the fontsizeHist_percharacter-bins to the title-class failed!")

    # Done:
    return Answer    
    
def TestPassInfo_headlines() -> bool:
    """
    # Unit test for the passinfo-function of the textsplitter-class.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Begin by creating a textsplitter-object:
    thetest = textsplitter()
    thetest.set_documentpath("/some/input/path")
    thetest.set_documentname("Some document name")
    thetest.set_outputpath("/some/output/path")
    thetest.set_labelname("/some/input/path")
    thetest.set_histogramsize(100.0)
    
    # Put in some hard-coded information:
    thetest.fontsizeHist_perline = hardcodedfontsizehist()
    thetest.fontsizeHist_percharacter = hardcodedfontsizehist()
    thetest.fontregions = hardcodedfontregions("pdfminer")
    thetest.textalineas = hardcodedalineas_SplitDoc("pdfminer")
    thetest.headerboundary = 432.0
    thetest.footerboundary = 123.0
    
    # Now, call the passinfo function:
    thetest.passinfo()
    
    # And check if all the information correctly came through.
    # NOTE: In this function, we only test the headlines-object.
    Answer = True
    
    if not (thetest.histogramsize==thetest.headlines.histogramsize): Answer = False
    if not (thetest.documentpath==thetest.headlines.documentpath): Answer = False
    if not (thetest.documentname==thetest.headlines.documentname): Answer = False
    if not (thetest.outputpath==thetest.headlines.outputpath): Answer = False
    if not (thetest.headerboundary==thetest.headlines.headerboundary): Answer = False
    if not (thetest.footerboundary==thetest.headlines.footerboundary): Answer = False
    
    if not Answer: print("Passing the single-arguments to the headlines-class failed!")
    
    index = 0
    for region in thetest.fontregions:
        if not region.compare(thetest.headlines.fontregions[index]): Answer = False
        index = index + 1
    if not Answer: print("Passing the fontregions to the headlines-class failed!")
    
    index = 0
    for number in thetest.fontsizeHist_perline[0]:
        if (abs(number-thetest.headlines.fontsizeHist_perline[0][index])>1e-3): Answer = False
        index = index + 1
    if not Answer: print("Passing the fontsizeHist_perline-content to the headlines-class failed!")
    
    index = 0
    for number in thetest.fontsizeHist_perline[1]:
        if (abs(number-thetest.headlines.fontsizeHist_perline[1][index])>1e-3): Answer = False
        index = index + 1
    if not Answer: print("Passing the fontsizeHist_perline-bins to the headlines-class failed!")
    
    index = 0
    for number in thetest.fontsizeHist_percharacter[0]:
        if (abs(number-thetest.headlines.fontsizeHist_percharacter[0][index])>1e-3): Answer = False
        index = index + 1
    if not Answer: print("Passing the fontsizeHist_percharacter-content to the headlines-class failed!")
    
    index = 0
    for number in thetest.fontsizeHist_percharacter[1]:
        if (abs(number-thetest.headlines.fontsizeHist_percharacter[1][index])>1e-3): Answer = False
        index = index + 1
    if not Answer: print("Passing the fontsizeHist_percharacter-bins to the headlines-class failed!")

    # Done:
    return Answer
    
def TestPassInfo_footer() -> bool:
    """
    # Unit test for the passinfo-function of the textsplitter-class.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Begin by creating a textsplitter-object:
    thetest = textsplitter()
    thetest.set_documentpath("/some/input/path")
    thetest.set_documentname("Some document name")
    thetest.set_outputpath("/some/output/path")
    thetest.set_labelname("/some/input/path")
    thetest.set_histogramsize(100.0)
    
    # Put in some hard-coded information:
    thetest.fontsizeHist_perline = hardcodedfontsizehist()
    thetest.fontsizeHist_percharacter = hardcodedfontsizehist()
    thetest.fontregions = hardcodedfontregions("pdfminer")
    thetest.textalineas = hardcodedalineas_SplitDoc("pdfminer")
    thetest.headerboundary = 432.0
    thetest.footerboundary = 123.0
    
    # Now, call the passinfo function:
    thetest.passinfo()
    
    # And check if all the information correctly came through.
    # NOTE: In this function, we only test the footer-object.
    Answer = True
    
    if not (thetest.histogramsize==thetest.footer.histogramsize): Answer = False
    if not (thetest.documentpath==thetest.footer.documentpath): Answer = False
    if not (thetest.documentname==thetest.footer.documentname): Answer = False
    if not (thetest.outputpath==thetest.footer.outputpath): Answer = False
    if not (thetest.headerboundary==thetest.footer.headerboundary): Answer = False
    if not (thetest.footerboundary==thetest.footer.footerboundary): Answer = False
    
    if not Answer: print("Passing the single-arguments to the footer-class failed!")
    
    index = 0
    for region in thetest.fontregions:
        if not region.compare(thetest.footer.fontregions[index]): Answer = False
        index = index + 1
    if not Answer: print("Passing the fontregions to the footer-class failed!")
    
    index = 0
    for number in thetest.fontsizeHist_perline[0]:
        if (abs(number-thetest.footer.fontsizeHist_perline[0][index])>1e-3): Answer = False
        index = index + 1
    if not Answer: print("Passing the fontsizeHist_perline-content to the footer-class failed!")
    
    index = 0
    for number in thetest.fontsizeHist_perline[1]:
        if (abs(number-thetest.footer.fontsizeHist_perline[1][index])>1e-3): Answer = False
        index = index + 1
    if not Answer: print("Passing the fontsizeHist_perline-bins to the footer-class failed!")
    
    index = 0
    for number in thetest.fontsizeHist_percharacter[0]:
        if (abs(number-thetest.footer.fontsizeHist_percharacter[0][index])>1e-3): Answer = False
        index = index + 1
    if not Answer: print("Passing the fontsizeHist_percharacter-content to the footer-class failed!")
    
    index = 0
    for number in thetest.fontsizeHist_percharacter[1]:
        if (abs(number-thetest.footer.fontsizeHist_percharacter[1][index])>1e-3): Answer = False
        index = index + 1
    if not Answer: print("Passing the fontsizeHist_percharacter-bins to the footer-class failed!")

    # Done:
    return Answer

# NOTE: Add new textparts here!
# New textparts should have their own unit-test on passinfo as well!
    
def TestPassInfo_alineas() -> bool:
    """
    # Unit test for the passinfo-function of the textsplitter-class.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Begin by creating a textsplitter-object:
    thetest = textsplitter()
    thetest.set_documentpath("/some/input/path")
    thetest.set_documentname("Some document name")
    thetest.set_outputpath("/some/output/path")
    thetest.set_labelname("/some/input/path")
    thetest.set_histogramsize(100.0)
    
    # Put in some hard-coded information:
    thetest.fontsizeHist_perline = hardcodedfontsizehist()
    thetest.fontsizeHist_percharacter = hardcodedfontsizehist()
    thetest.fontregions = hardcodedfontregions("pdfminer")
    thetest.textalineas = hardcodedalineas_SplitDoc("pdfminer")
    thetest.headerboundary = 432.0
    thetest.footerboundary = 123.0
    
    # Now, call the passinfo function:
    thetest.passinfo()
    
    # And check if all the information correctly came through.
    # NOTE: In this function, we only test the textalinea-object.
    Answer = True
    
    # Loop over all alineas:
    for alinea in thetest.textalineas:
    
        if not (thetest.histogramsize==alinea.histogramsize): Answer = False
        if not (thetest.documentpath==alinea.documentpath): Answer = False
        if not (thetest.documentname==alinea.documentname): Answer = False
        if not (thetest.outputpath==alinea.outputpath): Answer = False
        if not (thetest.headerboundary==alinea.headerboundary): Answer = False
        if not (thetest.footerboundary==alinea.footerboundary): Answer = False
    
        if not Answer: print("Passing the single-arguments to the textalinea-class failed!")
    
        index = 0
        for region in thetest.fontregions:
            if not region.compare(alinea.fontregions[index]): Answer = False
            index = index + 1
        if not Answer: print("Passing the fontregions to the textalinea-class failed!")
    
        index = 0
        for number in thetest.fontsizeHist_perline[0]:
            if (abs(number-alinea.fontsizeHist_perline[0][index])>1e-3): Answer = False
            index = index + 1
        if not Answer: print("Passing the fontsizeHist_perline-content to the textalinea-class failed!")
    
        index = 0
        for number in thetest.fontsizeHist_perline[1]:
            if (abs(number-alinea.fontsizeHist_perline[1][index])>1e-3): Answer = False
            index = index + 1
        if not Answer: print("Passing the fontsizeHist_perline-bins to the textalinea-class failed!")
    
        index = 0
        for number in thetest.fontsizeHist_percharacter[0]:
            if (abs(number-alinea.fontsizeHist_percharacter[0][index])>1e-3): Answer = False
            index = index + 1
        if not Answer: print("Passing the fontsizeHist_percharacter-content to the textalinea-class failed!")
    
        index = 0
        for number in thetest.fontsizeHist_percharacter[1]:
            if (abs(number-alinea.fontsizeHist_percharacter[1][index])>1e-3): Answer = False
            index = index + 1
        if not Answer: print("Passing the fontsizeHist_percharacter-bins to the textalinea-class failed!")

    # Done:
    return Answer
    
    
# Definition of collection:    
def TestPassInfo() -> bool:
    """
    # Collection-function of Integration-tests.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    Answer = True
    if (TestPassInfo_body()==False): Answer=False 
    if (TestPassInfo_title()==False): Answer=False 
    if (TestPassInfo_footer()==False): Answer=False 
    if (TestPassInfo_headlines()==False): Answer=False 
    if (TestPassInfo_alineas()==False): Answer=False 
    return Answer

if __name__ == '__main__':
    if TestPassInfo():
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
