# Python functionality:
import re

def remove_nonletters(textline: str) -> str:
    """
    Function that removes all characters from a line,
    except small and captial letters. whitespaces are
    also removed.
    
    # Parameters:
    textline: str: the string you would like to edit.
    Returns: str: the edited string.
    
    # ATTENTION: When changing or adding something to this function, be sure
    to add more testcases to hardcodedexpressions.py as well!!!
    """

    # ---------------------------------------------------    

    reduction = re.sub(r'[^a-zA-Z \s+ ]', '', textline)
    reduction = reduction.replace(' ', '')
    return reduction

def text_isnotcapped(textline: str) -> str:
    """
    Function that uses regex-expressions to test if a certain string
    is capped text or not. The most obvious way to do so, is to
    test if it end in a point or not, but teh function can be expanded.
    
    # Parameters:
    textline: str: the string you would like to edit.
    Returns: str: the edited string.
    
    # ATTENTION: When changing or adding something to this function, be sure
    to add more testcases to hardcodedexpressions.py as well!!!
    """

    # ---------------------------------------------------    

    # Define all allowed chapter regex expressions:
    capped_regex_expressions = []
    capped_regex_expressions.append(r'(\.)$')

    # Test if the textline starts/ends with one of them:
    Answer = False
    for expression in capped_regex_expressions:
        if re.compile(expression).search(textline):
            Answer = True

    # Return the answer. If it DOES contain a point (or another
    # expression), the text is NOT capped, so Answer==True.
    if (textline==""): Answer = False
    return Answer

def contains_tablecontentsregex(textline: str) -> bool:
    """
    Function to check wether a certain textline starts
    with certain regional expression (regex). The regex
    is hard-coded in this function, as it is specific for
    identification of the table of contents:
    
    # Parameters:
    textline: str: the string you would like to test
    Returns: bool: the answer to the question.
    
    # ATTENTION: When changing or adding something to this function, be sure
    to add more testcases to hardcodedexpressions.py as well!!!
    """

    # ---------------------------------------------------    

    # Define all allowed chapter regex expressions:
    contenttabel_regex_expressions = []
    contenttabel_regex_expressions.append(r'^Content')
    contenttabel_regex_expressions.append(r'^content')
    contenttabel_regex_expressions.append(r'content$')
    contenttabel_regex_expressions.append(r'contents$')
    contenttabel_regex_expressions.append(r'content.$')
    contenttabel_regex_expressions.append(r'contents.$')
    contenttabel_regex_expressions.append(r'^Inhoud')
    contenttabel_regex_expressions.append(r'^inhoud')

    # Test if the extline starts with one of them:
    Answer = False
    for expression in contenttabel_regex_expressions:
        if re.compile(expression).search(textline):
            Answer = True

    # Return the answer:
    if (textline==""): Answer = False
    return Answer

def contains_artikelregex(textline: str) -> bool:
    """
    Function to check wether a certain textline starts
    with certain regional expression (regex). The regex
    is hard-coded in this function, as it is specific for
    a chapter-textline.
    
    # Parameters:
    textline: str: the string you would like to test
    Returns: bool: the answer to the question.
    
    # ATTENTION: When changing or adding something to this function, be sure
    to add more testcases to hardcodedexpressions.py as well!!!
    """

    # ---------------------------------------------------    

    # Define all allowed chapter regex expressions:
    artikel_regex_expressions = []

    # Standard scientific chapters:
    artikel_regex_expressions.append(r'^Artikel (\d+)')
    artikel_regex_expressions.append(r'^Article (\d+)')

    # Test if the extline starts with one of them:
    Answer = False
    for expression in artikel_regex_expressions:
        if re.compile(expression, re.MULTILINE).search(textline):
            Answer = True
    
    # NOTE: make sure that it does NOT accidentally fire 'true'
    # on a section or signmark:
    if re.compile(r'^(\d+)(\.)(\d+)').search(textline): Answer = False
    if re.compile(r'^ –').search(textline): Answer = False
    if (textline==""): Answer = False

    # Return the answer:
    return Answer

def contains_chapterregex(textline: str) -> bool:
    """
    Function to check wether a certain textline starts
    with certain regional expression (regex). The regex
    is hard-coded in this function, as it is specific for
    a chapter-textline.
    
    # Parameters:
    textline: str: the string you would like to test
    Returns: bool: the answer to the question.
    
    # ATTENTION: When changing or adding something to this function, be sure
    to add more testcases to hardcodedexpressions.py as well!!!
    """

    # ---------------------------------------------------    

    # Define all allowed chapter regex expressions:
    chapter_regex_expressions = []

    # Standard scientific chapters:
    chapter_regex_expressions.append(r'^(\d+) ')
    chapter_regex_expressions.append(r'^(\d+)$')
    chapter_regex_expressions.append(r'^(\d+)(\.) ')
    chapter_regex_expressions.append(r'^(\d+)(\.)$')
    chapter_regex_expressions.append(r'^Chapter (\d+)')
    chapter_regex_expressions.append(r'^chapter (\d+)')
    chapter_regex_expressions.append(r'^Hoofdstuk (\d+)')
    chapter_regex_expressions.append(r'^hoofdstuk (\d+)')
    chapter_regex_expressions.append(r'^M{0,3}(CM|CD|D?C{0,3})?(XC|XL|L?X{0,3})?(IX|IV|V?I{0,3})? ')
    chapter_regex_expressions.append(r'^M{0,3}(CM|CD|D?C{0,3})?(XC|XL|L?X{0,3})?(IX|IV|V?I{0,3})?$')
    chapter_regex_expressions.append(r'^Chapter M{0,3}(CM|CD|D?C{0,3})?(XC|XL|L?X{0,3})?(IX|IV|V?I{0,3})?')
    chapter_regex_expressions.append(r'^chapter M{0,3}(CM|CD|D?C{0,3})?(XC|XL|L?X{0,3})?(IX|IV|V?I{0,3})?')
    chapter_regex_expressions.append(r'^Hoofdstuk M{0,3}(CM|CD|D?C{0,3})?(XC|XL|L?X{0,3})?(IX|IV|V?I{0,3})?')
    chapter_regex_expressions.append(r'^hoofdstuk M{0,3}(CM|CD|D?C{0,3})?(XC|XL|L?X{0,3})?(IX|IV|V?I{0,3})?')
    
    # To get the correct structure from documents like cellar:
    chapter_regex_expressions.append(r'^Artikel (\d+)')
    chapter_regex_expressions.append(r'^Article (\d+)')
    chapter_regex_expressions.append(r'^Annex (\d+)')
    chapter_regex_expressions.append(r'^ANNEX (\d+)')
    chapter_regex_expressions.append(r'^Abstract')

    # Test if the extline starts with one of them:
    Answer = False
    for expression in chapter_regex_expressions:
        if re.compile(expression, re.MULTILINE).search(textline):
            Answer = True
    
    # NOTE: make sure that it does NOT accidentally fire 'true'
    # on a section or signmark:
    if re.compile(r'^(\d+)(\.)(\d+)').search(textline): Answer = False
    if re.compile(r'^ –').search(textline): Answer = False
    if (textline==""): Answer = False

    # Return the answer:
    return Answer

