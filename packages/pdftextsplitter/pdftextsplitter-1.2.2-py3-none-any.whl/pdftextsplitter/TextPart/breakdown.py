# Textpart imports:
from .masterrule import texttype
from .enum_type import enum_type
from .textalinea import textalinea
from .CurrentLine import CurrentLine
from .regex_expressions import contains_headlines_regex
from .regex_expressions import contains_chapterregex
from .regex_expressions import contains_pointtwo_enumeration
from .regex_expressions import contains_digit_enumeration

def breakdown_textsplitter(self):
    """
    This function will break a pdf document apart into its native structure
    of chapters, section, subsections, etc. A default number of structure
    elements is not necessary; the code works with so-called cascade-levels.
    0 = entire document, and each time we go into a smaller part of the
    document, we go one cascade level up. We start a new textpart
    (at arbitrary cascade level) once a new headline shows up.
    
    The decision process is made though the different textparts in
    textsplitter and their associated rules (that override the rule-function)
    in textpart, which they inherit from. The rules of the different
    textparts are then unified in the masterrule, which is what is used
    here to take depencencies between the textparts into account.
    
    If, based on these rules, texttype = HEADLINES (enumeration), we will
    start a new textalinea in textsplitter and if texttype = BODY, we
    will add the text to the current textalinea.
    
    Inside the body & headlines rule-function, different ways to identify
    headlines may be used. One of the supported methods is to look
    at fontsize. This can also be used to identify the cascade-levels.
    currently, fontsizes can only be obtained through the pdfminer option
    in the textgeneration-function and to utilize the fontsizes, one has to
    create font histograms and font regions too. This process is conveniently
    supported through the defaultinitialization function. Calling this
    function in textsplitter should then be done firts, then passinfo
    should be called and then, this function.
    
    # Parameters: None. Information comes from the class.
    # Return: None. Information is stored in self.textalineas
    
    """
    
    # ----------------------------------------------------------------------
    
    # Before we begin, we will create a mother-textalinea-object corresponding to the entire
    # document:
    self.textalineas.clear()
    newalinea = textalinea()
    newalinea.texttitle = self.documentname
    newalinea.textlevel = 0
    newalinea.typelevel = 0
    newalinea.alineatype = texttype.TITLE
    newalinea.enumtype = enum_type.UNKNOWN
    newalinea.textcontent.clear()
    newalinea.pagenumbers.clear()
    newalinea.nativeID = 0
    newalinea.parentID = -1
    self.textalineas.append(newalinea)
    
    # Begin by looping over all textlines in textcontent:
    lineindex = -1
    alineaindex = 0 # NOTE: on purpose, to point to the mother-object.
    pagenumberlength = len(self.pagenumbers)
    fontlength = len(self.fontsize_perline)
    poslength = len(self.positioncontent)
    whitelinelength = len(self.whitelinesize)
    bold_length = len(self.is_bold)
    italic_length = len(self.is_italic)
    highlight_length = len(self.is_highlighted)
    fontsize = 10.0
    this_pagenumber = 0
    textpos = 150.0
    previous_textline = ""
    previous_whiteline = 1.0
    next_whiteline = 1.0
    previous_isheadline = False
    previousline_IsBroken = False
    previous_headline_cascadelevel = 0
    previous_headline_alineaindex = -1 # NOTE: On purpose!
    previous_fontsize = 0
    current_cascade = 0 # NOTE: start with 0 on purpose!
    is_bold = False
    is_italic = False
    thisline = CurrentLine()
    self.textclassification.clear()
    self.enumeration.hierarchy.clear() # so we start with a clean list.
    is_bold = False
    is_italic = False
    is_highlighted = False
    
    # First, add fontregions to the textclassification:
    for region in self.fontregions:
        self.textclassification.append(region.exportregion())
    self.textclassification.append("\n\n")
    
    # Also, add lineregions to the textclassification:
    for region in self.lineregions:
        self.textclassification.append(region.exportregion())
    self.textclassification.append("\n\n")
     
    for textline in self.textcontent:
        
        # Begin by updating the lineindex:
        lineindex = lineindex + 1
        
        # Next, collect the fontsize too:
        if (lineindex<fontlength): fontsize = self.fontsize_perline[lineindex]
        
        # And vertical position:
        if (lineindex<poslength): textpos = self.positioncontent[lineindex]

        # And bold and italic text
        if (lineindex < bold_length): is_bold = self.is_bold[lineindex]
        if (lineindex < italic_length): is_italic = self.is_italic[lineindex]
        if (lineindex < highlight_length): is_highlighted = self.is_highlighted[lineindex]
        
        # And whitelines:
        if (lineindex<whitelinelength): previous_whiteline = self.whitelinesize[lineindex]
        if ((lineindex+1)<whitelinelength): next_whiteline = self.whitelinesize[lineindex+1]
        
        # And page numbers:
        if (lineindex<pagenumberlength): this_pagenumber = self.pagenumbers[lineindex]
        
        # Then, assemble the CurrentLine-object:
        thisline.textline = textline
        thisline.previous_textline = previous_textline
        thisline.fontsize = fontsize
        thisline.vertical_position = textpos
        thisline.previous_whiteline = previous_whiteline
        thisline.next_whiteline = next_whiteline
        thisline.is_bold = is_bold
        thisline.is_italic = is_italic
        thisline.is_highlighted = is_highlighted
        thisline.previousline_IsBroken = previousline_IsBroken
        thisline.previous_IsHeadline = previous_isheadline
        thisline.previous_Headlines_cascade = previous_headline_cascadelevel
        thisline.previous_fontsize = previous_fontsize
        thisline.current_cascade = current_cascade
        thisline.current_pagenumber = this_pagenumber
        
        # Then, call the enumeration-masterrule:
        [thetype,thecascadelevel] = self.rulecomparison(thisline)
        
        # Store the decidion in a separate array:
        self.textclassification.append("[FONTSIZE="+str(fontsize) + "] <=> [VERTPOS="+str(textpos) + "] <=> [WHITELINES="+str(previous_whiteline)+";"+str(next_whiteline)+"] <=> [TEXTLEVEL="+str(thecascadelevel)+"] <=> [TEXTLABEL=<" + str(thetype) + "] <=> [CONTENT=<" + textline + ">]")
        
        # ---------------------------------------------------------------------------------------
        # Next, decide if this is a headline:
        if (thetype==texttype.HEADLINES):
            
            # now, if the previous textline was NOT a headline (check by tag OR by shift in fontsize);
            # The shift in fontsize is needed, because otherwise a previous headline with a different fontsize is viewed as the same.
            # The regex is necessary to not get someting as TOELICHTING 1. CONTEXT OF THE PROPOSAL on the same alinea-title.
           
            # TODO: change fontsize-statement to a difference in two fontregions.
            if (previous_isheadline==False)or(abs(fontsize-previous_fontsize)>1e-3)or(contains_headlines_regex(textline)):
                
                # creat a new alinea:
                newalinea = textalinea()
            
                # Properly set the title
                newalinea.texttitle = textline.replace("\n","") # to prevent needless enters in the titles.
                
                # Add the cascade level:
                newalinea.textlevel = thecascadelevel
                # NOTE: If this is negative, it means it is worthless, because the code could not extract the level.
                
                # And its type:
                newalinea.alineatype = texttype.HEADLINES
                newalinea.enumtype = enum_type.UNKNOWN
                newalinea.typelevel = thecascadelevel-1
                
                # Add it to the array:
                self.textalineas.append(newalinea)
                
                # And update the index:
                alineaindex = len(self.textalineas)-1
                
                # Also, update the index that always remembers where the last new HEADLINES-textalinea was created:
                previous_headline_alineaindex = alineaindex
                
                # Only update this one when creating a new textalinea UNDER texttype.HEADLINES:
                current_cascade = thecascadelevel
                
                # and appoint nativeID of the new textalinea, as nativeID must be appointed in the order of creation:
                self.textalineas[alineaindex].nativeID = alineaindex
                
                # And, clear the hierarchy in enumeration, so that when a new chapter/section/etc. starts,
                # a new order of enumerations can be auto-detected:
                self.enumeration.hierarchy.clear()
                
            else:
                
                # In that case, the title of the chapter/section/etc
                # extends over multiple lines (which may or may not be on the same height, so this structure still applies), 
                # so we must add it to the title of the existing alinea, not create a new one:
                if (alineaindex>=0):
                    self.textalineas[alineaindex].texttitle = self.textalineas[alineaindex].texttitle + " " + textline.replace("\n","") # to prevent needless enters in the titles.
            
            # Next, if we encountered a headline, state this:
            previous_isheadline = True
            previous_headline_cascadelevel = thecascadelevel
            
            # Also, add it to the textcontent of the headlines:
            self.headlines.textcontent.append(textline)
            self.headlines.pagenumbers.append(this_pagenumber)
        
        else:
            
            # Then, we must reset the mark on whether the previous line is a headline:
            previous_isheadline = False
        
        # ---------------------------------------------------------------------------------------
        # Next, handle the enumerations. In this case, we must ALSO create a new textalinea-object.
        # However, unlike the headlines, enumerations do not have a specific title, so we do not 
        # need to worry about titles extending over different textlines. simply create a new 
        # object when enumerations hits to true.
        if (thetype==texttype.ENUMERATION):
            
            # creat a new alinea:
            newalinea = textalinea()
            
            # Properly set the title
            words_textline = textline.split()
            newalinea.texttitle = ""
            for k in range(0,6):
                if (len(words_textline)>k):
                    newalinea.texttitle = newalinea.texttitle + words_textline[k] + " "
            if (len(words_textline)>6):
                newalinea.texttitle = newalinea.texttitle + "..."
            
            # And its type:
            hierarchy_index = thecascadelevel - 1 - current_cascade
            newalinea.alineatype = texttype.ENUMERATION
            newalinea.enumtype = self.enumeration.hierarchy[hierarchy_index]
            newalinea.typelevel = hierarchy_index
               
            # Add the cascade level:
            newalinea.textlevel = thecascadelevel
            # NOTE: If this is negative, it means it is worthless, because the code could not extract the level.
            
            # Add the first textline:
            newalinea.textcontent.append(textline)
            newalinea.pagenumbers.append(this_pagenumber)
                
            # Add it to the array:
            self.textalineas.append(newalinea)
                
            # And update the index:
            alineaindex = len(self.textalineas)-1
                
            # and appoint nativeID of the new textalinea, as nativeID must be appointed in the order of creation:
            self.textalineas[alineaindex].nativeID = alineaindex
            
            # Finally, also add the line to the body of the enumeratio-object:
            self.enumeration.textcontent.append(textline)
            self.enumeration.pagenumbers.append(this_pagenumber)
            
            # Now, in case this is a 2.-enumeration and the previous one is both a headline and an enumeration, 
            # we must adapt the previous alinea from headline to enumeration:
            if contains_pointtwo_enumeration(textline,False):
                
                # Then, collect the previous alinea:
                test_alineaindex = alineaindex-1
                if (test_alineaindex>=0):
                    
                    # Collect its title:
                    alinea_totest = self.textalineas[test_alineaindex]
                    title_totest = alinea_totest.texttitle
                    
                    # Test that it is both a chapter and an enumeration:
                    if (contains_digit_enumeration(title_totest,False))and(contains_chapterregex(title_totest)):
                        
                        # Test that it also is a chapter:
                        if (alinea_totest.alineatype==texttype.HEADLINES):
                        
                            # Then, we should adapt the alinea. Start by adapting the content:
                            alinea_totest.textcontent.insert(0,title_totest)
                        
                            # Appropriately change the title:
                            words_textline = title_totest.split()
                            alinea_totest.texttitle = ""
                            for k in range(0,6):
                                if (len(words_textline)>k):
                                    alinea_totest.texttitle = alinea_totest.texttitle + words_textline[k] + " "
                            if (len(words_textline)>6):
                                alinea_totest.texttitle = alinea_totest.texttitle + "..."
                        
                            # Change the type:
                            alinea_totest.alineatype = texttype.ENUMERATION
                            alinea_totest.enumtype = enum_type.DIGIT
                            alinea_totest.typelevel = newalinea.typelevel
                            alinea_totest.textlevel = thecascadelevel+1 # Because enumeration will still give the wrong cascade level.
                            
                            # Also adapt the other cascades:
                            current_cascade = current_cascade + 1
                            self.textalineas[alineaindex].textlevel = self.textalineas[alineaindex].textlevel + 1
                            
                            # Put it back into the array:
                            self.textalineas[test_alineaindex] = alinea_totest
                            
                            # Update previous headline index:
                            Found_Headline = False
                            for k in range(0,test_alineaindex):
                                k_index = test_alineaindex-k-1 # NOTE: reverse-looping:
                                
                                # test if this is a headlines:
                                if (Found_Headline==False)and(self.textalineas[k_index].alineatype==texttype.HEADLINES):
                                    
                                    # Then, change the previous alinea_index:
                                    Found_Headline = True
                                    previous_headline_alineaindex = k_index
                            
                            # Done.
            
        # ---------------------------------------------------------------------------------------
        # Next, decide what happens if it is a body:
        if (thetype==texttype.BODY):
            
            # Next, we must make sure that we switch back to the last headlines-alinea IF
            # the last enumeration-object ends:
            if (previous_headline_alineaindex>=0)and(self.whiteline_isbig(previous_whiteline)):
                alineaindex = previous_headline_alineaindex
            
            # In that case, we simply add the line to the currect textalinea:
            if (alineaindex>=0):
                self.textalineas[alineaindex].textcontent.append(textline)
                self.textalineas[alineaindex].pagenumbers.append(this_pagenumber)
                # NOTE: if no alinea has been created because no headline was formed, the bodytext will
                # simply be ignored in the alineas, but not in body.
                # NOTE: If the enumeratio-object extends over multiple lines, the other lines should
                # be recognised as BODY-text and, therefore, be added to the current alinea, as they should.
                
            # And we also add it to the textbody:
            self.body.textcontent.append(textline)
            self.body.pagenumbers.append(this_pagenumber)
            
        # ---------------------------------------------------------------------------------------
        # Then, decide over other textparts as well:
        if (thetype==texttype.FOOTER):
            self.footer.textcontent.append(textline)
            self.footer.pagenumbers.append(this_pagenumber)
        
        # ---------------------------------------------------------------------------------------
        # if (thetype==texttype.TITLE):
        #     self.title.textcontent.append(textline)
        #     self.title.pagenumbers.append(this_pagenumber)
            
        # ---------------------------------------------------------------------------------------
        # NOTE: Add new textparts here!
        
        # Finally, update previous-variables:
        previous_fontsize = fontsize
        previous_textline = textline
        previousline_IsBroken = False
        if (len(textline)>0):
            if (textline[len(textline)-1]=="-"): 
                previousline_IsBroken = True
            if (textline.lower().endswith("figure"))or(textline.lower().endswith("figure "))or(textline.lower().endswith("figures"))or(textline.lower().endswith("figures ")):
                previousline_IsBroken = True
            if (textline.lower().endswith("condition"))or(textline.lower().endswith("condition ")):
                previousline_IsBroken = True
