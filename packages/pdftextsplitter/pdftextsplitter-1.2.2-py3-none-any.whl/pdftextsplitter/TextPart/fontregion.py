class fontregion:
    """
    # This class manages the different font sizes found in a document.
    # Based on the histogram of font-sizes, we identify different
    # font regions: one for each peak in the histogram. Such a region
    # can then be stored and accessed in this class.
    """
    
    # -----------------------------------------------------------------
    
    def __init__(self):
        self.left = 0.0         # left boundary of the font region.
        self.right = 0.0        # right boundary of the font region.
        self.value = 0.0        # the center value of the peak.
        self.frequency = 0.0 # percentage of how often the font occurs.
        self.cascadelevel = 0   # Document cascade level that belongs to this region (chapter, section, etc.)
        self.isregular = False  # If this is true, the region corresponds to body-tekst.
    
    # get-functions:
    def get_left(self) -> float: return self.left
    def get_right(self) -> float: return self.right
    def get_value(self) -> float: return self.value
    def get_frequency(self) -> float: return self.frequency
    def get_cascadelevel(self) -> int: return self.cascadelevel
    def get_isregular(self) -> bool: return self.isregular

    # set-functions:
    def set_left(self, theinput: float): self.left = theinput
    def set_right(self, theinput: float): self.right = theinput
    def set_value(self, theinput: float): self.value = theinput
    def set_frequency(self, theinput: float): self.frequency = theinput
    def set_cascadelevel(self, theinput: int): self.cascadelevel = theinput
    def set_isregular(self, theinput: bool): self.isregular = theinput
    
    # Class functionality:
    def isinregion(self, thisfont: float) -> bool:
        """
        Decision if a font is in this region or not.
        # parameters: thisfont (float): the fontsize you would like to check.
        # Return: bool: whether it is in the region or not.
        """
        return (thisfont>self.left)and(thisfont<=self.right)
        # NOTE: we include the right boundary and exclude the lower boundary.
        # This will prevent double-selection, as only a single region
        # can be appointed to a certain value, but it does fix the issue
        # with that the largest font falls outside the largest region.
    
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
        return "Left="+str(self.left)+" | Value="+str(self.value)+" | Right="+str(self.right)+" | Freq="+str(self.frequency)+" | Cascade="+str(self.cascadelevel)+" | Regular="+str(self.isregular)
    
    def compare(self, other) -> bool:
        """
        Function that identifies whether two fontregions are the same or not.
        # parameters: self & other (fontregion): the two objects to compare.
        # Returns: bool: whether they are the same or not.
        """
        # Simply compare all content:
        issame = True
        if abs(self.left - other.left)>1e-3: issame = False
        if abs(self.right - other.right)>1e-3: issame = False
        if abs(self.value - other.value)>1e-3: issame = False
        if abs(self.frequency - other.frequency)>1e-3: issame = False
        if not (self.cascadelevel==other.cascadelevel): issame = False
        if not (self.isregular==other.isregular): issame = False
        return issame
    
    def printcode(self):
        """
        Function meant to easily generate code for storing hard-coded fontregions
        in case you need them for testing purposes.
        # Parameters: None, # Return: None.
        """
        print("")
        print("    thisregion = fontregion()")
        print("    thisregion.set_left("+str(self.left)+")")
        print("    thisregion.set_right("+str(self.right)+")")
        print("    thisregion.set_value("+str(self.value)+")")
        print("    thisregion.set_frequency("+str(self.frequency)+")")
        print("    thisregion.set_cascadelevel("+str(self.cascadelevel)+")")
        print("    thisregion.set_isregular("+str(self.isregular)+")")
        print("    trueregions.append(thisregion)")
        
