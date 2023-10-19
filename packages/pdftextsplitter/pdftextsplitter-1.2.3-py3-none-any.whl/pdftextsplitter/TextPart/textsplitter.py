# Python functionality:
import time

# Import all classes that are part of the package. they need to be here (even if not used),
# to allow for import from within django.
# Independent classes:
from .OpenAI_Keys import OpenAI_Keys
from .fontregion import fontregion
from .lineregion import lineregion
from .CurrentLine import CurrentLine
from .read_native_toc import Native_TOC_Element

# Classes that inherit from textpart (textpart itself in the top):
from .textpart import textpart
from .title import title
from .body import body
from .footer import footer
from .headlines import headlines
from .enum_type import enum_type
from .enumeration import enumeration
from .textalinea import textalinea
from .masterrule import texttype

# Independent functions:
from .stringmatch import stringmatch

# Next, import the member functions of the textsplitter class:
from .masterrule import rulecomparison_textsplitter
from .masterrule import masterrule_textsplitter
from .passinfo import passinfo_textsplitter
from .breakdown import breakdown_textsplitter
from .exportdecisions import exportdecisions_textsplitter
from .exportalineas import exportalineas_textsplitter
from .calculatetree import calculatetree_textsplitter
from .summarize import summarize_textsplitter
from .summarize import summarize_dummy_textsplitter
from .summarize_openai import summarize_openai_textsplitter
from .summarize_huggingface import summarize_huggingface_textsplitter
from .layered_summary import layered_summary_textsplitter
from .textparser import alineas_to_html_textsplitter
from .read_native_toc import read_native_toc_textsplitter
from .printcode import printcode_textsplitter
from .Languagemodels import set_LanguageModel_textsplitter
from .shiftcontents import shiftcontents_textsplitter
from .document_metadata import document_metadata_textsplitter

