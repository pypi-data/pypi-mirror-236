# Textpart imports:
from .textpart import textpart
from .CurrentLine import CurrentLine

class footer(textpart):
    """
    This class is a specific textual element that inherits from textpart.
    It is meant to identify the headers and footers of a given document, using its
    own (overwritten) rule-function. All other functionality comes from 
    the parent-class.
    """

    # Definition of the default-constructor:
    def __init__(self):
        super().__init__() # First initiates all elements of textpart
        super().set_labelname("Footer") # Then, change the label to reflext that this is about the headers and footers.
    
    # Definition of the specific Footer-rule that filters out the title:
    def rule(self, thisline: CurrentLine) -> tuple[bool,int]:
        # NOTE: continue to refine this rule-code (test-driven development)
        
        # NOTE: We use the lay-out boundaries for this:
        Answer = False
        if (thisline.vertical_position<self.footerboundary): Answer = True
        if (thisline.vertical_position>self.headerboundary): Answer = True
        
        # Assign body-txt+1 cascade level:
        text_level = self.findregularfontregion().get_cascadelevel()+1
        
        # Add another rule based on fontsize:
        if self.fontsize_smallerthenregular(thisline.fontsize): Answer = True
        
        # Return the final answer:
        return Answer,text_level
