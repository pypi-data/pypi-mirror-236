class lineregion:
    """
    # This class manages the different whitespaces found in a document between the textlines.
    # Based on the histogram of whitelines-sizes, we identify different
    # lineregions: one for each peak in the histogram. Such a region
    # can then be stored and accessed in this class.
    
    # This approach is similar to the lineregions, but NOT the same.
    # For example, we do not appoint cascade levels to lineregions, as
    # a larger whiteline does not necessarily correspond to a different
    # cascade level. Moreover, whitelines are much more complex than
    # font regions, which is why they have more boolian markings.
    
    """
    
    # -----------------------------------------------------------------
    
    def __init__(self):
        self.left = 0.0         # left boundary of the lineregion.
        self.right = 0.0        # right boundary of the lineregion.
        self.value = 0.0        # the center value of the peak.
        self.frequency = 0.0    # percentage of how often the line occurs.
        self.isregular = False  # If this is true, the region corresponds to the standard whitespaces between body-text lines.
        self.issmall = False    # If this is true, the region corresponds to whitelines smaller than standard body text.
        self.isbig = False      # If this is true, the region corresponds to whitelines larger than standard body text.
        self.iszero = False     # If this is true. the region corresponds to 'zero' whitelines: text elements that are on the same height and, therefore, have no whiteline.
        self.isvalid = True     # If this is false, the region corresponds to negative whitelines; used to mark an invalid computation due to header/footer boundaries.
    
    # get-functions:
    def get_left(self) -> float: return self.left
    def get_right(self) -> float: return self.right
    def get_value(self) -> float: return self.value
    def get_frequency(self) -> float: return self.frequency
    def get_isregular(self) -> bool: return self.isregular
    def get_issmall(self) -> bool: return self.issmall
    def get_isbig(self) -> bool: return self.isbig
    def get_iszero(self) -> bool: return self.iszero
    def get_isvalid(self) -> bool: return self.isvalid

    # set-functions:
    def set_left(self, theinput: float): self.left = theinput
    def set_right(self, theinput: float): self.right = theinput
    def set_value(self, theinput: float): self.value = theinput
    def set_frequency(self, theinput: float): self.frequency = theinput
    def set_isregular(self, theinput: bool): self.isregular = theinput
    def set_issmall(self, theinput: bool): self.issmall = theinput
    def set_isbig(self, theinput: bool): self.isbig = theinput
    def set_iszero(self, theinput: bool): self.iszero = theinput
    def set_isvalid(self, theinput: bool): self.isvalid = theinput
    
    # Class functionality:
    def isinregion(self, thisline: float) -> bool:
        """
        Decision if a whiteline is in this region or not.
        # parameters: thisline (float): the whitespace you would like to check.
        # Return: bool: whether it is in the region or not.
        """
        return (thisline>self.left)and(thisline<=self.right)
        # NOTE: we include the right boundary and exclude the lower boundary.
        # This will prevent double-selection, as only a single region
        # can be appointed to a certain value.
    
    def printregion(self):
        """
        Function to give terminal output of thsi object.
        # Parameters: None, # Return: None (terminal)
        """
        print(self.exportregion())
    
    def exportregion(self) -> str:
        """
        Function to give descriptive str-output on this object.
        Parameters & Return: that str.
        """
        return "L="+str(self.left)+" | Val="+str(self.value)+" | R="+str(self.right)+" | Freq="+str(self.frequency)+" | Reg="+str(self.isregular)+" | small="+str(self.issmall)+" | BIG="+str(self.isbig)+" | zero="+str(self.iszero)+" | valid="+str(self.isvalid)
    
    def compare(self, other) -> bool:
        """
        Function that identifies whether two lineregions are the same or not.
        # parameters: self & other (lineregion): the two objects to compare.
        # Returns: bool: whether they are the same or not.
        """
        # Simply compare all content:
        issame = True
        if abs(self.left - other.left)>1e-3: issame = False
        if abs(self.right - other.right)>1e-3: issame = False
        if abs(self.value - other.value)>1e-3: issame = False
        if abs(self.frequency - other.frequency)>1e-3: issame = False
        if not (self.isregular==other.isregular): issame = False
        if not (self.issmall==other.issmall): issame = False
        if not (self.isbig==other.isbig): issame = False
        if not (self.iszero==other.iszero): issame = False
        if not (self.isvalid==other.isvalid): issame = False
        return issame
    
    def printcode(self):
        """
        Function meant to easily generate code for storing hard-coded lineregions
        in case you need them for testing purposes.
        # Parameters: None, # Return: None.
        """
        print("")
        print("    thisregion = lineregion()")
        print("    thisregion.set_left("+str(self.left)+")")
        print("    thisregion.set_right("+str(self.right)+")")
        print("    thisregion.set_value("+str(self.value)+")")
        print("    thisregion.set_frequency("+str(self.frequency)+")")
        print("    thisregion.set_isregular("+str(self.isregular)+")")
        print("    thisregion.set_issmall("+str(self.issmall)+")")
        print("    thisregion.set_isbig("+str(self.isbig)+")")
        print("    thisregion.set_iszero("+str(self.iszero)+")")
        print("    thisregion.set_isvalid("+str(self.isvalid)+")")
        print("    trueregions.append(thisregion)")
        
