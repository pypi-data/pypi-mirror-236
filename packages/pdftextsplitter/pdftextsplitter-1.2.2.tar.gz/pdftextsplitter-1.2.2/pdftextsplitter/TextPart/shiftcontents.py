# Textpart imports:
from .regex_expressions import contains_letter_signing

def shiftcontents_textsplitter(self):
    """
    This function is meant to be called immendiately after breakdown
    and before claculating the tree structure (all member functions
    of textsplitter, just like this one). Some documents can contain letters
    from politicians, which are then signed by their names. Without this function,
    the name of the politician would become a chapter-title with the content
    FOLLOWING their name. This is not correct for signed letters. As such,
    this function will take those situations and shift title/content
    to make sure that the right letters go to the right names.
    
    # Parameters: None (taken from the class).
    # Return: none (stored in the class).
    
    """
    
    # --------------------------------------------------------------------------
    
    # Begin by sorting the array to nativeID (which is the same as their index):
    self.textalineas = sorted(self.textalineas, key=lambda x: x.nativeID, reverse=False)
    
    # Extract the length:
    alinealength = len(self.textalineas)
    
    # Search the alineas for letter signings:
    Letter_Signings = []
    for alinea in self.textalineas:
        if contains_letter_signing(alinea.texttitle):
            Letter_Signings.append(alinea)
    
    # Next, we require that the LAST element of the letter signing has empty content.
    # If the document indeed contains letter signings, then the last signing
    # should always be followed by a new headline or other structural element,
    # leaving the last signing an empty alinea. This is not only a good check to
    # see when it is wise to fiddle with content/title combinations, but it will also
    # ensure that we have space to put the new content in.
    
    # Collect parameters:
    nr_signings = len(Letter_Signings)
    
    # Collect textual content:
    Textual_content = ""
    if (nr_signings>0):
        for textline in Letter_Signings[nr_signings-1].textcontent:
            Textual_content = Textual_content + textline
        
        # Prepare textual content:
        Textual_content = Textual_content.replace("\n","")
        Textual_content = Textual_content.replace(" ","")
        
    else:
        Textual_content = "We found no signings"
        # this will make sure the test does not pass; as should be the case here.
    
    # Make the test. If we do not pass; we will simply not do anything to the content:
    if (Textual_content==""):
        
        # Next, we will loop over the letter-signings in REVERSE order and put in the content
        # that belongs to the nativeID-1 element (provided it exist). We will then delete
        # the content of that element (making room for the next signing; due to reverse-looping).
        for index in range(nr_signings-1,-1,-1):
       
            # Check that we actually can access nativeID-1:
            ThisNativeID = Letter_Signings[index].nativeID
            if (ThisNativeID>0):
                
                # Loop over the textual content:
                textindex = 0
                for textline in self.textalineas[ThisNativeID-1].textcontent:
                    
                    # Insert the textual content of the previous item ABOVE the one of the current signing (so no text is lost):
                    Letter_Signings[index].textcontent.insert(textindex,textline)
                    
                    # Update the textindex:
                    textindex = textindex + 1
                
                # Next, clear out the content of the previous alinea:
                self.textalineas[ThisNativeID-1].textcontent.clear()
                
                # And, due to the reverse-looping: that should do it.
                
                    
        
        
        
        
    
