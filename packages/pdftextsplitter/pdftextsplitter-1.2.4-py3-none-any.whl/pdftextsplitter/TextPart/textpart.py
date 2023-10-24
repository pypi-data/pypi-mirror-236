# Textpart imports:
from .export import export_textpart
from .load import load_textpart
from .textgeneration import textgeneration_textpart
from .fontsizehist import fontsizehist_textpart
from .fontregion import fontregion
from .fontregion import findfontregions_textpart
from .fontregion import selectfontregion_textpart
from .fontregion import findregularfontregion_textpart
from .fontregion import fontsize_smallerthenregular_textpart
from .fontregion import fontsize_equalstoregular_textpart
from .fontregion import fontsize_biggerthenregular_textpart
from .whitelinehist import whitelinehist_textpart
from .lineregion import lineregion
from .lineregion import findlineregions_textpart
from .lineregion import selectlineregion_textpart
from .lineregion import findregularlineregion_textpart
from .lineregion import whiteline_isregular_textpart
from .lineregion import whiteline_issmall_textpart
from .lineregion import whiteline_isbig_textpart
from .lineregion import whiteline_iszero_textpart
from .lineregion import whiteline_isvalid_textpart
from .lineregion import whiteline_smallerthenregular_textpart
from .read_native_toc import Native_TOC_Element
from .CurrentLine import CurrentLine
from .fill_from_other_textpart import fill_from_other_textpart_textpart
from .calculate_footerboundaries import calculate_footerboundaries_textpart