def findlineregions_textpart(self):
    """
    This function locates the different peaks in the histogram and stores them
    as lineregion-objects. It does not appoint cascadelevels, as those are hard to
    predict based on whitespaces. It does provide all the different boolian markers.
    
    # Parameters: None (taken from textpart-class).
    # Return: None (stored in textpart-class).
    
    """
    
    # -----------------------------------------------------
    
    # Begin by clearing the array of lineregions:
    self.lineregions.clear()
    
    # Check that the histogram has the proper size:
    Histogramcheck = True
    if (self.histogramsize<1): Histogramcheck = False
    if not (len(self.whitespaceHist_perline)==3): Histogramcheck = False
    else:
        if not (len(self.whitespaceHist_perline[0])==self.histogramsize): Histogramcheck = False
        if not (len(self.whitespaceHist_perline[1])==self.histogramsize+1): Histogramcheck = False

    if Histogramcheck:
    
        # Next, loop over the histogram of fontsize-allcharacters to identify the peaks:
        bincenter = 0.0
        bincontent = 0.0
        xmin = min(self.whitespaceHist_perline[1])
        xmax = max(self.whitespaceHist_perline[1])
        nbins = self.histogramsize
        binsize = (xmax-xmin)/nbins
        
        # In the case that we have >=3 bins:
        if (nbins>2):
    
            # loop over inner bins:
            for k in range(1,nbins-1):
                bincenter = self.whitespaceHist_perline[1][k] + 0.5*binsize
                bincontent = self.whitespaceHist_perline[0][k]
            
                # Identify if this is a peak:
                if (bincontent>=self.whitespaceHist_perline[0][k+1])and(bincontent>self.whitespaceHist_perline[0][k-1]): 
                    newregion = lineregion()
                    newregion.set_value(bincenter)
                    self.lineregions.append(newregion)
            
            # Deal with the left-most bin separately:
            k=0
            bincenter = self.whitespaceHist_perline[1][k] + 0.5*binsize
            bincontent = self.whitespaceHist_perline[0][k]
            
            if (bincontent>self.whitespaceHist_perline[0][k+1]):
                newregion = lineregion()
                newregion.set_value(bincenter)
                self.lineregions.append(newregion)
            
            # Deal with the right-most bin separately:
            k=nbins-1
            bincenter = self.whitespaceHist_perline[1][k] + 0.5*binsize
            bincontent = self.whitespaceHist_perline[0][k]
            
            if (bincontent>self.whitespaceHist_perline[0][k-1]):
                newregion = lineregion()
                newregion.set_value(bincenter)
                self.lineregions.append(newregion)
        
        # Next, deal with the nbins=2 case:
        elif (nbins==2):
            leftbincenter = self.whitespaceHist_perline[1][0]
            rightbincenter = self.whitespaceHist_perline[1][1]
            leftbincontent = self.whitespaceHist_perline[0][0]
            rightbincontent = self.whitespaceHist_perline[0][1]
            
            newregion = lineregion()
            if (rightbincontent>leftbincontent): newregion.set_value(rightbincenter + 0.5*binsize)
            else: newregion.set_value(leftbincenter + 0.5*binsize)
            self.lineregions.append(newregion)
            
        # Next, deal with the nbins=1 case:
        elif (nbins==1):
            bincenter = self.whitespaceHist_perline[1][0] + 0.5*binsize
            bincontent = self.whitespaceHist_perline[0][0]
            
            newregion = lineregion()
            newregion.set_value(bincenter)
            self.lineregions.append(newregion)
            
        # NOTE: No else here: nbins<1 is literally impossible, due to the Histogramcheck.
    
        # Next, we must calculate the other properties of the lineregions:
        if (len(self.lineregions)==1):
            
            # This is easy:
            self.lineregions[0].set_left(xmin)
            self.lineregions[0].set_right(1e5)
            self.lineregions[0].set_frequency(1.0)
            self.lineregions[0].set_isregular(True)
            
            # Adapt for the 2-bin case:
            if (nbins==2):
                if (self.lineregions[0].get_value()<self.whitespaceHist_perline[1][1]):
                    self.lineregions[0].set_frequency(self.whitespaceHist_perline[0][0]/(self.whitespaceHist_perline[0][0]+self.whitespaceHist_perline[0][1]))
                    self.lineregions[0].set_left(self.whitespaceHist_perline[1][0])
                else:
                    self.lineregions[0].set_frequency(self.whitespaceHist_perline[0][1]/(self.whitespaceHist_perline[0][0]+self.whitespaceHist_perline[0][1]))
                    self.lineregions[0].set_left(self.whitespaceHist_perline[1][1])
            
            # Extend the left of the smallest-whiteline and the right of the largest-whiteline:
            self.lineregions[0].set_left(self.lineregions[0].get_left()-binsize)
            
            # Provide markings:
            self.lineregions[0].isregular = True
            self.lineregions[0].isbig = False
            self.lineregions[0].issmall = False
            if (self.lineregions[0].isinregion(0.0)==True): self.lineregions[0].iszero = True
            else: self.lineregions[0].iszero = False
            if (self.lineregions[0].get_right()<0.0): self.lineregions[0].isvalid = False
            else:  self.lineregions[0].isvalid = True
            
        elif (len(self.lineregions)>1):
            
            # Then we must first sort them according to increasing line spaces:
            self.lineregions = sorted(self.lineregions, key=lambda x: x.value, reverse=False)
            
            # Then, loop over them to calculate the boundaries:
            for k in range(0,len(self.lineregions)):
                
                if (k==0): self.lineregions[k].set_left(xmin)
                else: self.lineregions[k].set_left(0.5*(self.lineregions[k].get_value()+self.lineregions[k-1].get_value()))
                
                if (k==len(self.lineregions)-1): self.lineregions[k].set_right(xmax)
                else: self.lineregions[k].set_right(0.5*(self.lineregions[k].get_value()+self.lineregions[k+1].get_value()))
        
            # Extend the left of the smallest-whiteline and the right of the largest-whiteline:
            self.lineregions = sorted(self.lineregions, key=lambda x: x.left, reverse=False)
            self.lineregions[0].set_left(self.lineregions[0].get_left()-binsize)
            
            self.lineregions = sorted(self.lineregions, key=lambda x: x.right, reverse=True)
            self.lineregions[0].set_right(self.lineregions[0].get_right()+binsize)
            
            # Next, we must calculate the frequencies:
            totalfreq = sum(self.whitespaceHist_perline[0])
        
            # and this requires looping over them again:
            for k in range(0,nbins):
                bincenter = self.whitespaceHist_perline[1][k] + 0.5*binsize
                bincontent = self.whitespaceHist_perline[0][k]
            
                for n in range(0,len(self.lineregions)):
                    if (self.lineregions[n].isinregion(bincenter)):
                        self.lineregions[n].set_frequency(self.lineregions[n].get_frequency() + bincontent/totalfreq)
        
            # Next, we must provide the boolian markings. For the regular mark, we sort according to decending frequency:
            self.lineregions = sorted(self.lineregions, key=lambda x: x.frequency, reverse=True)
            self.lineregions[0].set_isregular(True)
            
            # Then, for the other markings, sort the array according to increasing whitelines:
            self.lineregions = sorted(self.lineregions, key=lambda x: x.value, reverse=False)
            
            # Next, find the index of the regular element:
            index = 0
            for k in range(0,len(self.lineregions)):
                if (self.lineregions[k].get_isregular()==True):
                    index = k
                    
            # Now, the idea is that, in situations where we get a lot of lineregions, that regions
            # that do not differ enough from the regular region, get absorbed into the regular region:
            if (index<(len(self.lineregions)-1)):
                for k in range(len(self.lineregions)-1,index,-1): # NOTE: Reversed-looping so deleting an element is no problem. start at len-1 & loop TILL index, not include index.
                    if (self.lineregions[k].get_left()<1.05*self.lineregions[index].get_value()):
                        # Extend the right boundary of the previous region:
                        self.lineregions[k-1].set_right(self.lineregions[k].get_right())
                        self.lineregions[k-1].set_frequency(self.lineregions[k-1].get_frequency() + self.lineregions[k].get_frequency())
                        # Delete the current region:
                        self.lineregions.pop(k)
            
            # Now, do the same for the regions on the smaller side of the regular one:
            if (index>0):
                Indexes_to_delete = []
                for k in range(0,index): # NOTE: normal-looping here!
                    if (self.lineregions[k].get_right()>0.961*self.lineregions[index].get_value()):
                        # Extend the left boundary of the next region:
                        self.lineregions[k+1].set_left(self.lineregions[k].get_left())
                        self.lineregions[k+1].set_frequency(self.lineregions[k+1].get_frequency() + self.lineregions[k].get_frequency())
                        # Mark the current region:
                        Indexes_to_delete.append(k)
                
                # Next, delete them using reversed-looping:
                for k in range(len(Indexes_to_delete)-1,-1,-1):
                    self.lineregions.pop(Indexes_to_delete[k])
            
            # Now, loop over the array to set the markings:
            for region in self.lineregions:
                
                # Valid-marking:
                if (region.get_right()<0.0): region.isvalid = False
                else: region.isvalid = True
                
                # Zero-markings:
                if (region.isinregion(0.0)==True): region.iszero = True
                else: region.iszero = False
                
                # Small markings:
                if (region.get_right()<self.lineregions[index].get_value()): region.issmall = True
                else: region.issmall = False
                
                # Big markings (account for fluctuations):
                if (region.get_left()>self.lineregions[index].get_value()): region.isbig = True
                else: region.isbig = False
            
            # Finally, because some lineregions can extend to very large numbers, extend the right boundary:
            self.lineregions[len(self.lineregions)-1].set_right(1e5)
            
            # Done.       

