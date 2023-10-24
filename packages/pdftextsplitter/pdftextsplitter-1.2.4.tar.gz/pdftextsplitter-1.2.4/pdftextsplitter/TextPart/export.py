def export_textpart(self, option: str):
    """
    This function is meant as a member function of the textpart-class
    It will write the textual content to a seperate .txt-file.
    Most information is taken from the textpart-class and the output
    is a .txt-file, not an object.
    
    # Parameters:
    option (str): default, fontsize (default just prints the text, fontsize adds the size of the first character in front of every line.
    # Return: none (.txt-file).
    """
    
    # Begin by onpening a new .txt-file:
    exportfile = open(self.outputpath + self.documentname + ".txt", 'w', encoding='utf-8')
    size = len(self.textcontent)
    fontlen = len(self.fontsize_perline)
    whitelen = len(self.whitelinesize)
    index = 0
    exportline = ""
    
    # Then, iterate of the text-content:
    for textline in self.textcontent:
        
        # Adjust index to match textline:
        index = index + 1
        
        # Write exportline based on option:
        if (option=="default"): 
            exportline = textline
        
        elif (option=="fontsize"):
            if ((index-1)<fontlen):
                exportline = "[" + str(self.fontsize_perline[index-1]) + "] " + textline
            else:
                exportline = "[UNKNOWN] " + textline
            
        elif (option=="whitelines"):
            if ((index-1)<whitelen):
                exportline = "[" + str(self.whitelinesize[index-1]) + "] " + textline
            else:
                exportline = "[UNKNOWN] " + textline
        
        else:
            exportline = "[UNSUPPORTED OPTION]"
        
        # Then, write it to the .txt-file:
        exportfile.write(exportline)
        if (index<size): exportfile.write("\n")
    
    # Also add one line if the content is empty:
    if (size==0): exportfile.write("\n")
    
    # Next, close the file:
    exportfile.close()
    
    # Done.
