import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from TextPart code:
sys.path.insert(1, '../../')
from TextPart.fontregion import fontregion
from TextPart.textsplitter import textsplitter
from TextPart.CurrentLine import CurrentLine
from TextPart.textalinea import textalinea

# Imports from Tools:
sys.path.insert(2, '../Tools/')
from hardcodedtextlines import hardcodedtextlines
from hardcodedfontsizehist import hardcodedfontsizehist
from hardcodedfontregions import hardcodedfontregions
from AlineasPresent import AlineasPresent
from hardcodedalineas import hardcodedalineas_SplitDoc
from FileComparison import FileComparison
from hardcodedlineregions import hardcodedlineregions_pdfminer_SplitDoc
from hardcodedwhitelinehist import hardcodedwhitelinehist

# Definition of paths:
inputpath = "../Inputs/"
outputpath = "../Calc_Outputs/"
truthpath = "../True_Outputs/"

# Definition of unit tests:
def TestBreakDown() -> bool:
    """
    # Unit test for the breakdown-function of the textsplitter-class.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Begin by creating a textsplitter:
    filename = "TestBreakDown"
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_labelname(filename)
    thetest.set_outputpath(outputpath)
    thetest.set_labelname("SplitDoc pdfminer breakdown test")
    
    # Next, put everything in there hard-coded:
    thelines = hardcodedtextlines()
    thetest.textcontent.clear()
    thetest.positioncontent.clear()
    thetest.fontsize_perline.clear()
    thetest.whitelinesize.clear()
    thetest.min_vertpos = 85.73225559999993 # for SplitDoc & pdfminer
    thetest.max_vertpos = 596.9073026       # for SplitDoc & pdfminer
    thetest.boldchars_ratio = 0.03
    thetest.boldratio_threshold = 0.05
    thetest.headerboundary = 625.0 # Approprioate for SplitDoc-pdfminer
    thetest.footerboundary = 40.0  # Approprioate for SplitDoc-pdfminer
    
    for oneline in thelines:
        thetest.textcontent.append(oneline.textline)
        thetest.positioncontent.append(oneline.vertical_position)
        thetest.fontsize_perline.append(oneline.fontsize)
        thetest.whitelinesize.append(oneline.previous_whiteline)
        thetest.is_bold.append(oneline.is_bold)
        thetest.is_italic.append(oneline.is_italic)
        thetest.is_highlighted.append(oneline.is_highlighted)
    
    thetest.fontsizeHist_perline = hardcodedfontsizehist()
    thetest.fontsizeHist_percharacter = hardcodedfontsizehist()
    thetest.fontregions = hardcodedfontregions("pdfminer")
    thetest.lineregions = hardcodedlineregions_pdfminer_SplitDoc()
    thetest.whitespaceHist_perline = hardcodedwhitelinehist()
    
    # Obviously, do not forget to pass the required information to
    # the elements inside textsplitter. We do this without passinfo
    # to keep it a unit test:
    thetest.body.fontregions = thetest.fontregions
    thetest.title.fontregions = thetest.fontregions
    thetest.headlines.fontregions = thetest.fontregions
    thetest.footer.fontregions = thetest.fontregions
    thetest.enumeration.fontregions = thetest.fontregions
    thetest.body.lineregions = thetest.lineregions
    thetest.title.lineregions = thetest.lineregions
    thetest.headlines.lineregions = thetest.lineregions
    thetest.footer.lineregions = thetest.lineregions
    thetest.enumeration.lineregions = thetest.lineregions
    thetest.title.min_vertpos = thetest.min_vertpos
    thetest.headlines.min_vertpos = thetest.min_vertpos
    thetest.body.min_vertpos = thetest.min_vertpos
    thetest.footer.min_vertpos = thetest.min_vertpos
    thetest.enumeration.min_vertpos = thetest.min_vertpos
    thetest.title.max_vertpos = thetest.max_vertpos
    thetest.headlines.max_vertpos = thetest.max_vertpos
    thetest.body.max_vertpos = thetest.max_vertpos
    thetest.footer.max_vertpos = thetest.max_vertpos
    thetest.enumeration.max_vertpos = thetest.max_vertpos
    thetest.title.boldchars_ratio = thetest.boldchars_ratio
    thetest.headlines.boldchars_ratio = thetest.boldchars_ratio
    thetest.body.boldchars_ratio = thetest.boldchars_ratio
    thetest.footer.boldchars_ratio = thetest.boldchars_ratio
    thetest.enumeration.boldchars_ratio = thetest.boldchars_ratio
    thetest.title.boldratio_threshold = thetest.boldratio_threshold
    thetest.headlines.boldratio_threshold = thetest.boldratio_threshold
    thetest.body.boldratio_threshold = thetest.boldratio_threshold
    thetest.footer.boldratio_threshold = thetest.boldratio_threshold
    thetest.enumeration.boldratio_threshold = thetest.boldratio_threshold
    thetest.title.headerboundary = thetest.headerboundary
    thetest.headlines.headerboundary = thetest.headerboundary
    thetest.body.headerboundary = thetest.headerboundary
    thetest.footer.headerboundary = thetest.headerboundary
    thetest.enumeration.headerboundary = thetest.headerboundary
    thetest.title.footerboundary = thetest.footerboundary
    thetest.headlines.footerboundary = thetest.footerboundary
    thetest.body.footerboundary = thetest.footerboundary
    thetest.footer.footerboundary = thetest.footerboundary
    thetest.enumeration.footerboundary = thetest.footerboundary
    # NOTE: Add new textparts here!
    
    # Then, execute the breakdown-function:
    thetest.breakdown()
    thetest.textalineas[0].texttitle = "SplitDoc" # Because that is what we test against, while the document here has a different name.
    
    # Next, calculate whether all required alineas exist:
    alineas_thatshouldbethere = hardcodedalineas_SplitDoc("pdfminer")
    
    # Now, obviously, only testing breakdown will NOT account
    # for the tree structure and summaries, so blend those out in the real answer:
    for alinea in alineas_thatshouldbethere:
        alinea.parentID = -1
        alinea.horizontal_ordering = -1
        alinea.summary = ""
        alinea.sum_CanbeEmpty = False
    
    # Then, compare the calculated alineas to the correct answer:
    Answer = AlineasPresent(alineas_thatshouldbethere,thetest.textalineas)
    
    # Next, we test exportdecisions also as part of this function,
    # as it is impossible to test the output without executing
    # breakdown() first.
    thetest.exportdecisions()
    
    # Then, compare the output to the reference:
    rapport = FileComparison(outputpath+filename+"_decisions",truthpath+filename+"_decisions","txt")
    if not (rapport==""): 
        Answer = False 
        print(" ==> exportdecisions() file comparison:\n\n" + rapport + "----------------------------------------------------")
    
    # Done:
    return Answer
    
if __name__ == '__main__':
    if TestBreakDown():
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