def selectlineregion_textpart(self, whiteline: float) -> lineregion:
    """
    Once textpart.lineregions has been filled by calling the above findlineregions-function,
    this function can be used to select the lineregion to which a given whiteline belongs.
    
    # Parameters:
    whiteline (float): the whiteline you would like to classify
    # Returns: lineregion, the element from textpart.lineregions the whiteline belongs to.
    """
    
    # ------------------------------------------------------------------------------------
    
    # Begin by sorting the array according to increasing whitelines:
    self.lineregions = sorted(self.lineregions, key=lambda x: x.value, reverse=False)
    
    # Next, loop through the array and attempt to identify the proper region:
    index = 0
    theindex = -1
    for region in self.lineregions:
        if region.isinregion(whiteline):
            theindex = index
        index += 1
    
    # If we identified a region, we are done:
    if (theindex>=0): return self.lineregions[theindex]
    else:
        
        # Then no proper region exists, so then we have to create one:
        newregion = lineregion()
        newregion.set_left(0.0)
        newregion.set_right(10000.0)
        newregion.set_value(whiteline)
        newregion.set_frequency(-1.0) # NOTE: to identify that this is not an answer we would like to give!
        newregion.set_isregular(False)
        newregion.set_isbig(False)
        newregion.set_issmall(False)
        newregion.set_iszero(False)
        newregion.set_isvalid(False)
        
        # See if the problem is that no lineregion exist:
        if (len(self.lineregions)==0): return newregion
        else:
            
            # Then, the whiteline is either too small, or too large:
            if (whiteline<=self.lineregions[0].get_left()):
                newregion.set_right(self.lineregions[0].get_left())
                newregion.set_left(whiteline - abs(whiteline - newregion.get_right()))
                return newregion
            elif (whiteline>=self.lineregions[len(self.lineregions)-1].get_right()):
                newregion.set_left(self.lineregions[len(self.lineregions)-1].get_right())
                newregion.set_right(whiteline + abs(whiteline - newregion.get_left()))
                return newregion
            else:
                
                # Then there is a bug in the code, this situation should not exist!
                newregion.set_frequency(-2.0)
                return newregion
            
                # Done.