def contains_sectionregex(textline: str) -> bool:
    """
    Function to check wether a certain textline starts
    with certain regional expression (regex). The regex
    is hard-coded in this function, as it is specific for
    a section-textline.
    
    # Parameters:
    textline: str: the string you would like to test
    Returns: bool: the answer to the question.
    
    # ATTENTION: When changing or adding something to this function, be sure
    to add more testcases to hardcodedexpressions.py as well!!!
    """

    # ---------------------------------------------------    

    # Define all allowed chapter regex expressions:
    section_regex_expressions = []

    # Standard scientific sections:
    section_regex_expressions.append(r'^(\d+)(\.)(\d+)')
    section_regex_expressions.append(r'^Section (\d+)')
    section_regex_expressions.append(r'^section (\d+)')
    section_regex_expressions.append(r'^Sectie (\d+)')
    section_regex_expressions.append(r'^sectie (\d+)')
    section_regex_expressions.append(r'^[A-Z](\.)(\d+)')

    # Test if the textline starts with one of them:
    Answer = False
    for expression in section_regex_expressions:
        if (re.compile(expression).search(textline)):
            Answer = True

    # NOTE: make sure that it does NOT accidentally fire 'true'
    # on a subsection:
    if re.compile(r'^(\d+)(\.)(\d+)(\.)(\d+)').search(textline): Answer = False
    if (textline==""): Answer = False
    
    # Return the answer:
    return Answer

def contains_subsectionregex(textline: str) -> bool:
    """
    Function to check wether a certain textline starts
    with certain regional expression (regex). The regex
    is hard-coded in this function, as it is specific for
    a subsection-textline.
    
    # Parameters:
    textline: str: the string you would like to test
    Returns: bool: the answer to the question.
    
    # ATTENTION: When changing or adding something to this function, be sure
    to add more testcases to hardcodedexpressions.py as well!!!
    """

    # ---------------------------------------------------    

    # Define all allowed chapter regex expressions:
    subsection_regex_expressions = []

    # Standard scientific subsections:
    subsection_regex_expressions.append(r'^(\d+)(\.)(\d+)(\.)(\d+)')
    subsection_regex_expressions.append(r'^Subsection (\d+)')
    subsection_regex_expressions.append(r'^subsection (\d+)')
    subsection_regex_expressions.append(r'^Subsectie (\d+)')
    subsection_regex_expressions.append(r'^subsectie (\d+)')

    # Test if the extline starts with one of them:
    Answer = False
    for expression in subsection_regex_expressions:
        if re.compile(expression).search(textline):
            Answer = True

    # NOTE: make sure that it does NOT accidentally fire 'true'
    # on a subsubsection:
    if re.compile(r'^(\d+)(\.)(\d+)(\.)(\d+)(\.)(\d+)').search(textline): Answer = False
    if (textline==""): Answer = False
    
    # Return the answer:
    return Answer


def contains_subsubsectionregex(textline: str) -> bool:
    """
    Function to check wether a certain textline starts
    with certain regional expression (regex). The regex
    is hard-coded in this function, as it is specific for
    a subsubsection-textline.
    
    # Parameters:
    textline: str: the string you would like to test
    Returns: bool: the answer to the question.
    
    # ATTENTION: When changing or adding something to this function, be sure
    to add more testcases to hardcodedexpressions.py as well!!!
    """

    # ---------------------------------------------------    

    # Define all allowed chapter regex expressions:
    subsubsection_regex_expressions = []

    # standard scientific subsubsections:
    subsubsection_regex_expressions.append(r'^(\d+)(\.)(\d+)(\.)(\d+)(\.)(\d+)')

    # Test if the extline starts with one of them:
    Answer = False
    for expression in subsubsection_regex_expressions:
        if re.compile(expression).search(textline):
            Answer = True

    # NOTE: make sure that it does NOT accidentally fire 'true'
    # on a lower level:
    if re.compile(r'^(\d+)(\.)(\d+)(\.)(\d+)(\.)(\d+)(\.)(\d+)').search(textline): Answer = False
    if (textline==""): Answer = False
    
    # Return the answer:
    return Answer

def contains_headlines_regex(textline: str) -> bool:
    """
    This function collects all the regex-functions that 
    are meant to detect headlines, so you can efficiently
    test on all of them at the same time, if that is what you want:
    
    # Parameters:
    textline: str: the string you would like to test
    Returns: bool: the answer to the question.
    """
    
    Answer = False
    if contains_chapterregex(textline): Answer = True
    if contains_sectionregex(textline): Answer = True
    if contains_subsectionregex(textline): Answer = True
    if contains_subsubsectionregex(textline): Answer = True
    return Answer

