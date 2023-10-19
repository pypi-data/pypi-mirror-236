def stringmatch(first: str, second: str) -> float:
    """
    This function will calculate how much two strings agree
    with each other on a scale between 0.0 and 1.0. The length of 
    the strings does not need to be equal.
    
    Consider this picture:
            [*********************************]                 Longest string
    [*********]->                             |                 shortest string (start code)
                          <-[*********]->     |                 shortest string (middle of code)
                                          <-[*********]         shortest string (end of code)
    We move the shortest string along the longest one. From a single
    character in agreement to all. Then, for each position of the 
    shortest string, we count the number of equal characters.
    Then, we take the max. agreement over the different position
    of the shortest. Finally, we divide by the total number of characters
    in the shortest string. That is the answer that we calculate.
    So, if the phrases of the shortest string are found (somewhat)
    in the longest string, we get a reasonable agreement.    
    
    # Parameters:
    first: str: first string to compare.
    second: str: second string to compare
    # Return: float: the level of agreement on a scale 0.0-1.0
    """
    
    # ------------------------------------------------------------
    
    # Begin with identifying which string is shorter/longer:
    len1 = len(first)
    len2 = len(second)
    
    shortest = ""
    longest = ""
    minlength = min(len1,len2)
    maxlength = max(len1,len2)
    lendiff = abs(len1-len2)
    
    if (len1<=len2):
        shortest = first
        longest = second
    else:
        shortest = second
        longest = first
    
    # Count number of characters that agree:
    nchar_agree = []
    this_agree = 0
    percentage_agreement = 0.0
    
    # Before anything else: test whether both strings are >0:
    if (minlength>0)and(maxlength>0):

        # Begin with looping over the startposition of the shortest string.
        # It runs from 0 till len1+len2-1 (because there has to be at least a single character of overlap.
        # In this case, the long string starts at index minlength-1 (single overlap).
        for startposition in range(0,minlength+maxlength-1):
        
            # Next, loop over the characters in the shortest string:
            for stringchar in range(0,minlength):
            
                # Then, we must calculate the indices in both strings that we need to compare:
                shortindex = stringchar
                longindex = startposition - minlength + 1 + stringchar
            
                # then, only compare if we can actually use longindex:
                if (longindex>=0)and(longindex<maxlength):
                
                    # Then, compare characters:
                    if (shortest[shortindex].lower()==longest[longindex].lower()):
                    
                        # Count this character:
                        this_agree = this_agree + 1
        
            # Now, once the for-loop over the shortest string is complete, add the
            # number of correct strings to the array:
            nchar_agree.append(this_agree)
        
            # Reset the currect counter:
            this_agree = 0
        
        # Next, after the for-loops: find the max. agreement:
        if (len(nchar_agree)>0): percentage_agreement = max(nchar_agree)/minlength
    
    # Then, return the answer:
    return percentage_agreement
                    
                    
