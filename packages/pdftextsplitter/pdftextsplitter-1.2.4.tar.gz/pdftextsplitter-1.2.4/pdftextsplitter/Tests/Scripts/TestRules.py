import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from TextPart code:
sys.path.insert(1, '../../')
from TextPart.body import body
from TextPart.title import title
from TextPart.headlines import headlines
from TextPart.footer import footer
from TextPart.enumeration import enumeration
from TextPart.enum_type import enum_type
from TextPart.textalinea import textalinea
from TextPart.textsplitter import textsplitter
from TextPart.textpart import textpart
from TextPart.CurrentLine import CurrentLine
from TextPart.regex_expressions import contains_headlines_regex
from TextPart.regex_expressions import contains_tablecontentsregex
from TextPart.regex_expressions import remove_nonletters

# Imports from Tools:
sys.path.insert(2, '../Tools/')
from hardcodedexpressions import ExpressionType
from hardcodedexpressions import TestExpression
from hardcodedexpressions import hardcodedexpressions
from hardcodedfontregions import hardcodedfontregions
from hardcodedlineregions import hardcodedlineregions_pdfminer_SplitDoc

def TestRule_body() -> bool:
    """
    # Unit tests for the rule-function of the body-class that inherits from textpart.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Begin by collecting the data that we need:
    fontregions = hardcodedfontregions("pdfminer")
    lineregions = hardcodedlineregions_pdfminer_SplitDoc()
    expressions = hardcodedexpressions()
    positions = [50.0, 100.0, 200.0]
    Headlinetag = [True, False]
    Headlinecascade = [1, 2]
    fontstyles = [True, False]
    fontsizes = [8.0, 9.9, 14.0]
    whitelines = [8.0, 12.0, 20.0]
    
    # Then, define the class and pass relevant information:
    thebody = body()
    thebody.footerboundary = 60.0
    thebody.headerboundary = 180.0
    thebody.max_vertpos = 180.0 
    thebody.min_vertpos = 60.0
    thebody.fontregions = fontregions
    thebody.lineregions = lineregions
    
    # Create a CurrenLine-object:
    thisline = CurrentLine()
    
    # Next, Define the answer and other parameters that we may need:
    Answer = True
    regularfontsize = thebody.findregularfontregion().get_value()
    regularlevel = thebody.findregularfontregion().get_cascadelevel()
    previousfontsize = 0.0
    previouswhiteline = -1.0
    
    # Then, loop over all expressions and over all positions and fontsizes:
    for expression in expressions:
        for fontsize in fontsizes:
            for position in positions:
                for whiteline in whitelines:
                    for isbold in fontstyles:
                        for isitalic in fontstyles:
                            for head_k in range(0,2):
                
                                # Begin by calling the outcome of the rule:
                                thisline.textline = expression.TheExpression
                                thisline.fontsize = fontsize
                                thisline.vertical_position = position
                                thisline.previous_whiteline = previouswhiteline
                                thisline.next_whiteline = whiteline
                                thisline.previous_IsHeadline = Headlinetag[head_k]
                                thisline.previous_Headlines_cascade = Headlinecascade[head_k]
                                thisline.previous_fontsize = previousfontsize
                                thisline.is_bold = isbold
                                thisline.is_italic = isitalic
                                [decision,level] = thebody.rule(thisline)
                
                                # Next, we must test if the outcome is what we expect:
                                # NOTE: this is obviously different for each rule.
                                if (decision==False)and(thebody.fontsize_equalstoregular(fontsize)):
                                    Answer = False
                                    print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" the decision should be [True], as regular fontsize equals "+str(regularfontsize))
                
                                if (decision==True)and(not(thebody.fontsize_equalstoregular(fontsize))):
                                    Answer = False
                                    print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" the decision should be [False], as regular fontsize equals "+str(regularfontsize))
                    
                                if (decision==True)and(not(level==regularlevel)):
                                    Answer = False
                                    print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+": when the decision==True, cascadelevel("+str(level)+") should equal the regular cascadelevel ("+str(regularlevel)+")")
                
                        # Adapt previous tags:
                    previouswhiteline = whiteline
            previousfontsize = fontsize
    return Answer

def TestRule_headlines_a() -> bool:
    """
    # Unit tests for the rule-function of the headlines-class that inherits from textpart.
    # Here, we put the istableofcontents-flag at False.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Begin by collecting the data that we need:
    fontregions = hardcodedfontregions("pdfminer")
    lineregions = hardcodedlineregions_pdfminer_SplitDoc()
    expressions = hardcodedexpressions()
    fontstyles = [True, False]
    positions = [-2.0, 50.0, 100.0, 200.0]
    Headlinetag = [True, False]
    Headlinecascade = [1, 2]
    fontsizes = [8.0, 9.9, 14.0]
    whitelines = [8.0, 12.0, 20.0]
    
    # Then, define the class and pass relevant information:
    theheadlines = headlines()
    theheadlines.istableofcontents = False
    theheadlines.footerboundary = 60.0
    theheadlines.headerboundary = 180.0
    theheadlines.max_vertpos = 180.0 
    theheadlines.min_vertpos = 60.0
    theheadlines.fontregions = fontregions
    theheadlines.lineregions = lineregions
    
    # Create a CurrenLine-object:
    thisline = CurrentLine()
    
    # Next, Define the answer and other parameters that we may need:
    Answer = True
    regularfontsize = theheadlines.findregularfontregion().get_value()
    regularlevel = theheadlines.findregularfontregion().get_cascadelevel()
    previousfontsize = 0.0
    previouswhiteline = -1.0
    
    # Then, loop over all expressions and over all positions and fontsizes:
    for expression in expressions:
        for fontsize in fontsizes:
            for position in positions:
                for whiteline in whitelines:
                    for isbold in fontstyles:
                        for isitalic in fontstyles:
                            for head_k in range(0,2):
                
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
                                [decision,level] = theheadlines.rule(thisline)
                                
                                # Calculate the letter-condition:
                                Full_linelength = len(thisline.textline)
                                pure_letters = remove_nonletters(thisline.textline)
                                Nr_spaces = thisline.textline.count(" ")
                                Letter_Length = len(pure_letters)
                                Nospace_length = Full_linelength - Nr_spaces
        
                                # Calculate ratio:
                                letter_ratio = 1.0
                                if (Nospace_length>0):
                                    letter_ratio = Letter_Length/Nospace_length
                                Letter_condition = False
                                if (letter_ratio>0.67): # This threshold is a very specific value needed.
                                    Letter_condition = True
                                
                                # Next, we must test if the outcome is what we expect:
                                # NOTE: this is obviously different for each rule.
                                
                                if (isbold)or(theheadlines.fontsize_biggerthenregular(fontsize))or(theheadlines.whiteline_isbig(whiteline)):
                                    if ((theheadlines.whiteline_isbig(previouswhiteline))or(Headlinetag[head_k]))and(Letter_condition==True):
                                        if (decision==False):
                                            counterror = True
                                            
                                            # in principle, this should be a headline, unless:
                                            if ((isbold==False)and(theheadlines.fontsize_biggerthenregular(fontsize)==False)and(theheadlines.whiteline_isbig(whiteline)==True)):
                                                if (not(contains_headlines_regex(expression.TheExpression)))and(not(contains_tablecontentsregex(expression.TheExpression))): counterror = False
                                                
                                                
                                            if (theheadlines.whiteline_isbig(previouswhiteline)==True)or(Headlinetag[head_k]==True):
                                                if (not(contains_headlines_regex(expression.TheExpression)))and(not(contains_tablecontentsregex(expression.TheExpression))): counterror = False
                                            
                                            if counterror:
                                                Answer = False
                                                print("Bold fontstyle = " + str(isbold) + " | next_whiteline = " + str(theheadlines.whiteline_isbig(whiteline)) + " | fontsize = " + str(fontsize) + " | previous_whiteline = " + str(theheadlines.whiteline_isbig(previouswhiteline)) + " | previous_IsHeadline = " + str(Headlinetag[head_k]) + " | Expression = " + str(expression.TheExpression) + " ==> This should be a headline!")
                                
                                if (isbold==False)and(theheadlines.fontsize_biggerthenregular(fontsize)==False)and(theheadlines.whiteline_isbig(whiteline)==False):
                                    if (theheadlines.whiteline_isbig(previouswhiteline)==False)and(Headlinetag[head_k]==False):
                                        if (decision==True):
                                            Answer = False
                                            print("Bold fontstyle = " + str(isbold) + " | next_whiteline = " + str(theheadlines.whiteline_isbig(whiteline)) + " | fontsize = " + str(fontsize) + " | previous_whiteline = " + str(theheadlines.whiteline_isbig(previouswhiteline)) + " | previous_IsHeadline = " + str(Headlinetag[head_k]) + " | Expression = " + str(expression.TheExpression) + " ==> This should be a headline!")
                                
                                if (decision)and(Headlinetag[head_k]==False):
                                    if (expression.Type==ExpressionType.TABLEOFCONTENTS)and(not(level==1)):
                                        Answer = False
                                        print("If expression <"+expression.TheExpression+"> is recognised as a headlines, its cascadelevel should be 1! It is " + str(level))
                                
                                if (decision)and(Headlinetag[head_k]==False):
                                    if (expression.Type==ExpressionType.CHAPTER)and(not(level==1)):
                                        Answer = False
                                        print("If expression <"+expression.TheExpression+"> is recognised as a headlines, its cascadelevel should be 1! It is " + str(level))
                                        
                                if (decision)and(Headlinetag[head_k]==False):
                                    if (expression.Type==ExpressionType.SECTION)and(not(level==2)):
                                        Answer = False
                                        print("If expression <"+expression.TheExpression+"> is recognised as a headlines, its cascadelevel should be 2! It is " + str(level))
                                
                                if (decision)and(Headlinetag[head_k]==False):
                                    if (expression.Type==ExpressionType.SUBSECTION)and(not(level==3)):
                                        Answer = False
                                        print("If expression <"+expression.TheExpression+"> is recognised as a headlines, its cascadelevel should be 3! It is " + str(level))
                                
                                if (decision)and(Headlinetag[head_k]==False):
                                    if (expression.Type==ExpressionType.SUBSUBSECTION)and(not(level==4)):
                                        Answer = False
                                        print("If expression <"+expression.TheExpression+"> is recognised as a headlines, its cascadelevel should be 4! It is " + str(level))
                                
                        # Adapt previous tags:
                    previouswhiteline = whiteline
            previousfontsize = fontsize
    # Then, return the answer:
    return Answer