def findfontregions_textpart(self):
    """
    This function locates the different peaks in the histogram and stores them
    as fontregion-objects. Based on the peak positions and heights, it also
    appoints cascade levels.
    
    # Parameters: None (taken from textpart-class).
    # Return: None (stored in textpart-class).
    
    """
    
    # -----------------------------------------------------
    
    # Begin by clearing the array of fontregions:
    self.fontregions.clear()
    
    # Check that the histogram has the proper size:
    Histogramcheck = True
    if (self.histogramsize<1): Histogramcheck = False
    if not (len(self.fontsizeHist_percharacter)==3): Histogramcheck = False
    else:
        if not (len(self.fontsizeHist_percharacter[0])==self.histogramsize): Histogramcheck = False
        if not (len(self.fontsizeHist_percharacter[1])==self.histogramsize+1): Histogramcheck = False

    if Histogramcheck:
    
        # Next, loop over the histogram of fontsize-allcharacters to identify the peaks:
        bincenter = 0.0
        bincontent = 0.0
        xmin = min(self.fontsizeHist_percharacter[1])
        xmax = max(self.fontsizeHist_percharacter[1])
        nbins = self.histogramsize
        binsize = (xmax-xmin)/nbins
        
        # In the case that we have >=3 bins:
        if (nbins>2):
    
            # loop over inner bins:
            for k in range(1,nbins-1):
                bincenter = self.fontsizeHist_percharacter[1][k] + 0.5*binsize
                bincontent = self.fontsizeHist_percharacter[0][k]
            
                # Identify if this is a peak:
                if (bincontent>=self.fontsizeHist_percharacter[0][k+1])and(bincontent>self.fontsizeHist_percharacter[0][k-1]): 
                    newregion = fontregion()
                    newregion.set_value(bincenter)
                    self.fontregions.append(newregion)
            
            # Deal with the left-most bin separately:
            k=0
            bincenter = self.fontsizeHist_percharacter[1][k] + 0.5*binsize
            bincontent = self.fontsizeHist_percharacter[0][k]
            
            if (bincontent>self.fontsizeHist_percharacter[0][k+1]):
                newregion = fontregion()
                newregion.set_value(bincenter)
                self.fontregions.append(newregion)
            
            # Deal with the right-most bin separately:
            k=nbins-1
            bincenter = self.fontsizeHist_percharacter[1][k] + 0.5*binsize
            bincontent = self.fontsizeHist_percharacter[0][k]
            
            if (bincontent>self.fontsizeHist_percharacter[0][k-1]):
                newregion = fontregion()
                newregion.set_value(bincenter)
                self.fontregions.append(newregion)
        
        # Next, deal with the nbins=2 case:
        elif (nbins==2):
            leftbincenter = self.fontsizeHist_percharacter[1][0]
            rightbincenter = self.fontsizeHist_percharacter[1][1]
            leftbincontent = self.fontsizeHist_percharacter[0][0]
            rightbincontent = self.fontsizeHist_percharacter[0][1]
            
            newregion = fontregion()
            if (rightbincontent>leftbincontent): newregion.set_value(rightbincenter + 0.5*binsize)
            else: newregion.set_value(leftbincenter + 0.5*binsize)
            self.fontregions.append(newregion)
            
        # Next, deal with the nbins=1 case:
        elif (nbins==1):
            bincenter = self.fontsizeHist_percharacter[1][0] + 0.5*binsize
            bincontent = self.fontsizeHist_percharacter[0][0]
            
            newregion = fontregion()
            newregion.set_value(bincenter)
            self.fontregions.append(newregion)
            
        # NOTE: an else-statement is literally impossible due to Histogramcheck!
    
        # Next, we must calculate the other properties of the fontregions:
        if (len(self.fontregions)==1):
            
            # This is easy:
            self.fontregions[0].set_left(xmin)
            self.fontregions[0].set_right(xmax)
            self.fontregions[0].set_frequency(1.0)
            self.fontregions[0].set_cascadelevel(1) # 0 = Title, 1=all else in this case.
            self.fontregions[0].set_isregular(True)
            
            # Adapt for the 2-bin case:
            if (nbins==2):
                if (self.fontregions[0].get_value()<self.fontsizeHist_percharacter[1][1]):
                    self.fontregions[0].set_frequency(self.fontsizeHist_percharacter[0][0]/(self.fontsizeHist_percharacter[0][0]+self.fontsizeHist_percharacter[0][1]))
                    self.fontregions[0].set_left(self.fontsizeHist_percharacter[1][0])
                    self.fontregions[0].set_right(self.fontsizeHist_percharacter[1][1])
                else:
                    self.fontregions[0].set_frequency(self.fontsizeHist_percharacter[0][1]/(self.fontsizeHist_percharacter[0][0]+self.fontsizeHist_percharacter[0][1]))
                    self.fontregions[0].set_left(self.fontsizeHist_percharacter[1][1])
                    self.fontregions[0].set_right(self.fontsizeHist_percharacter[1][2])
            
            # Extend the left of the smallest-font and the right of the largest-font:
            self.fontregions[0].set_left(self.fontregions[0].get_left()-binsize)
            self.fontregions[0].set_right(self.fontregions[0].get_right()+binsize)
            
        elif (len(self.fontregions)>1):
            
            # Then we must first sort them according to increasing font size:
            self.fontregions = sorted(self.fontregions, key=lambda x: x.value, reverse=False)
            
            # Then, loop over them to calculate the boundaries:
            for k in range(0,len(self.fontregions)):
                
                if (k==0): self.fontregions[k].set_left(xmin)
                else: self.fontregions[k].set_left(0.5*(self.fontregions[k].get_value()+self.fontregions[k-1].get_value()))
                
                if (k==len(self.fontregions)-1): self.fontregions[k].set_right(xmax)
                else: self.fontregions[k].set_right(0.5*(self.fontregions[k].get_value()+self.fontregions[k+1].get_value()))
        
            # Extend the left of the smallest-font and the right of the largest-font:
            self.fontregions = sorted(self.fontregions, key=lambda x: x.left, reverse=False)
            self.fontregions[0].set_left(self.fontregions[0].get_left()-binsize)
            
            self.fontregions = sorted(self.fontregions, key=lambda x: x.right, reverse=True)
            self.fontregions[0].set_right(self.fontregions[0].get_right()+binsize)
            
            # Next, we must calculate the frequencies:
            totalfreq = sum(self.fontsizeHist_percharacter[0])
        
            # and this requires looping over them again:
            for k in range(0,nbins):
                bincenter = self.fontsizeHist_percharacter[1][k] + 0.5*binsize
                bincontent = self.fontsizeHist_percharacter[0][k]
            
                for n in range(0,len(self.fontregions)):
                    if (self.fontregions[n].isinregion(bincenter)):
                        self.fontregions[n].set_frequency(self.fontregions[n].get_frequency() + bincontent/totalfreq)
        
            # Then we must sort the array based on decending frequency:
            self.fontregions = sorted(self.fontregions, key=lambda x: x.frequency, reverse=True)
        
            # Now, Notice that the highest freq is body tekst.
            # We first put this at cascade level 0:
            self.fontregions[0].set_isregular(True)
            
            # Now, the idea is that, in situations where the author uses a lot of really
            # big characters, we do not gain a lot from assigning all of them their own
            # text cascade level. So then, we must eliminate those large regions from
            # the array and extend the region with largest font size. So sort according to increasing font size:
            self.fontregions = sorted(self.fontregions, key=lambda x: x.value, reverse=False)
            
            # Find the index of the regular region:
            index = 0
            for k in range(0,len(self.fontregions)):
                if (self.fontregions[k].get_isregular()==True):
                    index = k
                    
            # Now, we want to keep at most 3 regions larger than the regular one:
            max_R = self.fontregions[len(self.fontregions)-1].get_right()
            temp_freq = 0.0
            if ((index+4)<len(self.fontregions)):
                for k in range(len(self.fontregions)-1,index+3,-1): #reverse-looping to make sure we do not have problems with deleting:
                    temp_freq = self.fontregions[k].get_frequency()
                    self.fontregions.pop(k)
            self.fontregions[len(self.fontregions)-1].set_right(max_R)
            self.fontregions[len(self.fontregions)-1].set_frequency(self.fontregions[len(self.fontregions)-1].get_frequency()+temp_freq)

            # Then, for appointing cascade levels: sort the array according to decending fontsizes:
            self.fontregions = sorted(self.fontregions, key=lambda x: x.value, reverse=True)
            
            # Then, we can now appoint cascade levels easy:
            cascade_start = 1
            for region in self.fontregions:
                region.set_cascadelevel(cascade_start)
                cascade_start = cascade_start + 1
            
            # Done.       

