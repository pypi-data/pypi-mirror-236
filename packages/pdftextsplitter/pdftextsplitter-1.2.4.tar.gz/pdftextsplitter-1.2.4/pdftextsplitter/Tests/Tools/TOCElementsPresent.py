import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from TextPart code:
sys.path.insert(1, '../../')
from TextPart.textalinea import textalinea
from TextPart.read_native_toc import Native_TOC_Element

# Import from fellow tools:
from CompareTexts import CompareTexts

def TOCElementsPresent(TOClist: list[Native_TOC_Element], Alinealist: list[textalinea]) -> bool:
    """
    Function that identifies whether each element in TOClist is present in the second list of textalineas. 
    If this is the case, it returns True, otherwise, it returns False.
    
    # Parameters:
    TOClist: list[Native_TOC_Element]: the list for which every element has to be located.
    Alinealist: list[textalinea]: the list where to look for presence.
    # Return: bool: the answer.
    """
    
    # --------------------------------------------------------
    
    # Declare an array of boolians for each element in TOClist:
    Compare_Array = []
    firstindex = 0
    
    # loop over all elements in TOClist:
    for TOCelement in TOClist:
        
        # Append the false in the array:
        Compare_Array.append(False)
        max_ratio = 0.0
        alineaindex = -1
        secondindex = 0
        
        # Next, loop over all elements in Alinealist:
        for alinea in Alinealist:
            
            # Set up what we need:
            TheTest = True
            compare_ratio = CompareTexts(TOCelement.title,alinea.texttitle)
            if (compare_ratio>max_ratio): 
                max_ratio = compare_ratio
                alineaindex = secondindex
            
            # Test for equality:
            if (compare_ratio<90.0): TheTest = False
            if not (TOCelement.cascadelevel==alinea.textlevel): TheTest = False
            
            # Update the array if we found at least a single match:
            if TheTest:
                Compare_Array[firstindex] = True
                
            # Update index:
            secondindex = secondindex + 1
        
        # Now, if after looping through the full Alinealist, we still did not
        # find a match, print the outcome:
        if not Compare_Array[firstindex]:
            print(" ==> ATTENTION!!! we could not locate the TOC-element:")
            TOCelement.print_TOC_element()
            if (alineaindex>-1):
                print(" ==> Best match we found (fuzz-ratio = " + str(max_ratio) + "):")
                print(Alinealist[alineaindex].texttitle + " LEVEL=" + str(Alinealist[alineaindex].textlevel))
                print("\n")
            else:
                print(" ==> We could not find a best-match. Fuzz-ratio is always 0.\n")
            
        # Increase index:
        firstindex = firstindex + 1
        
    # Close the first for-loop and compose the answer:
    Answer = True
    for test in Compare_Array:
        if (test==False): Answer = False
    
    # Return the answer:
    return Answer
