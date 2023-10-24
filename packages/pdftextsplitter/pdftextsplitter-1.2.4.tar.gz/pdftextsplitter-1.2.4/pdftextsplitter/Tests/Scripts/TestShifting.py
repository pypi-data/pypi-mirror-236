import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from TextPart code:
sys.path.insert(1, '../../')
from TextPart.textsplitter import textsplitter
from TextPart.textalinea import textalinea

# Imports from Tools:
sys.path.insert(2, '../Tools/')
from AlineasPresent import AlineasPresent
from hardconedalineas_shifting import hardcodedalineas_Signings_Correct
from hardconedalineas_shifting import hardcodedalineas_Signings_Wrong
from hardcodedalineas import hardcodedalineas_SplitDoc

# Definition of paths:
inputpath = "../Inputs/"
outputpath = "../Calc_Outputs/"
truthpath = "../True_Outputs/"

# Definition of unit tests:
def TestShifting_a() -> bool:
    """
    # Unit test for the shiftcontent-function of the textsplitter-class.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Begin by creating a textsplitter:
    filename = "TestShifting"
    thetest = textsplitter()
    thetest.set_documentpath("/not/important/here/")
    thetest.set_documentname(filename)
    thetest.set_labelname(filename)
    thetest.set_outputpath("/not/important/here/")
    thetest.set_labelname("TestShifting")
    
    # Next, put in the alineas hardcoded:
    thetest.textalineas = hardcodedalineas_Signings_Wrong()
    
    # Execute the shift:
    thetest.shiftcontents()
    
    # Then, compare to what it should be:
    correctalineas = hardcodedalineas_Signings_Correct()
    Answer = AlineasPresent(correctalineas,thetest.textalineas)
    
    # Check whether we have the correct number of alineas:
    if not (len(correctalineas)==len(thetest.textalineas)):
        Answer = False
        print("The code found some additional structure-elements that were not supposed to be found!")
  
    # Done:
    return Answer

# Definition of unit tests:
def TestShifting_b() -> bool:
    """
    # Unit test for the shiftcontent-function of the textsplitter-class.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Begin by creating a textsplitter:
    filename = "TestShifting"
    thetest = textsplitter()
    thetest.set_documentpath("/not/important/here/")
    thetest.set_documentname(filename)
    thetest.set_labelname(filename)
    thetest.set_outputpath("/not/important/here/")
    thetest.set_labelname("TestShifting")
    
    # Next, put in the alineas hardcoded:
    thetest.textalineas = hardcodedalineas_SplitDoc("pdfminer")
    
    # Execute the shift (which, for these alineas, should not do anything!)
    thetest.shiftcontents()
    
    # Then, compare to what it should be:
    correctalineas = hardcodedalineas_SplitDoc("pdfminer")
    Answer = AlineasPresent(correctalineas,thetest.textalineas)
    
    # Check whether we have the correct number of alineas:
    if not (len(correctalineas)==len(thetest.textalineas)):
        Answer = False
        print("The code found some additional structure-elements that were not supposed to be found!")
  
    # Done:
    return Answer
    
# Definition of collection:
def TestShifting() -> bool:
    """
    # Collection-function of unit-tests.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: Christiaan Douma
    """
    
    # Declare the answer:
    Answer = True
    
    # Go over the cases:
    if not TestShifting_a():
        Answer = False
        print('TestShifting_a() failed!')
    if not TestShifting_b():
        Answer = False
        print('TestShifting_b() failed!')
    
    # Return the answer:
    return Answer

if __name__ == '__main__':
    if TestShifting():
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
