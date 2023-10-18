class CurrentLine:
    """
    This stores the various aspects of a selected textline. s such, this class
    will serve as the input for the rule-functions of the textpart-class.
    Otherwise, the signature of the rule-functions becomes very messy. 
    """
    
    # Definition of the default-constructor:
    def __init__(self):
        self.textline = ""                      # String with the textual content of the textline we want to apply the rule to.
        self.previous_textline = ""             # String of the previous textline we applied a rule to.
        self.fontsize = 0.0                     # Fontsize of the (fisrt character of) the textline we want to apply the rule to.
        self.vertical_position = 0.0            # The vertical position (y0 of bbox) where the textline is found on the page.
        self.previous_whiteline = 0.0           # The vertical distance between the current textline and the PREVIOUS one (based on vertical_position).
        self.next_whiteline = 0.0               # The vertical distance between the current textline and the NEXT one (based on vertical_position).
        self.previous_IsHeadline = False        # This boolian states whether the previous textline was a headline or not.
        self.previous_Headlines_cascade = 0     # If previous_IsHeadline==True, this will hold the cascade level of that previous headline.
        self.previous_fontsize = 0.0            # Holds the fontsize of the previous textline.
        self.previousline_IsBroken = False      # States if the previous textline ends with a "-" character or not.
        self.current_cascade = 0                # Cascadelevel of the last time a new textalinea was created using headlines.
        self.is_italic = False                  # This is_italic boolean shows when the given textpart is italic.
        self.is_bold = False                    # This is_bold boolean shows when the given textpart is bold.
        self.is_highlighted = False             # This is_highlighted boolean shows when the given textpart is highlighted.
        self.current_pagenumber = 0             # The page number this textline was found on (note: file numbering starting at 1, not document-native numbering!)
    
    def printcode(self):
        """
        This is used to generate a hardcode-print of this object, which can then be
        used to contruct unit tests.
        # Parameters: None (taken from the class)
        # Return: None (printed on the screen)
        """
        
        print('    mytestline = CurrentLine()')
        print('    mytestline.textline = "' + str(self.textline)+'"')
        print('    mytestline.previous_textline = "' + str(self.previous_textline)+'"')
        print('    mytestline.fontsize = ' + str(self.fontsize))
        print('    mytestline.vertical_position = ' + str(self.vertical_position))
        print('    mytestline.previous_whiteline = ' + str(self.previous_whiteline))
        print('    mytestline.next_whiteline = ' + str(self.next_whiteline))
        print('    mytestline.previous_IsHeadline = ' + str(self.previous_IsHeadline))
        print('    mytestline.previous_Headlines_cascade = ' + str(self.previous_Headlines_cascade))
        print('    mytestline.previous_fontsize = ' + str(self.previous_fontsize))
        print('    mytestline.previousline_IsBroken = ' + str(self.previousline_IsBroken))
        print('    mytestline.current_cascade = ' + str(self.current_cascade))
        print('    mytestline.is_italic = ' + str(self.is_italic))
        print('    mytestline.is_bold = ' + str(self.is_bold))
        print('    mytestline.is_highlighted = ' + str(self.is_highlighted))
        print('    mytestline.current_pagenumber = ' + str(self.current_pagenumber))
        print('    textlines.append(mytestline)')
        print("")
        
        # Done.
        
