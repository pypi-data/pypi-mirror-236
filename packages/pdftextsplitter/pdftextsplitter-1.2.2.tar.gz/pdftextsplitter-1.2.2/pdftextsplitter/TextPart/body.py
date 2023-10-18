# Textpart imports:
from .textpart import textpart
from .CurrentLine import CurrentLine

class body(textpart):
    """
    This class is a specific textual element that inherits from textpart.
    It is meant to identify the body of a given document, using its
    own (overwritten) rule-function. All other functionality comes from 
    the parent-class.
    """

    # Definition of the default-constructor:
    def __init__(self):
        super().__init__() # First initiates all elements of textpart
        super().set_labelname("Body") # Then, change the label to reflext that this is about the body.
    
    # Definition of the specific Title-rule that filters out the title:
    def rule(self, thisline: CurrentLine) -> tuple[bool,int]: 
        # NOTE: continue to refine this rule-code (test-driven development)
        
        # NOTE: Assuming that fontregions have been created:
        fontsize_isregular = self.fontsize_equalstoregular(thisline.fontsize)
        body_level = self.findregularfontregion().get_cascadelevel()
        
        # Return the final asnwer:
        return fontsize_isregular,body_level
