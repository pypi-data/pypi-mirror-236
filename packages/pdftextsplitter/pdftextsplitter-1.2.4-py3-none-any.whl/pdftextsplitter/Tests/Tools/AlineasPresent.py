# ATTENTION: Requires an import of textalinea first!!!
def AlineasPresent(first, second) -> bool:
    """
    Function that identifies whether each element in the first list of textalinea-elements
    is present in the second list of textalineas. If this is the case, it returns True, 
    otherwise, it returns False, including printing the elements it could not find.
    
    # Parameters:
    first: list[textalinea]: the list for which every element has to be located.
    second: list[textalinea]: the list where to look for presence.
    # Return: bool: the answer.
    """
    
    # --------------------------------------------------------
    
    # Begin by sorting both arrays in native increasing ordering:
    first = sorted(first, key=lambda x: x.nativeID, reverse=False)
    second = sorted(second, key=lambda x: x.nativeID, reverse=False)    
    
    # Declare an array of boolians for each element in first:
    Compare_Array = []
    Compare_Array_NoParent = []
    firstindex = 0
    
    # loop over all elements in first:
    for firstalinea in first:
        
        # Append the false in the array:
        Compare_Array.append(False)
        Compare_Array_NoParent.append(False)
        
        # Next, loop over all elements in second:
        for secondalinea in second:
            
            # Test for equality:
            if firstalinea.compare(secondalinea):
                
                # Next, we must separately test ParentID's, as those cannot be 
                # reliably tested in textalinea.compare()
                
                # Make an exception if either of them has cascade level 0:
                if (firstalinea.textlevel==0)or(secondalinea.textlevel==0):
                    Compare_Array[firstindex] = True
                else:
                    
                    # then, test if the parentID's point to an existing alinea:
                    if (firstalinea.parentID>=0)and(secondalinea.parentID>=0):
                        
                        # Then, collect the parents:
                        firstparent = first[firstalinea.parentID]
                        secondparent = second[secondalinea.parentID]
                        
                        # then, make a note if comparing the parents does not work:
                        Compare_Array_NoParent[firstindex] = True
                
                        # Then, also compare the parents:
                        if firstparent.compare(secondparent):
                    
                            # Next, comparing nativeID's is meaningless, as those
                            # have only meaning within their own arrays. But we
                            # can compare horizontal orderings:
                            if (firstalinea.horizontal_ordering==secondalinea.horizontal_ordering):
                    
                                # Then, we can indeed state that it worked:
                                Compare_Array[firstindex] = True
                    
                    # We need to add this to be able to unit-test Breakdown:
                    else: 
                        Compare_Array[firstindex] = True
                
        # Now, after closing the for-loop, decide on printing:
        if not Compare_Array[firstindex]:
            print(" ==> ATTENTION!!! we could not locate the TRUE textalinea:")
            if Compare_Array_NoParent[firstindex]:
                print(" ==> Problem is in the PARENT of this alinea!")
            firstalinea.printalinea()
            
        # Increase index:
        firstindex = firstindex + 1
        
    # Close the first for-loop and compose the answer:
    Answer = True
    for test in Compare_Array:
        if (test==False): Answer = False
    
    # Return the answer:
    return Answer
