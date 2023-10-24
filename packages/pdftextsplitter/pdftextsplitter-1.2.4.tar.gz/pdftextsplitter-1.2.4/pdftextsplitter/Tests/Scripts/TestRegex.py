import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from TextPart code:
sys.path.insert(1, '../../')
from TextPart.regex_expressions import remove_nonletters
from TextPart.regex_expressions import contains_tablecontentsregex
from TextPart.regex_expressions import contains_chapterregex
from TextPart.regex_expressions import contains_artikelregex
from TextPart.regex_expressions import contains_sectionregex
from TextPart.regex_expressions import contains_subsectionregex
from TextPart.regex_expressions import contains_subsubsectionregex
from TextPart.regex_expressions import contains_bigroman_enumeration
from TextPart.regex_expressions import contains_smallroman_enumeration
from TextPart.regex_expressions import contains_bigletter_enumeration
from TextPart.regex_expressions import contains_smallletter_enumeration
from TextPart.regex_expressions import contains_digit_enumeration
from TextPart.regex_expressions import contains_pointtwo_enumeration
from TextPart.regex_expressions import contains_signmark_enumeration
from TextPart.regex_expressions import contains_headlines_regex
from TextPart.regex_expressions import text_isnotcapped
from TextPart.regex_expressions import contains_letter_signing

# Imports from Tools:
sys.path.insert(2, '../Tools/')
from hardcodedexpressions import ExpressionType
from hardcodedexpressions import TestExpression
from hardcodedexpressions import hardcodedexpressions

# Definition of unit tests:
def TestRegex_remove_nonletters() -> bool:
    """
    # Unit tests for the function remove_nonletters from the script regex_expressions.py
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define the answer:
    Answer = True
    
    # Test a certain number of cases:
    if not (remove_nonletters("dhdkhd")=="dhdkhd"):
        Answer = False
        print('The outcome of remove_nonletters("dhdkhd") is <'+remove_nonletters("dhdkhd")+'> while we expected <dhdkhd>.')
    
    if not (remove_nonletters("dhHFdkhJTd")=="dhHFdkhJTd"):
        Answer = False
        print('The outcome of remove_nonletters("dhHFdkhJTd") is <'+remove_nonletters("dhHFdkhJTd")+'> while we expected <dhHFdkhJTd>.')
    
    if not (remove_nonletters("12 dhdkhd")=="dhdkhd"):
        Answer = False
        print('The outcome of remove_nonletters("12 dhdkhd") is <'+remove_nonletters("12 dhdkhd")+'> while we expected <dhdkhd>.')
    
    if not (remove_nonletters("12 dh &@dkhd")=="dhdkhd"):
        Answer = False
        print('The outcome of remove_nonletters("12 dh &@dkhd") is <'+remove_nonletters("12 dh &@dkhd")+'> while we expected <dhdkhd>.')
    
    # Return the answer:
    return Answer

def TestRegex_contains_tablecontentsregex() -> bool:
    """
    # Unit tests for the function contains_tablecontentsregex from the script regex_expressions.py
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define the answer:
    Answer = True
    
    # Load the hard-code expressions:
    expressions = hardcodedexpressions()
    
    # loop over them and test them:
    for expression in expressions:
        if (contains_tablecontentsregex(expression.TheExpression))and(not(expression.Type==ExpressionType.TABLEOFCONTENTS)):
                Answer = False
                print("The outcome of contains_tablecontentsregex("+expression.TheExpression+") is supposed to be [False]")
        if (not(contains_tablecontentsregex(expression.TheExpression)))and(expression.Type==ExpressionType.TABLEOFCONTENTS):
                Answer = False
                print("The outcome of contains_tablecontentsregex("+expression.TheExpression+") is supposed to be [True]")
    
    # Return the answer:
    return Answer

