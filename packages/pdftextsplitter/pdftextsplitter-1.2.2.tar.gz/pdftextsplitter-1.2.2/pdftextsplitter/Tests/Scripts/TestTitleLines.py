import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from Source code:
sys.path.insert(1, '../../')
from Source.GetTitleLines import GetTitleLines

# Definition of unit tests:
def TestTitleLines_a() -> bool:
    """
    # Unit test for text the script using the GetTitleLines.py script.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    filename="CADouma_DNN_Publication"
    Lines = GetTitleLines(filename)
    
    Answer = False
    if (Lines==[8, 9]): Answer = True
    return Answer

# Definition of unit tests:
def TestTitleLines_b() -> bool:
    """
    # Unit test for text the script using the GetTitleLines.py script.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    filename="fgfghh"
    Lines = GetTitleLines(filename)
    
    Answer = False
    if (len(Lines)>0):
        if (isinstance(Lines[0], int)==True):
            Answer = True
    return Answer

def TestTitleLines_c() -> bool:
    """
    # Unit test for text the script using the GetTitleLines.py script.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    filename="CADouma_Veto_Publication"
    Lines = GetTitleLines(filename)
    
    Answer = False
    if (Lines==[8, 9]): Answer = True
    return Answer

def TestTitleLines_d() -> bool:
    """
    # Unit test for text the script using the GetTitleLines.py script.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    filename="CADouma_BGT_Publication"
    Lines = GetTitleLines(filename)
    
    Answer = False
    if (Lines==[7, 8]): Answer = True
    return Answer

def TestTitleLines_e() -> bool:
    """
    # Unit test for text the script using the GetTitleLines.py script.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    filename="BigTest"
    Lines = GetTitleLines(filename)
    
    Answer = False
    if (Lines==[28, 29, 30, 31]): Answer = True
    return Answer

def TestTitleLines_f() -> bool:
    """
    # Unit test for text the script using the GetTitleLines.py script.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    filename="SplitDoc"
    Lines = GetTitleLines(filename)
    
    Answer = False
    if (Lines==[1, 2]): Answer = True
    return Answer

# Definition of collection:    
def TestTitleLines() -> bool:
    """
    # Collection-function of unit-tests.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    Answer = True
    if (TestTitleLines_a()==False): 
        Answer=False
        print('Test getting the title lines for DNN publication (a)')
    
    if (TestTitleLines_b()==False): 
        Answer=False
        print('Test getting the title lines for some stupid string (b)')
        
    if (TestTitleLines_c()==False): 
        Answer=False
        print('Test getting the title lines for Veto publication (c)')
        
    if (TestTitleLines_d()==False): 
        Answer=False
        print('Test getting the title lines for BGT publication (d)')
        
    if (TestTitleLines_e()==False): 
        Answer=False
        print('Test getting the title lines for BigTest document (e)')
        
    if (TestTitleLines_f()==False): 
        Answer=False
        print('Test getting the title lines for SplitDoc document (f)')
      
    return Answer

if __name__ == '__main__':
    if TestTitleLines():
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