# Main class definition:
class textsplitter(textpart):
    """
    This class handles the splitting of documents. It utilizes different text-elements
    such as Body, Alinea, Title, etc. that all inherit from textpart. This class then
    collects those different parts to fill them from the document.
    
    It also collects the different rules from the different textparts and collects them
    into a single master-rule. In order to have direct access to the functionality
    of textpart, it also inherits itself from this class. As such, it becomes
    capable of overriding the masterrule definition, so all other textparts
    can also benefit from that.
     
    """
    
    # ------------------------------------------------------------------------------------
    
    # Definition of the default-constructor:
    def __init__(self):
        super().__init__() # First initiates all elements of textpart
        super().set_labelname("TextSplitter") # Then, change the label to reflext that this is the master control class TextSplitter.
        self.VERSION = "1.2.3"                # To keep track on which version (selection rules) was used in the analysis.
        
        # Manage security of ChatGPT:
        self.thekeys = OpenAI_Keys()                                # List of all avaliable keys we can choose from.
        self.ChatGPT_Key = self.thekeys.standard_key                # Key to the ChatGPT-account this class can connect to.
        
        # Manage ChatGPT API rate limits:
        self.ratelimit_timeunit = self.thekeys.ratelimit_timeunit   # Time interval for which the rate limits of the account are defined.     
        self.ratelimit_calls = self.thekeys.ratelimit_calls         # Maximum number of calls that are allowed within the time interval.
        self.ratelimit_tokens = self.thekeys.ratelimit_tokens       # Maximum number of tokens that are allowed within the time interval.
        self.Costs_price = self.thekeys.Costs_price                 # Amount of euro's that a single ChatGPT-call costs.
        self.Costs_tokenportion = self.thekeys.Costs_tokenportion   # Amount of tokens that can maximally be within a single call to charge this price.
        
        self.api_rate_starttime = time.time()   # This will be the starting point to measure time for managing the API rate limits.
        self.api_rate_currenttime = 0.0         # This is the current time for the api rate limit. #tokens & #calls should stay below boundaries as song as current-start<timeunit.
        self.api_rate_currenttokens = 0         # Token counter to see if we pass the rate limit for the OpenAI API or not.
        self.api_rate_currentcalls = 0          # Call counter to see if we pass the rate limit for the OpenAI API or not.
        self.callcounter = 0                    # Internally counts the number of needed ChatGPT-calls for the document at hand; also used for a-priori cost estimation.
        self.api_totalprice = 0.0               # Total price of all calls made to the ChatGPT API.
        self.api_wrongcalls_duetomaxwhile = 0   # This counts the number of summaries that are incorrect but kept due to hitting the max on the while-loop.
        
        # Next, add all textelements:
        self.body = body()                      # This textpart will contain all body-text of the document
        self.footer = footer()                  # This textpart will contain all footer-text and header-text of the document
        self.headlines = headlines()            # This textpart will contain all headline-text of the document
        self.title = title()                    # This textpart will contain all title-text of the document
        self.enumeration = enumeration()        # This textpart will contain all enumerations/itemizations of the document
        # NOTE: Add new textparts here!
        
        # Next, add class members that we need for processing the data:
        self.textalineas = []                   # This textpart-array will contain the separate alineas (chapters, sections, subsections, etc.) of the document.
        self.textclassification = []            # This array of strings will mirror textpart.textcontent, but then with font sizes and enum-labels added.
        self.html_visualization = ""            # string that contains the html visualization of the summarized document.
        self.native_TOC = []                    # This Native_TOC_Element-array contains the different elements from the TOC of the PDF document. NOTE: Not every document has a TOC!
        self.logfile = []                       # This will become a logging .txt-file for ChatGPT-calls. The file is opened & closed in layered_summary().
        
        # Next, add parameters that we need, but are not already defined in textpart:
        self.MaxSummaryLength = 50              # maximum number of words a summary can have when we ask ChatGPT to make a summary from a given text.
        self.summarization_threshold = 50       # Texts with fewer words then this number will not be summarized at all. Instead, the original tekst is kept.
        self.UseDummySummary = True             # Decides whether we actually summarize tekst with ChatGPT, or blindly select the fisrt n words (dummy-summary).
        self.LanguageModel = "gpt-3.5-turbo"    # The language model for the ChatGPT API-completion that will be used (NB: tiktoken must support it as well).
        self.BackendChoice = "openai"           # This parameter keeps trach on which bakend-function for summarization should be used.
        self.LanguageChoice = "Default"         # This parameters controls in which language a text is summarized: Original/Ducth/English; Original means that the original language is kept. 
        self.LanguageTemperature = 0.1          # this is the temperature-parameter that is passed to ChatGPT. It should be strictly between 0 & 1.
        self.MaxCallRepeat = 20                 # Maximum number of repeats that we allow, when a response from ChatGPT does not match our criteria.
        
        # Next, add parameters to store high-level meta-data from the document:
        self.doc_metadata_author = "None"       # Author of the document, if this was stored as metadata (extracted with pypdf2)
        self.doc_metadata_creator = "None"      # Creator of the document, if this was stored as metadata (extracted with pypdf2)
        self.doc_metadata_producer = "None"     # Producer of the document, if this was stored as metadata (extracted with pypdf2)
        self.doc_metadata_subject = "None"      # Subject of the document, if this was stored as metadata (extracted with pypdf2)
        self.doc_metadata_title = "None"        # Title of the document, if this was stored as metadata (extracted with pypdf2)
        self.doc_metadata_fullstring = ""       # String as to how we display the output in our html visualisation.
        
    # Definition of getters:
    def get_MaxSummaryLength(self) -> int: return self.MaxSummaryLength
    def get_UseDummySummary(self) -> bool: return self.UseDummySummary
    def get_LanguageModel(self) -> str: return self.LanguageModel
    def get_LanguageChoice(self) -> str: return self.LanguageChoice
    def get_summarization_threshold(self) -> int: return self.summarization_threshold
    def get_LanguageTemperature(self) -> float: return self.LanguageTemperature
    def get_MaxCallRepeat(self) -> int: return self.MaxCallRepeat
    
    # Definition of setters:
    def set_MaxSummaryLength(self, newnum: int): self.MaxSummaryLength = newnum
    def set_UseDummySummary(self, newbool: bool): self.UseDummySummary = newbool
    def set_LanguageChoice(self, thechoice: str): self.LanguageChoice = thechoice
    def set_summarization_threshold(self, newnum: int): self.summarization_threshold = newnum
    def set_LanguageTemperature(self, newnum: float): self.LanguageTemperature = newnum
    def set_MaxCallRepeat(self, newnum: int): self.MaxCallRepeat = newnum
    set_LanguageModel = set_LanguageModel_textsplitter # NOTE: To check that one selects a valid model!
    
    # Definition of function to set all parameters to their default values:
    def standard_params(self):
        """
        This function simply sets the different parameters of the class to
        standard values. It is ideal for 'just running the code' instead of using
        advanced applications. 
        
        ATTENTION:
        It does not hold documentpath, documentname, outputpath.
        Those parameters should still be selected by the user.
        
        # Parameters: None
        # Return: None
        """
        
        self.set_labelname("TextSplitter")
        self.set_histogramsize(100)
        self.set_MaxSummaryLength(50)
        self.set_summarization_threshold(50)
        self.set_LanguageModel("gpt-3.5-turbo")
        self.set_LanguageChoice("Default")
        self.set_LanguageTemperature(0.1) # works nice for professional summaries.
        self.set_MaxCallRepeat(20) # should not be too low; most of the time we just take 1x attempt.
        self.set_ruleverbosity(0)
        self.set_UseDummySummary(True)
    
    # Definition of standard processing function:
    def process(self, verbose_option = 0) -> int:
        """
        This function simply calls the different processing modules of the class in
        standard order. It is ideal for 'just running the code' instead of using
        advanced applications. 
        
        # Parameters: None
        # Return: the number of textelements that have an empty summary but should not have one.
        """
        
        self.document_metadata()
        self.read_native_toc("pdfminer")
        self.textgeneration("pdfminer")
        self.calculate_footerboundaries(verbose_option)
        if (verbose_option>=0): self.export("default")
        self.fontsizehist(verbose_option)
        self.findfontregions()
        self.whitelinehist(verbose_option)
        self.findlineregions()
        self.passinfo()
        self.breakdown()
        self.shiftcontents()
        self.calculatetree()
        num_errors = self.layered_summary(verbose_option) # NOTE: Verbose-options -1, 0, 1, 2, 3, ...
        if (verbose_option>=0): self.exportdecisions()
        if (verbose_option>=0): self.exportalineas("default")
        html_mode = "standalone"
        if (verbose_option<0): html_mode = "django"
        self.alineas_to_html(html_mode)
        return num_errors
    
    # Definition of other class functionality (that is imported):
    rulecomparison = rulecomparison_textsplitter
    masterrule = masterrule_textsplitter
    passinfo = passinfo_textsplitter
    breakdown = breakdown_textsplitter
    exportalineas = exportalineas_textsplitter
    exportdecisions = exportdecisions_textsplitter
    calculatetree = calculatetree_textsplitter
    summarize = summarize_textsplitter
    summarize_dummy = summarize_dummy_textsplitter
    summarize_openai = summarize_openai_textsplitter
    summarize_huggingface = summarize_huggingface_textsplitter
    layered_summary = layered_summary_textsplitter
    alineas_to_html = alineas_to_html_textsplitter
    printcode = printcode_textsplitter
    read_native_toc = read_native_toc_textsplitter
    shiftcontents = shiftcontents_textsplitter
    document_metadata = document_metadata_textsplitter
