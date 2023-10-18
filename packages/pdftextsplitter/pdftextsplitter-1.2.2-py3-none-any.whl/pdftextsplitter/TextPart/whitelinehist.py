# Python functionality:
import matplotlib.pyplot as plt
import numpy as np

def whitelinehist_textpart(self, verbose_option = 0):
    """
    This function creates histograms from the data in textpart on whitelines
    and plots them. It takes the whiteline-information from the vertical position
    y0 of the bbox by calculating differences of the y0-bbox positions of the
    textlines. Then, these differences are interpreted as whitelines and processed
    in a histogram, so that findlineregions can be used to identify peaks
    in the histogram and, therefore, identify which type of whitelines are
    present in the histogram.
    
    # Parameters: verbose_option: if smaller then 0, no histogram pictures are saved (default=0).
    # Return: None (.png output)
    """
    
    # --------------------------------------------------------
    
    # First, calculate the max & min vertical positions:
    self.max_vertpos = -1000000.0
    self.min_vertpos = 1000000.0
    
    for thispos in self.positioncontent:
        if (thispos>=self.footerboundary)and(thispos<=self.headerboundary):
            if (thispos<self.min_vertpos): self.min_vertpos = thispos
            if (thispos>self.max_vertpos): self.max_vertpos = thispos
    
    # Begin by computing all the differences of the y0-bbox positions:
    self.whitelinesize.clear()
    poslength = len(self.positioncontent)
    
    # Check if there is enough information to actually compute differences:
    if (len(self.positioncontent)>=2):
        
        # Then, calculate the differences. Note that we should
        # not calculate a difference for each textline blindly, as
        # we should not take headers & footers into account. As such, we
        # should only calculate difference w.r.t. the header and footer boundary.
        
        # Begin with defining the indices:
        Previousindex = 0
        
        # next, loop over all vertical positions:
        for Currentindex in range(0,poslength):
            
            # Check whether item Currentindex is part of the header/footer:
            if (self.positioncontent[Currentindex]>=self.footerboundary)and(self.positioncontent[Currentindex]<=self.headerboundary):
                
                # If this is the case, we can use it to calculate a whiteline.
                # But Currentindex-1 might be part of the header/footer. So loop back
                # until we find a previous line that is also not part of header/footer:
                FoundPrevious = False
                Previousindex = Currentindex
                while not FoundPrevious:
                    
                    # Make a loop back:
                    Previousindex = Previousindex - 1
                    
                    # If we enter a negative area:
                    if (Previousindex<0): FoundPrevious = True
                    # So that the loop ends. We can measure succes from whether Previousindex is negative or not.
                    
                    # Check whether the previous line is part of header/footer:
                    else:
                        if (self.positioncontent[Previousindex]>=self.footerboundary)and(self.positioncontent[Previousindex]<=self.headerboundary):
                            # then we found it, so stop the loop:
                            FoundPrevious = True
                
                # Now, we can calculate the whitelines IF we found a suitable previous index:
                if (Previousindex>=0):
                    self.whitelinesize.append(self.positioncontent[Previousindex] - self.positioncontent[Currentindex]) # Order is because vertpos is decreasing in our program.
                    # ATTENTION: This way, whitelinesize[n] contains the distance between textcontent[n] and its PREVIUOS textline.
                else:
                    # Then, we must mark that it was impossible to find something:
                    self.whitelinesize.append(-1.0)
            
            # Next, we must also mark it, if it was impossible to find something for Currentindex:
            else:
                self.whitelinesize.append(-2.0)
                    
    # --------------------------------------------------------------------------------
    
    # Next, we must identify the page breaks. This is easy, as those will be the only
    # negative numbers (apart from -1.0 & -2.0 as marked above).
    # But we must be careful: the size of these negative numbers also 
    # play an important role, as a chapter-break can occur (and usually will occur) at
    # a page-break. So we must not simply reset those.
    
    # Rather, we must identify the space between lines of body-text and calculate:
    # (neg. value) + |max. neg. value| + (body-space). If a textblock ends
    # prematurely and/or starts later on the next page, the negative value will not be
    # as far negative as usually, so by adding this, the resulting whiteline will also
    # be bigger (positive).
    
    # The implementation is far from trivial, as the distances between the bbox-positions
    # fluctuate, even withing body-text. So just calculating a histogram blindly is not 
    # recommended. Rather, we must first find the 'best' histogram by shifting the bin
    # boundaries gradually and see when we find the largest peak (that means that as
    # many as possile body-text whitelines fall within the same bin).
    
    # Begin by calculating the appropriate bin size:
    min_line = min(self.whitelinesize)
    max_line = max(self.whitelinesize)
    binsize = abs(max_line-min_line)/self.histogramsize
    binlimit_L = min_line - 2*binsize
    binlimit_R = max_line + 2*binsize
    # NOTE, that gives us self.histogramsize+5 bins.
    
    # Next, gradually shift the bin boundaries:
    highest_peak = 0
    highest_index = -1
    nr_shifts = 10
    thebins = []
    for n in range(0,self.histogramsize+5):
        thebins.append(0.0)
    
    for k in range(0,nr_shifts):
        
        # Calculate the current bin boundaries:
        current_binlimit_L = binlimit_L + (k/nr_shifts)*binsize
        current_binlimit_R = binlimit_R + (k/nr_shifts)*binsize
        
        # We cannot build this array using range, so we do it manually:
        for n in range(0,self.histogramsize+5):
            thebins[n] = current_binlimit_L + n*binsize
        
        # Calculate the histogram:
        temphist = plt.hist(self.whitelinesize, bins=thebins)
        
        # Calculate the maximum bincontent:
        max_height = max(temphist[0])
        
        # Compare to find the highest one over all shifts:
        if (max_height>highest_peak):
            highest_peak = max_height
            highest_index = k
        
        # Close histogram:
        plt.close()
    
    # Then, next calculate the histogram with this configuration:
    binlimit_L = binlimit_L + (highest_index/nr_shifts)*binsize
    binlimit_R = binlimit_R + (highest_index/nr_shifts)*binsize

    for n in range(0,self.histogramsize+5):
            thebins[n] = binlimit_L + n*binsize

    self.whitespaceHist_perline = plt.hist(self.whitelinesize, bins=thebins)
    if (verbose_option>=0): plt.savefig(self.outputpath + self.documentname + "_Whitelines_WithNegatives.png",dpi=500)
    plt.close()
    
    # Then, find the index of the highest bin, that is NOT zero. So first identify the 
    # zero-bin:
    zerobinindex = -1
    zerobincontent = 0
    for n in range (0,self.histogramsize+4): # Because we use n=1 as well:
        if (self.whitespaceHist_perline[1][n]<0.0)and(self.whitespaceHist_perline[1][n+1]>=0.0):
            zerobinindex = n
            zerobincontent = self.whitespaceHist_perline[0][n]
    
    # Then, for the search, first put the zero-bin to zero while searching for the max. bin:
    self.whitespaceHist_perline[0][zerobinindex] = 0.0
    maxbincontent = max(self.whitespaceHist_perline[0])
    maxbinindex = np.argmax(self.whitespaceHist_perline[0])
    maxbincenter = binlimit_L + (maxbinindex+0.5)*binsize
    self.whitespaceHist_perline[0][zerobinindex] = zerobincontent
    
    # and find the index of the first bin with content (the largest negative one):
    isfound = False
    negbinindex = -1
    negbincontent = 0.0
    
    for n in range(0,self.histogramsize+5):
        if not isfound:
            if (self.whitespaceHist_perline[0][n]>0.5):
                isfound = True
                negbinindex = n
                negbincontent = self.whitespaceHist_perline[0][n]
    
    negbincenter = binlimit_L + (negbinindex+0.5)*binsize
    
    # Then, loop through the differences and correct the negative values:
    for k in range(0,len(self.whitelinesize)):
        if (self.whitelinesize[k]<-3.0): #and(abs(self.whitelinesize[k]+1.0)>1e-3)and(abs(self.whitelinesize[k]+2.0)>1e-3):
            # NOTE: sometines items on the same line fluctuate a bit, giving slight negative values.
            # Those are not a problem. Incorporating this and -1.0 & -2.0 cases gives  as an ideal case.
            self.whitelinesize[k] = self.whitelinesize[k] + abs(negbincenter) + abs(maxbincenter)
            
    # Then, we must now define a new histogram, again by shifting until we get the highest peak. But 
    # now with new & proper binlimits. We do not need the outliers, so we scale up to 3*body-distance.
    binlimit_R = 3*maxbincenter
    binlimit_L = -3.0 # To take care of the negative values.
    binsize = abs(binlimit_R-binlimit_L)/self.histogramsize
    binlimit_L = binlimit_L - 2*binsize # To make sure we do not exclude anything.
    binlimit_R = binlimit_R + 2*binsize # To make sure we do not exclude anything.
    binsize = abs(binlimit_R-binlimit_L)/self.histogramsize # To make sure we get self.histogramsize nr. of bins.
    thebins.clear()
    highest_peak = 0.0
    highest_index = -1
    
    for n in range(0,self.histogramsize+1):
        thebins.append(0.0)
    
    for k in range(0,nr_shifts):
        
        # Calculate the current bin boundaries:
        current_binlimit_L = binlimit_L + (k/nr_shifts)*binsize
        current_binlimit_R = binlimit_R + (k/nr_shifts)*binsize
        
        # We cannot build this array using range, so we do it manually:
        for n in range(0,self.histogramsize+1):
            thebins[n] = current_binlimit_L + n*binsize
        
        # Calculate the histogram:
        temphist = plt.hist(self.whitelinesize, bins=thebins)
        
        # Calculate the maximum bincontent:
        max_height = max(temphist[0])
        
        # Compare to find the highestone over all shifts:
        if (max_height>highest_peak):
            highest_peak = max_height
            highest_index = k
        
        # Close histogram:
        plt.close()
    
    # Then, next calculate the histogram with this configuration:
    binlimit_L = binlimit_L + (highest_index/nr_shifts)*binsize
    binlimit_R = binlimit_R + (highest_index/nr_shifts)*binsize

    for n in range(0,self.histogramsize+1):
        thebins[n] = binlimit_L + n*binsize
    
    # Then, we should now recreate the real histogram for which page breaks are fixed and
    # the range has been properly set:
    self.whitespaceHist_perline = plt.hist(self.whitelinesize, bins=thebins)
    if (verbose_option>=0): plt.savefig(self.outputpath + self.documentname + "_Whitelines_PerTextLine.png",dpi=500)
    plt.close()   
        
    # Done.
