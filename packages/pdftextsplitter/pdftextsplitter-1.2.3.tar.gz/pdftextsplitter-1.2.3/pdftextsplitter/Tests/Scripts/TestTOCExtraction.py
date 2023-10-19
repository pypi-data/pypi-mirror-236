import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from TextPart code:
sys.path.insert(1, '../../')
from TextPart.textsplitter import textsplitter

# Imports from Tools:
sys.path.insert(2, '../Tools/')
from hardcoded_TOC_Elements import hardcoded_DNN_TOC
from hardcoded_TOC_Elements import hardcoded_cellar_TOC

# Definition of paths:
inputpath = "../Inputs/"
outputpath = "../Calc_Outputs/"
truthpath = "../True_Outputs/"

# Definition of unit tests:
def TestTOCExtraction_a() -> bool:
    """
    # Unit test for TOC-extraction using the textpart-class.
    # For a document that contains a native TOC.
    # Parameters: None
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    # Perform the TOC-extraction:
    filename = "CADouma_DNN_Publication"
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.set_labelname("DNN_TOCTest")
    thetest.read_native_toc("pdfminer")
    
    # Obtain the correct answers:
    Correct_TOC_elements = hardcoded_DNN_TOC()
    
    # Compare elements:
    Answer = True
    if not (len(Correct_TOC_elements)==len(thetest.native_TOC)):
        Answer = False
        print("The obtained(pdfminer) Native TOC-array does not have the correct length.")
        print("Therefore, it must contain incorrect TOC-elements.")
    else:
        # Then, compare individual elements:
        index = 0
        for element in Correct_TOC_elements:
            if not element.compare(thetest.native_TOC[index]):
                print("We found(pdfminer) an inconsistency at array-element " + str(index) + ": ==>")
                element.print_TOC_element()
                thetest.native_TOC[index].print_TOC_element()
                Answer = False
            index = index + 1
    
    # Done:
    return Answer

# Definition of unit tests:
def TestTOCExtraction_b() -> bool:
    """
    # Unit test for TOC-extraction using the textpart-class,
    # Now to a document that has no native TOC.
    # Parameters: None
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    # Perform the TOC-extraction:
    filename = "SplitDoc"
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.set_labelname("SplitDoc_TOCTest")
    thetest.read_native_toc("pdfminer")
   
    # Check that the array has zero-length:
    Answer = False
    if (len(thetest.native_TOC)==0): Answer = True
    else:
        print("SplitDoc.pdf is not supposed to have a TOC. So we expected(pdfminer) to find")
        print("Arraylength=0, but we found instead:")
        
        for element in thetest.native_TOC:
            element.print_TOC_element()
    
    # Done:
    return Answer

# Definition of unit tests:
def TestTOCExtraction_c() -> bool:
    """
    # Unit test for TOC-extraction using the textpart-class.
    # For a document that contains a native TOC.
    # Parameters: None
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    # Perform the TOC-extraction:
    filename = "CADouma_DNN_Publication"
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.set_labelname("DNN_TOCTest")
    thetest.read_native_toc("pymupdf")
    
    # Obtain the correct answers:
    Correct_TOC_elements = hardcoded_DNN_TOC()
    
    # Compare elements:
    Answer = True
    if not (len(Correct_TOC_elements)==len(thetest.native_TOC)):
        Answer = False
        print("The obtained(pymupdf) Native TOC-array does not have the correct length.")
        print("Therefore, it must contain incorrect TOC-elements.")
    else:
        # Then, compare individual elements:
        index = 0
        for element in Correct_TOC_elements:
            if not element.compare(thetest.native_TOC[index]):
                print("We found(pymupdf) an inconsistency at arry-element " + str(index) + ": ==>")
                element.print_TOC_element()
                thetest.native_TOC[index].print_TOC_element()
                Answer = False
            index = index + 1
    
    # Done:
    return Answer

# Definition of unit tests:
def TestTOCExtraction_d() -> bool:
    """
    # Unit test for TOC-extraction using the textpart-class,
    # Now to a document that has no native TOC.
    # Parameters: None
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    # Perform the TOC-extraction:
    filename = "SplitDoc"
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.set_labelname("SplitDoc_TOCTest")
    thetest.read_native_toc("pymupdf")
   
    # Check that the array has zero-length:
    Answer = False
    if (len(thetest.native_TOC)==0): Answer = True
    else:
        print("SplitDoc.pdf is not supposed to have a TOC. So we expected(pymupdf) to find")
        print("Arraylength=0, but we found instead:")
        
        for element in thetest.native_TOC:
            element.print_TOC_element()
    
    # Done:
    return Answer