def TestRegex_text_isnotcapped() -> bool:
    """
    # Unit tests for the function text_isnotcapped from the script regex_expressions.py
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define the answer:
    Answer = True
    
    # This requires the use of some special expressions:
    Expression1 = "This is some story that is not capped."
    Expression2 = "This text is capped and should"
    
    # Test them:
    if not text_isnotcapped(Expression1):
        Answer = False
        print("Expression <"+str(Expression1)+"> should be registered as not capped!")
    if text_isnotcapped(Expression2):
        Answer = False
        print("Expression <"+str(Expression2)+"> should be registered as capped!")
    
    # Return the answer:
    return Answer

def TestRegex_lettersigning() -> bool:
    """
    # Unit tests for the function contains_letter_signing from the script regex_expressions.py
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define the answer:
    Answer = True
    
    # This requires the use of some special expressions:
    Expression1 = "This is some text that is not supposed to hit anything."
    Expression2 = "Queen Elizabeth"
    Expression3 = "Ministre des Sports et des Jeux"
    Expression4 = "Getekend door een minister"
    
    # Test them:
    if contains_letter_signing(Expression1):
        Answer = False
        print("Expression <"+str(Expression1)+"> should be FALSE!")
    if contains_letter_signing(Expression2):
        Answer = False
        print("Expression <"+str(Expression2)+"> should be FALSE!")
    if not contains_letter_signing(Expression3):
        Answer = False
        print("Expression <"+str(Expression3)+"> should be TRUE!")
    if not contains_letter_signing(Expression4):
        Answer = False
        print("Expression <"+str(Expression4)+"> should be TRUE!")
    
    # Return the answer:
    return Answer

def TestRegex_contains_chapterregex() -> bool:
    """
    # Unit tests for the function contains_tablecontentsregex from the script regex_expressions.py
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define the answer:
    Answer = True
    
    # Load the hard-code expressions:
    expressions = hardcodedexpressions()
    
    # loop over them and test them:
    for expression in expressions:
        if (contains_chapterregex(expression.TheExpression))and(not(expression.Type==ExpressionType.CHAPTER)):
            if not((contains_digit_enumeration(expression.TheExpression,False))and(expression.Type==ExpressionType.DIGIT_ENUMERATION)): # to filter out the double-hits like <2. headline>
                Answer = False
                print("The outcome of contains_chapterregex("+expression.TheExpression+") is supposed to be [False]")
        if (not(contains_chapterregex(expression.TheExpression)))and(expression.Type==ExpressionType.CHAPTER):
            if not((contains_digit_enumeration(expression.TheExpression,False))and(expression.Type==ExpressionType.DIGIT_ENUMERATION)): # to filter out the double-hits like <2. headline>
                Answer = False
                print("The outcome of contains_chapterregex("+expression.TheExpression+") is supposed to be [True]")
    
    # Return the answer:
    return Answer

def TestRegex_contains_artikelregex() -> bool:
    """
    # Unit tests for the function contains_tablecontentsregex from the script regex_expressions.py
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define the answer:
    Answer = True

    # test the selection process:
    if not contains_artikelregex("Artikel 12"):
        Answer = False
        print('The outcome of contains_artikelregex("Artikel 12") is supposed to be [True]')
    if not contains_artikelregex("Article 9"):
        Answer = False
        print('The outcome of contains_artikelregex("Article 9") is supposed to be [True]')
    if contains_artikelregex("Chapter 7"):
        Answer = False
        print('The outcome of contains_artikelregex("Chapter 7") is supposed to be [False]')
    
    # Return the answer:
    return Answer

def TestRegex_contains_sectionregex() -> bool:
    """
    # Unit tests for the function contains_tablecontentsregex from the script regex_expressions.py
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define the answer:
    Answer = True
    
    # Load the hard-code expressions:
    expressions = hardcodedexpressions()
    
    # loop over them and test them:
    for expression in expressions:
        if (contains_sectionregex(expression.TheExpression))and(not(expression.Type==ExpressionType.SECTION)):
                Answer = False
                print("The outcome of contains_sectionregex("+expression.TheExpression+") is supposed to be [False]")
        if (not(contains_sectionregex(expression.TheExpression)))and(expression.Type==ExpressionType.SECTION):
                Answer = False
                print("The outcome of contains_sectionregex("+expression.TheExpression+") is supposed to be [True]")
    
    # Return the answer:
    return Answer

def TestRegex_contains_subsectionregex() -> bool:
    """
    # Unit tests for the function contains_tablecontentsregex from the script regex_expressions.py
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define the answer:
    Answer = True
    
    # Load the hard-code expressions:
    expressions = hardcodedexpressions()
    
    # loop over them and test them:
    for expression in expressions:
        if (contains_subsectionregex(expression.TheExpression))and(not(expression.Type==ExpressionType.SUBSECTION)):
                Answer = False
                print("The outcome of contains_subsectionregex("+expression.TheExpression+") is supposed to be [False]")
        if (not(contains_subsectionregex(expression.TheExpression)))and(expression.Type==ExpressionType.SUBSECTION):
                Answer = False
                print("The outcome of contains_subsectionregex("+expression.TheExpression+") is supposed to be [True]")
    
    # Return the answer:
    return Answer