def contains_bigroman_enumeration(textline: str) -> bool:
    """
    Function to check wether a certain textline starts
    with certain regional expression (regex). The regex
    is hard-coded in this function, as it is specific for
    a big-roman enumeration textline.
    
    # Parameters:
    textline: str: the string you would like to test
    Returns: bool: the answer to the question.
    
    # ATTENTION: When changing or adding something to this function, be sure
    to add more testcases to hardcodedexpressions.py as well!!!
    """

    # ---------------------------------------------------    

    # Define all allowed chapter regex expressions:
    enums_regex_expressions = []

    # Standard scientific sections:
    enums_regex_expressions.append(r'^M{0,3}(CM|CD|D?C{0,3})?(XC|XL|L?X{0,3})?(IX|IV|V?I{0,3})?(\.) ') # Big roman number followed by a dot.
    enums_regex_expressions.append(r'^M{0,3}(CM|CD|D?C{0,3})?(XC|XL|L?X{0,3})?(IX|IV|V?I{0,3})?(\)) ') # Big roman number followed by a parenthesis
    enums_regex_expressions.append(r'^(\()M{0,3}(CM|CD|D?C{0,3})?(XC|XL|L?X{0,3})?(IX|IV|V?I{0,3})?(\)) ') # Big roman number surrounded by parenthesis
    enums_regex_expressions.append(r'^M{0,3}(CM|CD|D?C{0,3})?(XC|XL|L?X{0,3})?(IX|IV|V?I{0,3})?(\.)$') # Big roman number followed by a dot.
    enums_regex_expressions.append(r'^M{0,3}(CM|CD|D?C{0,3})?(XC|XL|L?X{0,3})?(IX|IV|V?I{0,3})?(\))$') # Big roman number followed by a parenthesis
    enums_regex_expressions.append(r'^(\()M{0,3}(CM|CD|D?C{0,3})?(XC|XL|L?X{0,3})?(IX|IV|V?I{0,3})?(\))$') # Big roman number surrounded by parenthesis

    # Test if the extline starts with one of them:
    Answer = False
    for expression in enums_regex_expressions:
        if (re.compile(expression).search(textline)):
            Answer = True
    
    # NOTE: make sure that it does NOT accidentally fire 'true' on sections (etc).
    if re.compile(r'^(\d+)(\.)(\d+)').search(textline): Answer = False
    if re.compile(r'^(\.)').search(textline): Answer = False
    if re.compile(r'^(\)) ').search(textline): Answer = False
    if (textline==""): Answer = False
    
    # Return the answer:
    return Answer

def contains_smallroman_enumeration(textline: str) -> bool:
    """
    Function to check wether a certain textline starts
    with certain regional expression (regex). The regex
    is hard-coded in this function, as it is specific for
    a big-roman enumeration textline.
    
    # Parameters:
    textline: str: the string you would like to test
    Returns: bool: the answer to the question.
    
    # ATTENTION: When changing or adding something to this function, be sure
    to add more testcases to hardcodedexpressions.py as well!!!
    """

    # ---------------------------------------------------    

    # Define all allowed chapter regex expressions:
    enums_regex_expressions = []

    # Standard scientific sections:
    enums_regex_expressions.append(r'^m{0,3}(cm|cd|d?c{0,3})?(xc|xl|l?x{0,3})?(ix|iv|v?i{0,3})?(\.) ') # small roman number followed by a dot.
    enums_regex_expressions.append(r'^m{0,3}(cm|cd|d?c{0,3})?(xc|xl|l?x{0,3})?(ix|iv|v?i{0,3})?(\)) ') # Big roman number followed by a parenthesis
    enums_regex_expressions.append(r'^(\()m{0,3}(cm|cd|d?c{0,3})?(xc|xl|l?x{0,3})?(ix|iv|v?i{0,3})?(\)) ') # Big roman number surrounded by parenthesis
    enums_regex_expressions.append(r'^m{0,3}(cm|cd|d?c{0,3})?(xc|xl|l?x{0,3})?(ix|iv|v?i{0,3})?(\.)$') # small roman number followed by a dot.
    enums_regex_expressions.append(r'^m{0,3}(cm|cd|d?c{0,3})?(xc|xl|l?x{0,3})?(ix|iv|v?i{0,3})?(\))$') # Big roman number followed by a parenthesis
    enums_regex_expressions.append(r'^(\()m{0,3}(cm|cd|d?c{0,3})?(xc|xl|l?x{0,3})?(ix|iv|v?i{0,3})?(\))$') # Big roman number surrounded by parenthesis

    # Test if the extline starts with one of them:
    Answer = False
    for expression in enums_regex_expressions:
        if (re.compile(expression).search(textline)):
            Answer = True
            
    # NOTE: make sure that it does NOT accidentally fire 'true' on sections (etc).
    if re.compile(r'^(\d+)(\.)(\d+)').search(textline): Answer = False
    if re.compile(r'^(\.)').search(textline): Answer = False
    if re.compile(r'^(\)) ').search(textline): Answer = False
    if (textline==""): Answer = False
    
    # Return the answer:
    return Answer

def contains_bigletter_enumeration(textline: str) -> bool:
    """
    Function to check wether a certain textline starts
    with certain regional expression (regex). The regex
    is hard-coded in this function, as it is specific for
    a big-letter enumeration
    
    # Parameters:
    textline: str: the string you would like to test
    Returns: bool: the answer to the question.
    
    # ATTENTION: When changing or adding something to this function, be sure
    to add more testcases to hardcodedexpressions.py as well!!!
    """

    # ---------------------------------------------------    

    # Define all allowed chapter regex expressions:
    enums_regex_expressions = []

    # Enumeration by capitals:
    enums_regex_expressions.append(r'^[A-Z](\.) ')
    enums_regex_expressions.append(r'^[A-Z](\.)$')
    enums_regex_expressions.append(r'^[A-Z](\)) ')
    enums_regex_expressions.append(r'^[A-Z](\))$')
    enums_regex_expressions.append(r'^(\()[A-Z](\)) ')
    enums_regex_expressions.append(r'^(\()[A-Z](\))$')

    # Test if the extline starts with one of them:
    Answer = False
    for expression in enums_regex_expressions:
        if re.compile(expression, re.MULTILINE).search(textline):
            Answer = True
        
    # NOTE: make sure that it does NOT accidentally fire 'true' on sections (etc).
    if re.compile(r'^(\d+)(\.)(\d+)').search(textline): Answer = False
    if re.compile(r'^(\.)').search(textline): Answer = False
    if (textline==""): Answer = False
    
    # Return the answer:
    return Answer

