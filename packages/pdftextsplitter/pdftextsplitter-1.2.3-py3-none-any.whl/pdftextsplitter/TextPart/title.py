# Textpart imports:
from .textpart import textpart
from .CurrentLine import CurrentLine

class title(textpart):
    """
    This class is a specific textual element that inherits from textpart.
    It is meant to identify the title of a given document, using its
    own (overwritten) rule-function. All other functionality comes from 
    the parent-class.
    """

    # Definition of the default-constructor:
    def __init__(self):
        super().__init__() # First initiates all elements of textpart
        super().set_labelname("Title") # Then, change the label to reflext that this is about the title.
    
    # Definition of the specific Title-rule that filters out the title:
    def rule(self, thisline: CurrentLine) -> tuple[bool,int]: 
        # TODO: develop this rule-code (test-driven development)
        return False,0
