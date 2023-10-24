import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from TextPart code:
sys.path.insert(1, '../../')
from TextPart.textsplitter import textsplitter
from TextPart.textalinea import textalinea

# Imports from Tools:
sys.path.insert(2, '../Tools/')
from AlineasPresent import AlineasPresent
from hardcodedalineas import hardcodedalineas_SplitDoc
from hardcodedalineas import hardcodedalineas_TestTex

# Definition of paths:
inputpath = "../Inputs/"
outputpath = "../Calc_Outputs/"
truthpath = "../True_Outputs/"

# Definition of unit tests:
def TestLayeredSummary_a() -> bool:
    """
    # Unit test for the layered_summary-function of the textsplitter-class.
    # Parameters: None, Return: bool: succes of the test.
    # Author: christiaan Douma
    """
    
    # Begin by creating a textsplitter:
    filename = "TestLayeredSummary"
    thetest = textsplitter()
    thetest.set_documentpath("/not/important/here/")
    thetest.set_documentname(filename)
    thetest.set_labelname(filename)
    thetest.set_outputpath(outputpath)
    
    # With these settings and the ultra-short text in the hardcodedalineas,
    # it is actually possible to check the cascade-structure of the summaries
    # on content, because dummy-summary with a lot of words, should essentially
    # mean that all the text from parents and children is added to each other:
    thetest.set_UseDummySummary(True)
    thetest.set_MaxSummaryLength(600)
    
    # Next, gather the alineas we want to calculate the tree structure for:
    thetest.textalineas = hardcodedalineas_SplitDoc("pdfminer")
    
    # clean the summaries:
    for alinea in thetest.textalineas:
        alinea.summary = ""
        
    # Then, execute the summary:
    Num_Errors = thetest.layered_summary(-1)
    # NOTE: -1 will suppress even the dummy warnings. That is what
    # we want, as we intend to use the dummy version here all the time!!!
    
    # Next, see if we actually managed to provide summaries,
    # by checking the length:
    Answer = True
    for alinea in thetest.textalineas:
        sum_array = alinea.summary.split()
        lengthsum = len(sum_array)
        if (lengthsum<3)and(alinea.sum_CanbeEmpty==False): Answer = False
        
    # Also, check if we encountered errors in the summarization procedure:
    if not (Num_Errors==0):
        Answer = False
        print("textsplitter.layered_summary() encountered " + str(Num_Errors) + "x a child with empty summary.")
        print("This should not be possible, so the test failed!")
    
    # Next, test the summaries on content. Begin by looping over the alineas:
    thetest.textalineas = sorted(thetest.textalineas, key=lambda x: x.nativeID, reverse=False)
    
    for alinea in thetest.textalineas:
        
        # loop over the textcontent inside:
        for textline_raw in alinea.textcontent:
            
            # remove newlines; they could be bothering us.
            textline = textline_raw.replace("\n","")
            
            # Next, test if this line is present in all summaries up
            # to the highest parent:
            alinea_to_check = alinea
            ThisParentID = alinea_to_check.nativeID
            
            while (ThisParentID>=0):
                
                # Begin by checking the summary:
                if not (textline in alinea_to_check.summary):
                    Answer = False
                    print(" ==> we failed to locate <"+textline+"> in the summary of the following alinea:")
                    alinea_to_check.printalinea()
                
                # Then, update alinea_to_check:
                ThisParentID = alinea_to_check.parentID
                if (ThisParentID>=0):
                    alinea_to_check = thetest.textalineas[ThisParentID]
                
    # That should provide the test on content.             
    
    # Done:
    return Answer