def contains_smallletter_enumeration(textline: str) -> bool:
    """
    Function to check wether a certain textline starts
    with certain regional expression (regex). The regex
    is hard-coded in this function, as it is specific for
    a small-letter enumeration
    
    # Parameters:
    textline: str: the string you would like to test
    Returns: bool: the answer to the question.
    
    # ATTENTION: When changing or adding something to this function, be sure
    to add more testcases to hardcodedexpressions.py as well!!!
    """

    # ---------------------------------------------------    

    # Define all allowed chapter regex expressions:
    enums_regex_expressions = []

    # Enumeration by capitals:
    enums_regex_expressions.append(r'^[a-z](\.) ')
    enums_regex_expressions.append(r'^[a-z](\.)$')
    enums_regex_expressions.append(r'^[a-z](\)) ')
    enums_regex_expressions.append(r'^[a-z](\))$')
    enums_regex_expressions.append(r'^(\()[a-z](\)) ')
    enums_regex_expressions.append(r'^(\()[a-z](\))$')

    # Test if the textline starts with one of them:
    Answer = False
    for expression in enums_regex_expressions:
        if re.compile(expression, re.MULTILINE).search(textline):
            Answer = True
            
    # NOTE: make sure that it does NOT accidentally fire 'true' on sections (etc).
    if re.compile(r'^(\d+)(\.)(\d+)').search(textline): Answer = False
    if re.compile(r'^(\.)').search(textline): Answer = False
    if (textline==""): Answer = False
    
    # Return the answer:
    return Answer

def contains_digit_enumeration(textline: str, nextline_isbig: bool) -> bool:
    """
    Function to check wether a certain textline starts
    with certain regional expression (regex). The regex
    is hard-coded in this function, as it is specific for
    a digit-enumeration
    
    # Parameters:
    textline: str: the string you would like to test
    nextline_isbig: bool: boolian to state whether the line is followed by a large whiteline or not.
    Returns: bool: the answer to the question.
    
    # ATTENTION: When changing or adding something to this function, be sure
    to add more testcases to hardcodedexpressions.py as well!!!
    """

    # ---------------------------------------------------    

    # Define all allowed chapter regex expressions:
    enums_regex_expressions = []

    # Enumerations-by-digits (no further then 3 digits; we can handle to 999), but we 
    # do not trigger year-numbers.
    enums_regex_expressions.append(r'^(\d{1,3})(\.) ')
    enums_regex_expressions.append(r'^(\d{1,3})(\.)$')
    enums_regex_expressions.append(r'^(\()(\d{1,3})(\)) ')
    enums_regex_expressions.append(r'^(\()(\d{1,3})(\))$')
    enums_regex_expressions.append(r'^(\d{1,3})(\)) ')
    enums_regex_expressions.append(r'^(\d{1,3})(\))$')

    # Add for AI-impact assesment:
    enums_regex_expressions.append(r'^i (\d{1,3})(\.) ')
    enums_regex_expressions.append(r'^f (\d{1,3})(\.) ')
    enums_regex_expressions.append(r'^fo (\d{1,3})(\.) ')
    enums_regex_expressions.append(r'^t (\d{1,3})(\.) ')
    enums_regex_expressions.append(r'^to (\d{1,3})(\.) ')
    enums_regex_expressions.append(r'^d (\d{1,3})(\.) ')
    enums_regex_expressions.append(r'^do (\d{1,3})(\.) ')
    enums_regex_expressions.append(r'^r (\d{1,3})(\.) ')
    enums_regex_expressions.append(r'^ro (\d{1,3})(\.) ')
    enums_regex_expressions.append(r'^v (\d{1,3})(\.) ')
    enums_regex_expressions.append(r'^vo (\d{1,3})(\.) ')

    # Test if the extline starts with one of them:
    Answer = False
    for expression in enums_regex_expressions:
        if (re.compile(expression).search(textline)):
            Answer = True
            
    # NOTE: make sure that it does NOT accidentally fire 'true' on sections (etc).
    if re.compile(r'^(\d+)(\.)(\d+)').search(textline): Answer = False
    if re.compile(r'^(\.)').search(textline): Answer = False
    if (textline==""): Answer = False
    
    # If we end in a large whiteline, the termination-regex should not fire:
    if (nextline_isbig==True)and(re.compile(r'^(\d+)(\.)$').search(textline)): Answer = False
    if (nextline_isbig==True)and(re.compile(r'^(\d+)(\))$').search(textline)): Answer = False
    if (nextline_isbig==True)and(re.compile(r'^(\()(\d+)(\))$').search(textline)): Answer = False
    
    # Return the answer:
    return Answer

