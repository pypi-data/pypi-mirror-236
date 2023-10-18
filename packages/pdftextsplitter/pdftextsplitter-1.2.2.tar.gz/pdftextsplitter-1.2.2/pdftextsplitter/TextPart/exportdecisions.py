def exportdecisions_textsplitter(self):
    """
    Function to export the content of the textclassification-array to a .txt-file for later inspection.
    This will contain not only the textlines of the pdf, but also their fontsizes, textpart-decision 
    and cascade-level. Created fontregions are also added. The array is only filled after breakdown has been called.
    
    # Parameters: None.
    # Return: None (the .txt-file)
    """
    
    # ---------------------------------------------------------------------------
    
    # Begin by opening a new .txt-file:
    exportfile = open(self.outputpath + self.documentname + "_decisions.txt", 'w', encoding="utf-8")
    
    # Next, loop over the alineas:
    if (len(self.textclassification)>0):
        
        # Begin by adding some general comments:
        exportfile.write("##################################################################\n")
        exportfile.write("### [TEXTSPLITTER CLASS] #########################################\n")
        exportfile.write("### [Breakdown decisions for document "+self.documentname + "] ###\n")
        exportfile.write("##################################################################\n")
        exportfile.write("\n")
        
        # Then, iterate of the text-content:
        for textline in self.textclassification:
             exportfile.write(textline + "\n")
    
    else:
        
        exportfile.write("You did not execute textsplitter.breakdown() before calling this function.\n")
        exportfile.write("As such, we could not display any decisions for document\n")
        exportfile.write(self.documentname + "\n")
        exportfile.write("\n")
    
    # Close off:
    exportfile.close()
       
