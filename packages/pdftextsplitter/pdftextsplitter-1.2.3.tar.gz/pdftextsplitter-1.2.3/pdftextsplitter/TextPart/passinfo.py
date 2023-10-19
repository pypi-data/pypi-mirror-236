def passinfo_textsplitter(self):
    """
    Passes the class information that textsplitter inherits directly from textpart (such as document name & path) 
    to all subclasses such as title, body, etc. at once, except for the labelname, textcontent, and the 
    arrays mimicing textcontent. These arrays are: fontsize_perline, fontsize_percharacter, positioncontent.
    
    Thoe subclasses also inherit from textpart and, therefore, need the same information as Textsplitter has itself.
    # Parameters: None, # Return: None.
    
    """
    
    # -------------------------------------------------------------------------
    
    self.body.histogramsize = self.histogramsize
    self.body.fontsizeHist_perline = self.fontsizeHist_perline
    self.body.fontsizeHist_percharacter = self.fontsizeHist_percharacter
    self.body.documentpath = self.documentpath
    self.body.documentname = self.documentname
    self.body.outputpath = self.outputpath
    self.body.fontregions = self.fontregions  
    self.body.headerboundary = self.headerboundary
    self.body.footerboundary = self.footerboundary
    self.body.native_TOC = self.native_TOC
    self.body.whitespaceHist_perline = self.whitespaceHist_perline
    self.body.lineregions = self.lineregions
    self.body.min_vertpos = self.min_vertpos
    self.body.max_vertpos = self.max_vertpos
    self.body.ruleverbosity = self.ruleverbosity
    self.body.verbosetextline = self.verbosetextline
    self.body.nr_bold_chars = self.nr_bold_chars
    self.body.nr_total_chars = self.nr_total_chars
    self.body.boldchars_ratio = self.boldchars_ratio
    self.body.boldratio_threshold = self.boldratio_threshold
    
    self.footer.histogramsize = self.histogramsize
    self.footer.fontsizeHist_perline = self.fontsizeHist_perline
    self.footer.fontsizeHist_percharacter = self.fontsizeHist_percharacter
    self.footer.documentpath = self.documentpath
    self.footer.documentname = self.documentname
    self.footer.outputpath = self.outputpath
    self.footer.fontregions = self.fontregions 
    self.footer.headerboundary = self.headerboundary
    self.footer.footerboundary = self.footerboundary
    self.footer.native_TOC = self.native_TOC
    self.footer.whitespaceHist_perline = self.whitespaceHist_perline
    self.footer.lineregions = self.lineregions
    self.footer.min_vertpos = self.min_vertpos
    self.footer.max_vertpos = self.max_vertpos
    self.footer.ruleverbosity = self.ruleverbosity
    self.footer.verbosetextline = self.verbosetextline
    self.footer.nr_bold_chars = self.nr_bold_chars
    self.footer.nr_total_chars = self.nr_total_chars
    self.footer.boldchars_ratio = self.boldchars_ratio
    self.footer.boldratio_threshold = self.boldratio_threshold
    
    self.headlines.histogramsize = self.histogramsize
    self.headlines.fontsizeHist_perline = self.fontsizeHist_perline
    self.headlines.fontsizeHist_percharacter = self.fontsizeHist_percharacter
    self.headlines.documentpath = self.documentpath
    self.headlines.documentname = self.documentname
    self.headlines.outputpath = self.outputpath
    self.headlines.fontregions = self.fontregions  
    self.headlines.headerboundary = self.headerboundary
    self.headlines.footerboundary = self.footerboundary
    self.headlines.native_TOC = self.native_TOC
    self.headlines.whitespaceHist_perline = self.whitespaceHist_perline
    self.headlines.lineregions = self.lineregions
    self.headlines.min_vertpos = self.min_vertpos
    self.headlines.max_vertpos = self.max_vertpos
    self.headlines.ruleverbosity = self.ruleverbosity
    self.headlines.verbosetextline = self.verbosetextline
    self.headlines.nr_bold_chars = self.nr_bold_chars
    self.headlines.nr_total_chars = self.nr_total_chars
    self.headlines.boldchars_ratio = self.boldchars_ratio
    self.headlines.boldratio_threshold = self.boldratio_threshold
    
    self.title.histogramsize = self.histogramsize
    self.title.fontsizeHist_perline = self.fontsizeHist_perline
    self.title.fontsizeHist_percharacter = self.fontsizeHist_percharacter
    self.title.documentpath = self.documentpath
    self.title.documentname = self.documentname
    self.title.outputpath = self.outputpath
    self.title.fontregions = self.fontregions 
    self.title.headerboundary = self.headerboundary
    self.title.footerboundary = self.footerboundary
    self.title.native_TOC = self.native_TOC
    self.title.whitespaceHist_perline = self.whitespaceHist_perline
    self.title.lineregions = self.lineregions
    self.title.min_vertpos = self.min_vertpos
    self.title.max_vertpos = self.max_vertpos
    self.title.ruleverbosity = self.ruleverbosity
    self.title.verbosetextline = self.verbosetextline
    self.title.nr_bold_chars = self.nr_bold_chars
    self.title.nr_total_chars = self.nr_total_chars
    self.title.boldchars_ratio = self.boldchars_ratio
    self.title.boldratio_threshold = self.boldratio_threshold
    
    self.enumeration.histogramsize = self.histogramsize
    self.enumeration.fontsizeHist_perline = self.fontsizeHist_perline
    self.enumeration.fontsizeHist_percharacter = self.fontsizeHist_percharacter
    self.enumeration.documentpath = self.documentpath
    self.enumeration.documentname = self.documentname
    self.enumeration.outputpath = self.outputpath
    self.enumeration.fontregions = self.fontregions 
    self.enumeration.headerboundary = self.headerboundary
    self.enumeration.footerboundary = self.footerboundary
    self.enumeration.native_TOC = self.native_TOC
    self.enumeration.whitespaceHist_perline = self.whitespaceHist_perline
    self.enumeration.lineregions = self.lineregions
    self.enumeration.min_vertpos = self.min_vertpos
    self.enumeration.max_vertpos = self.max_vertpos
    self.enumeration.ruleverbosity = self.ruleverbosity
    self.enumeration.verbosetextline = self.verbosetextline
    self.enumeration.nr_bold_chars = self.nr_bold_chars
    self.enumeration.nr_total_chars = self.nr_total_chars
    self.enumeration.boldchars_ratio = self.boldchars_ratio
    self.enumeration.boldratio_threshold = self.boldratio_threshold
    
    # NOTE: Add new textparts here!
    # NOTE: Be sure to adapt TestPassInfo.py as well to test for these items!
    
    for textalinea in self.textalineas:
        textalinea.histogramsize = self.histogramsize
        textalinea.fontsizeHist_perline = self.fontsizeHist_perline
        textalinea.fontsizeHist_percharacter = self.fontsizeHist_percharacter
        textalinea.documentpath = self.documentpath
        textalinea.documentname = self.documentname
        textalinea.outputpath = self.outputpath
        textalinea.fontregions = self.fontregions  
        textalinea.headerboundary = self.headerboundary
        textalinea.footerboundary = self.footerboundary
        textalinea.native_TOC = self.native_TOC
        textalinea.whitespaceHist_perline = self.whitespaceHist_perline
        textalinea.lineregions = self.lineregions
        textalinea.min_vertpos = self.min_vertpos
        textalinea.max_vertpos = self.max_vertpos
        textalinea.ruleverbosity = self.ruleverbosity
        textalinea.verbosetextline = self.verbosetextline
        textalinea.nr_bold_chars = self.nr_bold_chars
        textalinea.nr_total_chars = self.nr_total_chars
        textalinea.boldchars_ratio = self.boldchars_ratio
        textalinea.boldratio_threshold = self.boldratio_threshold
    
