import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from TextPart code:
sys.path.insert(1, '../../')
from TextPart.textpart import textpart

# Imports from Tools:
sys.path.insert(2, '../Tools/')
from hardcodedwhitelinehist import hardcodedwhitelinehist_LineTest1
from hardcodedwhitelinehist import hardcodedwhitelinedata_LineTest1

# Definition of paths:
inputpath = "../Inputs/"
outputpath = "../Calc_Outputs/"
truthpath = "../True_Outputs/"

# Definition of unit tests:
def TestWhiteLineHist() -> bool:
    """
    # Unit test for the whitelinehist-function of the textpart-class.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Begin by creating a textpart:
    thetest = textpart()
    thetest.set_documentpath("/not/important/here/")
    thetest.set_documentname("whitelinehist_unittest")
    thetest.set_labelname("whitelinehist_unittest")
    thetest.set_outputpath(outputpath)
    thetest.set_labelname("LineTest1 pdfminer breakdown test")
    
    # Next, put in hard-coded what we need:
    thetest.positioncontent = hardcodedwhitelinedata_LineTest1()
    theoutcome = hardcodedwhitelinehist_LineTest1()
    thetest.headerboundary = 1000.0 # Approprioate for this unit-test & LineTest1.pdf/pdfminer
    thetest.footerboundary = 55.0   # Approprioate for this unit-test & LineTest1.pdf/pdfminer
    
    # Next, execute the test:
    thetest.whitelinehist()
    
    # Then, verify the outcome:
    Answer = True
    if not (len(thetest.whitespaceHist_perline)==3):
        Answer = False
        print("thetest.whitelinehist() failed to create a histogram at all!")
    else:
        
        # Verify bin contents:
        if not (len(thetest.whitespaceHist_perline[0])==len(theoutcome[0])):
            Answer = False
            print("thetest.whitelinehist() does not have the correct length ["+str(len(theoutcome[0]))+"] for bincontents!")
        else:
            length = len(theoutcome[0])
            for k in range(0,length):
                if (abs(thetest.whitespaceHist_perline[0][k] - theoutcome[0][k])>1e-3):
                    Answer = False
                    print("Bincontents at bin ["+str(k)+"] are not equal!")
        
        # Verify bin boundaries:
        if not (len(thetest.whitespaceHist_perline[1])==len(theoutcome[1])):
            Answer = False
            print("thetest.whitelinehist() does not have the correct length ["+str(len(theoutcome[0]))+"] for bin boundaries!")
        else:
            length = len(theoutcome[1])
            for k in range(0,length):
                if (abs(thetest.whitespaceHist_perline[1][k] - theoutcome[1][k])>1e-3):
                    Answer = False
                    print("Bin boundaries at bin ["+str(k)+"] are not equal!")
  
    # Done:
    return Answer
    
if __name__ == '__main__':
    if TestWhiteLineHist():
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
