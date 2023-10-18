# Textpart imports:
from .CurrentLine import CurrentLine
from .textpart import textpart
from .masterrule import texttype
from .enum_type import enum_type

class textalinea(textpart):
    """
    This class is a specific textual element that inherits from textpart.
    It is meant to identify an alinea of a given document, using its
    own (overwritten) rule-function. textalinea's can come in different
    levels. To support this splitting of levels, this class has some added
    functionality on top of textpart.    
    """

    # Definition of the default-constructor:
    def __init__(self):
        super().__init__() # First initiates all elements of textpart
        super().set_labelname("Alinea") # Then, change the label to reflext that this is about the title.
        
        # Core variables necessary to create the layered summary:
        self.textlevel = 0                      # 0 = whole document, 1 = chapter, 2 = section, etc. Each time, we dive deeper into the document.
        self.typelevel = 0                      # textlevel of a specific element. This always starts at 0 for an enumeration, while textlevel starts at the chapter/section/etc.
        self.texttitle = ""                     # title of this part of the document.
        self.nativeID = -1                      # ID is filled during breakdown() of textsplitter and this will perserve the natural order (parentID will always point OK to this).
        self.parentID = -1                      # pythonindex (0 till n-1) of the parent element in native ordering: the chapter the current section belongs to, etc. -1 means: parent=full doc.
        self.horizontal_ordering = -1           # When multiple elements point to the same parent, this (starting at 0) will give the proper ordering of these elements. -1 means: unknown.
        self.summary = ""                       # This field yields a textual summary of the textcontent-field (inherited from textpart).
        self.sum_CanbeEmpty = False             # This flag is used in layered summaries to determine when a child's summary can be empty and when not.
        self.alineatype = texttype.UNKNOWN      # This hold the texttype appointed by the masterrule at the moment the alinea was created.
        self.enumtype = enum_type.UNKNOWN       # If the alinea was created as an enumeration-type, this will hold the type of enumeration that was appointed.
        
        # html visualization variables:
        self.html_visualization = ""            # This string is used to build nice html-visualizations per textalinea, which can then be collected.
        
        # meta-data variables:
        self.summarized_wordcount = 0           # This string holds the number of words in the summary plus the number of words in the titles of the direct children.
        self.total_wordcount = 0                # This holds the number of words of textcontent in ALL children (direct or indirect) under the textalinea element.
        self.nr_decendants = 0                  # This holds all textalinea-objects that live under this item. If there are no smaller structure elements in the text, this is 0.
        self.nr_children = 0                    # Like nr_decendants, but now we only count objects that directly below this one.
        self.nr_depths = 0                      # This is how deep we can go somewhere in the structure. 0 at the highest cascade level and so on.
        self.nr_pages = 0                       # The number of pages of this textpart (including all decendants) as how it appears in the text.
    
    # Definition of the specific textalinea-rule that determines whether a textline should be in this alinea or not.
    def rule(self, thisline: CurrentLine) -> tuple[bool,int]: 
        # NOTE: At this moment, this function serves no purpose in textalinea, so keep it equal to textpart:
        return False,0
        

    # Definition of printing function:
    def printalinea(self):
        """
        Prints the content of the class (not all of it, just what you need to see
        if the document splitting works.)
        # Parameters: None (taken from the class).
        # Return: None (terminal-printed).
        """
        print("---------------------------------------------------------------------------------")
        print(" [ALINEA-TITLE] Cascade-level="+str(self.textlevel))
        print(" [TITLE] = " + self.texttitle)
        print(" parentID="+str(self.parentID)+" & horizontal_ordering="+str(self.horizontal_ordering))
        print(" texttype="+str(self.alineatype)+" & enumeration-type="+str(self.enumtype))
        print(" Summary Flag = "+str(self.sum_CanbeEmpty))
              
        print("\n")
        
        print(" [ALINEA-SUMMARY]:")
        print(self.summary)
            
        print("\n")
        
        print(" [ALINEA-CONTENT]:")
        for textline in self.textcontent:
            print(textline)
        
        print("\n")

    # Definition of function to compare different alinea's:
    def compare(self, other) -> bool:
        """
        This function decides when we call two given textalinea-elements
        the same. This is the case if the titles, textual content and textlevel are the same.
        We do not test on nativeID, parentID or horizontal_ordering, as those can only
        be the same if self and other come from the same array, which may not always
        be the case. When you know they are in the same array, use compare_samearray() instead
        to take these values along. For different arrays, use AlineasPresent.py if you want
        to test for these numbers too.
        
        # Parameters: textalinea: self & other: the two textalinea-elements to compare.
        # Return: bool: to decide if we call them the same or not.
        """
        
        title_compare = (self.texttitle==other.texttitle)
        level_compare = (self.textlevel==other.textlevel)
        flag_compare = (self.sum_CanbeEmpty==other.sum_CanbeEmpty)
        texttypecompare = (self.alineatype==other.alineatype)
        enumcompare = (self.enumtype==other.enumtype)
        
        summary_compare = False
        if (self.summary=="")and(other.summary==""): summary_compare = True
        if (not(self.summary==""))and(not(other.summary=="")): summary_compare = True
        
        allselftext = ""
        for textline in self.textcontent:
            allselftext +=textline
        allselftext.replace("\n"," ")
        
        allothertext = ""
        for textline in other.textcontent:
            allothertext += textline
        allothertext.replace("\n"," ")
        
        text_compare = (allselftext==allothertext)
        hor_compare = (self.horizontal_ordering==other.horizontal_ordering)
        
        return (title_compare)and(level_compare)and(text_compare)and(flag_compare)and(summary_compare)and(enumcompare)and(texttypecompare)and(hor_compare)
    
    # Definition of function to compare alineas when you know they belong to the same array:
    def compare_samearray(self, other) -> bool:
        """
        Does the same as the compare-function, but now it assumes that both textalinea-elements
        come from the same array, so we can indeed test for parentID's as well.
        
        # Parameters: textalinea: self & other: the two textalinea-elements to compare.
        # Return: bool: to decide if we call them the same or not.
        """
        native_compare = (self.nativeID==other.nativeID)
        parent_compare = (self.parentID==other.parentID)
        return (self.compare(other))and(parent_compare)and(native_compare)

    # Definition for printing python code so it is easy to design regression tests:
    def printcode(self, textfile):
        """
        This function will write python code to create a new textalinea-object filled with
        the data it has at the moment of calling this function. This code will be written 
        to the object textfile. This can be used to easily design regression tests by
        calling this function on all textalinea-objects when you know the output is
        as desired. Then, you can store the desired output hardcoded for easy comparison.
        
        # Parameters: textfile (a textfile-object to write the code to)
        # Return: Nothing (in that textfile)
        """
        if textfile.writable():
            textfile.write('    thisalinea = textalinea()\n')
            textfile.write('    thisalinea.textlevel = ' + str(self.textlevel) + '\n')
            textfile.write('    thisalinea.texttitle = "' + str(self.texttitle)+ '"\n')
            textfile.write('    thisalinea.nativeID = ' + str(self.nativeID) + '\n')
            textfile.write('    thisalinea.parentID = ' + str(self.parentID) + '\n')
            textfile.write('    thisalinea.alineatype = ' + str(self.alineatype) + '\n')
            textfile.write('    thisalinea.enumtype = ' + str(self.enumtype) + '\n')
            textfile.write('    thisalinea.horizontal_ordering = ' + str(self.horizontal_ordering) + '\n')
            textfile.write('    thisalinea.summary = "' + str(self.summary) + '"\n')
            textfile.write('    thisalinea.sum_CanbeEmpty = ' + str(self.sum_CanbeEmpty) + '\n')
            textfile.write('    thisalinea.textcontent.clear()\n')
            
            for thisline in self.textcontent:
                textfile.write('    thisalinea.textcontent.append("' + str(thisline) + '")\n')
            
            textfile.write('    alineas.append(thisalinea)\n')
            textfile.write('\n')
