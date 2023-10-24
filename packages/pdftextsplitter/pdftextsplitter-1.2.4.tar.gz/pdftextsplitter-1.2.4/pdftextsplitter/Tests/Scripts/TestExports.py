import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from TextPart code:
sys.path.insert(1, '../../')
from TextPart.textsplitter import textsplitter
from TextPart.CurrentLine import CurrentLine

# Imports from Tools:
sys.path.insert(2, '../Tools/')
from hardcodedalineas import hardcodedalineas_SplitDoc
from hardcodedalineas import hardcodedalineas_TestTex
from FileComparison import FileComparison
from hardcodedtextlines import hardcodedtextlines

# Definition of paths:
inputpath = "../Inputs/"
outputpath = "../Calc_Outputs/"
truthpath = "../True_Outputs/"

# Definition of unit tests:
def TestExport_Alineas_a() -> bool:
    """
    # Unit-test for the export_alineas-function of the textsplitter-class.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: Christiaan Douma
    """
    
    # Begin by declaring a textsplitter-class:
    filename = "Export_Alinea_test_a"
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.set_labelname(filename)
    
    # Load hard-coded alineas into the textsplitter:
    thetest.textalineas = hardcodedalineas_SplitDoc("pdfminer")
    
    # Then, perform the export:
    thetest.exportalineas("complete")
    
    # Next, compare the outputs:
    rapport = FileComparison(outputpath+filename+"_BreakdownResults",truthpath+filename+"_BreakdownResults","txt")
    Answer = False
    if (rapport==""): Answer = True 
    else: print(" ==> TestExport_Alineas_a()|SplitDoc & pdfminer:\n\n" + rapport + "----------------------------------------------------")
    
    # Return the answer:
    return Answer

def TestExport_Alineas_b() -> bool:
    """
    # Unit-test for the export_alineas-function of the textsplitter-class.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: Christiaan Douma
    """
    
    # Begin by declaring a textsplitter-class:
    filename = "Export_Alinea_test_b"
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.set_labelname(filename)
    
    # Load hard-coded alineas into the textsplitter:
    thetest.textalineas = hardcodedalineas_SplitDoc("pymupdf")
    
    # Then, perform the export:
    thetest.exportalineas("complete")
    
    # Next, compare the outputs:
    rapport = FileComparison(outputpath+filename+"_BreakdownResults",truthpath+filename+"_BreakdownResults","txt")
    Answer = False
    if (rapport==""): Answer = True 
    else: print(" ==> TestExport_Alineas_b()|SplitDoc & pymupdf:\n\n" + rapport + "----------------------------------------------------")
    
    # Return the answer:
    return Answer

def TestExport_Alineas_c() -> bool:
    """
    # Unit-test for the export_alineas-function of the textsplitter-class.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: Christiaan Douma
    """
    
    # Begin by declaring a textsplitter-class:
    filename = "Export_Alinea_test_c"
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.set_labelname(filename)
    
    # Load hard-coded alineas into the textsplitter:
    thetest.textalineas = hardcodedalineas_TestTex("pymupdf")
    
    # Then, perform the export:
    thetest.exportalineas("default")
    
    # Next, compare the outputs:
    rapport = FileComparison(outputpath+filename+"_BreakdownResults",truthpath+filename+"_BreakdownResults","txt")
    Answer = False
    if (rapport==""): Answer = True 
    else: print(" ==> TestExport_Alineas_c()|TestTex & pymupdf:\n\n" + rapport + "----------------------------------------------------")
    
    # Return the answer:
    return Answer

def TestExport_Alineas_d() -> bool:
    """
    # Unit-test for the export_alineas-function of the textsplitter-class.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: Christiaan Douma
    """
    
    # Begin by declaring a textsplitter-class:
    filename = "Export_Alinea_test_d"
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.set_labelname(filename)
    
    # Load hard-coded alineas into the textsplitter:
    thetest.textalineas = hardcodedalineas_TestTex("pdfminer")
    
    # Then, perform the export:
    thetest.exportalineas("default")
    
    # Next, compare the outputs:
    rapport = FileComparison(outputpath+filename+"_BreakdownResults",truthpath+filename+"_BreakdownResults","txt")
    Answer = False
    if (rapport==""): Answer = True 
    else: print(" ==> TestExport_Alineas_d()|TestTex & pdfminer:\n\n" + rapport + "----------------------------------------------------")
    
    # Return the answer:
    return Answer