def TestRegex_contains_subsubsectionregex() -> bool:
    """
    # Unit tests for the function contains_tablecontentsregex from the script regex_expressions.py
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define the answer:
    Answer = True
    
    # Load the hard-code expressions:
    expressions = hardcodedexpressions()
    
    # loop over them and test them:
    for expression in expressions:
        if (contains_subsubsectionregex(expression.TheExpression))and(not(expression.Type==ExpressionType.SUBSUBSECTION)):
                Answer = False
                print("The outcome of contains_subsubsectionregex("+expression.TheExpression+") is supposed to be [False]")
        if (not(contains_subsubsectionregex(expression.TheExpression)))and(expression.Type==ExpressionType.SUBSUBSECTION):
                Answer = False
                print("The outcome of contains_subsubsectionregex("+expression.TheExpression+") is supposed to be [True]")
    
    # Return the answer:
    return Answer

def TestRegex_contains_headlinesregex() -> bool:
    """
    # Unit tests for the function contains_headlines_regex from the script regex_expressions.py
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define the answer:
    Answer = True
    
    # Load the hard-code expressions:
    expressions = hardcodedexpressions()
    
    # loop over them and test them:
    for expression in expressions:
        if (not(contains_headlines_regex(expression.TheExpression))):
                if (expression.Type==ExpressionType.SUBSUBSECTION)or(expression.Type==ExpressionType.SUBSECTION)or(expression.Type==ExpressionType.SECTION)or(expression.Type==ExpressionType.CHAPTER):
                    if not((contains_digit_enumeration(expression.TheExpression,False))and(expression.Type==ExpressionType.DIGIT_ENUMERATION)): # to filter out the double-hits like <2. headline>
                        Answer = False
                        print("The outcome of contains_headlines_regex("+expression.TheExpression+") is supposed to be [True]")
        if (contains_headlines_regex(expression.TheExpression)):
                if (not((expression.Type==ExpressionType.SUBSUBSECTION)or(expression.Type==ExpressionType.SUBSECTION)or(expression.Type==ExpressionType.SECTION)or(expression.Type==ExpressionType.CHAPTER))):
                    if not((contains_digit_enumeration(expression.TheExpression,False))and(expression.Type==ExpressionType.DIGIT_ENUMERATION)): # to filter out the double-hits like <2. headline>
                        Answer = False
                        print("The outcome of contains_headlines_regex("+expression.TheExpression+") is supposed to be [False]")

    # Return the answer:
    return Answer

def TestRegex_contains_bigroman_enumeration_regex() -> bool:
    """
    # Unit tests for the function contains_bigroman_enumeration from the script regex_expressions.py
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define the answer:
    Answer = True
    
    # Load the hard-code expressions:
    expressions = hardcodedexpressions()
    
    # loop over them and test them:
    for expression in expressions:
        if (contains_bigroman_enumeration(expression.TheExpression))and(not(expression.Type==ExpressionType.BIGROMAN_ENUMERATION)):
                Answer = False
                print("The outcome of contains_bigroman_enumeration("+expression.TheExpression+") is supposed to be [False]")
        if (not(contains_bigroman_enumeration(expression.TheExpression)))and(expression.Type==ExpressionType.BIGROMAN_ENUMERATION):
                Answer = False
                print("The outcome of contains_bigroman_enumeration("+expression.TheExpression+") is supposed to be [True]")
    
    # Return the answer:
    return Answer

def TestRegex_contains_smallroman_enumeration_regex() -> bool:
    """
    # Unit tests for the function contains_smallroman_enumeration from the script regex_expressions.py
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define the answer:
    Answer = True
    
    # Load the hard-code expressions:
    expressions = hardcodedexpressions()
    
    # loop over them and test them:
    for expression in expressions:
        if (contains_smallroman_enumeration(expression.TheExpression))and(not(expression.Type==ExpressionType.SMALLROMAN_ENUMERATION)):
                Answer = False
                print("The outcome of contains_smallroman_enumeration("+expression.TheExpression+") is supposed to be [False]")
        if (not(contains_smallroman_enumeration(expression.TheExpression)))and(expression.Type==ExpressionType.SMALLROMAN_ENUMERATION):
                Answer = False
                print("The outcome of contains_smallroman_enumeration("+expression.TheExpression+") is supposed to be [True]")
    
    # Return the answer:
    return Answer