# Main class definition:
class textpart:
    """
    This class serves as a base class for all text element that we want to identify within
    a document. Classes like Body, Headlines, Title, Abstract, Footer, etc. should
    all derive from this class. Only the rule-function should be overwritten.
    
    As such, a flexible architecture is created that allows the developers to easily
    extent the kind of textual elements that we want to identify. Child-classes
    should then only override the rule-function that determines whether a certain
    textual line should be added to that textual part or not. All other functionality
    should be added to this class instead.   
    """

    # Default constructor definition of the class:
    def __init__(self):
        
        # Definition of parameters:
        self.labelname = "Textpart"         # This label identifies what kind of textual part we are dealing with. Its content will be overwritten by child-classes.
        self.documentpath = "./"            # This string contains the absolute path to the location of the pdf-document that will be analyzed.
        self.documentname = ""              # This string contains the document name of the pdf-document that will be analyzed. Without the .pdf-extension.
        self.outputpath = "./"              # This string contains the absolute path to the location where output .txt-files will be written to.
        self.histogramsize = 100            # This gives the number of bins in the fontsize & whiteline histograms.
        self.ruleverbosity = 0              # This parameter controls how much informatin is printed on the screen when allpiying selection rules in children of this class.
        self.verbosetextline = ""           # We only give verbose-output in this string is present in the textline that we are analysing.
        
        # Definition of line/character-arrays:
        self.textcontent = []               # This string-array contains the full textual content of the text element.
        self.pagenumbers = []               # This int-array contains the page number (PDF-file, not internal!) of each textline.
        self.positioncontent = []           # This float-array contains the y0-position of the bbox of each textline.
        self.horposcontent = []             # This float-array contains the x0-position of the bbox of each textline.
        self.whitelinesize = []             # This float-array contains the difference of the bbox-y0-positions and is, therefore, a measure of whitelines between text.
        self.whitespaceHist_perline = []    # This float-array contains the histogram bin content of all the whitepaces between textlines in the PDF.
        self.fontsize_perline = []          # This float-array contains the font sizes of the first character per textline in the PDF.
        self.fontsizeHist_perline = []      # This float-array contains the histogram bin contents of the first character per textline in the PDF.
        self.fontsize_percharacter = []     # This float-array contains the font sizes of all the characters of all textlines in the PDF. 
        self.fontsizeHist_percharacter = [] # This float-array contains the histogram bin contents of all the characters of all textlines in the PDF. 
        self.is_italic = []                 # This is_italic boolean shows when the given textpart is italic.
        self.is_bold = []                   # This is_bold boolean shows when the given textpart is bold.
        self.is_highlighted = []            # This is_highlighted boolean shows when the given textpart is highlighted.
        self.nr_bold_chars = 0              # Counts the total number of bold characters in the entire document.
        self.nr_total_chars = 0             # Counts the total number of characters in the entire document.
        self.boldchars_ratio = 0.0          # ratio between the number of bold & total characters in the document (calculated during textgeneration).
        self.boldratio_threshold = 0.05     # Above this ratio, bold is not taken along in the headlines-selection rules.
        
        # Definition of calculated arrays:
        self.fontregions = []               # This fontregion-array contain sthe different fontsizes indentified in the document.
        self.lineregions = []               # This lineregion-array contain sthe different whitelines indentified in the document.
        
        # Definition of other members needed for processing:
        self.max_vertpos = 0.0              # This gives the largest vertical position in the array that still falls below the header boundary.
        self.min_vertpos = 0.0              # This gives the smallest vertical position in the array that still falls above the footer boundary.
        self.headerboundary = 1000.0        # This gives the vertical position of the page to idicate the difference between header and body; above boundary=header.
        self.footerboundary = 55.0          # This gives the vertical position of the page to idicate the difference between footer and body; below boundary=footer.

    # Definition of get-functions:
    def get_labelname(self) -> str: return self.labelname
    def get_textcontent(self) -> list[str]: return self.textcontent
    def get_documentpath(self) -> str: return self.documentpath
    def get_documentname(self) -> str: return self.documentname
    def get_outputpath(self) -> str: return self.outputpath
    def get_histogramsize(self) -> float: return self.histogramsize
    def get_ruleverbosity(self) -> int: return self.ruleverbosity
    def get_verbosetextline(self) -> str: return self.verbosetextline

    # Definition of set-functions:
    def set_labelname(self, newstr: str): self.labelname = newstr
    def set_textcontent(self, newstr: list[str]): self.textcontent = newstr
    def set_documentpath(self, newstr: str): self.documentpath = newstr
    def set_documentname(self, newstr: str): self.documentname = newstr
    def set_outputpath(self, newstr: str): self.outputpath = newstr
    def set_histogramsize(self, newnum: float): self.histogramsize = newnum
    def set_ruleverbosity(self, newnum: int): self.ruleverbosity = newnum
    def set_verbosetextline(self, newstr: str): self.verbosetextline = newstr

    # Definition of rule-function (to be overwritten by specific textparts):
    def rule(self, thisline: CurrentLine) -> tuple[bool,int]:
        """
        # Parameters:
        thisline (CurrentLine): CurrentLine-object that holds all the relevant information of the current textline 
                            masterrule should make a decision about. See documentation of CurrentLine.py
        # Return: bool: whether the line should be added or not.
        # Return: int: document cascade level of the textline (0=entire doc, higher=deeper into the document).
        """
        return False,0

    # Definition masterrule, to be overwritten ONLY in textsplitter:
    def masterrule(self, thisline: CurrentLine) -> bool: 
        """
        # Parameters:
        thisline (CurrentLine): CurrentLine-object that holds all the relevant information of the current textline 
                            masterrule should make a decision about. See documentation of CurrentLine.py
        # Return: bool: whether the line should be added or not. No textlevel should be returned here, as that should be processed inside masterrule.
        """
        [thisrule,thislevel] = self.rule(thisline)
        return thisrule

    # Definition of appending function; to append a
    # textline to the textual content of this element:
    def fillcontent(self, thisline: CurrentLine):
        if self.masterrule(thisline): # NOTE: By calling masterrule, and not _masterrule, calling this will always call the overwritten rule-function, as should be the case.
            self.textcontent.append(thisline.textline)
    
    # Definition to always append, regardless of rules:
    def blindfill(self, thisline: CurrentLine):
        self.textcontent.append(thisline.textline)
        
    # Definition of other class functionality (that is imported):
    export = export_textpart
    load = load_textpart
    textgeneration = textgeneration_textpart
    fontsizehist = fontsizehist_textpart
    findfontregions = findfontregions_textpart
    selectfontregion = selectfontregion_textpart
    findregularfontregion = findregularfontregion_textpart
    fontsize_smallerthenregular = fontsize_smallerthenregular_textpart
    fontsize_equalstoregular = fontsize_equalstoregular_textpart
    fontsize_biggerthenregular = fontsize_biggerthenregular_textpart
    whitelinehist = whitelinehist_textpart
    findlineregions = findlineregions_textpart
    selectlineregion = selectlineregion_textpart
    findregularlineregion = findregularlineregion_textpart
    whiteline_isregular = whiteline_isregular_textpart
    whiteline_issmall = whiteline_issmall_textpart
    whiteline_isbig = whiteline_isbig_textpart
    whiteline_iszero = whiteline_iszero_textpart
    whiteline_isvalid = whiteline_isvalid_textpart
    whiteline_smallerthenregular = whiteline_smallerthenregular_textpart
    fill_from_other_textpart = fill_from_other_textpart_textpart
    calculate_footerboundaries = calculate_footerboundaries_textpart