def TestLayeredSummary_b() -> bool:
    """
    # Unit test for the layered_summary-function of the textsplitter-class.
    # Parameters: None, Return: bool: succes of the test.
    # Author: christiaan Douma
    """
    
    # Begin by creating a textsplitter:
    filename = "TestLayeredSummary"
    thetest = textsplitter()
    thetest.set_documentpath("/not/important/here/")
    thetest.set_documentname(filename)
    thetest.set_labelname(filename)
    thetest.set_outputpath(outputpath)
    
    # With these settings and the ultra-short text in the hardcodedalineas,
    # it is actually possible to check the cascade-structure of the summaries
    # on content, because dummy-summary with a lot of words, should essentially
    # mean that all the text from parents and children is added to each other:
    thetest.set_UseDummySummary(True)
    thetest.set_MaxSummaryLength(600)
    
    # Next, gather the alineas we want to calculate the tree structure for:
    thetest.textalineas = hardcodedalineas_SplitDoc("pymupdf")
    
    # clean the summaries:
    for alinea in thetest.textalineas:
        alinea.summary = ""
    
    # Then, execute the summary:
    Num_Errors = thetest.layered_summary(-1)
    # NOTE: -1 will suppress even the dummy warnings. That is what
    # we want, as we intend to use the dummy version here all the time!!!
    
    # Next, see if we actually managed to provide summaries,
    # by checking the length:
    Answer = True
    for alinea in thetest.textalineas:
        sum_array = alinea.summary.split()
        lengthsum = len(sum_array)
        if (lengthsum<3)and(alinea.sum_CanbeEmpty==False): Answer = False
        
    # Also, check if we encountered errors in the summarization procedure:
    if not (Num_Errors==0):
        Answer = False
        print("textsplitter.layered_summary() encountered " + str(Num_Errors) + "x a child with empty summary.")
        print("This should not be possible, so the test failed!")
    
    # Next, test the summaries on content. Begin by looping over the alineas:
    thetest.textalineas = sorted(thetest.textalineas, key=lambda x: x.nativeID, reverse=False)
    
    for alinea in thetest.textalineas:
        
        # loop over the textcontent inside:
        for textline_raw in alinea.textcontent:
            
            # remove newlines; they could be bothering us.
            textline = textline_raw.replace("\n","")
            
            # Next, test if this line is present in all summaries up
            # to the highest parent:
            alinea_to_check = alinea
            ThisParentID = alinea_to_check.nativeID
            
            while (ThisParentID>=0):
                
                # Begin by checking the summary:
                if not (textline in alinea_to_check.summary):
                    Answer = False
                    print(" ==> we failed to locate <"+textline+"> in the summary of the following alinea:")
                    alinea_to_check.printalinea()
                
                # Then, update alinea_to_check:
                ThisParentID = alinea_to_check.parentID
                if (ThisParentID>=0):
                    alinea_to_check = thetest.textalineas[ThisParentID]
                
    # That should provide the test on content.             
    
    # Done:
    return Answer

def TestLayeredSummary_c() -> bool:
    """
    # Unit test for the layered_summary-function of the textsplitter-class.
    # Parameters: None, Return: bool: succes of the test.
    # Author: christiaan Douma
    """
    
    # Begin by creating a textsplitter:
    filename = "TestLayeredSummary"
    thetest = textsplitter()
    thetest.set_documentpath("/not/important/here/")
    thetest.set_documentname(filename)
    thetest.set_labelname(filename)
    thetest.set_outputpath(outputpath)
    
    # With these settings and the ultra-short text in the hardcodedalineas,
    # it is actually possible to check the cascade-structure of the summaries
    # on content, because dummy-summary with a lot of words, should essentially
    # mean that all the text from parents and children is added to each other:
    thetest.set_UseDummySummary(True)
    thetest.set_MaxSummaryLength(600)
    
    # Next, gather the alineas we want to calculate the tree structure for:
    thetest.textalineas = hardcodedalineas_TestTex("pdfminer")
    
    # clean the summaries:
    for alinea in thetest.textalineas:
        alinea.summary = ""
    
    # Then, execute the summary:
    Num_Errors = thetest.layered_summary(-1)
    # NOTE: -1 will suppress even the dummy warnings. That is what
    # we want, as we intend to use the dummy version here all the time!!!
    
    # Next, see if we actually managed to provide summaries,
    # by checking the length:
    Answer = True
    for alinea in thetest.textalineas:
        sum_array = alinea.summary.split()
        lengthsum = len(sum_array)
        if (lengthsum<3)and(alinea.sum_CanbeEmpty==False): Answer = False
        
    # Also, check if we encountered errors in the summarization procedure:
    if not (Num_Errors==0):
        Answer = False
        print("textsplitter.layered_summary() encountered " + str(Num_Errors) + "x a child with empty summary.")
        print("This should not be possible, so the test failed!")
    
    # Next, test the summaries on content. Begin by looping over the alineas:
    thetest.textalineas = sorted(thetest.textalineas, key=lambda x: x.nativeID, reverse=False)
    
    for alinea in thetest.textalineas:
        
        # loop over the textcontent inside:
        for textline_raw in alinea.textcontent:
            
            # remove newlines; they could be bothering us.
            textline = textline_raw.replace("\n","")
            
            # Next, test if this line is present in all summaries up
            # to the highest parent:
            alinea_to_check = alinea
            ThisParentID = alinea_to_check.nativeID
            
            while (ThisParentID>=0):
                
                # Begin by checking the summary:
                if not (textline in alinea_to_check.summary):
                    Answer = False
                    print(" ==> we failed to locate <"+textline+"> in the summary of the following alinea:")
                    alinea_to_check.printalinea()
                
                # Then, update alinea_to_check:
                ThisParentID = alinea_to_check.parentID
                if (ThisParentID>=0):
                    alinea_to_check = thetest.textalineas[ThisParentID]
                
    # That should provide the test on content.             
    
    # Done:
    return Answer

