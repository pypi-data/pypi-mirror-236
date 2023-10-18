import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from TextPart code:
sys.path.insert(1, '../../')
from TextPart.stringmatch import stringmatch

# Definition of unit tests:
def TestStringMatch() -> bool:
    """
    # Unit tests for the script stringmatch.py
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define the answer:
    Answer = True
    
    # Test a certain number of cases:
    if (abs(stringmatch("jahdjhd","jahdjhd")-1.0)>1e-3):
        Answer = False
        print('stringmatch("jahdjhd","jahdjhd") should return 1.0, but returned instead:'+str(stringmatch("jahdjhd","jahdjhd")))
    
    if (abs(stringmatch("jahdjhd","jahdjhdjfkfj")-1.0)>1e-3):
        Answer = False
        print('stringmatch("jahdjhd","jahdjhdjfkfj") should return 1.0, but returned instead:'+str(stringmatch("jahdjhd","jahdjhdjfkfj")))
    
    if (abs(stringmatch("fsfjahdjhd","jahdjhd")-1.0)>1e-3):
        Answer = False
        print('stringmatch("fsfjahdjhd","jahdjhd") should return 1.0, but returned instead:'+str(stringmatch("fsfjahdjhd","jahdjhd")))
    
    if (abs(stringmatch("aaaaaa","bbbb")-0.0)>1e-3):
        Answer = False
        print('stringmatch("aaaaaa","bbbb") should return 0.0, but returned instead:'+str(stringmatch("aaaaaa","bbbb")))
    
    if (abs(stringmatch("aaaaaa","bbba")-0.25)>1e-3):
        Answer = False
        print('stringmatch("aaaaaa","bbba") should return 0.25, but returned instead:'+str(stringmatch("aaaaaa","bbba")))
        
    if (abs(stringmatch("aaaaaa","bbaa")-0.5)>1e-3):
        Answer = False
        print('stringmatch("aaaaaa","bbaa") should return 0.5, but returned instead:'+str(stringmatch("aaaaaa","bbaa")))
    
    if (abs(stringmatch("aaaaaa","baab")-0.5)>1e-3):
        Answer = False
        print('stringmatch("aaaaaa","baab") should return 0.5, but returned instead:'+str(stringmatch("aaaaaa","baab")))
    
    if (abs(stringmatch("aaaaaa","BAAA")-0.75)>1e-3):
        Answer = False
        print('stringmatch("aaaaaa","BAAA") should return 0.75, but returned instead:'+str(stringmatch("aaaaaa","BAAA")))
    
    if (abs(stringmatch("","jahdjhd")-0.0)>1e-3):
        Answer = False
        print('stringmatch("","jahdjhd") should return 0.0, but returned instead:'+str(stringmatch("","jahdjhd")))
        
    if (abs(stringmatch("jahdjhd","")-0.0)>1e-3):
        Answer = False
        print('stringmatch("jahdjhd","") should return 0.0, but returned instead:'+str(stringmatch("jahdjhd","")))
    
    if (abs(stringmatch("","")-0.0)>1e-3):
        Answer = False
        print('stringmatch("","") should return 0.0, but returned instead:'+str(stringmatch("","")))
    
    # Return the answer:
    return Answer

if __name__ == '__main__':
    if TestStringMatch():
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
