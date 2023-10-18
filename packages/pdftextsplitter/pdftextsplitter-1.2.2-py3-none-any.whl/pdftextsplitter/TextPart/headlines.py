# Python functionality:
import re

# Textpart imports:
from .textpart import textpart
from .CurrentLine import CurrentLine
from .regex_expressions import remove_nonletters
from .regex_expressions import contains_artikelregex
from .regex_expressions import contains_chapterregex
from .regex_expressions import contains_sectionregex
from .regex_expressions import contains_subsectionregex
from .regex_expressions import contains_subsubsectionregex
from .regex_expressions import contains_tablecontentsregex
from .regex_expressions import contains_headlines_regex
from .regex_expressions import contains_bigroman_enumeration
from .regex_expressions import contains_smallroman_enumeration
from .regex_expressions import contains_bigletter_enumeration
from .regex_expressions import contains_smallletter_enumeration
from .regex_expressions import contains_digit_enumeration
from .regex_expressions import contains_signmark_enumeration
from .enum_type import enum_type

class headlines(textpart):
    """
    This class is a specific textual element that inherits from textpart.
    It is meant to identify the headlines (chaper-tuiles, etc.) of a given document, using its
    own (overwritten) rule-function. All other functionality comes from 
    the parent-class.
    
    # For bold text: Plan_Velo:  41970 /13375 characters. ratio = 0.318680
    #                Cellar:    155903 / 1612 characters. ratio = 0.010340
    #                Copernicus: 16735 /  310 characters. ratio = 0.018524
    
    """

    # Definition of the default-constructor:
    def __init__(self):
        super().__init__() # First initiates all elements of textpart
        super().set_labelname("Headlines") # Then, change the label to reflext that this is about the headlines.
        self.hierarchy = []                # Duplicate of the same item in enumeration.
    
    # Definition of the specific headlines-rule that filters out the title:
    def rule(self, thisline: CurrentLine) -> tuple[bool,int]:
        
        # We ONLY use headlines that match all three of the following conditions: 
        # 1) it is preceded by either another headline, or a large whiteline
        # 2) it is either bold/highlighted, or a large fontsize, or it has a large whiteline below.
        # 3) It contains sufficient textual characters.
        
        if (self.ruleverbosity>0)and(self.verbosetextline in thisline.textline):
            print("--------------------------------------------------------------------")
            print(" ==> HEADLINES decision process for <" + str(thisline.textline) + ">")
        
        # Textual characters condition:
        Full_linelength = len(thisline.textline)
        pure_letters = remove_nonletters(thisline.textline)
        Nr_spaces = thisline.textline.count(" ")
        Letter_Length = len(pure_letters)
        Nospace_length = Full_linelength - Nr_spaces
        
        # Calculate ratio:
        letter_ratio = 1.0
        if (Nospace_length>0):
            letter_ratio = Letter_Length/Nospace_length
        Letter_condition = False
        if (letter_ratio>0.67): # This threshold is a very specific value needed.
            Letter_condition = True
        
        # Now, if the fontsize is large, we do not need to worry about this:
        if self.fontsize_biggerthenregular(thisline.fontsize):
            Letter_condition = True
        
        # Pass Plan-Velo:
        if contains_signmark_enumeration(thisline.textline):
            Letter_condition = True
        
        # Prevent single-character titles:
        if (Full_linelength==0)or (Full_linelength==1):
            Letter_condition = False
        
        # Take care of single-digit starters & SOME of the big romans (if we do all, we hit other problems like with C.or D. chapter titles...)
        # NOTE: we cannot allow single-digits because that will screw up article 413 of civillian law.
        if re.compile(r'^(\d+)(\.)(\d+)(\.)$').search(thisline.textline): Letter_condition = True
        if re.compile(r'^I(\.)$').search(thisline.textline): Letter_condition = True
        if re.compile(r'^II(\.)$').search(thisline.textline): Letter_condition = True
        if re.compile(r'^IV(\.)$').search(thisline.textline): Letter_condition = True
        if re.compile(r'^V(\.)$').search(thisline.textline): Letter_condition = True
        if re.compile(r'^VI(\.)$').search(thisline.textline): Letter_condition = True
        if re.compile(r'^IX(\.)$').search(thisline.textline): Letter_condition = True
        if re.compile(r'^X(\.)$').search(thisline.textline): Letter_condition = True
            
        # Give some output to show the decision process:
        if (self.ruleverbosity>0)and(self.verbosetextline in thisline.textline):
            print("Total number of characters in the line: " + str(Full_linelength))
            print("Number of characters (no spaces):       " + str(Nospace_length))
            print("Number of pure letters in the line:     " + str(Letter_Length))
            print("Ratio for testint:                      " + str(letter_ratio))
            print("Full Letter Condition = " + str(Letter_condition))
            print("")
        
        # Condition above:
        Above_Condition = False
        if thisline.previous_IsHeadline: Above_Condition = True # preceded by another headline
        if self.whiteline_isbig(thisline.previous_whiteline): Above_Condition = True # preceded by a alrge whiteline.
        
        # However, if a new chapter accidentally starts at the top of the page, we must not dismiss it:
        if (Above_Condition==False)and(abs(thisline.vertical_position - self.max_vertpos)<3.0):
            # Then, we want to allow this. But if the layout did not mark this line appropriately,
            # we must check the regex as additional safety:
            Above_Condition = False
            if (contains_tablecontentsregex(thisline.textline)): Above_Condition = True
            if (contains_headlines_regex(thisline.textline)): Above_Condition = True
            # This is to make sure that we pass SplitDoc-tests.
        
        # If it is the top of the document:
        if (Above_Condition==False)and((abs(thisline.vertical_position+2.0)<1e-3)or(abs(thisline.vertical_position+1.0)<1e-3)):
            # Then, we want to allow this. But if the layout did not mark this line appropriately,
            # we must check the regex as additional safety:
            Above_Condition = False
            if (contains_tablecontentsregex(thisline.textline)): Above_Condition = True
            if (contains_headlines_regex(thisline.textline)): Above_Condition = True
            # This is to make sure that we pass SplitDoc-tests.
        
        # Next, the very first line of the document gets a special treatment:
        if (abs(thisline.previous_whiteline+1.0)<1e-3):
            Above_Condition = True
            # This is to make sure that we pass SplitDoc-tests.
            
        # Also, if a lot of other conditions are satisfied, we skip the above-condition:
        if (contains_headlines_regex(thisline.textline)):
            if self.fontsize_biggerthenregular(thisline.fontsize):
                if (thisline.next_whiteline>1.75*self.findregularlineregion().get_value()):
                    Above_Condition = True
                
        # Give some output to show the decision process:
        if (self.ruleverbosity>0)and(self.verbosetextline in thisline.textline):
            print("Previous Line Is Headline: " + str(thisline.previous_IsHeadline))
            print("Previous WhiteLine Is Big: " + str(self.whiteline_isbig(thisline.previous_whiteline)) + "; value = " + str(thisline.previous_whiteline))
            print("Thisline in Table of Contents (Regex): " + str(contains_tablecontentsregex(thisline.textline)))
            print("Thisline in Headline (Regex):          " + str(contains_headlines_regex(thisline.textline)))
            print("Full Above Condition = " + str(Above_Condition))
            print("")
     
        # Condition below:
        Below_condition = False
        if self.whiteline_isbig(thisline.next_whiteline): Below_condition = True # followed by a large whiteline
        if self.fontsize_biggerthenregular(thisline.fontsize): Below_condition = True # Large fontsize.
        
        # Do textual layout like bold fonts, highlight, etc. separately:
        Layout_Condition = False
        if (thisline.is_bold)and(self.boldchars_ratio<self.boldratio_threshold): Layout_Condition = True # bold font style; if bold is suffiently scarse that it has meaning for headlines.
        if (thisline.is_highlighted): Layout_Condition = True # Highlighted font-style (textmarker).
        if Layout_Condition: Below_condition = True
        
        # However, we do NOT just want to start a new headline if we have regular tekst that just happens
        # to be a single line. On the other hand, not everyone marks headlines by fontsizes or styles.
        # So, adapt Below_condition based on regex:
        if self.whiteline_isbig(thisline.next_whiteline):
            if not Layout_Condition:
                if not self.fontsize_biggerthenregular(thisline.fontsize):
                    
                    # Then, in this case we demand that at least some regex has to fire:
                    Below_condition = False
                    if (contains_tablecontentsregex(thisline.textline)): Below_condition = True
                    if (contains_headlines_regex(thisline.textline)): Below_condition = True
                    # This is to make sure that we pass SplitDoc-tests.
                    
                    # But, if the regex fires, make sure that it was not yet detected as an enumeration before (Copernicus):
                    if Below_condition:
                        if (contains_bigroman_enumeration(thisline.textline))and(enum_type.BIGROMAN in self.hierarchy): Below_condition = False
                        if (contains_smallroman_enumeration(thisline.textline))and(enum_type.SMALLROMAN in self.hierarchy): Below_condition = False
                        if (contains_bigletter_enumeration(thisline.textline))and(enum_type.BIGLETTER in self.hierarchy): Below_condition = False
                        if (contains_smallletter_enumeration(thisline.textline))and(enum_type.SMALLLETTER in self.hierarchy): Below_condition = False
                        if (contains_digit_enumeration(thisline.textline,self.whiteline_isbig(thisline.next_whiteline)))and(enum_type.DIGIT in self.hierarchy): Below_condition = False
                        if (contains_signmark_enumeration(thisline.textline))and(enum_type.SIGNMARK in self.hierarchy): Below_condition = False
                        
                    # In case we missed an enumeration because it is the first element in the hierarchy:
                    if re.compile(r':$').search(thisline.textline): Below_condition = False
        
        # Give some output to show the decision process:
        if (self.ruleverbosity>0)and(self.verbosetextline in thisline.textline):
            print("Bold ratio in document:       " + str(self.boldchars_ratio) + " (threshold = " + str(self.boldratio_threshold) + ")")
            print("Next WhiteLine Is Big:        " + str(self.whiteline_isbig(thisline.next_whiteline)) + "; value = " + str(thisline.next_whiteline))
            print("This textline is Bold:        " + str(thisline.is_bold))
            print("This textline is Highlighted: " + str(thisline.is_highlighted))
            print("This Fontsize is Big:         " + str(self.fontsize_biggerthenregular(thisline.fontsize)) + "; value = " + str(thisline.fontsize))
            print("Full Below Condition =        " + str(Below_condition))
            print("")
        
        # Next, Unify the conditions:
        Headline_Condition = (Above_Condition)and(Below_condition)and(Letter_condition)
        
        # Now, if the previous line is a headline and an article and this one is a digit enumeration,
        # this one cannot be a headlines:
        if (thisline.previous_IsHeadline==True):
            if (contains_artikelregex(thisline.previous_textline)==True):
                if (contains_digit_enumeration(thisline.textline,self.whiteline_isbig(thisline.next_whiteline))==True):
                    Headline_Condition = False
        
        # Give some output to show the decision process:
        if (self.ruleverbosity>0)and(self.verbosetextline in thisline.textline):
            print("Full HEADLINE Condition = " + str(Headline_Condition))
            print("")
        
        # Next, attempt to come up with a reasonable guess for the cascadelevel:
        cascadelevel = 0
        
        # We only need this information to be OK if we actually found a headline.
        # So better not to waste CPU-power:
        if Headline_Condition: 
            
            # See if fontsize is going to help us:
            if self.fontsize_biggerthenregular(thisline.fontsize):
                # This is easy:
                cascadelevel = self.selectfontregion(thisline.fontsize).get_cascadelevel()
            else:
                # This is harder:
                cascadelevel = self.findregularfontregion().get_cascadelevel()-1
                if (cascadelevel<0): cascadelevel = 0
            
            # Next, improve our guesses using regex:
            if (contains_tablecontentsregex(thisline.textline)):
                cascadelevel = 1
            
            if (contains_chapterregex(thisline.textline)):
                cascadelevel = 1
                
            if (contains_sectionregex(thisline.textline)):
                cascadelevel = 2
            
            if (contains_subsectionregex(thisline.textline)):
                cascadelevel = 3
                
            if (contains_subsubsectionregex(thisline.textline)):
                cascadelevel = 4
            
            # TODO: If a level is taken by regex, then we need to change it that this level
            # can no longer be guesses from fontsizes.
            
            # However, if the previous line was also a headline, we must NEVER change cascade levels,
            # unless we are in the table-of-contents (that one is already taken care of), or if the new one fires on a regex:
            if (not((contains_tablecontentsregex(thisline.textline))or(contains_headlines_regex(thisline.textline)))):
                
                # But we should only do this, if the previous one and this one belong to the same font region:
                prev_region = self.selectfontregion(thisline.previous_fontsize)
                this_region = self.selectfontregion(thisline.fontsize)
                if (abs(prev_region.get_value()-this_region.get_value())<1e-3):
                    if thisline.previous_IsHeadline: cascadelevel = thisline.previous_Headlines_cascade
        
        # Give some output to show the decision process:
        if (self.ruleverbosity>0)and(self.verbosetextline in thisline.textline):
            print("Thisline in Chapter (Regex):       " + str(contains_chapterregex(thisline.textline)))
            print("Thisline in Section (Regex):       " + str(contains_sectionregex(thisline.textline)))
            print("Thisline in SubSection (Regex):    " + str(contains_subsectionregex(thisline.textline)))
            print("Thisline in SubSubSection (Regex): " + str(contains_subsubsectionregex(thisline.textline)))
            print("")
            print("Calculated Cascade Level: " + str(cascadelevel))
            print("")
        
        # Return the final answer:
        return Headline_Condition,cascadelevel
