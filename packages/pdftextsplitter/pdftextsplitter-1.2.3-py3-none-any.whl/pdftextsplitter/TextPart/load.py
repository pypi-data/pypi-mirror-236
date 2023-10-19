def load_textpart(self):
    """
    This function is meant as a member function of the textpart-class
    It will write the textual content to a seperate .txt-file.
    It does not take any parameters or return, as that information is
    taken from the textpart-class.
    """
    
    # Begin by opening the .txt document that we have to import:
    loadfile = open(self.documentpath + self.documentname + ".txt", 'r',encoding='utf-8',errors='ignore')
    
    # Clear the textcontent:
    self.textcontent.clear()
    self.positioncontent.clear()
    self.fontsize_perline.clear()
    self.fontsize_percharacter.clear()
    
    # Then, iterate over the textfile:
    for textline in loadfile:
        self.textcontent.append(textline)
    
    # Next, close the file:
    loadfile.close()
    
    # Done.
