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

# Definition of unit tests:
def TestTreeStructure_a() -> bool:
    """
    # Unit test for the calculatetree-function of the textsplitter-class.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Begin by creating a textsplitter:
    filename = "TestTreeStructure"
    thetest = textsplitter()
    thetest.set_documentpath("/not/important/here/")
    thetest.set_documentname(filename)
    thetest.set_labelname(filename)
    thetest.set_outputpath("/not/important/either/")
    
    # Next, gather the alineas we want to calculate the tree structure for:
    thetest.textalineas = hardcodedalineas_SplitDoc("pdfminer")
    truealineas = hardcodedalineas_SplitDoc("pdfminer")
    # We call the same function twice, because we do not want python to create 2 
    # pointers to the same object, we really want 2 different objects.
    
    # Then, blind the parentID & horizontal ordering:
    for alinea in thetest.textalineas:
        alinea.parentID = -1
        alinea.horizontal_ordering = -1
        
    # Then, calculate the tree structure:
    thetest.calculatetree()
    
    # Next, see if we found the correct structure:
    index = 0
    Answer = True
    for alinea in thetest.textalineas:
        if not alinea.compare_samearray(truealineas[index]): # Because in these unit-tests we know we get exactly the correct parentID.
            Answer = False
            print(" ==> We calculated the wrong parentID ["+str(alinea.parentID)+"] or horizontal ordering ["+str(alinea.horizontal_ordering)+"] for the following alinea:")
            truealineas[index].printalinea()
        index = index + 1
  
    # Done:
    return Answer

def TestTreeStructure_b() -> bool:
    """
    # Unit test for the calculatetree-function of the textsplitter-class.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Begin by creating a textsplitter:
    filename = "TestTreeStructure"
    thetest = textsplitter()
    thetest.set_documentpath("/not/important/here/")
    thetest.set_documentname(filename)
    thetest.set_labelname(filename)
    thetest.set_outputpath("/not/important/either/")
    
    # Next, gather the alineas we want to calculate the tree structure for:
    thetest.textalineas = hardcodedalineas_SplitDoc("pymupdf")
    truealineas = hardcodedalineas_SplitDoc("pymupdf")
    # We call the same function twice, because we do not want python to create 2 
    # pointers to the same object, we really want 2 different objects.
    
    # Then, blind the parentID & horizontal ordering:
    for alinea in thetest.textalineas:
        alinea.parentID = -1
        alinea.horizontal_ordering = -1
    
    # For pymupdf-splitdoc integration test the horizontal_ordering of element 1 was
    # put to zero, because that is what comes out of the integration test.
    # But it is not what we expect to come out here, so:
    truealineas[1].horizontal_ordering = 1
    
    # Then, calculate the tree structure:
    thetest.calculatetree()
    
    # To correct for that pymupdf accidentally finds another level==1 in the titlepage that pdfminer does not:
    for alinea in thetest.textalineas:
        if (alinea.textlevel==1):
            alinea.horizontal_ordering = alinea.horizontal_ordering + 1
    
    # Next, see if we found the correct structure:
    index = 0
    Answer = True
    for alinea in thetest.textalineas:
        if not alinea.compare_samearray(truealineas[index]):
            Answer = False
            print(" ==> We calculated the wrong parentID ["+str(alinea.parentID)+"] or horizontal ordering ["+str(alinea.horizontal_ordering)+"] for the following alinea:")
            truealineas[index].printalinea()
        index = index + 1
  
    # Done:
    return Answer

