import sys
from enum import Enum
# caution: path[0] is reserved for script path (or '' in REPL)

# Expression enumeration definition:
class ExpressionType(Enum):
    UNKNOWN = 0
    TABLEOFCONTENTS = 1
    CHAPTER = 2
    SECTION = 3
    SUBSECTION = 4
    SUBSUBSECTION = 5
    UNSUPPORTED = 6
    BIGROMAN_ENUMERATION = 7
    SMALLROMAN_ENUMERATION = 8
    BIGLETTER_ENUMERATION = 9
    SMALLLETTER_ENUMERATION = 10
    DIGIT_ENUMERATION = 11
    SIGNMARK_ENUMERATION = 12
    NORMAL = 13
    
# TestExpression definition:
class TestExpression:
    def __init__(self):
        self.Type = ExpressionType.UNKNOWN
        self.TheExpression = ""
        self.cascadelevel = 0

def hardcodedexpressions() -> list[TestExpression]:
    """
    Function to load hard-coded strings with a label about what
    you want to test (for example, using regex expressions)
    
    # Parameters: None
    # Return: list[TestExpression]: the expressions you want to use.
    """
    
    # --------------------------------------------------------
    
    # Declare array:
    expressions = []
    index = 0
    
    # Fill it:
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "Inhoudsopgave"
    expressions[index].cascadelevel = 1
    expressions[index].Type = ExpressionType.TABLEOFCONTENTS
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "Inhoud"
    expressions[index].cascadelevel = 1
    expressions[index].Type = ExpressionType.TABLEOFCONTENTS
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "Contents"
    expressions[index].cascadelevel = 1
    expressions[index].Type = ExpressionType.TABLEOFCONTENTS
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "Table of contents"
    expressions[index].cascadelevel = 1
    expressions[index].Type = ExpressionType.TABLEOFCONTENTS
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "Chapter 12"
    expressions[index].cascadelevel = 1
    expressions[index].Type = ExpressionType.CHAPTER
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "12 Some stupid stuff"
    expressions[index].cascadelevel = 1
    expressions[index].Type = ExpressionType.CHAPTER
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "143 Some stuff"
    expressions[index].cascadelevel = 1
    expressions[index].Type = ExpressionType.CHAPTER
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "Hoofdstuk 12 en dan..."
    expressions[index].cascadelevel = 1
    expressions[index].Type = ExpressionType.CHAPTER
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "Hoofdstuk III."
    expressions[index].cascadelevel = 1
    expressions[index].Type = ExpressionType.CHAPTER
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "chapter XI"
    expressions[index].cascadelevel = 1
    expressions[index].Type = ExpressionType.CHAPTER
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "Section 12"
    expressions[index].cascadelevel = 2
    expressions[index].Type = ExpressionType.SECTION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "sectie 12"
    expressions[index].cascadelevel = 2
    expressions[index].Type = ExpressionType.SECTION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "12.1 Some title"
    expressions[index].cascadelevel = 2
    expressions[index].Type = ExpressionType.SECTION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "5.2."
    expressions[index].cascadelevel = 2
    expressions[index].Type = ExpressionType.SECTION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "2.13.8 and some more annoying stuff"
    expressions[index].cascadelevel = 3
    expressions[index].Type = ExpressionType.SUBSECTION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "subsectie 2.13.8"
    expressions[index].cascadelevel = 3
    expressions[index].Type = ExpressionType.SUBSECTION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "Subsection 2.13.8"
    expressions[index].cascadelevel = 3
    expressions[index].Type = ExpressionType.SUBSECTION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "31.4.7.91 and some more annoying stuff"
    expressions[index].cascadelevel = 4
    expressions[index].Type = ExpressionType.SUBSUBSECTION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "31.4.7.91.12 and some more annoying stuff"
    expressions[index].cascadelevel = 4
    expressions[index].Type = ExpressionType.NORMAL # ATTENTION: it is not normal, but we denote it as, as our current code does not recognise this and will, therefore, classify it as BODY.
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "F. kjsjd"
    expressions[index].cascadelevel = 5
    expressions[index].Type = ExpressionType.BIGLETTER_ENUMERATION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "G) kjsjd"
    expressions[index].cascadelevel = 5
    expressions[index].Type = ExpressionType.BIGLETTER_ENUMERATION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "(K) kjsjd"
    expressions[index].cascadelevel = 5
    expressions[index].Type = ExpressionType.BIGLETTER_ENUMERATION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "E."
    expressions[index].cascadelevel = 5
    expressions[index].Type = ExpressionType.BIGLETTER_ENUMERATION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "f. kjsjd"
    expressions[index].cascadelevel = 5
    expressions[index].Type = ExpressionType.SMALLLETTER_ENUMERATION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "g) kjsjd"
    expressions[index].cascadelevel = 5
    expressions[index].Type = ExpressionType.SMALLLETTER_ENUMERATION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "(k) kjsjd"
    expressions[index].cascadelevel = 5
    expressions[index].Type = ExpressionType.SMALLLETTER_ENUMERATION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "e."
    expressions[index].cascadelevel = 5
    expressions[index].Type = ExpressionType.SMALLLETTER_ENUMERATION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "IV. kjsjd"
    expressions[index].cascadelevel = 5
    expressions[index].Type = ExpressionType.BIGROMAN_ENUMERATION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "IX."
    expressions[index].cascadelevel = 5
    expressions[index].Type = ExpressionType.BIGROMAN_ENUMERATION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "VI)"
    expressions[index].cascadelevel = 5
    expressions[index].Type = ExpressionType.BIGROMAN_ENUMERATION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "(VIII)"
    expressions[index].cascadelevel = 5
    expressions[index].Type = ExpressionType.BIGROMAN_ENUMERATION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "iv. kjsjd"
    expressions[index].cascadelevel = 5
    expressions[index].Type = ExpressionType.SMALLROMAN_ENUMERATION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "ix."
    expressions[index].cascadelevel = 5
    expressions[index].Type = ExpressionType.SMALLROMAN_ENUMERATION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "vi)"
    expressions[index].cascadelevel = 5
    expressions[index].Type = ExpressionType.SMALLROMAN_ENUMERATION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "(xiv)"
    expressions[index].cascadelevel = 5
    expressions[index].Type = ExpressionType.SMALLROMAN_ENUMERATION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "iii. and some more annoying stuff"
    expressions[index].cascadelevel = 5
    expressions[index].Type = ExpressionType.SMALLROMAN_ENUMERATION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "1)"
    expressions[index].cascadelevel = 5
    expressions[index].Type = ExpressionType.DIGIT_ENUMERATION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "2."
    expressions[index].cascadelevel = 5
    expressions[index].Type = ExpressionType.DIGIT_ENUMERATION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "(3)"
    expressions[index].cascadelevel = 5
    expressions[index].Type = ExpressionType.DIGIT_ENUMERATION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "4. Some stuff"
    expressions[index].cascadelevel = 5
    expressions[index].Type = ExpressionType.DIGIT_ENUMERATION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "3."
    expressions[index].cascadelevel = 5
    expressions[index].Type = ExpressionType.DIGIT_ENUMERATION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "- some tekst"
    expressions[index].cascadelevel = 5
    expressions[index].Type = ExpressionType.SIGNMARK_ENUMERATION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "– some tekst"
    expressions[index].cascadelevel = 5
    expressions[index].Type = ExpressionType.SIGNMARK_ENUMERATION
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "and this is then some plain line with 12 45 some digits."
    expressions[index].cascadelevel = 5
    expressions[index].Type = ExpressionType.NORMAL
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "Now we just add some more random text."
    expressions[index].cascadelevel = 5
    expressions[index].Type = ExpressionType.NORMAL
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "Then we talk about chapters, figures and other stuff..."
    expressions[index].cascadelevel = 5
    expressions[index].Type = ExpressionType.NORMAL
    
    expressions.append(TestExpression())
    index = len(expressions)-1
    expressions[index].TheExpression = "finally, we state that the EU is ineed a bureaucratic mess..."
    expressions[index].cascadelevel = 5
    expressions[index].Type = ExpressionType.NORMAL
    
    # return the expressions:
    return expressions