def selectfontregion_textpart(self, fontsize: float) -> fontregion:
    """
    Once textpart.fontregions has been filled by calling the above findfontregions-function,
    this function can be used to select the fontregion to which a given fontsize belongs.
    
    # Parameters:
    fontsize (float): the fontsize you would like to classify
    #Returns: fontregion, the element from textpart.fontregions the fontsize belongs to.
    """
    
    # ------------------------------------------------------------------------------------
    
    # Begin by sorting the array according to increasing fontsizes:
    self.fontregions = sorted(self.fontregions, key=lambda x: x.value, reverse=False)
    
    # Next, loop through the array and attempt to identify the proper region:
    index = 0
    theindex = -1
    for region in self.fontregions:
        if region.isinregion(fontsize):
            theindex = index
        index += 1
    
    # If we identified a region, we are done:
    if (theindex>=0): return self.fontregions[theindex]
    else:
        
        # Then no proper region exists, so then we have to create one:
        newregion = fontregion()
        newregion.set_left(0.001)
        newregion.set_right(10000.0)
        newregion.set_value(fontsize)
        newregion.set_frequency(1.0)
        newregion.set_cascadelevel(-1) # NOTE: to identify that this is not an answer we would like to give!
        newregion.set_isregular(False)
        
        # See if the problem is that no fontregions exist:
        if (len(self.fontregions)==0): return newregion
        else:
            
            # Then, the fontsize is either too small, or too large:
            if (fontsize<=self.fontregions[0].get_left()):
                newregion.set_right(self.fontregions[0].get_left())
                return newregion
            elif (fontsize>=self.fontregions[len(self.fontregions)-1].get_right()):
                newregion.set_left(self.fontregions[len(self.fontregions)-1].get_right())
                return newregion
            else:
                
                # Then there is a bug in the code, this situation should not exist!
                newregion.set_cascadelevel(-2)
                return newregion
            
                # Done.