def TestTreeStructure_c() -> bool:
    """
    # Unit test for the calculatetree-function of the textsplitter-class.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Begin by creating a textsplitter:
    filename = "TestTreeStructure"
    thetest = textsplitter()
    thetest.set_documentpath("/not/important/here/")
    thetest.set_documentname(filename)
    thetest.set_labelname(filename)
    thetest.set_outputpath("/not/important/either/")
    
    # Next, gather the alineas we want to calculate the tree structure for:
    thetest.textalineas = hardcodedalineas_TestTex("pdfminer")
    truealineas = hardcodedalineas_TestTex("pdfminer")
    # We call the same function twice, because we do not want python to create 2 
    # pointers to the same object, we really want 2 different objects.
    
    # Then, blind the parentID & horizontal ordering:
    for alinea in thetest.textalineas:
        alinea.parentID = -1
        alinea.horizontal_ordering = -1
        
    # For the integration test the horizontal orderings at cascade-level 1
    # are shifted (because the outcome of the integration test contains more
    # cascade-1 elements than that we test for). But that is not what will
    # happen here, so we need to shift back:
    
    # Then, calculate the tree structure:
    thetest.calculatetree()
    
    # Next, see if we found the correct structure:
    index = 0
    Answer = True
    for alinea in thetest.textalineas:
        if not alinea.compare_samearray(truealineas[index]):
            Answer = False
            print(" ==> We calculated the wrong parentID ["+str(alinea.parentID)+"] or horizontal ordering ["+str(alinea.horizontal_ordering)+"] for the following alinea:")
            truealineas[index].printalinea()
        index = index + 1
  
    # Done:
    return Answer

def TestTreeStructure_d() -> bool:
    """
    # Unit test for the calculatetree-function of the textsplitter-class.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Begin by creating a textsplitter:
    filename = "TestTreeStructure"
    thetest = textsplitter()
    thetest.set_documentpath("/not/important/here/")
    thetest.set_documentname(filename)
    thetest.set_labelname(filename)
    thetest.set_outputpath("/not/important/either/")
    
    # Next, gather the alineas we want to calculate the tree structure for:
    thetest.textalineas = hardcodedalineas_TestTex("pymupdf")
    truealineas = hardcodedalineas_TestTex("pymupdf")
    # We call the same function twice, because we do not want python to create 2 
    # pointers to the same object, we really want 2 different objects.
    
    # Then, blind the parentID & horizontal ordering:
    for alinea in thetest.textalineas:
        alinea.parentID = -1
        alinea.horizontal_ordering = -1
        
    # For the integration test the horizontal orderings at cascade-level 1
    # are shifted (because the outcome of the integration test contains more
    # cascade-1 elements than that we test for). But that is not what will
    # happen here, so we need to shift back:
    
    # Then, calculate the tree structure:
    thetest.calculatetree()
    
    # Next, see if we found the correct structure:
    index = 0
    Answer = True
    for alinea in thetest.textalineas:
        if not alinea.compare_samearray(truealineas[index]):
            Answer = False
            print(" ==> We calculated the wrong parentID ["+str(alinea.parentID)+"] or horizontal ordering ["+str(alinea.horizontal_ordering)+"] for the following alinea:")
            truealineas[index].printalinea()
        index = index + 1
  
    # Done:
    return Answer

def TestTreeStructure_e() -> bool:
    """
    # Unit test for the calculatetree-function of the textsplitter-class.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Begin by creating a textsplitter:
    filename = "TestTreeStructure"
    thetest = textsplitter()
    thetest.set_documentpath("/not/important/here/")
    thetest.set_documentname(filename)
    thetest.set_labelname(filename)
    thetest.set_outputpath("/not/important/either/")
    
    # Next, gather the alineas we want to calculate the tree structure for. This time, we do it without
    # the top-level alinea, so we know for sure that this works too.
    thetest.textalineas = hardcodedalineas_SplitDoc("pdfminer")
    thetest.textalineas.pop(0)
    truealineas = hardcodedalineas_SplitDoc("pdfminer")
    truealineas.pop(0)
    # We call the same function twice, because we do not want python to create 2 
    # pointers to the same object, we really want 2 different objects.
    
    # Then, blind the parentID & horizontal ordering:
    for alinea in thetest.textalineas:
        alinea.parentID = -1
        alinea.horizontal_ordering = -1
    
    # Then, calculate the tree structure:
    thetest.calculatetree()
    
    # Next, change parentID's in true alineas to the situation of the missing top-alinea:
    for alinea in truealineas:
        if (alinea.parentID==0):
            alinea.parentID = -1
        else:
            alinea.parentID = alinea.parentID - 1
    
    # Next, see if we found the correct structure:
    index = 0
    Answer = True
    for alinea in thetest.textalineas:
        if not alinea.compare_samearray(truealineas[index]): # Because in these unit-tests we know we get exactly the correct parentID.
            Answer = False
            print(" ==> We calculated the wrong parentID ["+str(alinea.parentID)+"] or horizontal ordering ["+str(alinea.horizontal_ordering)+"] for the following alinea:")
            truealineas[index].printalinea()
        index = index + 1
  
    # Done:
    return Answer

def TestTreeStructure() -> bool:
    """
    # Collection of unit test for the calculatetree-function of the textsplitter-class.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Declare the answer:
    Answer = True
    
    if not TestTreeStructure_a():
        Answer = False
        print("==> TestTreeStructure_a() failed!")
    
    if not TestTreeStructure_b():
        Answer = False
        print("==> TestTreeStructure_b() failed!")
    
    if not TestTreeStructure_c():
        Answer = False
        print("==> TestTreeStructure_c() failed!")
    
    if not TestTreeStructure_d():
        Answer = False
        print("==> TestTreeStructure_d() failed!")
    
    if not TestTreeStructure_e():
        Answer = False
        print("==> TestTreeStructure_e() failed!")
    
    # Done:
    return Answer
    
if __name__ == '__main__':
    if TestTreeStructure():
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
