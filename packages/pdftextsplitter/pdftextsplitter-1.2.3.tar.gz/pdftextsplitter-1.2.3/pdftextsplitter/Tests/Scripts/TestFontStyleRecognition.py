import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from TextPart code:
sys.path.insert(1, '../../')
from TextPart.textpart import textpart
from TextPart.textgeneration import is_italic
from TextPart.textgeneration import is_bold

inputpath = "../Inputs/"


def TestFontStyleRecognition_a() -> bool:
    """
       # Unit test for the TestFontStyle for the code coverage:
       # Parameters: none; # Returns (bool): succes of the text.
       # Author: Remco van Groesen
       """
    check = is_italic('nothing important', 'nonexistingmethod')
    if check:
        print("is_italic('nothing important', 'nonexistingmethod') is supposed to return False!")
    return not check


def TestFontStyleRecognition_b() -> bool:
    """
       # Unit test for the TestFontStyle for the code coverage:
       # Parameters: none; # Returns (bool): succes of the text.
       # Author: Remco van Groesen
       """
    check = is_bold('nothing important', 'nonexistingmethod')
    if check:
        print("is_bold('nothing important', 'nonexistingmethod') is supposed to return False!")
    return not check


def TestFontStyleRecognition_c() -> bool:
    """
          # Unit test reading out bold font in a pdf correctly using pdfminer:
          # Parameters: none; # Returns (bool): succes of the text.
          # Author: Remco van Groesen
          """

    filename = "TestFontStylesDoc"
    thetest = textpart()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath('notimportant')
    thetest.set_labelname(filename)
    thetest.textgeneration("pdfminer")

    Answer = True
    true_is_bold_results = [True, False, True, False]
    if len(true_is_bold_results) != len(thetest.is_bold):
        print("The is_bold-array does not have the correct length for pdfminer!")
        Answer = False
    else:
        for i, val in enumerate(true_is_bold_results):
            if true_is_bold_results[i] != thetest.is_bold[i]:
                print("For pdfminer & textline " + str(i) + ", is_bold did not return " + str(true_is_bold_results[i]))
                Answer = False

    return Answer


def TestFontStyleRecognition_d() -> bool:
    """
          # Unit test reading out italic font in a pdf correctly using pdfminer:
          # Parameters: none; # Returns (bool): succes of the text.
          # Author: Remco van Groesen
          """

    filename = "TestFontStylesDoc"
    thetest = textpart()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath('notimportant')
    thetest.set_labelname(filename)
    thetest.textgeneration("pdfminer")

    Answer = True
    true_is_italic_results = [False, True, True, False]
    if len(true_is_italic_results) != len(thetest.is_italic):
        print("The is_italic-array does not have the correct length for pdfminer!")
        Answer = False
    else:
        for i, val in enumerate(true_is_italic_results):
            if true_is_italic_results[i] != thetest.is_italic[i]:
                print("For pdfminer & textline " + str(i) + ", is_italic did not return " + str(true_is_italic_results[i]))
                Answer = False

    return Answer


def TestFontStyleRecognition_e() -> bool:
    """
          # Unit test reading out bold font in a pdf correctly using pymupdf:
          # Parameters: none; # Returns (bool): succes of the text.
          # Author: Remco van Groesen
          """

    filename = "TestFontStylesDoc"
    thetest = textpart()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath('notimportant')
    thetest.set_labelname(filename)
    thetest.textgeneration("pymupdf")

    Answer = True
    true_is_bold_results = [True, False, True, False]
    if len(true_is_bold_results) != len(thetest.is_bold):
        print("The is_bold-array does not have the correct length for pymupdf!")
        Answer = False
    else:
        for i, val in enumerate(true_is_bold_results):
            if true_is_bold_results[i] != thetest.is_bold[i]:
                print("For pymupdf & textline " + str(i) + ", is_bold did not return " + str(true_is_bold_results[i]))
                Answer = False

    return Answer


def TestFontStyleRecognition_f() -> bool:
    """
          # Unit test reading out italic font in a pdf correctly using pymupdf:
          # Parameters: none; # Returns (bool): succes of the text.
          # Author: Remco van Groesen
          """

    filename = "TestFontStylesDoc"
    thetest = textpart()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath('notimportant')
    thetest.set_labelname(filename)
    thetest.textgeneration("pymupdf")

    Answer = True
    true_is_italic_results = [False, True, True, False]
    if len(true_is_italic_results) != len(thetest.is_italic):
        print("The is_italic-array does not have the correct length for pymupdf!")
        Answer = False
    else:
        for i, val in enumerate(true_is_italic_results):
            if true_is_italic_results[i] != thetest.is_italic[i]:
                print("For pymupdf & textline " + str(i) + ", is_italic did not return " + str(true_is_italic_results[i]))
                Answer = False

    return Answer


def TestFontStyleRecognition() -> bool:
    """
    # Collection-function of Unit-tests.
    # Parameters: None
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """

    Answer = True
    if not TestFontStyleRecognition_a(): Answer = False
    print("TestFontStyleRecognition_a()...")
    if not TestFontStyleRecognition_b(): Answer = False
    print("TestFontStyleRecognition_b()...")
    if not TestFontStyleRecognition_c(): Answer = False
    print("TestFontStyleRecognition_c()...")
    if not TestFontStyleRecognition_d(): Answer = False
    print("TestFontStyleRecognition_d()...")
    if not TestFontStyleRecognition_e(): Answer = False
    print("TestFontStyleRecognition_e()...")
    if not TestFontStyleRecognition_f(): Answer = False
    print("TestFontStyleRecognition_f()...")

    return Answer


if __name__ == '__main__':

    if TestFontStyleRecognition():
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