def TestTOCExtraction_e() -> bool:
    """
    # Unit test for TOC-extraction using the textpart-class.
    # For a document that contains a native TOC.
    # Parameters: None
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    # Perform the TOC-extraction:
    filename = "cellar"
    thetest = textsplitter()
    thetest.set_documentpath("../Regressie/")
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.set_labelname("DNN_TOCTest")
    thetest.read_native_toc("pymupdf")
    
    # Obtain the correct answers:
    Correct_TOC_elements = hardcoded_cellar_TOC()
    
    # Compare elements:
    Answer = True
    if not (len(Correct_TOC_elements)==len(thetest.native_TOC)):
        Answer = False
        print("The obtained(pymupdf) Native TOC-array does not have the correct length.")
        print("Therefore, it must contain incorrect TOC-elements.")
    else:
        # Then, compare individual elements:
        index = 0
        for element in Correct_TOC_elements:
            if not element.compare_withpagenr(thetest.native_TOC[index]):
                print("We found(pymupdf) an inconsistency at array-element " + str(index) + ": ==>")
                element.print_TOC_element()
                thetest.native_TOC[index].print_TOC_element()
                Answer = False
            index = index + 1
    
    # Done:
    return Answer

def TestTOCExtraction_f() -> bool:
    """
    # Unit test for TOC-extraction using the textpart-class.
    # For a document that contains a native TOC.
    # Parameters: None
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    # Perform the TOC-extraction:
    filename = "cellar"
    thetest = textsplitter()
    thetest.set_documentpath("../Regressie/")
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.set_labelname("DNN_TOCTest")
    thetest.read_native_toc("pdfminer")
    
    # Obtain the correct answers:
    Correct_TOC_elements = hardcoded_cellar_TOC()
    
    # Compare elements:
    Answer = True
    if not (len(Correct_TOC_elements)==len(thetest.native_TOC)):
        Answer = False
        print("The obtained(pymupdf) Native TOC-array does not have the correct length.")
        print("Therefore, it must contain incorrect TOC-elements.")
    else:
        # Then, compare individual elements:
        index = 0
        for element in Correct_TOC_elements:
            if not element.compare_withpos(thetest.native_TOC[index]):
                print("We found(pymupdf) an inconsistency at array-element " + str(index) + ": ==>")
                element.print_TOC_element()
                thetest.native_TOC[index].print_TOC_element()
                Answer = False
            index = index + 1
    
    # Done:
    return Answer
    
# Definition of collection:    
def TestTOCExtraction() -> bool:
    """
    # Collection-function of Unit-tests.
    # Parameters: None
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    Answer = True
    if (TestTOCExtraction_a()==False): Answer=False 
    print("TestTOCExtraction_a()...")
    if (TestTOCExtraction_b()==False): Answer=False 
    print("TestTOCExtraction_b()...")
    if (TestTOCExtraction_c()==False): Answer=False 
    print("TestTOCExtraction_c()...")
    if (TestTOCExtraction_d()==False): Answer=False 
    print("TestTOCExtraction_d()...")
    if (TestTOCExtraction_e()==False): Answer=False 
    print("TestTOCExtraction_e()...")
    if (TestTOCExtraction_f()==False): Answer=False 
    print("TestTOCExtraction_f()...")
    
    return Answer

if __name__ == '__main__':
    
    if TestTOCExtraction():
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
