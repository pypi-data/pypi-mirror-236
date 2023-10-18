# import commands:
from enum import Enum
from regex_expressions import contains_tablecontentsregex
from regex_expressions import remove_nonletters
from stringmatch import stringmatch
from CurrentLine import CurrentLine

# textpart enumeration definition:
class texttype(Enum):
    UNKNOWN = 0
    TITLE = 1
    HEADLINES = 2
    FOOTER = 3
    BODY = 4
    ENUMERATION = 5
    # NOTE: Add new textparts here!
    
# function definition to combine the rules:
def rulecomparison_textsplitter(self, thisline: CurrentLine) -> tuple[texttype,int]:
    """
    This function utilizes the different rules from the different
    textparts (such as body, title, etc) that are members from
    textpart. Then, it combines those rules into a single masterrule
    to take the interdependencies into account.
    
    # Parameters 
    thisline (CurrentLine): CurrentLine-object that holds all the relevant information of the current textline 
                            masterrule should make a decision about. See documentation of CurrentLine.py
    # Return (texttype): an enumeration with the outcome of the different rules.
    # Return (int): the document cascade level belonging to this textline (0=entire doc, higher is deeper into the doc)
    """
    
    # ----------------------------------------------------------------------------
    
    # Start by declaring the answer:
    Answer_type = texttype.UNKNOWN
    Answer_level = 0
    
    # Next, calculate each of the different rules:
    [title_rule,title_level] = self.title.rule(thisline)
    [footer_rule, footer_level] = self.footer.rule(thisline)
    [headlines_rule, headlines_level] = self.headlines.rule(thisline)
    [body_rule, body_level] = self.body.rule(thisline)
    # NOTE: Add new textparts here!
    
    # NOTE: we should only call this line if it is not a headline, else
    # we risk contaminating the hierarchy-array:
    enum_rule = False
    enum_level = body_level
    if not headlines_rule:
        [enum_rule, enum_level] = self.enumeration.rule(thisline)
        
    # Transport latest status from enumeration to headlines:
    self.headlines.hierarchy = self.enumeration.hierarchy
     
    # ----------------------------------------------------------------------------
    
    # then, take care of the interdependencies:
    if (title_rule==True): 
        Answer_type = texttype.TITLE
        Answer_level = title_level
    
    elif (footer_rule==True): 
        Answer_type = texttype.FOOTER
        Answer_level = footer_level
        # NOTE: Footer comes before body, as the footer-rule utilizes the position-separation, but body does not necessarily overlap 100% with that.
        # You also do not want the regex to kick-in for footnotes, that usually start with a digit, but have very small fontsize.
        
    elif (headlines_rule==True): 
        Answer_type = texttype.HEADLINES
        Answer_level = headlines_level
        # NOTE: Headlines needs to come before body, as otherwise the body-rule for regular-size font-text will overrule regex-expressions.
        
    elif (enum_rule==True): 
        Answer_type = texttype.ENUMERATION
        Answer_level = enum_level
        
    elif (body_rule==True): 
        Answer_type = texttype.BODY
        Answer_level = body_level
        
    else: 
        Answer_type = texttype.UNKNOWN
        Answer_level = 0
        
    # NOTE: Add new textparts here! to elif-structure.
    # NOTE: Include their dependencies here!
    
    # ----------------------------------------------------------------------------
    
    # TODO: Find a better solution for tableofcontents-flag! 
    # TODO: Once that is done, redesign testMasterRule_b
    
    # Now manipulate tableofcontents-flag in headlines-element:
    if (contains_tablecontentsregex(thisline.textline))and(Answer_type==texttype.HEADLINES): 
        self.headlines.istableofcontents = True
        self.headlines.tableofcontentsindex = len(self.textalineas) # No -1 or something, because we call this one before the anlinea is created in breakdown-function.
        # Marking this, causes that if 'Chapter 1' has a smaller font then the title of chapter 1, the code does not break down by loosing track on the contents-alinea.
    
    # Calculate whether the start of the given textline is already present in the last alinea.
    # If that is the case, it means we should stop with the table of contents-situations & swicth
    # the regional expressions back on:
    if (self.headlines.istableofcontents==True):
        # We first test whether the istableofcontents is True. Otherwise, this procedure is
        # completely unneeded and it is costly.
        
        # Begin by setting a flag to whether we find a repeated textline:
        isrepeat = False
    
        # Find the correct alinea that contains the table of contents:
        if (self.headlines.tableofcontentsindex>=0)and(self.headlines.tableofcontentsindex<len(self.textalineas)):
            lastalinea = self.textalineas[self.headlines.tableofcontentsindex] 
        
            # Loop over the lines in the last alinea:
            for alinealine in lastalinea.textcontent:
            
                # Now test if there is sufficient agreement:
                alinealine_clean = remove_nonletters(alinealine)
                textline_clean = remove_nonletters(thisline.textline)
                relative_lengthdifference = abs(len(alinealine_clean)-len(textline_clean))
                lengthsum = len(alinealine_clean)+len(textline_clean)
                if (lengthsum>0): relative_lengthdifference = relative_lengthdifference/lengthsum
                else: relative_lengthdifference = 1.0                                                                                                             
                
                if (stringmatch(remove_nonletters(alinealine),remove_nonletters(thisline.textline))>0.7)and(relative_lengthdifference<0.25):
                    # ATTENTION: Be careful about changing parameters 0.7 & 0.25; Be sure to do regression tests after such an adaptation!!!
                    isrepeat = True
        
        # Now, if we somehow found the angreement and the flag isrepeat has been put to true,
        # we can manipulate the tableofcontents-flag:
        if (isrepeat==True): 
            self.headlines.istableofcontents = False
        
            # In that case, we must also recalculate the textlevel:
            [headlines_rule, headlines_level] = self.headlines.rule(thisline)
            Answer_level = headlines_level
            Answer_type = texttype.HEADLINES
    
    # ----------------------------------------------------------------------------
    
    # Return answer:
    return Answer_type, Answer_level

def masterrule_textsplitter(self, thisline: CurrentLine) -> bool:
    """
    This function translates the enumeration of rulecomparison_textsplitter into a boolian,
    based on the value of the label.
    
    # Parameters:
    thisline (CurrentLine): CurrentLine-object that holds all the relevant information of the current textline 
                            masterrule should make a decision about. See documentation of CurrentLine.py
    # Retuns: bool: the desicion on whether to add or not.
    """
    
    # ------------------------------------------------
    
    # Declare the answer:
    Answer = False
    
    # Calculate the enumeration:
    [thetype,thelevel] = self.rulecomparison(thisline)
    
    # test all texttypes:
    if (self.labelname=="Body")and(thetype==texttype.BODY): Answer = True
    if (self.labelname=="Title")and(thetype==texttype.TITLE): Answer = True
    if (self.labelname=="Footer")and(thetype==texttype.FOOTER): Answer = True
    if (self.labelname=="Headlines")and(thetype==texttype.HEADLINES): Answer = True
    if (self.labelname=="Enumeration")and(thetype==texttype.ENUMERATION): Answer = True
    # NOTE: Add new textparts here!
    
    # Return answer:
    return Answer