def TestRegex_contains_bigletter_enumeration_regex() -> bool:
    """
    # Unit tests for the function contains_bigletter_enumeration from the script regex_expressions.py
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define the answer:
    Answer = True
    
    # Load the hard-code expressions:
    expressions = hardcodedexpressions()
    
    # loop over them and test them:
    for expression in expressions:
        if (contains_bigletter_enumeration(expression.TheExpression))and(not(expression.Type==ExpressionType.BIGLETTER_ENUMERATION)):
                Answer = False
                print("The outcome of contains_bigletter_enumeration("+expression.TheExpression+") is supposed to be [False]")
        if (not(contains_bigletter_enumeration(expression.TheExpression)))and(expression.Type==ExpressionType.BIGLETTER_ENUMERATION):
                Answer = False
                print("The outcome of contains_bigletter_enumeration("+expression.TheExpression+") is supposed to be [True]")
    
    # Return the answer:
    return Answer

def TestRegex_contains_smallletter_enumeration_regex() -> bool:
    """
    # Unit tests for the function contains_smallletter_enumeration from the script regex_expressions.py
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define the answer:
    Answer = True
    
    # Load the hard-code expressions:
    expressions = hardcodedexpressions()
    
    # loop over them and test them:
    for expression in expressions:
        if (contains_smallletter_enumeration(expression.TheExpression))and(not(expression.Type==ExpressionType.SMALLLETTER_ENUMERATION)):
                Answer = False
                print("The outcome of contains_smallletter_enumeration("+expression.TheExpression+") is supposed to be [False]")
        if (not(contains_smallletter_enumeration(expression.TheExpression)))and(expression.Type==ExpressionType.SMALLLETTER_ENUMERATION):
                Answer = False
                print("The outcome of contains_smallletter_enumeration("+expression.TheExpression+") is supposed to be [True]")
    
    # Return the answer:
    return Answer

def TestRegex_contains_digit_enumeration_regex() -> bool:
    """
    # Unit tests for the function contains_digit_enumeration from the script regex_expressions.py
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define the answer:
    Answer = True
    
    # Load the hard-code expressions:
    expressions = hardcodedexpressions()
    
    # loop over them and test them:
    for expression in expressions:
        if (contains_digit_enumeration(expression.TheExpression,False))and(not(expression.Type==ExpressionType.DIGIT_ENUMERATION)):
                Answer = False
                print("The outcome of contains_digit_enumeration("+expression.TheExpression+") is supposed to be [False]")
        if (not(contains_digit_enumeration(expression.TheExpression,False)))and(expression.Type==ExpressionType.DIGIT_ENUMERATION):
                Answer = False
                print("The outcome of contains_digit_enumeration("+expression.TheExpression+") is supposed to be [True]")
    
    # test the termination-process:
    if contains_digit_enumeration("3.",True): 
        Answer = False
        print('The outcome of contains_digit_enumeration("3.",True) is supposed to be [False]')
    if contains_digit_enumeration("4)",True): 
        Answer = False
        print('The outcome of contains_digit_enumeration("4)",True) is supposed to be [False]')
    if contains_digit_enumeration("(5)",True): 
        Answer = False
        print('The outcome of contains_digit_enumeration("(5)",True) is supposed to be [False]')
    
    # Return the answer:
    return Answer

def TestRegex_contains_pointtwo_enumeration_regex() -> bool:
    """
    # Unit tests for the function contains_digit_enumeration from the script regex_expressions.py
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define the answer:
    Answer = True

    # test the selection process:
    if not contains_pointtwo_enumeration("2. nog wat stuff",False): 
        Answer = False
        print('The outcome of contains_pointtwo_enumeration("2.",False) is supposed to be [True]')
    if not contains_pointtwo_enumeration("2) ",False): 
        Answer = False
        print('The outcome of contains_pointtwo_enumeration("2)",False) is supposed to be [True]')
    if not contains_pointtwo_enumeration("(2)",False): 
        Answer = False
        print('The outcome of contains_pointtwo_enumeration("(2)",False) is supposed to be [True]')
        
    # test the selection process:
    if contains_pointtwo_enumeration("3. nog wat stuff",False): 
        Answer = False
        print('The outcome of contains_pointtwo_enumeration("3.",False) is supposed to be [False]')
    if contains_pointtwo_enumeration("4) ",False): 
        Answer = False
        print('The outcome of contains_pointtwo_enumeration("4)",False) is supposed to be [False]')
    if contains_pointtwo_enumeration("(5)",False): 
        Answer = False
        print('The outcome of contains_pointtwo_enumeration("(5)",False) is supposed to be [False]')
    
    # test the termination-process:
    if contains_pointtwo_enumeration("2.",True): 
        Answer = False
        print('The outcome of contains_pointtwo_enumeration("2.",True) is supposed to be [False]')
    if contains_pointtwo_enumeration("2)",True): 
        Answer = False
        print('The outcome of contains_pointtwo_enumeration("2)",True) is supposed to be [False]')
    if contains_pointtwo_enumeration("(3)",True): 
        Answer = False
        print('The outcome of contains_pointtwo_enumeration("(3)",True) is supposed to be [False]')
    
    # Return the answer:
    return Answer

