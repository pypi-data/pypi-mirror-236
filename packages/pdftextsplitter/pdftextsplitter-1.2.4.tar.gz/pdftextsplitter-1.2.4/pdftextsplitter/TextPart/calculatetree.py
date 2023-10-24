# Textpart imports:
from .textalinea import textalinea

def calculatetree_textsplitter(self):
    """
    This function calculates the parentID and horizontal ordering of the 
    textalineas-array in the textsplitter-class. It is meant to be called
    AFTER the breakdown-function, as this function needs a filled
    textalineas-array with calculated cascade levels to work. It calculates
    parentID & horizontal ordering based on the order of the textalineas
    in the array, as this corresponds to the order in which they occur
    in the document.
    
    # Parameters: None; taken from the textsplitter-class.
    # Return: None; stored inside the textalineas.
    """
    
    # ---------------------------------------------------------------------
   
    # As the user may have done different operations in the meantime, begin
    # with sorting the array in native increasing ordering (the order of the document):
    self.textalineas = sorted(self.textalineas, key=lambda x: x.nativeID, reverse=False)
    
    # Begin with calculation of the parentID. This is done by
    # first looping over the array and then, for the current alinea,
    # we loop back up and identify the first previous alinea with 
    # a higher cascadelevel as the parent.
    currentindex = 0
    currentcascadelevel = 0
    foundparent = False
    
    for currentalinea in self.textalineas:
        
        # Extract current cascade level:
        currentcascadelevel = currentalinea.textlevel
        
        # Reset whether we found the parent:
        foundparent = False
        
        # Next, loop back up over the passed alineas:
        if (currentindex>0):
            for k in range(0,currentindex):
                
                # Only continue the loop as long as we did not find the parent,
                # as we need the FIRST parent back up the array.
                if not foundparent:
                
                    # Next, calculate the previous index:
                    previousindex = currentindex - k - 1
                
                    # Then, find the corresponding cascadelevel:
                    previouscascadelevel = self.textalineas[previousindex].textlevel
                
                    # Then, see if this is higher in the document than the current cascadelevel:
                    if (previouscascadelevel<currentcascadelevel):
                    
                        # Then, we have found our parent:
                        foundparent = True
                        currentalinea.parentID = previousindex
              
            # But, what if we did not find any parent up in the tree at all?
            if not foundparent:
                foundparent = True
                currentalinea.parentID = -1
            
        else:
            
            # Then, there is really only one option:
            currentalinea.parentID = -1
                    
        # Finally, update the currentindex:
        currentindex = currentindex + 1
    
    # Close the for-loop for parentID's.
    
    # Next, we must calculate the proper horizontal orderings. We do this by isolating the
    # textalineas that point to the same parentID and have the same cascade-level. Then, they
    # are appointed orderings 0, 1, 2, etc.
    
    # Loop over all alineas:
    nr_alineas = len(self.textalineas)
    currentindex = 0
    currentcascadelevel = 0
    currentparent = -1
    horiz_index = 0
    
    for currentalinea in self.textalineas:
        
        # Test if this one already has a horizontal ordering:
        if (currentalinea.horizontal_ordering<0):
            
            # Then, proceed to calculate it. Begin with extracting current cascadelevels
            # and parentID:
            currentparent = currentalinea.parentID
            currentcascadelevel = currentalinea.textlevel
            
            # Then, appoint it an ordering:
            currentalinea.horizontal_ordering = 0
            horiz_index = 1
            
            # Then, loop over the remaining alineas:
            if (currentindex<(nr_alineas-1)):
                for k in range(currentindex+1,nr_alineas):
                    
                    # Test if this alinea has the same parentID & cascadelevel:
                    if (currentcascadelevel==self.textalineas[k].textlevel)and(currentparent==self.textalineas[k].parentID):
                    
                        # Then, appoint it the same ordering:
                        self.textalineas[k].horizontal_ordering = horiz_index
                        horiz_index = horiz_index + 1
            
        # Next, update the current index:
        currentindex = currentindex + 1
    
    # That should do it.
    
    
        
