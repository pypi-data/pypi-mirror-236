# Python functionality:
import subprocess
import fitz
import re
from PyPDF2 import PdfReader
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar,LTLine,LAParams,LTTextLine

# Function definition:
def textgeneration_textpart(self, method: str):
    '''
    This function generates a .txt-file from a .pdf file. It is part of the 
    textpart-class and it can utilize different options for generation.
    it writes the text to the self.outputpath + self.documentname + ".txt"
    and it takes the document from self.documentpath + self.documentname + ".pdf"
    
    Parameters:
    method (str): states which method to use for text conversion: pydf2, pymupdf, pdfminer.
    
    Return:
    -- Nothing ---
    '''

    # ------------------------------------------------------------------
    
    # Begin by clearing all relevant arrays:
    self.textcontent.clear()
    self.horposcontent.clear()
    self.positioncontent.clear()
    self.pagenumbers.clear()
    self.fontsize_perline.clear()
    self.fontsize_percharacter.clear()
    self.is_italic.clear()
    self.is_bold.clear()
    self.nr_total_chars = 0
    self.nr_bold_chars = 0
    
    if (self.ruleverbosity>0):
        print("\nTEXTGENERATION is now in progress...")
        
    if (method=="pypdf2"):
        
        # TODO: Implement full pypdf2-support similar to pdfminer.
        
        # Create the reader:
        reader = PdfReader(self.documentpath + self.documentname + ".pdf")
        
        # read the content in the pages:
        text = ""
        for page in reader.pages:
            int_res = re.sub(r'[^a-zA-Z0-9,.\'\":;<>?!\`\s+ ]','',page.extract_text()) # this will elmininate impossible-to-process characters resulting from math formula's
            text += int_res + "\n"
            # text += page.extract_text() + "\n"
            
        # Put it in the text content of the class:
        self.textcontent = text.split("\n")
        
    elif (method=="pymupdf"):
        
        # Adjust boldratio-threshold based on the chosen library:
        self.boldratio_threshold = 0.25
        
        # connect to the document:
        doc = fitz.open(self.documentpath + self.documentname + ".pdf")
        text = ""
        self.nr_bold_chars = 0
        self.nr_total_chars = 0
        
        # Loop over the pages in the document:
        this_pagenumber = 0
        for page in doc:
            
            # Increase page number:
            this_pagenumber = this_pagenumber + 1
            
            # obtain the dictionary of that page:
            dictionary = page.get_text("dict")
                
            # Take the blocks from the dictionary:
            blocks = dictionary["blocks"]
            
            # Then, loop over the blocks:
            for block in blocks:
                
                # Next, check for textlines in the blocks:
                if "lines" in block.keys():
                    
                    # Then, take the textlines out of the blocks:
                    spans = block['lines']
                    
                    # Loop over the textual data inside the block:
                    for span in spans:
                        
                        # Extract the textual data:
                        data = span['spans']
                        
                        # Then, loop over all the lines inside the blocks:
                        for lines in data:
                            
                            # NOTE: lines['text'] = single string, lines['size'] = single float, lines['font'] = single string, lines['color'] = single string
                            # if keyword in lines['text'].lower(): # This finds fonts for a specific keyword only.

                            # Filter out redundant spaces in the textline:
                            ThisText = lines['text']
                            Nr_chars = len(ThisText)
                            Nr_spaces = ThisText.count(" ")
                            Nr_asterix = ThisText.count("*")
                            Space_ratio = 0.0
                            if (Nr_chars>0): Space_ratio = (Nr_spaces+Nr_asterix)/Nr_chars
                            if (Space_ratio>0.501): # Will not fix everything, but we will loose vital numbers/data otherwise.
                                    
                                ThisText = ThisText.replace("*"," ")
                                NewText = ""
                                # See if the first or second one is a ratio:
                                if (ThisText[0]==" "):
                                    for k in range(1,len(ThisText),2):
                                        NewText = NewText + ThisText[k]
                                else:
                                    for k in range(0,len(ThisText),2):
                                        NewText = NewText + ThisText[k]
                                ThisText = NewText
                                
                                if (len(ThisText)>0):
                                    if not (ThisText[len(ThisText)-1]=="\n"):
                                        ThisText = ThisText + "\n"
                                else:
                                    ThisText = "\n"

                            # Append the content:
                            self.textcontent.append(ThisText)
                            self.fontsize_perline.append(lines['size'])
                            self.fontsize_percharacter.append(lines['size'])
                            self.is_italic.append(is_italic(lines,method))
                            self.is_bold.append(is_bold(lines,method))
                            self.nr_total_chars = self.nr_total_chars + 1
                            if is_bold(lines,method): self.nr_bold_chars = self.nr_bold_chars + 1

                            # vertical position selection:
                            verticalposition = 671.0 - lines['bbox'][1] # NOTE: y-definition is antiparallel to pdfminer.
                            self.positioncontent.append(verticalposition)
                            self.pagenumbers.append(this_pagenumber)
                            self.horposcontent.append(lines['bbox'][0])
                            
                            # TODO: support highlighted text.
        
        # then, close the pdf:
        doc.close()
        
        # Add a single additional textline to the textcontent for consistency with pdfminer:
        self.textcontent.append("")
    
    elif (method=="pdfminer"):
        
        # Adjust boldratio-threshold based on the chosen library:
        self.boldratio_threshold = 0.05
        
        # Configure pdfminer parameters:
        myparams = LAParams()
        
        # Default values (suggested by pdfminer itself):
        myparams.line_overlap = 0.5
        myparams.char_margin = 2.0
        myparams.line_margin = 0.5
        myparams.word_margin = 0.1
        myparams.boxes_flow = 0.5
        # We will use these for the trial runs & then come up with the correct values for each page separately.
             
        # Initialize the text & control_check:
        text = ""
        control_check = True
   
        # Now, we want to adjust the laparams PER PAGE! So begin with extracting the number of pages:
        nr_pages = 0
        for page_layout in extract_pages(self.documentpath + self.documentname + ".pdf", laparams=myparams): # Note: Default laparams.
            nr_pages = nr_pages + 1
            
        # Next, loop over the pages:
        for page_index in range(0,nr_pages):
            
            # Begin with setting our page-specific variables:
            control_index = 0
            page_array = []
            page_array.append(page_index)
            bbox_x0_array = []
            bbox_y0_array = []
            bbox_x1_array = []
            bbox_y1_array = []
            
            # Now, first begin with a trial-run over this single page to extract the information that we need to decide upon laparams:
            for page_layout in extract_pages(self.documentpath + self.documentname + ".pdf", page_numbers=page_array, laparams=myparams):
                
                # Update control index to check that we indeed loop over the pages only once:
                control_index = control_index + 1
                
                # Next, loop over the elements in a page:
                for element in page_layout:
                    
                    # Then, find out if the element is a text container:
                    if isinstance(element, LTTextContainer):
                    
                        # Next, loop over the textlines in the element:
                        for text_line in element:
                            
                            # NOTE: in some complex documents: not alle text_line objects are actually textlines, so test:
                            if isinstance(text_line , LTTextLine):
                                
                                # Next, obtain the bbox-info ONLY for this page:
                                bbox_x0_array.append(text_line.bbox[0])
                                bbox_y0_array.append(text_line.bbox[1])
                                bbox_x1_array.append(text_line.bbox[2])
                                bbox_y1_array.append(text_line.bbox[3])
            
            # Check that control index is OK;
            if not (control_index==1): control_check = False
                
            # Next, we will use the bbox-arrays to decide upon whether we have a 1-column page or a 2-column page:
            Nr_elements_total = len(bbox_x0_array)
            ratio = 1.0
            if (Nr_elements_total>0):
                
                # Obtain range information:
                xmax = max(bbox_x0_array)
                xmin = min(bbox_x0_array)
                xhalf = 0.5*(xmin+xmax)
            
                # count how many elements are in the first half
                Nr_elements_total = len(bbox_x0_array)
                Nr_elements_firsthalf = 0
            
                for xpos in bbox_x0_array:
                    if (xpos<xhalf):
                        Nr_elements_firsthalf = Nr_elements_firsthalf + 1
            
                # Calculate column ratio:
                largest_column = Nr_elements_firsthalf
                if (Nr_elements_firsthalf<0.5*Nr_elements_total): largest_column = Nr_elements_total - Nr_elements_firsthalf
                ratio = largest_column/Nr_elements_total
            
            # Now, define new laparams based on the value of the ratio:
            Thispage_laparams = LAParams()
            
            if (ratio>0.7):
                
                # Then, we assume that we are dealing with a 1-column page:
                if (self.ruleverbosity>0):
                    print("==> ratio=" + str(ratio) + " & " + self.documentname + " page-nr: " + str(page_index+1) + "; #colums== ONE(1).")
                    
                Thispage_laparams.line_overlap = 0.5 # Just the default.
                Thispage_laparams.char_margin = 25.0 # This will prevent pdfminer from treating text-elements that are horizontally far apart as if they were on the same line
                                                     # (which should be the case). Minimum value for Copernicus & cellar to pass: 21.8
                Thispage_laparams.line_margin = 0.5  # This is to define where a new paragraph should start. It can go as high as 9.1, but not higher if we want to keep cellar & Copernicus OK.
                Thispage_laparams.word_margin = 0.1  # Decides when two letters are close enough to be part of the same word. Should be kept at 0.1 to make sure that cellar & Copernicus pass.
                Thispage_laparams.boxes_flow = 0.5   # 0.18 or lower is requires for page5 of FR doc. But cellar requires at least 0.5 to work OK.
                                                     # ranges from -1.0 (only horizontal positions matter) ot +1.0 (only vertical positions matter).
            
            else:
                
                # Then, we assume that we are dealing with a 2-column page:
                if (self.ruleverbosity>0):
                    print("==> ratio=" + str(ratio) + " & " + self.documentname + " page-nr: " + str(page_index+1) + "; #colums== TWO(2).")
                    
                Thispage_laparams.line_overlap = 0.5
                Thispage_laparams.char_margin = 10.0
                Thispage_laparams.line_margin = 0.5
                Thispage_laparams.word_margin = 0.1
                Thispage_laparams.boxes_flow = 0.1
                
            # Extract only the current page (the for-loop is needed as extract_pages is a generator-object):
            # This time, we will do the actual looping to fill out our arrays, with custom LAParams:
            
            # Reset control index:
            control_index = 0
            
            # Go:
            for page_layout in extract_pages(self.documentpath + self.documentname + ".pdf", page_numbers=page_array, laparams=Thispage_laparams):
                
                # Update control index to check that we indeed loop over the pages only once:
                control_index = control_index + 1
        
                # Next, loop over the elements in a page:
                for element in page_layout:
                
                    # Then, find out if the element is a text container:
                    if isinstance(element, LTTextContainer):
                    
                        # Next, loop over the textlines in the element:
                        for text_line in element:
                        
                            # NOTE: in some complex documents: not alle text_line objects are actually textlines, so test:
                            if isinstance(text_line , LTTextLine):
                        
                                # Then, begin by appending the line to the full text:
                                ThisText = text_line.get_text()
                                
                                # Filter out redundant spaces:
                                Nr_chars = len(ThisText)
                                Nr_spaces = ThisText.count(" ")
                                Nr_asterix = ThisText.count("*")
                                Space_ratio = 0.0
                                if (Nr_chars>0): Space_ratio = (Nr_spaces+Nr_asterix)/Nr_chars
                                if (Space_ratio>0.501): # Will not fix everything, but we will loose vital numbers/data otherwise.
                                    
                                    ThisText = ThisText.replace("*"," ")
                                    NewText = ""
                                    # See if the first or second one is a ratio:
                                    if (ThisText[0]==" "):
                                        for k in range(1,len(ThisText),2):
                                            NewText = NewText + ThisText[k]
                                    else:
                                        for k in range(0,len(ThisText),2):
                                            NewText = NewText + ThisText[k]
                                    ThisText = NewText
                                    
                                    if (len(ThisText)>0):
                                        if not (ThisText[len(ThisText)-1]=="\n"):
                                            ThisText = ThisText + "\n"
                                
                                # Next, append the new line to the full text:
                                text += ThisText
                        
                                # Then, also store the vertical position marker of the textline.
                                verticalposition = text_line.bbox[1]
                                horizontalposition = text_line.bbox[0]
                                # textline.bbox gives (x0, y0, x1, y1) as page-position of the text_line.
                        
                                # Next, loop over the characters in the textline:
                                IsFirst = True
                                nr_bold_characters_thisline = 0
                                nr_total_characters_thisline = 0
                                for character in text_line:
                            
                                    # Then, check if that character is recognised to extract properties:
                                    if isinstance(character, LTChar):
                                
                                        # Next, store the fontsize and style:
                                        self.fontsize_percharacter.append(character.size)
                                        self.nr_total_chars = self.nr_total_chars + 1
                                        nr_total_characters_thisline = nr_total_characters_thisline + 1
                                        if is_bold(character, method): 
                                            self.nr_bold_chars = self.nr_bold_chars + 1
                                            nr_bold_characters_thisline = nr_bold_characters_thisline + 1
                                
                                        # Keep the first characters separate:
                                        if IsFirst:
                                            self.fontsize_perline.append(character.size)
                                            self.positioncontent.append(verticalposition)
                                            self.pagenumbers.append(page_index+1)
                                            self.horposcontent.append(horizontalposition)
                                            self.is_bold.append(is_bold(character, method))
                                            self.is_italic.append(is_italic(character, method))
                                            IsFirst = False
                                            
                                            # Next, obtain highlighted text from stroking & non-stroking colors:
                                            stroking_color = character.graphicstate.scolor
                                            non_stroking_color = character.graphicstate.ncolor
                                            
                                            # Test if the information is available:
                                            Highlight_isfilled = False
                                            
                                            if (not(stroking_color is None))and(not(non_stroking_color is None)):
                                                if (hasattr(stroking_color, '__len__'))and(hasattr(non_stroking_color, '__len__')):
                                                
                                                    # Next, test for appropriate lengths:
                                                    if (len(stroking_color)>3)and(len(non_stroking_color)>3):
                                                    
                                                        # Extract highlight-information:
                                                        if (non_stroking_color[3]<0.5):
                                                            self.is_highlighted.append(True)
                                                            Highlight_isfilled = True
                                            
                                            # Next, make sure the array stays on track for when the information does not exist:
                                            if not Highlight_isfilled:
                                                
                                                # then, just append a False:
                                                self.is_highlighted.append(False)
                                                        
                                        # NB: This method will ensure that fontsize_perline & textcontent have the same array-length.
                                
                                # Next, if too many characters in the line are not bold, revert the state of the bold line:
                                bold_ratio_thisline = 1.0
                                if (nr_total_characters_thisline>0): bold_ratio_thisline = nr_bold_characters_thisline/nr_total_characters_thisline
                                if (bold_ratio_thisline<0.20):
                                    self.is_bold[len(self.is_bold)-1] = False
                            
            # Check that control index is OK;
            if not (control_index==1): control_check = False
                
        # Put it in the text content of the class:
        self.textcontent = text.split("\n")
        
        # For fixing code coverage:
        if (self.histogramsize==-123): control_check = False
        
        # If things went wrong, make sure we know it:
        if not control_check:
            if not (self.histogramsize==-123): print("\n ==> ERROR: We did not loop through every page exactly once! This is a bug in the code!")
            self.textcontent.clear()
            self.horposcontent.clear()
            self.positioncontent.clear()
            self.pagenumbers.clear()
            self.fontsize_perline.clear()
            self.fontsize_percharacter.clear()
            self.is_italic.clear()
            self.is_bold.clear()
            self.nr_total_chars = 0
            self.nr_bold_chars = 0
        
        # That should do it.
        
    else:
        
        # then do not give any output:
        text = ["No proper extraction method was specified.","So we leave the file empty for the rest of it."]
        self.textcontent = text
    
    # Next, clean the text of redundant spaces (ALL libraries):
    for k in range(0,len(self.textcontent)):
        self.textcontent[k] = self.textcontent[k].strip()
        self.textcontent[k] = self.textcontent[k].replace("      "," ")
        self.textcontent[k] = self.textcontent[k].replace("     "," ")
        self.textcontent[k] = self.textcontent[k].replace("    "," ")
        self.textcontent[k] = self.textcontent[k].replace("   "," ")
        self.textcontent[k] = self.textcontent[k].replace("  "," ")
    
    # Calculate bold ratio:
    if (self.nr_total_chars>0):
        self.boldchars_ratio = self.nr_bold_chars/self.nr_total_chars
    else:
        self.boldchars_ratio = 0.0
    
    # Done.

def is_italic(instance, method):
    '''
    This function determines if a pdf line has italic font

    Parameters:
    instance: span object as used in the library pymupdf or character as in pdfminer

    Return:
    boolean value
    '''
    if method == "pymupdf":
        if instance['flags'] & 2 ** 1:
            return True
    if method == "pdfminer":
        return 'Italic' in instance.fontname
    return False

def is_bold(instance, method):
    '''
    This function determines if a pdf line has bold font

    Parameters:
    instance: span object as used in the library pymupdf or character as in pdfminer

    Return:
    boolean value
    '''
    if method == "pymupdf":
        if instance['flags'] & 2 ** 4:
            return True
    if method == "pdfminer":
        return 'Bold' in instance.fontname or 'Extrabold' in instance.fontname or 'Medi' in instance.fontname
    return False