def TestExport_Alineas_e() -> bool:
    """
    # Unit-test for the export_alineas-function of the textsplitter-class.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: Christiaan Douma
    """
    
    # Begin by declaring a textsplitter-class:
    filename = "Export_Alinea_test_e"
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.set_labelname(filename)
    
    # Attempt to execute the export without loading anything, just to see what happens:
    thetest.exportalineas("default")
    
    # Next, compare the outputs:
    rapport = FileComparison(outputpath+filename+"_BreakdownResults",truthpath+filename+"_BreakdownResults","txt")
    Answer = False
    if (rapport==""): Answer = True 
    else: print(" ==> TestExport_Alineas_e():\n\n" + rapport + "----------------------------------------------------")
    
    # Return the answer:
    return Answer

# Definition of unit tests:
def TestExport_Decisions_a() -> bool:
    """
    # Unit-test for the exportdecisions-function of the textsplitter-class.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: Christiaan Douma
    """
    
    # Begin by creating a textsplitter:
    filename = "TestExportDecisions"
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_labelname(filename)
    thetest.set_outputpath(outputpath)
    thetest.set_labelname("TestExportDecisions")
    
    # Next, put in there hard-coded what we need:
    thelines = hardcodedtextlines()
    thetest.textclassification.clear()
    
    for oneline in thelines:
        thetest.textclassification.append(oneline.textline)
    
    # Then, perform the exportfunction:
    thetest.exportdecisions()
    
    # Then, compare the output to the reference:
    Answer = True
    rapport = FileComparison(outputpath+filename+"_decisions",truthpath+filename+"_decisions","txt")
    if not (rapport==""): 
        Answer = False 
        print(" ==> exportdecisions() file comparison:\n\n" + rapport + "----------------------------------------------------")
    
    return Answer

def TestExport_Decisions_b() -> bool:
    """
    # Unit-test for the exportdecisions-function of the textsplitter-class.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: Christiaan Douma
    """
    
    # Begin by creating a textsplitter:
    filename = "TestExportDecisions_b"
    thetest = textsplitter()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_labelname(filename)
    thetest.set_outputpath(outputpath)
    thetest.set_labelname("TestExportDecisions")
    
    # Attempt to execute the export without loading anything, just to see what happens:
    thetest.exportdecisions()
    
    # Then, compare the output to the reference:
    Answer = True
    rapport = FileComparison(outputpath+filename+"_decisions",truthpath+filename+"_decisions","txt")
    if not (rapport==""): 
        Answer = False 
        print(" ==> exportdecisions() file comparison:\n\n" + rapport + "----------------------------------------------------")
    
    return Answer

# Definition of collection:
def TestExports() -> bool:
    """
    # Collection-function of unit-tests.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: Christiaan Douma
    """
    
    # Declare the answer:
    Answer = True
    
    # Go over the cases:
    if not TestExport_Alineas_a():
        Answer = False
        print('TestExport_Alineas_a() failed!')
    
    if not TestExport_Alineas_b():
        Answer = False
        print('TestExport_Alineas_b() failed!')
        
    if not TestExport_Alineas_c():
        Answer = False
        print('TestExport_Alineas_c() failed!')
        
    if not TestExport_Alineas_d():
        Answer = False
        print('TestExport_Alineas_d() failed!')
        
    if not TestExport_Alineas_e():
        Answer = False
        print('TestExport_Alineas_e() failed!')
    
    if not TestExport_Decisions_a():
        Answer = False
        print('TestExport_Decisions_a() failed!')
      
    if not TestExport_Decisions_b():
        Answer = False
        print('TestExport_Decisions_b() failed!')
    
    # Return the answer:
    return Answer

if __name__ == '__main__':
    if TestExports():
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