def findregularlineregion_textpart(self) -> lineregion:
    """
    Once textpart.lineregions has been filled by calling the above findlineregions-function,
    this function can be used to identify the lineregion that is marked as regular (meaning 
    that it is the standard distance between lines of body-text). 
    This marking is done inside findlineregions_textpart and should be unique.
    
    # Parameters: None
    # Returns: lineregion, the element from textpart.lineregion that is marked as regular:
    """
    
    # ------------------------------------------------------------------------------------
    
    # Begin by sorting the array according to decreasing whitelines:
    self.lineregions = sorted(self.lineregions, key=lambda x: x.value, reverse=True)
    # This will ensure that if, by accident, we find multiple marked regions, we
    # will return the smallest whiteline with a mark.
    
    # Next, do the looping:
    index = 0
    theindex = -1
    for region in self.lineregions:
        if region.get_isregular():
            theindex = index
        index += 1
    
    # If we identified a region, we are done:
    if (theindex>=0): return self.lineregions[theindex]
    else:
        
        # Then, no proper region exists, so then we have to create one:
        newregion = lineregion()
        newregion.set_left(0.001)
        newregion.set_right(10000.0)
        newregion.set_value(10.0)
        newregion.set_frequency(-1.0) # NOTE: to identify that this is not an answer we would like to give!
        newregion.set_isregular(False)
        newregion.set_isbig(False)
        newregion.set_issmall(False)
        newregion.set_iszero(False)
        newregion.set_isvalid(False)
        return newregion
    
        # Done.
    