def contains_pointtwo_enumeration(textline: str, nextline_isbig: bool) -> bool:
    """
    Function to check wether a certain textline starts
    with certain regional expression (regex). The regex
    is hard-coded in this function, as it is specific for
    a digit-enumeration
    
    # Parameters:
    textline: str: the string you would like to test
    nextline_isbig: bool: boolian to state whether the line is followed by a large whiteline or not.
    Returns: bool: the answer to the question.
    
    # ATTENTION: When changing or adding something to this function, be sure
    to add more testcases to hardcodedexpressions.py as well!!!
    """

    # ---------------------------------------------------    

    # Define all allowed chapter regex expressions:
    enums_regex_expressions = []

    # Enumerations-by-digits (no further then 3 digits; we can handle to 999), but we 
    # do not trigger year-numbers.
    enums_regex_expressions.append(r'^[2](\.) ')
    enums_regex_expressions.append(r'^[2](\.)$')
    enums_regex_expressions.append(r'^(\()[2](\)) ')
    enums_regex_expressions.append(r'^(\()[2](\))$')
    enums_regex_expressions.append(r'^[2](\)) ')
    enums_regex_expressions.append(r'^[2](\))$')

    # Test if the extline starts with one of them:
    Answer = False
    for expression in enums_regex_expressions:
        if (re.compile(expression).search(textline)):
            Answer = True
            
    # NOTE: make sure that it does NOT accidentally fire 'true' on sections (etc).
    if re.compile(r'^(\d+)(\.)(\d+)').search(textline): Answer = False
    if re.compile(r'^(\.)').search(textline): Answer = False
    if (textline==""): Answer = False
    
    # If we end in a large whiteline, the termination-regex should not fire:
    if (nextline_isbig==True)and(re.compile(r'^(\d+)(\.)$').search(textline)): Answer = False
    if (nextline_isbig==True)and(re.compile(r'^(\d+)(\))$').search(textline)): Answer = False
    if (nextline_isbig==True)and(re.compile(r'^(\()(\d+)(\))$').search(textline)): Answer = False
    
    # Return the answer:
    return Answer

def contains_signmark_enumeration(textline: str) -> bool:
    """
    Function to check wether a certain textline starts
    with certain regional expression (regex). The regex
    is hard-coded in this function, as it is specific for
    a mark-sign (-) -enumeration
    
    # Parameters:
    textline: str: the string you would like to test
    Returns: bool: the answer to the question.
    
    # ATTENTION: When changing or adding something to this function, be sure
    to add more testcases to hardcodedexpressions.py as well!!!
    """

    # ---------------------------------------------------    

    # Define all allowed chapter regex expressions:
    enums_regex_expressions = []

    # enumerations by sign:
    enums_regex_expressions.append(r'^- ')
    enums_regex_expressions.append(r'^– ')
    enums_regex_expressions.append(r'^–$')
    enums_regex_expressions.append(r'^• ')
    enums_regex_expressions.append(r'^•$')
    enums_regex_expressions.append(r'^▪ ')
    enums_regex_expressions.append(r'^▪$')
    
    # NOTE: only do the long one, not the short one so that Copernicus works,
    # but the beaking of words (LineTest1) does not give trouble. 

    # Test if the extline starts with one of them:
    Answer = False
    for expression in enums_regex_expressions:
        if (re.compile(expression).search(textline)):
            Answer = True
            
    # NOTE: make sure that it does NOT accidentally fire 'true' on sections (etc).
    if re.compile(r'^(\d+)(\.)(\d+)').search(textline): Answer = False
    if re.compile(r'^(\.)').search(textline): Answer = False
    if (textline==""): Answer = False
    
    # Return the answer:
    return Answer

def contains_letter_signing(textline: str) -> bool:
    """
    Function to check wether a certain textline contains
    phrases (such as 'minister') that will make it likely
    that the current line is a letter-signing instead
    of a 'normal' textline.
    
    # Parameters:
    textline: str: the string you would like to test
    Returns: bool: the answer to the question.

    """

    # ---------------------------------------------------    

    # Define all allowed chapter regex expressions:
    letter_expressions = []

    # enumerations by sign:
    letter_expressions.append(r'Ministre')
    letter_expressions.append(r'ministre')
    letter_expressions.append(r'Minister')
    letter_expressions.append(r'minister')
    letter_expressions.append(r'Director')
    letter_expressions.append(r'director')
    
    # Test if the textline contains one of them:
    Answer = False
    for expression in letter_expressions:
        if (re.compile(expression).search(textline)):
            Answer = True
            
    # NOTE: make sure that it does NOT accidentally fire 'true' when we do not want it:
    if (textline==""): Answer = False
    
    # Return the answer:
    return Answer

