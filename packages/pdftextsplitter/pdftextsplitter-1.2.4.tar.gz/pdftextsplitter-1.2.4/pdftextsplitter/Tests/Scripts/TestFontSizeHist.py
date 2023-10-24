import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from TextPart code:
sys.path.insert(1, '../../')
from TextPart.textpart import textpart

# Imports from Tools:
sys.path.insert(2, '../Tools/')
from hardcodedfontsizehist import hardcodedfontsizehist
from hardcodedfontsizehist import hardcodedfontsizehist_perline
from hardcodedfontsizehist import hardcodedfontsizedata_perline
from hardcodedfontsizehist import hardcodedfontsizedata_percharacter

# Definition of paths:
inputpath = "../Inputs/"
outputpath = "../Calc_Outputs/"
truthpath = "../True_Outputs/"

# Definition of unit tests:
def TestFontSizeHist() -> bool:
    """
    # Unit test for the fontsizehist-function of the textpart-class.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Begin by creating a textpart:
    thetest = textpart()
    thetest.set_documentpath("/not/important/here/")
    thetest.set_documentname("fontsizehist_unittest")
    thetest.set_labelname("fontsizehist_unittest")
    thetest.set_outputpath(outputpath)
    thetest.set_labelname("SplitDoc pdfminer breakdown test")
    
    # Next, put in hard-coded what we need:
    thetest.fontsize_perline = hardcodedfontsizedata_perline()
    thetest.fontsize_percharacter = hardcodedfontsizedata_percharacter()
    theoutcome_perline = hardcodedfontsizehist_perline()
    theoutcome_percharacter = hardcodedfontsizehist()
    
    # Next, execute the test:
    thetest.fontsizehist()
    
    # Then, verify the outcome:
    Answer = True
    
    if not (len(thetest.fontsizeHist_percharacter)==3):
        Answer = False
        print("thetest.fontsizehist() failed to create a histogram per character at all!")
    else:
        
        # Verify bin contents:
        if not (len(thetest.fontsizeHist_percharacter[0])==len(theoutcome_percharacter[0])):
            Answer = False
            print("thetest.fontsizehist() for characters does not have the correct length ["+str(len(theoutcome_percharacter[0]))+"] for bincontents!")
        else:
            length = len(theoutcome_percharacter[0])
            for k in range(0,length):
                if (abs(thetest.fontsizeHist_percharacter[0][k] - theoutcome_percharacter[0][k])>1e-3):
                    Answer = False
                    print("Bincontents per character at bin ["+str(k)+"] are not equal!")
        
        # Verify bin boundaries:
        if not (len(thetest.fontsizeHist_percharacter[1])==len(theoutcome_percharacter[1])):
            Answer = False
            print("thetest.fontsizehist() for characters does not have the correct length ["+str(len(theoutcome_percharacter[0]))+"] for bin boundaries!")
        else:
            length = len(theoutcome_percharacter[1])
            for k in range(0,length):
                if (abs(thetest.fontsizeHist_percharacter[1][k] - theoutcome_percharacter[1][k])>1e-3):
                    Answer = False
                    print("Bin boundaries per character at bin ["+str(k)+"] are not equal!")
    
    # Next, for lines instead of characters:
    if not (len(thetest.fontsizeHist_perline)==3):
        Answer = False
        print("thetest.fontsizehist() failed to create a histogram per line at all!")
    else:
        
        # Verify bin contents:
        if not (len(thetest.fontsizeHist_perline[0])==len(theoutcome_perline[0])):
            Answer = False
            print("thetest.fontsizehist() for lines does not have the correct length ["+str(len(theoutcome_perline[0]))+"] for bincontents!")
        else:
            length = len(theoutcome_perline[0])
            for k in range(0,length):
                if (abs(thetest.fontsizeHist_perline[0][k] - theoutcome_perline[0][k])>1e-3):
                    Answer = False
                    print("Bincontents per line at bin ["+str(k)+"] are not equal!")
        
        # Verify bin boundaries:
        if not (len(thetest.fontsizeHist_perline[1])==len(theoutcome_perline[1])):
            Answer = False
            print("thetest.fontsizehist() for lines does not have the correct length ["+str(len(theoutcome_perline[0]))+"] for bin boundaries!")
        else:
            length = len(theoutcome_perline[1])
            for k in range(0,length):
                if (abs(thetest.fontsizeHist_perline[1][k] - theoutcome_perline[1][k])>1e-3):
                    Answer = False
                    print("Bin boundaries per line at bin ["+str(k)+"] are not equal!")
  
    # Done:
    return Answer
    
if __name__ == '__main__':
    if TestFontSizeHist():
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