def whiteline_isregular_textpart(self, whiteline: float) -> bool:
    """
    Once textpart.lineregions has been filled by calling the above findlineregions-function,
    this function can be used to decide whether a given whiteline falls inside a certain
    category, like zero, small, invalid, regular or big.
    
    This function returns true if the whiteline is in the regularregion.
    
    # Parameters:
    whiteline (float): the whiteline you would like to classify
    # Returns: bool, the answer to the above question.
    """
    
    # ------------------------------------------------------------------------------------
    
    # Select the current region:
    currentregion = self.selectlineregion(whiteline)

    # Take the test:
    Answer = True
    if (currentregion.get_isvalid()==False): Answer = False
    if (currentregion.get_iszero()==True): Answer = False
    if (currentregion.get_issmall()==True): Answer = False
    if (currentregion.get_isregular()==False): Answer = False
    if (currentregion.get_isbig()==True): Answer = False
    
    # Done.
    return Answer

def whiteline_issmall_textpart(self, whiteline: float) -> bool:
    """
    Once textpart.lineregions has been filled by calling the above findlineregions-function,
    this function can be used to decide whether a given whiteline falls inside a certain
    category, like zero, small, invalid, regular or big.
    
    This function returns true if the whiteline is in a small positive region.
    
    # Parameters:
    whiteline (float): the whiteline you would like to classify
    # Returns: bool, the answer to the above question.
    """
    
    # ------------------------------------------------------------------------------------
    
    # Select the current region:
    currentregion = self.selectlineregion(whiteline)

    # Take the test:
    Answer = True
    if (currentregion.get_isvalid()==False): Answer = False
    if (currentregion.get_iszero()==True): Answer = False
    if (currentregion.get_issmall()==False): Answer = False
    if (currentregion.get_isregular()==True): Answer = False
    if (currentregion.get_isbig()==True): Answer = False
    
    # Done.
    return Answer