def TestRule_footer() -> bool:
    """
    # Unit tests for the rule-function of the footer-class that inherits from textpart.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Begin by collecting the data that we need:
    fontregions = hardcodedfontregions("pdfminer")
    lineregions = hardcodedlineregions_pdfminer_SplitDoc()
    expressions = hardcodedexpressions()
    positions = [50.0, 100.0, 200.0]
    Headlinetag = [True, False]
    Headlinecascade = [1, 2]
    fontstyles = [True, False]
    fontsizes = [8.0, 9.9, 14.0]
    whitelines = [8.0, 12.0, 20.0]
    
    # Then, define the class and pass relevant information:
    thefooter = footer()
    thefooter.footerboundary = 60.0
    thefooter.headerboundary = 180.0
    thefooter.max_vertpos = 180.0 
    thefooter.min_vertpos = 60.0
    thefooter.fontregions = fontregions
    thefooter.lineregions = lineregions
    
    # Create a CurrenLine-object:
    thisline = CurrentLine()
    
    # Next, Define the answer and other parameters that we may need:
    Answer = True
    regularfontsize = thefooter.findregularfontregion().get_value()
    regularlevel = thefooter.findregularfontregion().get_cascadelevel()
    previousfontsize = 0.0
    previouswhiteline = -1.0
    
    # Then, loop over all expressions and over all positions and fontsizes:
    for expression in expressions:
        for fontsize in fontsizes:
            for position in positions:
                for whiteline in whitelines:
                    for isbold in fontstyles:
                        for isitalic in fontstyles:
                            for head_k in range(0,2):
                
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
                                [decision,level] = thefooter.rule(thisline)
                                
                                # Next, we must test if the outcome is what we expect:
                                # NOTE: this is obviously different for each rule.
                                if (decision==False)and(position<thefooter.footerboundary):
                                    Answer = False
                                    print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" the decision should be [True], as the position is below the footer boundary "+str(thefooter.footerboundary))
                                
                                if (decision==False)and(position>thefooter.headerboundary):
                                    Answer = False
                                    print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" the decision should be [True], as the position is above the header boundary "+str(thefooter.headerboundary))
                                    
                                if (decision==False)and(thefooter.fontsize_smallerthenregular(fontsize)):
                                    Answer = False
                                    print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" the decision should be [True], as the fontsize is smaller then regular")
                                    
                                if (decision==True)and(level<=regularlevel):
                                    Answer = False
                                    print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+": when the decision==True, cascadelevel("+str(level)+") should larger then the regular cascadelevel ("+str(regularlevel)+")")
                        
                        # Adapt previous tags:
                    previouswhiteline = whiteline
            previousfontsize = fontsize
    # Then, return the answer:
    return Answer

def TestRule_enumeration_a() -> bool:
    """
    # Unit tests for the rule-function of the enumeration-class that inherits from textpart.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Begin by collecting the data that we need:
    fontregions = hardcodedfontregions("pdfminer")
    lineregions = hardcodedlineregions_pdfminer_SplitDoc()
    expressions = hardcodedexpressions()
    positions = [50.0, 100.0, 200.0]
    Headlinetag = [True, False]
    Headlinecascade = [1, 2]
    fontstyles = [True, False]
    fontsizes = [8.0, 9.9, 14.0]
    whitelines = [8.0, 12.0, 20.0]
    
    # Then, define the class and pass relevant information:
    theenum = enumeration()
    theenum.footerboundary = 60.0
    theenum.headerboundary = 180.0
    theenum.max_vertpos = 180.0 
    theenum.min_vertpos = 60.0
    theenum.fontregions = fontregions
    theenum.lineregions = lineregions
    
    # Create a CurrenLine-object:
    thisline = CurrentLine()
    
    # Next, Define the answer and other parameters that we may need:
    Answer = True
    regularfontsize = theenum.findregularfontregion().get_value()
    regularlevel = theenum.findregularfontregion().get_cascadelevel()
    previousfontsize = 0.0
    previouswhiteline = -1.0
    
    # Then, loop over all expressions and over all positions and fontsizes:
    for expression in expressions:
        for fontsize in fontsizes:
            for position in positions:
                for whiteline in whitelines:
                    for isbold in fontstyles:
                        for isitalic in fontstyles:
                            for head_k in range(0,2):
                
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
                                [decision,level] = theenum.rule(thisline)
                                
                                # Next, we must test if the outcome is what we expect:
                                # NOTE: this is obviously different for each rule.
                                
                                # Then, check step-by-step when this is not possible:
                                if (expression.Type==ExpressionType.BIGROMAN_ENUMERATION)and(decision==False):
                                    Answer = False
                                    print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" the decision should not be [TRUE], as it starts with a bigroman enumeration-sign.")
                                
                                if (expression.Type==ExpressionType.SMALLROMAN_ENUMERATION)and(decision==False):
                                    Answer = False
                                    print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" the decision should not be [TRUE], as it starts with a smallroman enumeration-sign.")
                                
                                if (expression.Type==ExpressionType.BIGLETTER_ENUMERATION)and(decision==False):
                                    Answer = False
                                    print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" the decision should not be [TRUE], as it starts with a bigletter enumeration-sign.")
                                    
                                if (expression.Type==ExpressionType.SMALLLETTER_ENUMERATION)and(decision==False):
                                    Answer = False
                                    print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" the decision should not be [TRUE], as it starts with a smallletter enumeration-sign.")
                                    
                                if (expression.Type==ExpressionType.DIGIT_ENUMERATION)and(decision==False)and(theenum.whiteline_isbig(previouswhiteline)):
                                    Answer = False
                                    print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" the decision should not be [TRUE], as it starts with a digit enumeration-sign.")
                                    
                                if (expression.Type==ExpressionType.SIGNMARK_ENUMERATION)and(decision==False):
                                    Answer = False
                                    print("For expression <"+expression.TheExpression+">, fontsize="+str(fontsize)+", position="+str(position)+" the decision should not be [TRUE], as it starts with a sigmark (-) enumeration-sign.")
                                
                        # Adapt previous tags:
                    previouswhiteline = whiteline
            previousfontsize = fontsize
    # Then, return the answer:
    return Answer