def findregularfontregion_textpart(self) -> fontregion:
    """
    Once textpart.fontregions has been filled by calling the above findfontregions-function,
    this function can be used to identify the fontregion that is marked as regular (meaning 
    that it is body-text). This marking is done inside findfontregions_textpart and should be
    unique.
    
    # Parameters: None
    #Returns: fontregion, the element from textpart.fontregions that is marked as regular:
    """
    
    # ------------------------------------------------------------------------------------
    
    # Begin by sorting the array according to decreasing fontsizes:
    self.fontregions = sorted(self.fontregions, key=lambda x: x.value, reverse=True)
    # This will ensure that if, by accident, we find multiple marked regions, we
    # will return the smallest fontsize with a mark.
    
    # Next, do the looping:
    index = 0
    theindex = -1
    for region in self.fontregions:
        if region.get_isregular():
            theindex = index
        index += 1
    
    # If we identified a region, we are done:
    if (theindex>=0): return self.fontregions[theindex]
    else:
        
        # Then, no proper region exists, so then we have to create one:
        newregion = fontregion()
        newregion.set_left(0.001)
        newregion.set_right(10000.0)
        newregion.set_value(10.0)
        newregion.set_frequency(1.0)
        newregion.set_cascadelevel(-1) # NOTE: to identify that this is not an answer we would like to give!
        newregion.set_isregular(False)
        return newregion
    
        # Done.
    
