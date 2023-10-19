# Python functionality:
import re

# Textpart imports:
from .textpart import textpart
from .CurrentLine import CurrentLine
from .enum_type import enum_type
from .regex_expressions import contains_bigroman_enumeration
from .regex_expressions import contains_smallroman_enumeration
from .regex_expressions import contains_bigletter_enumeration
from .regex_expressions import contains_smallletter_enumeration
from .regex_expressions import contains_digit_enumeration
from .regex_expressions import contains_signmark_enumeration
from .regex_expressions import contains_smallalphabetic_order
from .regex_expressions import contains_bigalphabetic_order
    
class enumeration(textpart):
    """
    This class is a specific textual element that inherits from textpart.
    It is meant to identify all kinds of enumerations (including their 
    hierarchy) like 1), 2), 3),... or I. II. III. etc. It uses its
    own (overwritten) rule-function. All other functionality comes from 
    the parent-class.
    """

    # Definition of the default-constructor:
    def __init__(self):
        super().__init__()                      # First initiates all elements of textpart
        super().set_labelname("Enumeration")    # Then, change the label to reflext that this is about the title.
        self.hierarchy = []                     # Array with different enum_type-elements. It decided upon the hierarchy of enumeration types.
        self.last_enumtype_index = 0            # index in hierarchy of the enum-type found the last time we appointed an enumeration.
        self.this_enumtype_index = 0            # index in hierarchy of the enum-type found this time when we appoint an enumeration (which is one of the 6).
        self.last_textline_bigroman = ""        # The textline from the previous time we appointed an enumeration to be bigroman.
        self.last_textline_smallroman = ""      # The textline from the previous time we appointed an enumeration to be smallroman.
        self.last_textline_bigletter = ""       # The textline from the previous time we appointed an enumeration to be bigletter.
        self.last_textline_smallletter = ""     # The textline from the previous time we appointed an enumeration to be smallletter.
        self.last_textline_digit = ""           # The textline from the previous time we appointed an enumeration to be digit.
        self.last_textline_signmark = ""        # The textline from the previous time we appointed an enumeration to be signmark.
    
    # Definition of the specific enumeration-rule that filters out the enumerations in the document:
    def rule(self, thisline: CurrentLine) -> tuple[bool,int]: 
        
        # The challenge is not so much to detect the different enumerations (this is easy with regex),
        # but to auto-detect their hierarchy. This is done by the first for-loop. Then, by the second
        # part, we add to the hierarchy if we have something that was not previously detected.
        
        # ---------------------------------------------------------------------------------------------
        
        # Calculate some variables we may need:
        nextline_isbig = self.whiteline_isbig(thisline.next_whiteline)
        
        # Give some output in case we want to monitor the decision process:
        if (self.ruleverbosity>0)and(self.verbosetextline in thisline.textline):
            print("--------------------------------------------------------------------")
            print(" ==> ENUMERATION decision process for <" + str(thisline.textline) + ">")
            print("Thisline in BigRoman (Regex):    " + str(contains_bigroman_enumeration(thisline.textline)))
            print("Thisline in SmallRoman (Regex):  " + str(contains_smallroman_enumeration(thisline.textline)))
            print("Thisline in BigLetter (Regex):   " + str(contains_bigletter_enumeration(thisline.textline)))
            print("Thisline in SmallLetter (Regex): " + str(contains_smallletter_enumeration(thisline.textline)))
            print("Thisline in Digit (Regex):       " + str(contains_digit_enumeration(thisline.textline,nextline_isbig)))
            print("Thisline in Signmark (Regex):    " + str(contains_signmark_enumeration(thisline.textline)))
            print("")
            print("HIERACRCHY before the enumeration-rule is applied:")
            print(self.hierarchy)
            print("")
        
        # Begin with declaring the variables we need:
        Answer = False
        ThisCascade = thisline.current_cascade
        bigroman_isfound = False
        smallroman_isfound = False
        bigletter_isfound = False
        smallletter_isfound = False
        digit_isfound = False
        signmark_isfound = False
        
        # Next, loop through the elements of the hierarchy and attempt to detect the 
        # enumerations first that are already in the hierarchy:
        element_index = 0
        for one_element in self.hierarchy:
            
            # BIGROMAN type:
            if (one_element==enum_type.BIGROMAN)and(Answer==False):
                if contains_bigroman_enumeration(thisline.textline):
                    Answer = True
                    bigroman_isfound = True
                    self.this_enumtype_index = element_index
                    ThisCascade = thisline.current_cascade + element_index + 1
            
            # SMALLROMAN type:
            if (one_element==enum_type.SMALLROMAN)and(Answer==False):
                if contains_smallroman_enumeration(thisline.textline):
                    Answer = True
                    smallroman_isfound = True
                    self.this_enumtype_index = element_index
                    ThisCascade = thisline.current_cascade + element_index + 1
                    
            # BIGLETTER type:
            if (one_element==enum_type.BIGLETTER)and(Answer==False):
                if contains_bigletter_enumeration(thisline.textline):
                    Answer = True
                    bigletter_isfound = True
                    self.this_enumtype_index = element_index
                    ThisCascade = thisline.current_cascade + element_index + 1
            
            # SMALLLETTER type:
            if (one_element==enum_type.SMALLLETTER)and(Answer==False):
                if contains_smallletter_enumeration(thisline.textline):
                    Answer = True
                    smallletter_isfound = True
                    self.this_enumtype_index = element_index
                    ThisCascade = thisline.current_cascade + element_index + 1
                    
            # DIGIT type:
            if (one_element==enum_type.DIGIT)and(Answer==False):
                if contains_digit_enumeration(thisline.textline,nextline_isbig):
                    Answer = True
                    digit_isfound = True
                    self.this_enumtype_index = element_index
                    ThisCascade = thisline.current_cascade + element_index + 1
                    
            # SIGNMARK type:
            if (one_element==enum_type.SIGNMARK)and(Answer==False):
                if contains_signmark_enumeration(thisline.textline):
                    Answer = True
                    signmark_isfound = True
                    self.this_enumtype_index = element_index
                    ThisCascade = thisline.current_cascade + element_index + 1
                    
            # Increase index:
            element_index = element_index + 1
        
        # ---------------------------------------------------------------------------------------------
        
        # Next, we have to tackle the problem of roman numbers versus letters. If both are true at the same time, we must
        # use the alpabetic order with the previous time we found a letter to decide upon roman versus letter.
        # NOTE: This would make it hard to start a new roman-series under point h). However, even utilizing horizontal
        # positions would NOT make this a 100% solution, as the author may not have used those layout-options...
        # TODO: Fix the problem of roman numbers starting under h). 
        if (contains_smallroman_enumeration(thisline.textline))and(contains_smallletter_enumeration(thisline.textline)):
            
            # Then, look for the alphabetic order:
            if (contains_smallalphabetic_order(self.last_textline_smallletter,thisline.textline)):
                
                # In that case, we will choose letters:
                search_index = -1
                loop_index = 0
                        
                for one_element in self.hierarchy:
                    if (one_element==enum_type.SMALLLETTER):
                        search_index = loop_index
                    loop_index = loop_index + 1
                                
                if (search_index>=0):
                    ThisCascade = thisline.current_cascade + search_index + 1
                    self.this_enumtype_index = search_index
                    Answer = True
                else:
                    self.hierarchy.append(enum_type.SMALLLETTER)
                    ThisCascade = thisline.current_cascade + len(self.hierarchy)
                    self.this_enumtype_index = len(self.hierarchy)-1
                    Answer = True
            
            else:
                
                # Then, we choose small romans:
                search_index = -1
                loop_index = 0
                        
                for one_element in self.hierarchy:
                    if (one_element==enum_type.SMALLROMAN):
                        search_index = loop_index
                    loop_index = loop_index + 1
                                
                if (search_index>=0):
                    ThisCascade = thisline.current_cascade + search_index + 1
                    self.this_enumtype_index = search_index
                    Answer = True
                else:
                    self.hierarchy.append(enum_type.SMALLROMAN)
                    ThisCascade = thisline.current_cascade + len(self.hierarchy)
                    self.this_enumtype_index = len(self.hierarchy)-1
                    Answer = True
        
        # ---------------------------------------------------------------------------------------------
        
        # Next, do the same for big romans & letters:
        # TODO: Fix the problem of roman numbers starting under H). 
        if (contains_bigroman_enumeration(thisline.textline))and(contains_bigletter_enumeration(thisline.textline)):
            
            # Then, look for the alphabetic order:
            if (contains_bigalphabetic_order(self.last_textline_bigletter,thisline.textline)):
                
                # In that case, we will choose letters:
                search_index = -1
                loop_index = 0
                        
                for one_element in self.hierarchy:
                    if (one_element==enum_type.BIGLETTER):
                        search_index = loop_index
                    loop_index = loop_index + 1
                                
                if (search_index>=0):
                    ThisCascade = thisline.current_cascade + search_index + 1
                    self.this_enumtype_index = search_index
                    Answer = True
                else:
                    self.hierarchy.append(enum_type.BIGLETTER)
                    ThisCascade = thisline.current_cascade + len(self.hierarchy)
                    self.this_enumtype_index = len(self.hierarchy)-1
                    Answer = True
            
            else:
                
                # Then, we choose big romans:
                search_index = -1
                loop_index = 0
                        
                for one_element in self.hierarchy:
                    if (one_element==enum_type.BIGROMAN):
                        search_index = loop_index
                    loop_index = loop_index + 1
                                
                if (search_index>=0):
                    ThisCascade = thisline.current_cascade + search_index + 1
                    self.this_enumtype_index = search_index
                    Answer = True
                else:
                    self.hierarchy.append(enum_type.BIGROMAN)
                    ThisCascade = thisline.current_cascade + len(self.hierarchy)
                    self.this_enumtype_index = len(self.hierarchy)-1
                    Answer = True
        
        # ---------------------------------------------------------------------------------------------
                    
        # Then, test for all the items that we could not find in the hierarchy.
        # NB: The order here is important! We also test each one for
        # Answer being False, so that we cannot detect multiple
        # answers (& add them to the hierarchy) at the same textline.
        if (Answer==False):
            if (bigroman_isfound==False):
                if contains_bigroman_enumeration(thisline.textline):
                    Answer = True
                    self.hierarchy.append(enum_type.BIGROMAN)
                    ThisCascade = thisline.current_cascade + len(self.hierarchy)
                    self.this_enumtype_index = len(self.hierarchy) - 1
        
        if (Answer==False):
            if (smallroman_isfound==False):
                if contains_smallroman_enumeration(thisline.textline):
                    Answer = True
                    self.hierarchy.append(enum_type.SMALLROMAN)
                    ThisCascade = thisline.current_cascade + len(self.hierarchy)
                    self.this_enumtype_index = len(self.hierarchy) - 1
        
        if (Answer==False):
            if (bigletter_isfound==False):
                if contains_bigletter_enumeration(thisline.textline):
                    Answer = True
                    self.hierarchy.append(enum_type.BIGLETTER)
                    ThisCascade = thisline.current_cascade + len(self.hierarchy)
                    self.this_enumtype_index = len(self.hierarchy) - 1
        
        if (Answer==False):
            if (smallletter_isfound==False):
                if contains_smallletter_enumeration(thisline.textline):
                    Answer = True
                    self.hierarchy.append(enum_type.SMALLLETTER)
                    ThisCascade = thisline.current_cascade + len(self.hierarchy)
                    self.this_enumtype_index = len(self.hierarchy) - 1
        
        if (Answer==False):
            if (digit_isfound==False):
                if contains_digit_enumeration(thisline.textline,nextline_isbig):
                    Answer = True
                    self.hierarchy.append(enum_type.DIGIT)
                    ThisCascade = thisline.current_cascade + len(self.hierarchy)
                    self.this_enumtype_index = len(self.hierarchy) - 1
        
        if (Answer==False):
            if (signmark_isfound==False):
                if contains_signmark_enumeration(thisline.textline):
                    Answer = True
                    self.hierarchy.append(enum_type.SIGNMARK)
                    ThisCascade = thisline.current_cascade + len(self.hierarchy)
                    self.this_enumtype_index = len(self.hierarchy) - 1
        
        # ---------------------------------------------------------------------------------------------
        
        # Next, we know that we cannot get an enumeration IF the previous textline is broken off:
        if thisline.previousline_IsBroken: Answer = False
        
        # Next, fill previous quanities:
        if (len(self.hierarchy)>0)and(Answer==True):
            self.last_enumtype_index = self.this_enumtype_index
            if (self.hierarchy[self.this_enumtype_index]==enum_type.BIGROMAN): self.last_textline_bigroman = thisline.textline
            if (self.hierarchy[self.this_enumtype_index]==enum_type.SMALLROMAN): self.last_textline_smallroman = thisline.textline
            if (self.hierarchy[self.this_enumtype_index]==enum_type.BIGLETTER): self.last_textline_bigletter = thisline.textline
            if (self.hierarchy[self.this_enumtype_index]==enum_type.SMALLLETTER): self.last_textline_smallletter = thisline.textline
            if (self.hierarchy[self.this_enumtype_index]==enum_type.DIGIT): self.last_textline_digit = thisline.textline
            if (self.hierarchy[self.this_enumtype_index]==enum_type.SIGNMARK): self.last_textline_signmark = thisline.textline
            
        # Give some more verbose-output:
        if (self.ruleverbosity>0)and(self.verbosetextline in thisline.textline):
            print("HIERACRCHY after the enumeration-rule is applied:")
            print(self.hierarchy)
            print("")
            print("Final decision = " + str(Answer))
            print("Obtained cascade = " + str(ThisCascade))
            print("Base Cascade (of headline) = " + str(thisline.current_cascade))
            print("")
        
        # ---------------------------------------------------------------------------------------------
        
        # Finally, return the answer:
        return Answer,ThisCascade
