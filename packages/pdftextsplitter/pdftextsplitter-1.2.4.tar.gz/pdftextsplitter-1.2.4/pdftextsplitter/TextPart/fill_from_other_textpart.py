def fill_from_other_textpart_textpart(self, other):
    """
    This function will fill the class members of textpart
    with values from some other textpart-object.
    ATTENTION: It does not create a deep copy of the object,
    it only allows self to reach the content of other.
    # Parameters: other: textpart: the part that we take our information from (type hinting not possible due to that it requires circular imports)
    # Return: nothing (stored in the class).
    """
    
    # Definition of parameters:
    self.labelname = other.labelname
    self.documentpath = other.documentpath
    self.documentname = other.documentname
    self.outputpath = other.outputpath
    self.histogramsize = other.histogramsize
    self.headerboundary = other.headerboundary
    self.footerboundary = other.footerboundary
    self.ruleverbosity = other.ruleverbosity
    self.verbosetextline = other.verbosetextline
    
    # Definition of line/character-arrays:
    self.textcontent = other.textcontent
    self.pagenumbers = other.pagenumbers
    self.positioncontent = other.positioncontent
    self.horposcontent = other.horposcontent
    self.whitelinesize = other.whitelinesize
    self.whitespaceHist_perline = other.whitespaceHist_perline
    self.fontsize_perline = other.fontsize_perline
    self.fontsizeHist_perline = other.fontsizeHist_perline
    self.fontsize_percharacter = other.fontsize_percharacter
    self.fontsizeHist_percharacter = other.fontsizeHist_percharacter
    self.is_italic = other.is_italic
    self.is_bold = other.is_bold
    self.is_highlighted = other.is_highlighted
    self.nr_bold_chars = other.nr_bold_chars
    self.nr_total_chars = other.nr_total_chars
    self.boldchars_ratio = other.boldchars_ratio
    self.boldratio_threshold = other.boldratio_threshold
    
    # Definition of calculated arrays:
    self.fontregions = other.fontregions
    self.lineregions = other.lineregions
    
    # Definition of other members needed for processing:
    self.max_vertpos = other.max_vertpos
    self.min_vertpos = other.min_vertpos