def TestRule_enumeration_b() -> bool:
    """
    # Unit tests for the rule-function of the enumeration-class that inherits from textpart.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Begin by collecting the data that we need:
    fontregions = hardcodedfontregions("pdfminer")
    lineregions = hardcodedlineregions_pdfminer_SplitDoc()
    
    # Then, define the class and pass relevant information:
    theenum = enumeration()
    theenum.footerboundary = 60.0
    theenum.headerboundary = 180.0
    theenum.max_vertpos = 180.0 
    theenum.min_vertpos = 60.0
    theenum.fontregions = fontregions
    theenum.lineregions = lineregions
    Answer = True
    
    # Create a CurrenLine-object:
    thisline = CurrentLine()
    
    # Next, call a few specific cases that we wish to test. The idea is here
    # to specifically trigger the roman/letter discrepancy; small & big:
    # --------------------------------------------------------------------
    theenum.hierarchy.clear()
    
    thisline.textline = "h. some stuff"
    [decision,level1] = theenum.rule(thisline)
    if not decision: Answer = False
    
    thisline.textline = "i. some stuff"
    [decision,level2] = theenum.rule(thisline)
    if not decision: Answer = False
    
    # Now, level should be equal:
    if not (level1==level2):
        Answer = False
        print("h. -> i. incorrectly handled small roman/letter transfer.")
    theenum.hierarchy.clear()
    
    # --------------------------------------------------------------------
    theenum.hierarchy.clear()
    
    thisline.textline = "h. some stuff"
    [decision,level1] = theenum.rule(thisline)
    if not decision: Answer = False
    
    theenum.hierarchy.clear() # This is normally not a realistic case, but this way, we cover all possibilities in the code.
    
    thisline.textline = "i. some stuff"
    [decision,level2] = theenum.rule(thisline)
    if not decision: Answer = False
    
    # Now, level should be equal:
    if not (level1==level2):
        Answer = False
        print("h. -> i. incorrectly handled small roman/letter transfer.")
    theenum.hierarchy.clear()
    
    # --------------------------------------------------------------------

    thisline.textline = "b. some stuff"
    [decision,level1] = theenum.rule(thisline)
    if not decision: Answer = False
    
    thisline.textline = "i. some stuff"
    [decision,level2] = theenum.rule(thisline)
    if not decision: Answer = False
    
    # Now, level should NOT be equal:
    if (level1==level2):
        Answer = False
        print("b. -> i. incorrectly handled small roman/letter transfer.")
    theenum.hierarchy.clear()
    
    # --------------------------------------------------------------------
    
    thisline.textline = "b. some stuff"
    [decision,level1] = theenum.rule(thisline)
    if not decision: Answer = False
    
    theenum.hierarchy.append(enum_type.SMALLROMAN) # This is normally not a realistic case, but this way, we cover all possibilities in the code.
    
    thisline.textline = "i. some stuff"
    [decision,level2] = theenum.rule(thisline)
    if not decision: Answer = False
    
    # Now, level should NOT be equal:
    if (level1==level2):
        Answer = False
        print("b. -> i. incorrectly handled small roman/letter transfer.")
    theenum.hierarchy.clear()
    
    # --------------------------------------------------------------------
    
    thisline.textline = "H. some stuff"
    [decision,level1] = theenum.rule(thisline)
    if not decision: Answer = False
    
    thisline.textline = "I. some stuff"
    [decision,level2] = theenum.rule(thisline)
    if not decision: Answer = False

    # Now, level should be equal:
    if not (level1==level2):
        Answer = False
        print("H. -> I. incorrectly handled big roman/letter transfer.")
    theenum.hierarchy.clear()
    
    # --------------------------------------------------------------------
    theenum.hierarchy.clear()
    
    thisline.textline = "H. some stuff"
    [decision,level1] = theenum.rule(thisline)
    if not decision: Answer = False
    
    theenum.hierarchy.clear() # This is normally not a realistic case, but this way, we cover all possibilities in the code.
    
    thisline.textline = "I. some stuff"
    [decision,level2] = theenum.rule(thisline)
    if not decision: Answer = False

    # Now, level should be equal:
    if not (level1==level2):
        Answer = False
        print("H. -> I. incorrectly handled big roman/letter transfer.")
    theenum.hierarchy.clear()
    
    # --------------------------------------------------------------------
    
    thisline.textline = "B. some stuff"
    [decision,level1] = theenum.rule(thisline)
    if not decision: Answer = False
    
    thisline.textline = "I. some stuff"
    [decision,level2] = theenum.rule(thisline)
    if not decision: Answer = False
    
    # Now, level should NOT be equal:
    if (level1==level2):
        Answer = False
        print("B. -> I. incorrectly handled big roman/letter transfer.")
    theenum.hierarchy.clear()
    
    # --------------------------------------------------------------------
    
    thisline.textline = "B. some stuff"
    [decision,level1] = theenum.rule(thisline)
    if not decision: Answer = False
    
    theenum.hierarchy.append(enum_type.BIGROMAN) # This is normally not a realistic case, but this way, we cover all possibilities in the code.
    
    thisline.textline = "I. some stuff"
    [decision,level2] = theenum.rule(thisline)
    if not decision: Answer = False
    
    # Now, level should NOT be equal:
    if (level1==level2):
        Answer = False
        print("B. -> I. incorrectly handled big roman/letter transfer.")
    theenum.hierarchy.clear()
    
    # --------------------------------------------------------------------
    
    # return the Answer:
    return Answer

# NOTE: Add new textparts here!
# Bes ure to add a new unit-test for the new selection-rule!

def TestRule_title() -> bool:
    """
    # Unit tests for the rule-function of the title-class that inherits from textpart.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Begin by collecting the data that we need:
    fontregions = hardcodedfontregions("pdfminer")
    lineregions = hardcodedlineregions_pdfminer_SplitDoc()
    expressions = hardcodedexpressions()
    positions = [50.0, 100.0, 200.0]
    fontstyles = [True, False]
    Headlinetag = [True, False]
    Headlinecascade = [1, 2]
    fontsizes = [8.0, 9.9, 14.0]
    whitelines = [8.0, 12.0, 20.0]
    
    # Then, define the class and pass relevant information:
    thetitle = title()
    thetitle.footerboundary = 60.0
    thetitle.headerboundary = 180.0
    thetitle.max_vertpos = 180.0 
    thetitle.min_vertpos = 60.0
    thetitle.fontregions = fontregions
    thetitle.lineregions = lineregions
    
    # Create a CurrenLine-object:
    thisline = CurrentLine()
    
    # Next, Define the answer and other parameters that we may need:
    Answer = True
    regularfontsize = thetitle.findregularfontregion().get_value()
    regularlevel = thetitle.findregularfontregion().get_cascadelevel()
    previousfontsize = 0.0
    previouswhiteline = -1.0
    
    # Then, loop over all expressions and over all positions and fontsizes:
    for expression in expressions:
        for fontsize in fontsizes:
            for position in positions:
                for whiteline in whitelines:
                    for isbold in fontstyles:
                        for isitalic in fontstyles:
                            for head_k in range(0,2):
                
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
                                [decision,level] = thetitle.rule(thisline)
                                
                                # Next, we must test if the outcome is what we expect:
                                # NOTE: this is obviously different for each rule.
                                if (decision==True)or(not(level==0)):
                                    Answer = False
                                    print("As the title-rule has not yet been developed, it should never give anything else then [False,0]!")
                        
                        # Adapt previous tags:
                    previouswhiteline = whiteline
            previousfontsize = fontsize
    # Then, return the answer:
    return Answer

