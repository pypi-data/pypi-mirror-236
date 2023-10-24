import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from TextPart code:
sys.path.insert(1, '../../')
from TextPart.textsplitter import textsplitter
from TextPart.textpart import textpart
from TextPart.masterrule import texttype
from TextPart.CurrentLine import CurrentLine
from TextPart.regex_expressions import contains_headlines_regex
from TextPart.regex_expressions import contains_tablecontentsregex

# Imports from Tools:
sys.path.insert(2, '../Tools/')
from hardcodedexpressions import ExpressionType
from hardcodedexpressions import TestExpression
from hardcodedexpressions import hardcodedexpressions
from hardcodedfontregions import hardcodedfontregions
from hardcodedlineregions import hardcodedlineregions_pdfminer_SplitDoc

def TestMasterRule_a() -> bool:
    """
    # Unit tests for the masterrule-function of the textsplitter-class that inherits from textpart.
    # NOTE: This is when we put the table of contents-flag in the True-position; meaning that headlines utilizes regex.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Begin by collecting the data that we need:
    fontregions = hardcodedfontregions("pdfminer")
    lineregions = hardcodedlineregions_pdfminer_SplitDoc()
    expressions = hardcodedexpressions()
    positions = [50.0, 100.0, 200.0]
    labels = ["Body", "Headlines", "Title", "Footer", "Enumeration"]
    fontstyles = [True, False]
    Headlinetag = [True, False]
    Headlinecascade = [1, 2]
    fontsizes = [8.0, 9.9, 14.0]
    whitelines = [8.0, 12.0, 20.0]
    
    # Then, define the class and pass relevant information:
    filename = "TestMasterRule"
    thetest = textsplitter()
    thetest.set_documentpath("/not/important/here/")
    thetest.set_documentname(filename)
    thetest.set_labelname(filename)
    thetest.set_outputpath("/not/important/either/")
    thetest.set_labelname(filename)
    thetest.headerboundary = 180.0
    thetest.footerboundary = 60.0
    thetest.max_vertpos = 180.0 
    thetest.min_vertpos = 60.0
    thetest.fontregions = fontregions
    thetest.lineregions = lineregions
    
    # Create a CurrenLine-object:
    thisline = CurrentLine()
    
    # Next, pass information to the members:
    thetest.passinfo()
    
    # Next, Define the answer and other parameters that we may need:
    Answer = True
    regularfontsize = thetest.findregularfontregion().get_value()
    regularlevel = thetest.findregularfontregion().get_cascadelevel()
    previousfontsize = 0.0
    previouswhiteline = -1.0
    print("Looplength = " + str(len(labels)) + "*" + str(len(expressions)) + "*" + str(len(fontsizes)) + "*" + str(len(positions)) + "*" + str(len(whitelines)) + "*(" + str(len(fontsizes)) + "^2)*" + str(len(Headlinetag)) + " = " + str(len(labels)*len(expressions)*len(fontsizes)*len(positions)*len(whitelines)*len(fontstyles)*len(fontstyles)*len(Headlinetag)))
    
    # Then, loop over all expressions and over all positions and fontsizes:
    for label in labels:
        print ("Executing TestMasterRule_a(); Label=" + str(label) + " of " + str(len(labels)) + " labels...")
        for expression in expressions:
            for fontsize in fontsizes:
                for position in positions:
                    for whiteline in whitelines:
                        for isbold in fontstyles:
                            for isitalic in fontstyles:
                                for head_k in range(0,2):
                
                                    # Put the table-of-contents-flag back into the correct position so we know what is going to happen:
                                    thetest.headlines.istableofcontents = False
                                    
                                    # Change labelnames:
                                    thetest.set_labelname(label)
                
                                    # Begin by calling the outcome of the rule:
                                    thisline.textline = expression.TheExpression
                                    thisline.fontsize = fontsize
                                    thisline.vertical_position = position
                                    thisline.previous_whiteline = previouswhiteline
                                    thisline.next_whiteline = whiteline
                                    thisline.is_bold = isbold
                                    thisline.is_italic = isitalic
                                    thisline.previous_IsHeadline = Headlinetag[head_k]
                                    thisline.previous_Headlines_cascade = Headlinecascade[head_k]
                                    thisline.previous_fontsize = previousfontsize
                                    [calctype,level] = thetest.rulecomparison(thisline)
                                    
                                    # Then, put the table-of-contents-flag back into the correct position so we know what is going to happen:
                                    thetest.headlines.istableofcontents = False
                                    
                                    # Then, call the masterrule:
                                    decision = thetest.masterrule(thisline)
                                    
                                    # Also run the fill-function (for code coverage):
                                    thetest.fillcontent(thisline)
                                    
                                    # Next, we must test if the outcome is what we expect. For the masterrule, this means
                                    # that for each expression, it determines the level & type correctly:
                                    # NOTE: Add new textparts here!
                                    if (calctype==texttype.HEADLINES):
                                        
                                        # Then, check step-by-step when this is not possible:
                                        if (position<thetest.footerboundary):
                                            Answer = False
                                            print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" the decision should not be [HEADLINES], as its position is below the footer boundary.")
                                    
                                        if (position>thetest.headerboundary):
                                            Answer = False
                                            print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" the decision should not be [HEADLINES], as its position is above the header boundary.")
                                        
                                        if (not(((isbold)or(thetest.fontsize_biggerthenregular(fontsize))or(thetest.whiteline_isbig(whiteline)))and((thetest.whiteline_isbig(previouswhiteline))or(Headlinetag[head_k])))):
                                                print("Bold fontstyle = " + str(isbold) + " | next_whiteline = " + str(thetest.whiteline_isbig(whiteline)) + " | fontsize = " + str(fontsize) + " | previous_whiteline = " + str(thetest.whiteline_isbig(previouswhiteline)) + " | previous_IsHeadline = " + str(Headlinetag[head_k]) + " | Expression = " + str(expression.TheExpression) + " ==> the decision should not be [HEADLINES]")
                                        
                                        if (expression.Type==ExpressionType.TABLEOFCONTENTS)and(not(level==1)and(Headlinetag[head_k]==False)):
                                            Answer = False
                                            print("If expression <"+expression.TheExpression+"> is recognised as a headlines, its cascadelevel should be 1!")
                                                
                                        if (expression.Type==ExpressionType.CHAPTER)and(not(level==1)and(Headlinetag[head_k]==False)):
                                            Answer = False
                                            print("If expression <"+expression.TheExpression+"> is recognised as a headlines, its cascadelevel should be 1!")
                                                
                                        if (expression.Type==ExpressionType.SECTION)and(not(level==2)and(Headlinetag[head_k]==False)):
                                            Answer = False
                                            print("If expression <"+expression.TheExpression+"> is recognised as a headlines, its cascadelevel should be 2!")
                                        
                                        if (expression.Type==ExpressionType.SUBSECTION)and(not(level==3)and(Headlinetag[head_k]==False)):
                                            Answer = False
                                            print("If expression <"+expression.TheExpression+"> is recognised as a headlines, its cascadelevel should be 3!")
                                                
                                        if (expression.Type==ExpressionType.SUBSUBSECTION)and(not(level==4)and(Headlinetag[head_k]==False)):
                                            Answer = False
                                            print("If expression <"+expression.TheExpression+"> is recognised as a headlines, its cascadelevel should be 4!")
                                        
                                        if (not(decision))and(label=="Headlines"):
                                            Answer = False
                                            print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" | At decision [HEADLINES], the masterrule should return True when label equals [Headlines] and false otherwise")
                                            
                                        if (decision)and(not(label=="Headlines")):
                                            Answer = False
                                            print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" | At decision [HEADLINES], the masterrule should return True when label equals [Headlines] and false otherwise")
                                        
                                    if (calctype==texttype.FOOTER):
                                    
                                        # Then, check step-by-step when this is not possible:
                                        if (position>thetest.footerboundary)and(position<thetest.headerboundary)and(not(thetest.fontsize_smallerthenregular(fontsize))):
                                            Answer = False
                                            print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" the decision should not be [FOOTER], as it is between boundaries and the fontsize is not smaller than regular.")
                                        
                                        if (not(decision))and(label=="Footer"):
                                            Answer = False
                                            print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" | At decision [FOOTER], the masterrule should return True when label equals [Footer] and false otherwise")
                                            
                                        if (decision)and(not(label=="Footer")):
                                            Answer = False
                                            print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" | At decision [FOOTER], the masterrule should return True when label equals [Footer] and false otherwise")
                                            
                                    if (calctype==texttype.ENUMERATION):
                                        
                                        # Then, check step-by-step when this is not possible:
                                        if (position<thetest.footerboundary):
                                            Answer = False
                                            print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" the decision should not be [ENUMERATION], as its position is below the footer boundary.")
                                    
                                        if (position>thetest.headerboundary):
                                            Answer = False
                                            print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" the decision should not be [ENUMERATION], as its position is above the header boundary.")
                                        
                                        if (expression.Type==ExpressionType.BIGROMAN_ENUMERATION)and(not(calctype==texttype.ENUMERATION)):
                                            Answer = False
                                            print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" the decision should be [ENUMERATION], as it starts with a bigroman-enumeration-sign.")
                                        
                                        if (expression.Type==ExpressionType.SMALLROMAN_ENUMERATION)and(not(calctype==texttype.ENUMERATION)):
                                            Answer = False
                                            print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" the decision should be [ENUMERATION], as it starts with a smallroman-enumeration-sign.")
                                            
                                        if (expression.Type==ExpressionType.BIGLETTER_ENUMERATION)and(not(calctype==texttype.ENUMERATION)):
                                            Answer = False
                                            print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" the decision should be [ENUMERATION], as it starts with a bigletter-enumeration-sign.")
                                        
                                        if (expression.Type==ExpressionType.SMALLLETTER_ENUMERATION)and(not(calctype==texttype.ENUMERATION)):
                                            Answer = False
                                            print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" the decision should be [ENUMERATION], as it starts with a smallletter-enumeration-sign.")
                                            
                                        if (expression.Type==ExpressionType.DIGIT_ENUMERATION)and(not(calctype==texttype.ENUMERATION)):
                                            Answer = False
                                            print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" the decision should be [ENUMERATION], as it starts with a digit-enumeration-sign.")
                                        
                                        if (expression.Type==ExpressionType.SIGNMARK_ENUMERATION)and(not(calctype==texttype.ENUMERATION)):
                                            Answer = False
                                            print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" the decision should be [ENUMERATION], as it starts with a signmark (-) enumeration-sign.")
                                        
                                        if (not(decision))and(label=="Enumeration"):
                                            Answer = False
                                            print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" | At decision [ENUMERATION], the masterrule should return True when label equals [Enumeration] and false otherwise")
                                            
                                        if (decision)and(not(label=="Enumeration")):
                                            Answer = False
                                            print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" | At decision [ENUMERATION], the masterrule should return True when label equals [Enumeration] and false otherwise")
                                        
                                    if (calctype==texttype.TITLE):
                                    
                                        # Then, check step-by-step when this is not possible:
                                        Answer = False
                                        print("This option has not yet been developed. So it should never return [TITLE].")
                                        
                                        if (not(decision))and(label=="Title"):
                                            Answer = False
                                            print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" | At decision [TITLE], the masterrule should return True when label equals [Title] and false otherwise")
                                            
                                        if (decision)and(not(label=="Title")):
                                            Answer = False
                                            print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" | At decision [TITLE], the masterrule should return True when label equals [Title] and false otherwise")
                                    
                                    if (calctype==texttype.BODY):
                                    
                                        # Then, check step-by-step when this is not possible:
                                        if (position<thetest.footerboundary):
                                            Answer = False
                                            print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" the decision should not be [BODY], as its position is below the footer boundary.")
                                    
                                        if (position>thetest.headerboundary):
                                            Answer = False
                                            print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" the decision should not be [BODY], as its position is above the header boundary.")
                                  
                                        if (expression.Type==ExpressionType.NORMAL)and(not(thetest.fontsize_equalstoregular(fontsize))):
                                            Answer = False
                                            print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" the decision should not be [BODY], as non-NORMAL expressions can only be [BODY] at regular fontsize.")
                                            
                                        if (not(decision))and(label=="Body"):
                                            Answer = False
                                            print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" | At decision [BODY], the masterrule should return True when label equals [Body] and false otherwise")
                                            
                                        if (decision)and(not(label=="Body")):
                                            Answer = False
                                            print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" | At decision [BODY], the masterrule should return True when label equals [Body] and false otherwise")
                                    
                                    # Adapt previous tags:
                        previouswhiteline = whiteline
                previousfontsize = fontsize
    # Then, return the answer:
    return Answer

# Collection of all tests:
def TestMasterRule() -> bool:
    """
    # Collection of unit tests of all the functions in regex_expressions.py
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define the answer:
    Answer = True
    
    # test the cases:
    if not TestMasterRule_a():
        Answer = False
        print(" ==> TestMasterRule_a() failed!")
    
    # Return the answer:
    return Answer

if __name__ == '__main__':
    if TestMasterRule():
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