def TestLayeredSummary_d() -> bool:
    """
    # Unit test for the layered_summary-function of the textsplitter-class.
    # Parameters: None, Return: bool: succes of the test.
    # Author: christiaan Douma
    """
    
    # Begin by creating a textsplitter:
    filename = "TestLayeredSummary"
    thetest = textsplitter()
    thetest.set_documentpath("/not/important/here/")
    thetest.set_documentname(filename)
    thetest.set_labelname(filename)
    thetest.set_outputpath(outputpath)
    
    # With these settings and the ultra-short text in the hardcodedalineas,
    # it is actually possible to check the cascade-structure of the summaries
    # on content, because dummy-summary with a lot of words, should essentially
    # mean that all the text from parents and children is added to each other:
    thetest.set_UseDummySummary(True)
    thetest.set_MaxSummaryLength(600)
    
    # Next, gather the alineas we want to calculate the tree structure for:
    thetest.textalineas = hardcodedalineas_TestTex("pymupdf")
    
    # clean the summaries:
    for alinea in thetest.textalineas:
        alinea.summary = ""
    
    # Then, execute the summary:
    Num_Errors = thetest.layered_summary(-1)
    # NOTE: -1 will suppress even the dummy warnings. That is what
    # we want, as we intend to use the dummy version here all the time!!!
    
    # Next, see if we actually managed to provide summaries,
    # by checking the length:
    Answer = True
    for alinea in thetest.textalineas:
        sum_array = alinea.summary.split()
        lengthsum = len(sum_array)
        if (lengthsum<3)and(alinea.sum_CanbeEmpty==False): Answer = False
        
    # Also, check if we encountered errors in the summarization procedure:
    if not (Num_Errors==0):
        Answer = False
        print("textsplitter.layered_summary() encountered " + str(Num_Errors) + "x a child with empty summary.")
        print("This should not be possible, so the test failed!")
    
    # Next, test the summaries on content. Begin by looping over the alineas:
    thetest.textalineas = sorted(thetest.textalineas, key=lambda x: x.nativeID, reverse=False)
    
    for alinea in thetest.textalineas:
        
        # loop over the textcontent inside:
        for textline_raw in alinea.textcontent:
            
            # remove newlines; they could be bothering us.
            textline = textline_raw.replace("\n","")
            
            # Next, test if this line is present in all summaries up
            # to the highest parent:
            alinea_to_check = alinea
            ThisParentID = alinea_to_check.nativeID
            
            while (ThisParentID>=0):
                
                # Begin by checking the summary:
                if not (textline in alinea_to_check.summary):
                    Answer = False
                    print(" ==> we failed to locate <"+textline+"> in the summary of the following alinea:")
                    alinea_to_check.printalinea()
                
                # Then, update alinea_to_check:
                ThisParentID = alinea_to_check.parentID
                if (ThisParentID>=0):
                    alinea_to_check = thetest.textalineas[ThisParentID]
                
    # That should provide the test on content.             
    
    # Done:
    return Answer

# Definition of unit tests:
def TestLayeredSummary_e() -> bool:
    """
    # Unit test for the layered_summary-function of the textsplitter-class.
    # Parameters: None, Return: bool: succes of the test.
    # Author: christiaan Douma
    """
    
    # Begin by creating a textsplitter:
    filename = "TestLayeredSummary"
    thetest = textsplitter()
    thetest.set_documentpath("/not/important/here/")
    thetest.set_documentname(filename)
    thetest.set_labelname(filename)
    thetest.set_outputpath(outputpath)
    
    # With these settings and the ultra-short text in the hardcodedalineas,
    # it is actually possible to check the cascade-structure of the summaries
    # on content, because dummy-summary with a lot of words, should essentially
    # mean that all the text from parents and children is added to each other:
    thetest.set_UseDummySummary(True)
    thetest.set_MaxSummaryLength(0) # On purpose; to triger erros and see if they are handled OK.
    
    # Next, gather the alineas we want to calculate the tree structure for:
    thetest.textalineas = hardcodedalineas_SplitDoc("pdfminer")
    
    # clean the summaries:
    for alinea in thetest.textalineas:
        alinea.summary = ""
        
    # Then, execute the summary:
    Num_Errors = thetest.layered_summary(-1)
    # NOTE: -1 will suppress even the dummy warnings. That is what
    # we want, as we intend to use the dummy version here all the time!!!
        
    # Also, check if we encountered errors in the summarization procedure:
    Answer = True
    if not (Num_Errors==9):
        Answer = False
        print("textsplitter.layered_summary() is supposed to encounter 9 errors, but encountered " + str(Num_Errors) + "instead.")
    
    # Done:
    return Answer

def TestLayeredSummary() -> bool:
    """
    # Collection of unit test for the calculatetree-function of the textsplitter-class.
    # Parameters: None. Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    # Declare the answer:
    Answer = True
    
    if not TestLayeredSummary_a():
        Answer = False
        print("==> TestLayeredSummary_a() failed!")
    
    if not TestLayeredSummary_b():
        Answer = False
        print("==> TestLayeredSummary_b() failed!")
        
    if not TestLayeredSummary_c():
        Answer = False
        print("==> TestLayeredSummary_c() failed!")
    
    if not TestLayeredSummary_d():
        Answer = False
        print("==> TestLayeredSummary_d() failed!")
    
    if not TestLayeredSummary_e():
        Answer = False
        print("==> TestLayeredSummary_e() failed!")
    
    # Done:
    return Answer
    
if __name__ == '__main__':
    
    if TestLayeredSummary():
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