def TestRegex_contains_signmark_enumeration_regex() -> bool:
    """
    # Unit tests for the function contains_signmark_enumeration from the script regex_expressions.py
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define the answer:
    Answer = True
    
    # Load the hard-code expressions:
    expressions = hardcodedexpressions()
    
    # loop over them and test them:
    for expression in expressions:
        if (contains_signmark_enumeration(expression.TheExpression))and(not(expression.Type==ExpressionType.SIGNMARK_ENUMERATION)):
                Answer = False
                print("The outcome of contains_signmark_enumeration("+expression.TheExpression+") is supposed to be [False]")
        if (not(contains_signmark_enumeration(expression.TheExpression)))and(expression.Type==ExpressionType.SIGNMARK_ENUMERATION):
                Answer = False
                print("The outcome of contains_signmark_enumeration("+expression.TheExpression+") is supposed to be [True]")
    
    # Return the answer:
    return Answer


# Collection of all tests:
def TestRegex() -> bool:
    """
    # Collection of unit tests of all the functions in regex_expressions.py
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define the answer:
    Answer = True
    
    # test the cases:
    if not TestRegex_remove_nonletters():
        Answer = False
        print(" ==> TestRegex_remove_nonletters() failed!")
    
    if not TestRegex_text_isnotcapped():
        Answer = False
        print(" ==> TestRegex_text_isnotcapped() failed!")
        
    if not TestRegex_lettersigning():
        Answer = False
        print(" ==> TestRegex_lettersigning() failed!")
    
    if not TestRegex_contains_tablecontentsregex():
        Answer = False
        print(" ==> TestRegex_contains_tablecontentsregex() failed!")
        
    if not TestRegex_contains_artikelregex():
        Answer = False
        print(" ==> TestRegex_contains_artikelregex() failed!")
    
    if not TestRegex_contains_chapterregex():
        Answer = False
        print(" ==> TestRegex_contains_chapterregex() failed!")
        
    if not TestRegex_contains_sectionregex():
        Answer = False
        print(" ==> TestRegex_contains_sectionregex() failed!")
        
    if not TestRegex_contains_subsectionregex():
        Answer = False
        print(" ==> TestRegex_contains_subsectionregex() failed!")
        
    if not TestRegex_contains_subsubsectionregex():
        Answer = False
        print(" ==> TestRegex_contains_subsubsectionregex() failed!")
    
    if not TestRegex_contains_headlinesregex():
        Answer = False
        print(" ==> TestRegex_contains_headlinesregex() failed!")
        
    if not TestRegex_contains_bigroman_enumeration_regex():
        Answer = False
        print(" ==> TestRegex_contains_bigroman_enumeration_regex() failed!")
        
    if not TestRegex_contains_smallroman_enumeration_regex():
        Answer = False
        print(" ==> TestRegex_contains_smallroman_enumeration_regex() failed!")
        
    if not TestRegex_contains_bigletter_enumeration_regex():
        Answer = False
        print(" ==> TestRegex_contains_bigletter_enumeration_regex() failed!")
        
    if not TestRegex_contains_smallletter_enumeration_regex():
        Answer = False
        print(" ==> TestRegex_contains_smallletter_enumeration_regex() failed!")
        
    if not TestRegex_contains_digit_enumeration_regex():
        Answer = False
        print(" ==> TestRegex_contains_digit_enumeration_regex() failed!")
        
    if not TestRegex_contains_pointtwo_enumeration_regex():
        Answer = False
        print(" ==> TestRegex_contains_pointtwo_enumeration_regex() failed!")
        
    if not TestRegex_contains_signmark_enumeration_regex():
        Answer = False
        print(" ==> TestRegex_contains_signmark_enumeration_regex() failed!")
    
    # Return the answer:
    return Answer

if __name__ == '__main__':
    if TestRegex():
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