def fontsize_smallerthenregular_textpart(self, fontsize: float) -> bool:
    """
    Once textpart.fontregions has been filled by calling the above findfontregions-function,
    this function can be used to decide whether a given fontsize falls inside the regular
    region (meaning that it is body-text), or below (meaning it is caption, footer, etc.),
    or above (meaning it is a title, headline, etc.)
    
    This function returns true if the fontsize is smaller then the regular region.
    
    # Parameters:
    fontsize (float): the fontsize you would like to classify
    #Returns: bool, the answer to the above question.
    """
    
    # ------------------------------------------------------------------------------------
    
    # Select the two fontregions:    
    regularregion = self.findregularfontregion()
    currentregion = self.selectfontregion(fontsize)
    
    # test that we obtained proper answers:
    if (regularregion.get_cascadelevel()<0): return False
    if (currentregion.get_cascadelevel()<0): return False

    # Next, obtain the centervalues:
    regular_center = regularregion.get_value()
    current_center = currentregion.get_value()
    
    # Then, take the test:
    if (current_center<(regular_center-0.1)): return True
    else: return False

    # Done. We add the 0.1 to prevent cases where only a single fontsize
    # is available, but the program identifies multiple regions due to fluctuations.
    
def fontsize_equalstoregular_textpart(self, fontsize: float) -> bool:
    """
    Once textpart.fontregions has been filled by calling the above findfontregions-function,
    this function can be used to decide whether a given fontsize falls inside the regular
    region (meaning that it is body-text), or below (meaning it is caption, footer, etc.),
    or above (meaning it is a title, headline, etc.)
    
    This function returns true if the fontsize is equal to the regular region.
    
    # Parameters:
    fontsize (float): the fontsize you would like to classify
    #Returns: bool, the answer to the above question.
    """
    
    # ------------------------------------------------------------------------------------
    
    # Select the two fontregions:
    regularregion = self.findregularfontregion()
    currentregion = self.selectfontregion(fontsize)
    
    # test that we obtained proper answers:
    if (regularregion.get_cascadelevel()<0): return False
    if (currentregion.get_cascadelevel()<0): return False

    # Next, obtain the centervalues:
    regular_center = regularregion.get_value()
    current_center = currentregion.get_value()
    
    # Then, take the test:
    if (abs(current_center-regular_center)<=0.1): return True
    else: return False
    
    # Done.

def fontsize_biggerthenregular_textpart(self, fontsize: float) -> bool:
    """
    Once textpart.fontregions has been filled by calling the above findfontregions-function,
    this function can be used to decide whether a given fontsize falls inside the regular
    region (meaning that it is body-text), or below (meaning it is caption, footer, etc.),
    or above (meaning it is a title, headline, etc.)
    
    This function returns true if the fontsize is larger then the regular region.
    
    # Parameters:
    fontsize (float): the fontsize you would like to classify
    #Returns: bool, the answer to the above question.
    """
    
    # ------------------------------------------------------------------------------------
    
    # Select the two fontregions:
    regularregion = self.findregularfontregion()
    currentregion = self.selectfontregion(fontsize)
    
    # test that we obtained proper answers:
    if (regularregion.get_cascadelevel()<0): return False
    if (currentregion.get_cascadelevel()<0): return False

    # Next, obtain the centervalues:
    regular_center = regularregion.get_value()
    current_center = currentregion.get_value()
    
    # Then, take the test:
    if (current_center>(regular_center+0.1)): return True
    else: return False

    # Done. We add the 0.1 to prevent cases where only a single fontsize
    # is available, but the program identifies multiple regions due to fluctuations.
    