# NOTE: Add new textparts here!
# Bes ure to add a new unit-test for the new selection-rule!

def TestRule_alinea() -> bool:
    """
    # Unit tests for the rule-function of the textalinea-class that inherits from textpart.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Begin by collecting the data that we need:
    fontregions = hardcodedfontregions("pdfminer")
    lineregions = hardcodedlineregions_pdfminer_SplitDoc()
    expressions = hardcodedexpressions()
    positions = [50.0, 100.0, 200.0]
    fontstyles = [True, False]
    Headlinetag = [True, False]
    Headlinecascade = [1, 2]
    fontsizes = [8.0, 9.9, 14.0]
    whitelines = [8.0, 12.0, 20.0]
    
    # Then, define the class and pass relevant information:
    thealinea = textalinea()
    thealinea.footerboundary = 60.0
    thealinea.headerboundary = 180.0
    thealinea.max_vertpos = 180.0 
    thealinea.min_vertpos = 60.0
    thealinea.fontregions = fontregions
    thealinea.lineregions = lineregions
    
    # Create a CurrenLine-object:
    thisline = CurrentLine()
    
    # Next, Define the answer and other parameters that we may need:
    Answer = True
    regularfontsize = thealinea.findregularfontregion().get_value()
    regularlevel = thealinea.findregularfontregion().get_cascadelevel()
    previousfontsize = 0.0
    previouswhiteline = -1.0
    
    # Then, loop over all expressions and over all positions and fontsizes:
    for expression in expressions:
        for fontsize in fontsizes:
            for position in positions:
                for whiteline in whitelines:
                    for isbold in fontstyles:
                        for isitalic in fontstyles:
                            for head_k in range(0,2):
                
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
                                [decision,level] = thealinea.rule(thisline)
                                
                                # Next, we must test if the outcome is what we expect:
                                # NOTE: this is obviously different for each rule.
                                if (decision==True)or(not(level==0)):
                                    Answer = False
                                    print("the rule-function of textalinea-elements is not supposed to return anything else then [False,0]! textalinea-elements are not meant for selection.")
                        
                        # Adapt previous tags:
                    previouswhiteline = whiteline
            previousfontsize = fontsize
    # Then, return the answer:
    return Answer

def TestRule_textpart() -> bool:
    """
    # Unit tests for the rule-function of the textpart-class.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Begin by collecting the data that we need:
    fontregions = hardcodedfontregions("pdfminer")
    lineregions = hardcodedlineregions_pdfminer_SplitDoc()
    expressions = hardcodedexpressions()
    positions = [50.0, 100.0, 200.0]
    fontstyles = [True, False]
    Headlinetag = [True, False]
    Headlinecascade = [1, 2]
    fontsizes = [8.0, 9.9, 14.0]
    whitelines = [8.0, 12.0, 20.0]
    
    # Then, define the class and pass relevant information:
    thepart = textpart()
    thepart.footerboundary = 60.0
    thepart.headerboundary = 180.0
    thepart.max_vertpos = 180.0 
    thepart.min_vertpos = 60.0
    thepart.fontregions = fontregions
    thepart.lineregions = lineregions
    
    # Create a CurrenLine-object:
    thisline = CurrentLine()
    
    # Next, Define the answer and other parameters that we may need:
    Answer = True
    regularfontsize = thepart.findregularfontregion().get_value()
    regularlevel = thepart.findregularfontregion().get_cascadelevel()
    previousfontsize = 0.0
    previouswhiteline = -1.0
    
    # Then, loop over all expressions and over all positions and fontsizes:
    for expression in expressions:
        for fontsize in fontsizes:
            for position in positions:
                for whiteline in whitelines:
                    for isbold in fontstyles:
                        for isitalic in fontstyles:
                            for head_k in range(0,2):
                
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
                                [decision,level] = thepart.rule(thisline)
                                
                                # Next, we must test if the outcome is what we expect:
                                # NOTE: this is obviously different for each rule.
                                if (decision==True)or(not(level==0)):
                                    Answer = False
                                    print("the rule-function of textpart is not supposed to return anything else then [False,0]! The function is meant to be overwritten by children of textpart.")
                        
                        # Adapt previous tags:
                    previouswhiteline = whiteline
            previousfontsize = fontsize
    # Then, return the answer:
    return Answer