def contains_smallalphabetic_order(textline1: str, textline2: str) -> bool:
    """
    This function is meant to detect whether two strings start with an 
    enumeration-sign in alphabetic order. This is used to distinguish
    roman expressions from regular letters.
    
    # Parameters:
    textline1: str: the first string you would like to test
    textline1: str: the second string you would like to test
    Returns: bool: the answer to the question.
    
    # ATTENTION: When changing or adding something to this function, be sure
    to add more testcases to hardcodedexpressions.py as well!!!
    """
    
    if (re.compile(r'^a(\.)').search(textline1))and(re.compile(r'^b(\.)').search(textline2)): return True
    if (re.compile(r'^b(\.)').search(textline1))and(re.compile(r'^c(\.)').search(textline2)): return True
    if (re.compile(r'^c(\.)').search(textline1))and(re.compile(r'^d(\.)').search(textline2)): return True
    if (re.compile(r'^d(\.)').search(textline1))and(re.compile(r'^e(\.)').search(textline2)): return True
    if (re.compile(r'^e(\.)').search(textline1))and(re.compile(r'^f(\.)').search(textline2)): return True
    if (re.compile(r'^f(\.)').search(textline1))and(re.compile(r'^g(\.)').search(textline2)): return True
    if (re.compile(r'^g(\.)').search(textline1))and(re.compile(r'^h(\.)').search(textline2)): return True
    if (re.compile(r'^h(\.)').search(textline1))and(re.compile(r'^i(\.)').search(textline2)): return True
    if (re.compile(r'^i(\.)').search(textline1))and(re.compile(r'^j(\.)').search(textline2)): return True
    if (re.compile(r'^j(\.)').search(textline1))and(re.compile(r'^k(\.)').search(textline2)): return True
    if (re.compile(r'^k(\.)').search(textline1))and(re.compile(r'^l(\.)').search(textline2)): return True
    if (re.compile(r'^l(\.)').search(textline1))and(re.compile(r'^m(\.)').search(textline2)): return True
    if (re.compile(r'^m(\.)').search(textline1))and(re.compile(r'^n(\.)').search(textline2)): return True
    if (re.compile(r'^n(\.)').search(textline1))and(re.compile(r'^o(\.)').search(textline2)): return True
    if (re.compile(r'^o(\.)').search(textline1))and(re.compile(r'^p(\.)').search(textline2)): return True
    if (re.compile(r'^p(\.)').search(textline1))and(re.compile(r'^q(\.)').search(textline2)): return True
    if (re.compile(r'^q(\.)').search(textline1))and(re.compile(r'^r(\.)').search(textline2)): return True
    if (re.compile(r'^r(\.)').search(textline1))and(re.compile(r'^s(\.)').search(textline2)): return True
    if (re.compile(r'^s(\.)').search(textline1))and(re.compile(r'^t(\.)').search(textline2)): return True
    if (re.compile(r'^t(\.)').search(textline1))and(re.compile(r'^u(\.)').search(textline2)): return True
    if (re.compile(r'^u(\.)').search(textline1))and(re.compile(r'^v(\.)').search(textline2)): return True
    if (re.compile(r'^v(\.)').search(textline1))and(re.compile(r'^w(\.)').search(textline2)): return True
    if (re.compile(r'^w(\.)').search(textline1))and(re.compile(r'^x(\.)').search(textline2)): return True
    if (re.compile(r'^x(\.)').search(textline1))and(re.compile(r'^y(\.)').search(textline2)): return True
    if (re.compile(r'^y(\.)').search(textline1))and(re.compile(r'^z(\.)').search(textline2)): return True
    
    if (re.compile(r'^a(\))').search(textline1))and(re.compile(r'^b(\))').search(textline2)): return True
    if (re.compile(r'^b(\))').search(textline1))and(re.compile(r'^c(\))').search(textline2)): return True
    if (re.compile(r'^c(\))').search(textline1))and(re.compile(r'^d(\))').search(textline2)): return True
    if (re.compile(r'^d(\))').search(textline1))and(re.compile(r'^e(\))').search(textline2)): return True
    if (re.compile(r'^e(\))').search(textline1))and(re.compile(r'^f(\))').search(textline2)): return True
    if (re.compile(r'^f(\))').search(textline1))and(re.compile(r'^g(\))').search(textline2)): return True
    if (re.compile(r'^g(\))').search(textline1))and(re.compile(r'^h(\))').search(textline2)): return True
    if (re.compile(r'^h(\))').search(textline1))and(re.compile(r'^i(\))').search(textline2)): return True
    if (re.compile(r'^i(\))').search(textline1))and(re.compile(r'^j(\))').search(textline2)): return True
    if (re.compile(r'^j(\))').search(textline1))and(re.compile(r'^k(\))').search(textline2)): return True
    if (re.compile(r'^k(\))').search(textline1))and(re.compile(r'^l(\))').search(textline2)): return True
    if (re.compile(r'^l(\))').search(textline1))and(re.compile(r'^m(\))').search(textline2)): return True
    if (re.compile(r'^m(\))').search(textline1))and(re.compile(r'^n(\))').search(textline2)): return True
    if (re.compile(r'^n(\))').search(textline1))and(re.compile(r'^o(\))').search(textline2)): return True
    if (re.compile(r'^o(\))').search(textline1))and(re.compile(r'^p(\))').search(textline2)): return True
    if (re.compile(r'^p(\))').search(textline1))and(re.compile(r'^q(\))').search(textline2)): return True
    if (re.compile(r'^q(\))').search(textline1))and(re.compile(r'^r(\))').search(textline2)): return True
    if (re.compile(r'^r(\))').search(textline1))and(re.compile(r'^s(\))').search(textline2)): return True
    if (re.compile(r'^s(\))').search(textline1))and(re.compile(r'^t(\))').search(textline2)): return True
    if (re.compile(r'^t(\))').search(textline1))and(re.compile(r'^u(\))').search(textline2)): return True
    if (re.compile(r'^u(\))').search(textline1))and(re.compile(r'^v(\))').search(textline2)): return True
    if (re.compile(r'^v(\))').search(textline1))and(re.compile(r'^w(\))').search(textline2)): return True
    if (re.compile(r'^w(\))').search(textline1))and(re.compile(r'^x(\))').search(textline2)): return True
    if (re.compile(r'^x(\))').search(textline1))and(re.compile(r'^y(\))').search(textline2)): return True
    if (re.compile(r'^y(\))').search(textline1))and(re.compile(r'^z(\))').search(textline2)): return True
    
    if (re.compile(r'^(\()a(\))').search(textline1))and(re.compile(r'^(\()b(\))').search(textline2)): return True
    if (re.compile(r'^(\()b(\))').search(textline1))and(re.compile(r'^(\()c(\))').search(textline2)): return True
    if (re.compile(r'^(\()c(\))').search(textline1))and(re.compile(r'^(\()d(\))').search(textline2)): return True
    if (re.compile(r'^(\()d(\))').search(textline1))and(re.compile(r'^(\()e(\))').search(textline2)): return True
    if (re.compile(r'^(\()e(\))').search(textline1))and(re.compile(r'^(\()f(\))').search(textline2)): return True
    if (re.compile(r'^(\()f(\))').search(textline1))and(re.compile(r'^(\()g(\))').search(textline2)): return True
    if (re.compile(r'^(\()g(\))').search(textline1))and(re.compile(r'^(\()h(\))').search(textline2)): return True
    if (re.compile(r'^(\()h(\))').search(textline1))and(re.compile(r'^(\()i(\))').search(textline2)): return True
    if (re.compile(r'^(\()i(\))').search(textline1))and(re.compile(r'^(\()j(\))').search(textline2)): return True
    if (re.compile(r'^(\()j(\))').search(textline1))and(re.compile(r'^(\()k(\))').search(textline2)): return True
    if (re.compile(r'^(\()k(\))').search(textline1))and(re.compile(r'^(\()l(\))').search(textline2)): return True
    if (re.compile(r'^(\()l(\))').search(textline1))and(re.compile(r'^(\()m(\))').search(textline2)): return True
    if (re.compile(r'^(\()m(\))').search(textline1))and(re.compile(r'^(\()n(\))').search(textline2)): return True
    if (re.compile(r'^(\()n(\))').search(textline1))and(re.compile(r'^(\()o(\))').search(textline2)): return True
    if (re.compile(r'^(\()o(\))').search(textline1))and(re.compile(r'^(\()p(\))').search(textline2)): return True
    if (re.compile(r'^(\()p(\))').search(textline1))and(re.compile(r'^(\()q(\))').search(textline2)): return True
    if (re.compile(r'^(\()q(\))').search(textline1))and(re.compile(r'^(\()r(\))').search(textline2)): return True
    if (re.compile(r'^(\()r(\))').search(textline1))and(re.compile(r'^(\()s(\))').search(textline2)): return True
    if (re.compile(r'^(\()s(\))').search(textline1))and(re.compile(r'^(\()t(\))').search(textline2)): return True
    if (re.compile(r'^(\()t(\))').search(textline1))and(re.compile(r'^(\()u(\))').search(textline2)): return True
    if (re.compile(r'^(\()u(\))').search(textline1))and(re.compile(r'^(\()v(\))').search(textline2)): return True
    if (re.compile(r'^(\()v(\))').search(textline1))and(re.compile(r'^(\()w(\))').search(textline2)): return True
    if (re.compile(r'^(\()w(\))').search(textline1))and(re.compile(r'^(\()x(\))').search(textline2)): return True
    if (re.compile(r'^(\()x(\))').search(textline1))and(re.compile(r'^(\()y(\))').search(textline2)): return True
    if (re.compile(r'^(\()y(\))').search(textline1))and(re.compile(r'^(\()z(\))').search(textline2)): return True
    
    return False
    
