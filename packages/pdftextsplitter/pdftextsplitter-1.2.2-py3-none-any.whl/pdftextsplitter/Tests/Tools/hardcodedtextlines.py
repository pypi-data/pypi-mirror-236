import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from TextPart code:
sys.path.insert(1, '../../')
from TextPart.CurrentLine import CurrentLine

def hardcodedtextlines() -> list[CurrentLine]:
    """
    Function to load hard-coded textlines including information
    on font size and vertical position. This can be used for unit-tests
    on textsplitter-functionality.
    
    # NOTE: Based on SplitDoc.pdf & pdfminer-reading library
    
    # Parameters: None
    # Return: list[CurrentLine]: the textlines you want to use.
    """
    
    # --------------------------------------------------------
    
    # Declare array:
    textlines = []
    
    mytestline = CurrentLine()
    mytestline.textline = "First basic test Document"
    mytestline.previous_textline = ""
    mytestline.fontsize = 17.215400000000045
    mytestline.vertical_position = 401.041997
    mytestline.previous_whiteline = -1.0
    mytestline.next_whiteline = 52.76030579999997
    mytestline.previous_IsHeadline = False
    mytestline.previous_Headlines_cascade = 0
    mytestline.previous_fontsize = 0
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 0
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 1
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "Unit Data en Innovatie"
    mytestline.previous_textline = "First basic test Document"
    mytestline.fontsize = 11.95519999999999
    mytestline.vertical_position = 348.2816912
    mytestline.previous_whiteline = 52.76030579999997
    mytestline.next_whiteline = 39.96100000000001
    mytestline.previous_IsHeadline = True
    mytestline.previous_Headlines_cascade = 1
    mytestline.previous_fontsize = 17.215400000000045
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 1
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 1
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "20th of March 2023"
    mytestline.previous_textline = "Unit Data en Innovatie"
    mytestline.fontsize = 11.95519999999999
    mytestline.vertical_position = 308.3206912
    mytestline.previous_whiteline = 39.96100000000001
    mytestline.next_whiteline = 233.99124735200013
    mytestline.previous_IsHeadline = True
    mytestline.previous_Headlines_cascade = 3
    mytestline.previous_fontsize = 11.95519999999999
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 3
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 1
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "Contents"
    mytestline.previous_textline = "20th of March 2023"
    mytestline.fontsize = 24.78710000000001
    mytestline.vertical_position = 596.9073026
    mytestline.previous_whiteline = 233.99124735200013
    mytestline.next_whiteline = 43.894047
    mytestline.previous_IsHeadline = True
    mytestline.previous_Headlines_cascade = 3
    mytestline.previous_fontsize = 11.95519999999999
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 3
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 2
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "1 Let’s kick-of test-driven development"
    mytestline.previous_textline = "Contents"
    mytestline.fontsize = 9.962600000000066
    mytestline.vertical_position = 553.0132556
    mytestline.previous_whiteline = 43.894047
    mytestline.next_whiteline = 0.0
    mytestline.previous_IsHeadline = True
    mytestline.previous_Headlines_cascade = 1
    mytestline.previous_fontsize = 24.78710000000001
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 1
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 2
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "2"
    mytestline.previous_textline = "1 Let’s kick-of test-driven development"
    mytestline.fontsize = 9.962600000000066
    mytestline.vertical_position = 553.0132556
    mytestline.previous_whiteline = 0.0
    mytestline.next_whiteline = 11.955000000000041
    mytestline.previous_IsHeadline = False
    mytestline.previous_Headlines_cascade = 1
    mytestline.previous_fontsize = 9.962600000000066
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 1
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 2
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "1.1 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2"
    mytestline.previous_textline = "2"
    mytestline.fontsize = 9.962600000000066
    mytestline.vertical_position = 541.0582555999999
    mytestline.previous_whiteline = 11.955000000000041
    mytestline.next_whiteline = 11.955000000000041
    mytestline.previous_IsHeadline = False
    mytestline.previous_Headlines_cascade = 1
    mytestline.previous_fontsize = 9.962600000000066
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 1
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 2
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "1.2 Methods . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2"
    mytestline.previous_textline = "1.1 Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2"
    mytestline.fontsize = 9.962600000000066
    mytestline.vertical_position = 529.1032555999999
    mytestline.previous_whiteline = 11.955000000000041
    mytestline.next_whiteline = 11.955000000000041
    mytestline.previous_IsHeadline = False
    mytestline.previous_Headlines_cascade = 1
    mytestline.previous_fontsize = 9.962600000000066
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 1
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 2
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "1.3 Methods again . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2"
    mytestline.previous_textline = "1.2 Methods . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2"
    mytestline.fontsize = 9.962600000000066
    mytestline.vertical_position = 517.1482555999999
    mytestline.previous_whiteline = 11.955000000000041
    mytestline.next_whiteline = 11.954999999999927
    mytestline.previous_IsHeadline = False
    mytestline.previous_Headlines_cascade = 1
    mytestline.previous_fontsize = 9.962600000000066
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 1
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 2
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "1.4 One more section . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3"
    mytestline.previous_textline = "1.3 Methods again . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2"
    mytestline.fontsize = 9.962599999999952
    mytestline.vertical_position = 505.19325559999993
    mytestline.previous_whiteline = 11.954999999999927
    mytestline.next_whiteline = 21.918000000000006
    mytestline.previous_IsHeadline = False
    mytestline.previous_Headlines_cascade = 1
    mytestline.previous_fontsize = 9.962600000000066
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 1
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 2
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "2 A new chapter starts now"
    mytestline.previous_textline = "1.4 One more section . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 3"
    mytestline.fontsize = 9.962600000000009
    mytestline.vertical_position = 483.2752555999999
    mytestline.previous_whiteline = 21.918000000000006
    mytestline.next_whiteline = 0.0
    mytestline.previous_IsHeadline = False
    mytestline.previous_Headlines_cascade = 1
    mytestline.previous_fontsize = 9.962599999999952
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 1
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 2
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "4"
    mytestline.previous_textline = "2 A new chapter starts now"
    mytestline.fontsize = 9.962600000000009
    mytestline.vertical_position = 483.2752555999999
    mytestline.previous_whiteline = 0.0
    mytestline.next_whiteline = 11.954999999999984
    mytestline.previous_IsHeadline = False
    mytestline.previous_Headlines_cascade = 1
    mytestline.previous_fontsize = 9.962600000000009
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 1
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 2
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "2.1 A new section . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4"
    mytestline.previous_textline = "4"
    mytestline.fontsize = 9.962600000000009
    mytestline.vertical_position = 471.32025559999994
    mytestline.previous_whiteline = 11.954999999999984
    mytestline.next_whiteline = 11.954999999999984
    mytestline.previous_IsHeadline = False
    mytestline.previous_Headlines_cascade = 1
    mytestline.previous_fontsize = 9.962600000000009
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 1
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 2
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "2.1.1 Nice subsection . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4"
    mytestline.previous_textline = "2.1 A new section . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4"
    mytestline.fontsize = 9.962600000000009
    mytestline.vertical_position = 459.36525559999995
    mytestline.previous_whiteline = 11.954999999999984
    mytestline.next_whiteline = -2.0
    mytestline.previous_IsHeadline = False
    mytestline.previous_Headlines_cascade = 1
    mytestline.previous_fontsize = 9.962600000000009
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 1
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 2
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "1"
    mytestline.previous_textline = "2.1.1 Nice subsection . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4"
    mytestline.fontsize = 9.962599999999995
    mytestline.vertical_position = 37.14725559999993
    mytestline.previous_whiteline = -2.0
    mytestline.next_whiteline = 385.0358117520001
    mytestline.previous_IsHeadline = False
    mytestline.previous_Headlines_cascade = 1
    mytestline.previous_fontsize = 9.962600000000009
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 1
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 2
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "1 Let’s kick-of test-driven"
    mytestline.previous_textline = "1"
    mytestline.fontsize = 24.78710000000001
    mytestline.vertical_position = 596.9073026
    mytestline.previous_whiteline = 385.0358117520001
    mytestline.next_whiteline = 29.888000000000034
    mytestline.previous_IsHeadline = False
    mytestline.previous_Headlines_cascade = 1
    mytestline.previous_fontsize = 9.962599999999995
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 1
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 3
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "development"
    mytestline.previous_textline = "1 Let’s kick-of test-driven"
    mytestline.fontsize = 24.78710000000001
    mytestline.vertical_position = 567.0193026
    mytestline.previous_whiteline = 29.888000000000034
    mytestline.next_whiteline = 43.893047000000024
    mytestline.previous_IsHeadline = True
    mytestline.previous_Headlines_cascade = 1
    mytestline.previous_fontsize = 24.78710000000001
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 1
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 3
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "We start with some general text about the chapter."
    mytestline.previous_textline = "development"
    mytestline.fontsize = 9.962600000000066
    mytestline.vertical_position = 523.1262555999999
    mytestline.previous_whiteline = 43.893047000000024
    mytestline.next_whiteline = 11.95599999999996
    mytestline.previous_IsHeadline = True
    mytestline.previous_Headlines_cascade = 1
    mytestline.previous_fontsize = 24.78710000000001
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 1
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 3
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "with a line-break embedded in it."
    mytestline.previous_textline = "We start with some general text about the chapter."
    mytestline.fontsize = 9.962600000000009
    mytestline.vertical_position = 511.17025559999996
    mytestline.previous_whiteline = 11.95599999999996
    mytestline.next_whiteline = 43.68941840000002
    mytestline.previous_IsHeadline = False
    mytestline.previous_Headlines_cascade = 1
    mytestline.previous_fontsize = 9.962600000000066
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 1
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 3
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "1.1 Introduction"
    mytestline.previous_textline = "with a line-break embedded in it."
    mytestline.fontsize = 14.34620000000001
    mytestline.vertical_position = 467.48083719999994
    mytestline.previous_whiteline = 43.68941840000002
    mytestline.next_whiteline = 22.40658159999998
    mytestline.previous_IsHeadline = False
    mytestline.previous_Headlines_cascade = 1
    mytestline.previous_fontsize = 9.962600000000009
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 1
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 3
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "This is a small test for text extraction."
    mytestline.previous_textline = "1.1 Introduction"
    mytestline.fontsize = 9.962600000000009
    mytestline.vertical_position = 445.07425559999996
    mytestline.previous_whiteline = 22.40658159999998
    mytestline.next_whiteline = 43.690418400000055
    mytestline.previous_IsHeadline = True
    mytestline.previous_Headlines_cascade = 2
    mytestline.previous_fontsize = 14.34620000000001
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 2
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 3
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "1.2 Methods"
    mytestline.previous_textline = "This is a small test for text extraction."
    mytestline.fontsize = 14.34620000000001
    mytestline.vertical_position = 401.3838371999999
    mytestline.previous_whiteline = 43.690418400000055
    mytestline.next_whiteline = 22.40658159999998
    mytestline.previous_IsHeadline = False
    mytestline.previous_Headlines_cascade = 2
    mytestline.previous_fontsize = 9.962600000000009
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 2
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 3
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "And here is some more text."
    mytestline.previous_textline = "1.2 Methods"
    mytestline.fontsize = 9.962600000000009
    mytestline.vertical_position = 378.9772555999999
    mytestline.previous_whiteline = 22.40658159999998
    mytestline.next_whiteline = 11.954999999999984
    mytestline.previous_IsHeadline = True
    mytestline.previous_Headlines_cascade = 2
    mytestline.previous_fontsize = 14.34620000000001
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 2
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 3
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "With a line break and other stuf."
    mytestline.previous_textline = "And here is some more text."
    mytestline.fontsize = 9.962600000000009
    mytestline.vertical_position = 367.02225559999994
    mytestline.previous_whiteline = 11.954999999999984
    mytestline.next_whiteline = 43.68941840000002
    mytestline.previous_IsHeadline = False
    mytestline.previous_Headlines_cascade = 2
    mytestline.previous_fontsize = 9.962600000000009
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 2
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 3
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "1.3 Methods again"
    mytestline.previous_textline = "With a line break and other stuf."
    mytestline.fontsize = 14.34620000000001
    mytestline.vertical_position = 323.3328371999999
    mytestline.previous_whiteline = 43.68941840000002
    mytestline.next_whiteline = 22.407581599999958
    mytestline.previous_IsHeadline = False
    mytestline.previous_Headlines_cascade = 2
    mytestline.previous_fontsize = 9.962600000000009
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 2
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 3
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "Lets add some whitespaces:"
    mytestline.previous_textline = "1.3 Methods again"
    mytestline.fontsize = 9.962600000000009
    mytestline.vertical_position = 300.92525559999996
    mytestline.previous_whiteline = 22.407581599999958
    mytestline.next_whiteline = 215.19300000000004
    mytestline.previous_IsHeadline = True
    mytestline.previous_Headlines_cascade = 2
    mytestline.previous_fontsize = 14.34620000000001
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 2
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 3
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "And some text."
    mytestline.previous_textline = "Lets add some whitespaces:"
    mytestline.fontsize = 9.962600000000009
    mytestline.vertical_position = 85.73225559999993
    mytestline.previous_whiteline = 215.19300000000004
    mytestline.next_whiteline = -2.0
    mytestline.previous_IsHeadline = False
    mytestline.previous_Headlines_cascade = 2
    mytestline.previous_fontsize = 9.962600000000009
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 2
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 3
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "2"
    mytestline.previous_textline = "And some text."
    mytestline.fontsize = 9.962599999999995
    mytestline.vertical_position = 37.14725559999994
    mytestline.previous_whiteline = -2.0
    mytestline.next_whiteline = -2.0
    mytestline.previous_IsHeadline = False
    mytestline.previous_Headlines_cascade = 2
    mytestline.previous_fontsize = 9.962600000000009
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 2
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 3
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "Section 1.4"
    mytestline.previous_textline = "2"
    mytestline.fontsize = 9.962600000000066
    mytestline.vertical_position = 627.5052555999999
    mytestline.previous_whiteline = -2.0
    mytestline.next_whiteline = -2.0
    mytestline.previous_IsHeadline = False
    mytestline.previous_Headlines_cascade = 2
    mytestline.previous_fontsize = 9.962599999999995
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 2
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 4
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "Chapter 1: Let’s kick-of test-driven development"
    mytestline.previous_textline = "Section 1.4"
    mytestline.fontsize = 9.962600000000066
    mytestline.vertical_position = 627.5052555999999
    mytestline.previous_whiteline = -2.0
    mytestline.next_whiteline = 11.968277152000041
    mytestline.previous_IsHeadline = False
    mytestline.previous_Headlines_cascade = 2
    mytestline.previous_fontsize = 9.962600000000066
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 2
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 4
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "1.4 One more section"
    mytestline.previous_textline = "Chapter 1: Let’s kick-of test-driven development"
    mytestline.fontsize = 14.346200000000067
    mytestline.vertical_position = 596.3418372
    mytestline.previous_whiteline = 11.968277152000041
    mytestline.next_whiteline = 22.40658159999998
    mytestline.previous_IsHeadline = False
    mytestline.previous_Headlines_cascade = 2
    mytestline.previous_fontsize = 9.962600000000066
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 2
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 4
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "With some text..."
    mytestline.previous_textline = "1.4 One more section"
    mytestline.fontsize = 9.962600000000066
    mytestline.vertical_position = 573.9352556
    mytestline.previous_whiteline = 22.40658159999998
    mytestline.next_whiteline = -2.0
    mytestline.previous_IsHeadline = True
    mytestline.previous_Headlines_cascade = 2
    mytestline.previous_fontsize = 14.346200000000067
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 2
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 4
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "3 and some stupid footertext."
    mytestline.previous_textline = "With some text..."
    mytestline.fontsize = 9.962599999999995
    mytestline.vertical_position = 37.147255600000044
    mytestline.previous_whiteline = -2.0
    mytestline.next_whiteline = 499.60581175200014
    mytestline.previous_IsHeadline = False
    mytestline.previous_Headlines_cascade = 2
    mytestline.previous_fontsize = 9.962600000000066
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 2
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 4
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "2 A new chapter starts now"
    mytestline.previous_textline = "3 and some stupid footertext."
    mytestline.fontsize = 24.78710000000001
    mytestline.vertical_position = 596.9073026
    mytestline.previous_whiteline = 499.60581175200014
    mytestline.next_whiteline = 43.78304700000001
    mytestline.previous_IsHeadline = False
    mytestline.previous_Headlines_cascade = 2
    mytestline.previous_fontsize = 9.962599999999995
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 2
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 5
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "Now comes some extra text."
    mytestline.previous_textline = "2 A new chapter starts now"
    mytestline.fontsize = 9.962600000000066
    mytestline.vertical_position = 553.1242556
    mytestline.previous_whiteline = 43.78304700000001
    mytestline.next_whiteline = 11.955000000000041
    mytestline.previous_IsHeadline = True
    mytestline.previous_Headlines_cascade = 1
    mytestline.previous_fontsize = 24.78710000000001
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 1
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 5
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "With a line break."
    mytestline.previous_textline = "Now comes some extra text."
    mytestline.fontsize = 9.962600000000066
    mytestline.vertical_position = 541.1692555999999
    mytestline.previous_whiteline = 11.955000000000041
    mytestline.next_whiteline = 43.689418399999965
    mytestline.previous_IsHeadline = False
    mytestline.previous_Headlines_cascade = 1
    mytestline.previous_fontsize = 9.962600000000066
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 1
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 5
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "2.1 A new section"
    mytestline.previous_textline = "With a line break."
    mytestline.fontsize = 14.34620000000001
    mytestline.vertical_position = 497.47983719999996
    mytestline.previous_whiteline = 43.689418399999965
    mytestline.next_whiteline = 22.407581599999958
    mytestline.previous_IsHeadline = False
    mytestline.previous_Headlines_cascade = 1
    mytestline.previous_fontsize = 9.962600000000066
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 1
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 5
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "Lets give a splendid additional story."
    mytestline.previous_textline = "2.1 A new section"
    mytestline.fontsize = 9.962600000000009
    mytestline.vertical_position = 475.0722556
    mytestline.previous_whiteline = 22.407581599999958
    mytestline.next_whiteline = 29.277564400000017
    mytestline.previous_IsHeadline = True
    mytestline.previous_Headlines_cascade = 2
    mytestline.previous_fontsize = 14.34620000000001
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 2
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 5
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "2.1.1 Nice subsection"
    mytestline.previous_textline = "Lets give a splendid additional story."
    mytestline.fontsize = 11.95519999999999
    mytestline.vertical_position = 445.7946912
    mytestline.previous_whiteline = 29.277564400000017
    mytestline.next_whiteline = 21.53143560000001
    mytestline.previous_IsHeadline = False
    mytestline.previous_Headlines_cascade = 2
    mytestline.previous_fontsize = 9.962600000000009
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 2
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 5
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "with a beautiful subsection embedded in it."
    mytestline.previous_textline = "2.1.1 Nice subsection"
    mytestline.fontsize = 9.962600000000009
    mytestline.vertical_position = 424.2632556
    mytestline.previous_whiteline = 21.53143560000001
    mytestline.next_whiteline = -2.0
    mytestline.previous_IsHeadline = True
    mytestline.previous_Headlines_cascade = 3
    mytestline.previous_fontsize = 11.95519999999999
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 3
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 5
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = "4"
    mytestline.previous_textline = "with a beautiful subsection embedded in it."
    mytestline.fontsize = 9.962599999999995
    mytestline.vertical_position = 37.14725559999999
    mytestline.previous_whiteline = -2.0
    mytestline.next_whiteline = -2.0
    mytestline.previous_IsHeadline = False
    mytestline.previous_Headlines_cascade = 3
    mytestline.previous_fontsize = 9.962600000000009
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 3
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 5
    textlines.append(mytestline)

    mytestline = CurrentLine()
    mytestline.textline = ""
    mytestline.previous_textline = "4"
    mytestline.fontsize = 9.962599999999995
    mytestline.vertical_position = 37.14725559999999
    mytestline.previous_whiteline = -2.0
    mytestline.next_whiteline = -2.0
    mytestline.previous_IsHeadline = False
    mytestline.previous_Headlines_cascade = 3
    mytestline.previous_fontsize = 9.962599999999995
    mytestline.previousline_IsBroken = False
    mytestline.current_cascade = 3
    mytestline.is_italic = False
    mytestline.is_bold = False
    mytestline.is_highlighted = False
    mytestline.current_pagenumber = 5
    textlines.append(mytestline)
    
    return textlines