def TestMasterRule_textpart() -> bool:
    """
    # Unit tests for the masterrule-function of the textpart-class.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Begin by collecting the data that we need:
    fontregions = hardcodedfontregions("pdfminer")
    lineregions = hardcodedlineregions_pdfminer_SplitDoc()
    expressions = hardcodedexpressions()
    positions = [50.0, 100.0, 200.0]
    fontstyles = [True, False]
    Headlinetag = [True, False]
    Headlinecascade = [1, 2]
    fontsizes = [8.0, 9.9, 14.0]
    whitelines = [8.0, 12.0, 20.0]
    
    # Then, define the class and pass relevant information:
    thepart = textpart()
    thepart.footerboundary = 60.0
    thepart.headerboundary = 180.0
    thepart.max_vertpos = 180.0 
    thepart.min_vertpos = 60.0
    thepart.fontregions = fontregions
    thepart.lineregions = lineregions
    
    # Create a CurrenLine-object:
    thisline = CurrentLine()
    
    # Next, Define the answer and other parameters that we may need:
    Answer = True
    regularfontsize = thepart.findregularfontregion().get_value()
    regularlevel = thepart.findregularfontregion().get_cascadelevel()
    previousfontsize = 0.0
    previouswhiteline = -1.0
    
    # Then, loop over all expressions and over all positions and fontsizes:
    for expression in expressions:
        for fontsize in fontsizes:
            for position in positions:
                for whiteline in whitelines:
                    for isbold in fontstyles:
                        for isitalic in fontstyles:
                            for head_k in range(0,2):
                
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
                                decision = thepart.masterrule(thisline)
                                
                                # Next, we must test if the outcome is what we expect:
                                # NOTE: this is obviously different for each rule.
                                if (decision==True):
                                    Answer = False
                                    print("the masterrule-function of textpart is not supposed to return anything else then [False]! The function is meant to be overwritten by the textsplitter.")
                        
                        # Adapt previous tags:
                    previouswhiteline = whiteline
            previousfontsize = fontsize
    # Then, return the answer:
    return Answer

# Collection of all tests:
def TestRules() -> bool:
    """
    # Collection of unit tests of all the functions in regex_expressions.py
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define the answer:
    Answer = True
    
    # test the cases:
    
    if not TestRule_body():
        Answer = False
        print(" ==> TestRule_body() failed!")
    
    if not TestRule_headlines_a():
        Answer = False
        print(" ==> TestRule_headlines_a() failed!")
    
    if not TestRule_footer():
        Answer = False
        print(" ==> TestRule_footer() failed!")
    
    if not TestRule_enumeration_a():
        Answer = False
        print(" ==> TestRule_enumeration_a() failed!")
    
    if not TestRule_enumeration_b():
        Answer = False
        print(" ==> TestRule_enumeration_b() failed!")
    
    if not TestRule_title():
        Answer = False
        print(" ==> TestRule_title() failed!")
    
    if not TestRule_alinea():
        Answer = False
        print(" ==> TestRule_alinea() failed!")
        
    if not TestRule_textpart():
        Answer = False
        print(" ==> TestRule_textpart() failed!")
    
    if not TestMasterRule_textpart():
        Answer = False
        print(" ==> TestMasterRule_textpart() failed!")
        
    # Return the answer:
    return Answer

if __name__ == '__main__':
    if TestRules():
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