def contains_bigalphabetic_order(textline1: str, textline2: str) -> bool:
    """
    This function is meant to detect whether two strings start with an 
    enumeration-sign in alphabetic order. This is used to distinguish
    roman expressions from regular letters.
    
    # Parameters:
    textline1: str: the first string you would like to test
    textline1: str: the second string you would like to test
    Returns: bool: the answer to the question.
    
    # ATTENTION: When changing or adding something to this function, be sure
    to add more testcases to hardcodedexpressions.py as well!!!
    """
    
    if (re.compile(r'^A(\.)').search(textline1))and(re.compile(r'^B(\.)').search(textline2)): return True
    if (re.compile(r'^B(\.)').search(textline1))and(re.compile(r'^C(\.)').search(textline2)): return True
    if (re.compile(r'^C(\.)').search(textline1))and(re.compile(r'^D(\.)').search(textline2)): return True
    if (re.compile(r'^D(\.)').search(textline1))and(re.compile(r'^E(\.)').search(textline2)): return True
    if (re.compile(r'^E(\.)').search(textline1))and(re.compile(r'^F(\.)').search(textline2)): return True
    if (re.compile(r'^F(\.)').search(textline1))and(re.compile(r'^G(\.)').search(textline2)): return True
    if (re.compile(r'^G(\.)').search(textline1))and(re.compile(r'^H(\.)').search(textline2)): return True
    if (re.compile(r'^H(\.)').search(textline1))and(re.compile(r'^I(\.)').search(textline2)): return True
    if (re.compile(r'^I(\.)').search(textline1))and(re.compile(r'^J(\.)').search(textline2)): return True
    if (re.compile(r'^J(\.)').search(textline1))and(re.compile(r'^K(\.)').search(textline2)): return True
    if (re.compile(r'^K(\.)').search(textline1))and(re.compile(r'^L(\.)').search(textline2)): return True
    if (re.compile(r'^L(\.)').search(textline1))and(re.compile(r'^M(\.)').search(textline2)): return True
    if (re.compile(r'^M(\.)').search(textline1))and(re.compile(r'^N(\.)').search(textline2)): return True
    if (re.compile(r'^N(\.)').search(textline1))and(re.compile(r'^O(\.)').search(textline2)): return True
    if (re.compile(r'^O(\.)').search(textline1))and(re.compile(r'^P(\.)').search(textline2)): return True
    if (re.compile(r'^P(\.)').search(textline1))and(re.compile(r'^Q(\.)').search(textline2)): return True
    if (re.compile(r'^Q(\.)').search(textline1))and(re.compile(r'^R(\.)').search(textline2)): return True
    if (re.compile(r'^R(\.)').search(textline1))and(re.compile(r'^S(\.)').search(textline2)): return True
    if (re.compile(r'^S(\.)').search(textline1))and(re.compile(r'^T(\.)').search(textline2)): return True
    if (re.compile(r'^T(\.)').search(textline1))and(re.compile(r'^U(\.)').search(textline2)): return True
    if (re.compile(r'^U(\.)').search(textline1))and(re.compile(r'^V(\.)').search(textline2)): return True
    if (re.compile(r'^V(\.)').search(textline1))and(re.compile(r'^W(\.)').search(textline2)): return True
    if (re.compile(r'^W(\.)').search(textline1))and(re.compile(r'^X(\.)').search(textline2)): return True
    if (re.compile(r'^X(\.)').search(textline1))and(re.compile(r'^Y(\.)').search(textline2)): return True
    if (re.compile(r'^Y(\.)').search(textline1))and(re.compile(r'^Z(\.)').search(textline2)): return True
    
    if (re.compile(r'^A(\))').search(textline1))and(re.compile(r'^B(\))').search(textline2)): return True
    if (re.compile(r'^B(\))').search(textline1))and(re.compile(r'^C(\))').search(textline2)): return True
    if (re.compile(r'^C(\))').search(textline1))and(re.compile(r'^D(\))').search(textline2)): return True
    if (re.compile(r'^D(\))').search(textline1))and(re.compile(r'^E(\))').search(textline2)): return True
    if (re.compile(r'^E(\))').search(textline1))and(re.compile(r'^F(\))').search(textline2)): return True
    if (re.compile(r'^F(\))').search(textline1))and(re.compile(r'^G(\))').search(textline2)): return True
    if (re.compile(r'^G(\))').search(textline1))and(re.compile(r'^H(\))').search(textline2)): return True
    if (re.compile(r'^H(\))').search(textline1))and(re.compile(r'^I(\))').search(textline2)): return True
    if (re.compile(r'^I(\))').search(textline1))and(re.compile(r'^J(\))').search(textline2)): return True
    if (re.compile(r'^J(\))').search(textline1))and(re.compile(r'^K(\))').search(textline2)): return True
    if (re.compile(r'^K(\))').search(textline1))and(re.compile(r'^L(\))').search(textline2)): return True
    if (re.compile(r'^L(\))').search(textline1))and(re.compile(r'^M(\))').search(textline2)): return True
    if (re.compile(r'^M(\))').search(textline1))and(re.compile(r'^N(\))').search(textline2)): return True
    if (re.compile(r'^N(\))').search(textline1))and(re.compile(r'^O(\))').search(textline2)): return True
    if (re.compile(r'^O(\))').search(textline1))and(re.compile(r'^P(\))').search(textline2)): return True
    if (re.compile(r'^P(\))').search(textline1))and(re.compile(r'^Q(\))').search(textline2)): return True
    if (re.compile(r'^Q(\))').search(textline1))and(re.compile(r'^R(\))').search(textline2)): return True
    if (re.compile(r'^R(\))').search(textline1))and(re.compile(r'^S(\))').search(textline2)): return True
    if (re.compile(r'^S(\))').search(textline1))and(re.compile(r'^T(\))').search(textline2)): return True
    if (re.compile(r'^T(\))').search(textline1))and(re.compile(r'^U(\))').search(textline2)): return True
    if (re.compile(r'^U(\))').search(textline1))and(re.compile(r'^V(\))').search(textline2)): return True
    if (re.compile(r'^V(\))').search(textline1))and(re.compile(r'^W(\))').search(textline2)): return True
    if (re.compile(r'^W(\))').search(textline1))and(re.compile(r'^X(\))').search(textline2)): return True
    if (re.compile(r'^X(\))').search(textline1))and(re.compile(r'^Y(\))').search(textline2)): return True
    if (re.compile(r'^Y(\))').search(textline1))and(re.compile(r'^Z(\))').search(textline2)): return True

    if (re.compile(r'(\()A(\))').search(textline1))and(re.compile(r'(\()B(\))').search(textline2)): return True
    if (re.compile(r'(\()B(\))').search(textline1))and(re.compile(r'(\()C(\))').search(textline2)): return True
    if (re.compile(r'(\()C(\))').search(textline1))and(re.compile(r'(\()D(\))').search(textline2)): return True
    if (re.compile(r'(\()D(\))').search(textline1))and(re.compile(r'(\()E(\))').search(textline2)): return True
    if (re.compile(r'(\()E(\))').search(textline1))and(re.compile(r'(\()F(\))').search(textline2)): return True
    if (re.compile(r'(\()F(\))').search(textline1))and(re.compile(r'(\()G(\))').search(textline2)): return True
    if (re.compile(r'(\()G(\))').search(textline1))and(re.compile(r'(\()H(\))').search(textline2)): return True
    if (re.compile(r'(\()H(\))').search(textline1))and(re.compile(r'(\()I(\))').search(textline2)): return True
    if (re.compile(r'(\()I(\))').search(textline1))and(re.compile(r'(\()J(\))').search(textline2)): return True
    if (re.compile(r'(\()J(\))').search(textline1))and(re.compile(r'(\()K(\))').search(textline2)): return True
    if (re.compile(r'(\()K(\))').search(textline1))and(re.compile(r'(\()L(\))').search(textline2)): return True
    if (re.compile(r'(\()L(\))').search(textline1))and(re.compile(r'(\()M(\))').search(textline2)): return True
    if (re.compile(r'(\()M(\))').search(textline1))and(re.compile(r'(\()N(\))').search(textline2)): return True
    if (re.compile(r'(\()N(\))').search(textline1))and(re.compile(r'(\()O(\))').search(textline2)): return True
    if (re.compile(r'(\()O(\))').search(textline1))and(re.compile(r'(\()P(\))').search(textline2)): return True
    if (re.compile(r'(\()P(\))').search(textline1))and(re.compile(r'(\()Q(\))').search(textline2)): return True
    if (re.compile(r'(\()Q(\))').search(textline1))and(re.compile(r'(\()R(\))').search(textline2)): return True
    if (re.compile(r'(\()R(\))').search(textline1))and(re.compile(r'(\()S(\))').search(textline2)): return True
    if (re.compile(r'(\()S(\))').search(textline1))and(re.compile(r'(\()T(\))').search(textline2)): return True
    if (re.compile(r'(\()T(\))').search(textline1))and(re.compile(r'(\()U(\))').search(textline2)): return True
    if (re.compile(r'(\()U(\))').search(textline1))and(re.compile(r'(\()V(\))').search(textline2)): return True
    if (re.compile(r'(\()V(\))').search(textline1))and(re.compile(r'(\()W(\))').search(textline2)): return True
    if (re.compile(r'(\()W(\))').search(textline1))and(re.compile(r'(\()X(\))').search(textline2)): return True
    if (re.compile(r'(\()X(\))').search(textline1))and(re.compile(r'(\()Y(\))').search(textline2)): return True
    if (re.compile(r'(\()Y(\))').search(textline1))and(re.compile(r'(\()Z(\))').search(textline2)): return True
    
    return False
    
    
