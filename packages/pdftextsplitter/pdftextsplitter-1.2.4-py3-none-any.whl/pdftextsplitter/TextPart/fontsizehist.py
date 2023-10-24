# Python functionality:
import matplotlib.pyplot as plt

def fontsizehist_textpart(self, verbose_option = 0):
    """
    This function creates histograms from the data in textpart on fontsizes and plots them.
    
    # Parameters: verbose_option: if smaller then 0, no histogram pictures are saved (default=0).
    # Return: None (.png output)
    """
    
    # --------------------------------------------------------
    
    # Create the first histogram:
    self.fontsizeHist_percharacter = plt.hist(self.fontsize_percharacter, bins=self.histogramsize)
    if (verbose_option>=0): plt.savefig(self.outputpath + self.documentname + "_Fontsizes_allcharacters.png")
    plt.close()
    
    # Create the second histogram:
    self.fontsizeHist_perline = plt.hist(self.fontsize_perline, bins=self.histogramsize)
    if (verbose_option>=0): plt.savefig(self.outputpath + self.documentname + "_Fontsizes_Firstcharacters.png")
    plt.close()
    
    # Done.