def whiteline_isbig_textpart(self, whiteline: float) -> bool:
    """
    Once textpart.lineregions has been filled by calling the above findlineregions-function,
    this function can be used to decide whether a given whiteline falls inside a certain
    category, like zero, small, invalid, regular or big.
    
    This function returns true if the whiteline is in a big region.
    
    # Parameters:
    whiteline (float): the whiteline you would like to classify
    # Returns: bool, the answer to the above question.
    """
    
    # ------------------------------------------------------------------------------------
    
    # Select the current region:
    currentregion = self.selectlineregion(whiteline)

    # Take the test:
    Answer = True
    if (currentregion.get_isvalid()==False): Answer = False
    if (currentregion.get_iszero()==True): Answer = False
    if (currentregion.get_issmall()==True): Answer = False
    if (currentregion.get_isregular()==True): Answer = False
    if (currentregion.get_isbig()==False): Answer = False
    
    # Done.
    return Answer

def whiteline_iszero_textpart(self, whiteline: float) -> bool:
    """
    Once textpart.lineregions has been filled by calling the above findlineregions-function,
    this function can be used to decide whether a given whiteline falls inside a certain
    category, like zero, small, invalid, regular or big.
    
    This function returns true if the whiteline is in a zero region.
    
    # Parameters:
    whiteline (float): the whiteline you would like to classify
    # Returns: bool, the answer to the above question.
    """
    
    # ------------------------------------------------------------------------------------
    
    # Select the current region:
    currentregion = self.selectlineregion(whiteline)

    # Take the test:
    Answer = True
    if (currentregion.get_isvalid()==False): Answer = False
    if (currentregion.get_iszero()==False): Answer = False
    if (currentregion.get_issmall()==False): Answer = False
    if (currentregion.get_isregular()==True): Answer = False
    if (currentregion.get_isbig()==True): Answer = False
    
    # Done.
    return Answer

def whiteline_isvalid_textpart(self, whiteline: float) -> bool:
    """
    Once textpart.lineregions has been filled by calling the above findlineregions-function,
    this function can be used to decide whether a given whiteline falls inside a certain
    category, like zero, small, invalid, regular or big.
    
    This function returns true if the whiteline is in an valid region.
    
    # Parameters:
    whiteline (float): the whiteline you would like to classify
    # Returns: bool, the answer to the above question.
    """
    
    # ------------------------------------------------------------------------------------
    
    # Select the current region:
    currentregion = self.selectlineregion(whiteline)

    # Return the answer:
    return currentregion.get_isvalid()

def whiteline_smallerthenregular_textpart(self, whiteline: float) -> bool:
    """
    Once textpart.lineregions has been filled by calling the above findlineregions-function,
    this function can be used to decide whether a given whiteline falls inside a certain
    category, like zero, small, invalid, regular or big.
    
    This function returns true if the whiteline is a region below the regular one.
    
    # Parameters:
    whiteline (float): the whiteline you would like to classify
    # Returns: bool, the answer to the above question.
    """
    
    # ------------------------------------------------------------------------------------
    
    # Select the current region:
    currentregion = self.selectlineregion(whiteline)
    
    # Find the regularregion:
    regularregion = self.findregularlineregion()
    
    # See if the center values have the proper hierachy:
    if (currentregion.get_value()<regularregion.get_value()): return True
    else: return False
