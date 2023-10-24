# Python functionality:
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import PDFObjRef, resolve1
import fitz

class Native_TOC_Element:
    """
    This class stores the information extracted from the native TOC in 
    a PDF-document. We use this class to store the information to have a
    common default instead of that every library uses its own method.
    """
    
    # Definition of the default-constructor:
    def __init__(self):
        self.cascadelevel = 0
        self.title = ""
        self.page = 0
        self.Xpos = 0.0
        self.Ypos = 0.0
        self.Zpos = 0.0
    
    # Printing function:
    def print_TOC_element(self):
        """
        Prints the content of the class in a terminal window.
        # Parameters: None, # Return: None.
        """
        print("[TITLE:] " + str(self.title))
        print("CASCADELEVEL=" + str(self.cascadelevel) + " | X=" + str(self.Xpos) + " | Y=" + str(self.Ypos) + " | Z=" + str(self.Zpos) + " | pageNR=" + str(self.page))
    
    # Comparing function:
    def compare(self, other) -> bool:
        """
        Compare two instances of the class Native_TOC_Element to see if they are the same.
        We do not take position elements or page numbers into account, as those are not (always) of interest.
        # Parameters: self (this instance) & other (the other instance): the two Native_TOC_Element-objects to compare.
        # return: bool: whether they are the same or not.
        """
        Answer = True
        if not (self.cascadelevel==other.cascadelevel): Answer = False
        if not (self.title==other.title): Answer = False
        return Answer

    # Comparing function (with position elements):
    def compare_withpos(self, other) -> bool:
        """
        Compare two instances of the class Native_TOC_Element to see if they are the same.
        We do take position elements into account, as those are of interest to the user that
        specifically calls this function.
        # Parameters: self (this instance) & other (the other instance): the two Native_TOC_Element-objects to compare.
        # return: bool: whether they are the same or not.
        """
        Answer = self.compare(other)
        if (abs(self.Xpos - other.Xpos)>1e-3): Answer = False
        if (abs(self.Ypos - other.Ypos)>1e-3): Answer = False
        if (abs(self.Zpos - other.Zpos)>1e-3): Answer = False
        return Answer
    
    # Comparing function (with page numbers):
    def compare_withpagenr(self, other) -> bool:
        """
        Compare two instances of the class Native_TOC_Element to see if they are the same.
        We do take page numbers into account, as those are of interest to the user that
        specifically calls this function.
        # Parameters: self (this instance) & other (the other instance): the two Native_TOC_Element-objects to compare.
        # return: bool: whether they are the same or not.
        """
        Answer = self.compare(other)
        if not (self.page==other.page): Answer = False
        return Answer
    
    def printcode(self):
        """
        This function prints the content of the class as hardcode in the terminal
        So it becomes easy to create hardcoded elements.
        """
        print("")
        print("    thiselement = Native_TOC_Element()")
        print("    thiselement.cascadelevel = " + str(self.cascadelevel))
        print('    thiselement.title = "' + str(self.title) + '"')
        print("    thiselement.Xpos = " + str(self.Xpos))
        print("    thiselement.Ypos = " + str(self.Ypos))
        print("    thiselement.Zpos = " + str(self.Zpos))
        print("    thiselement.page = " + str(self.page))
        print("    true_elements.append(thiselement)")

def read_native_toc_textsplitter(self, method: str):
    """
    This function reads the native Table of Contents (TOC) from a PDF
    document and stores it inside the textpart-class. No selection rules
    of classes inherited from textpart are used. It checks whether the 
    pdf document already has a TOC from itself and then, reads that.
    
    Not every PDf document contains a native TOC and, if it does
    contain one, it is not always known which parts of text belong
    to which TOC-item. As such, the selection rules remain the preferred
    method of breaking down a document. However, the information
    from this function can then serve as a nice benchmark to how well
    the selection rules can perform.
    
    # Parameters: 
    method (str): decides which library to use for extraction of the TOC:
                  pdfminer, pymupdf, shell, etc. Just like textgeneration.py
    # Return: None: stored inside the class.
    """
    
    # ---------------------------------------------------------------------
    
    # Begin by clearing out the array of TOC-elements:
    self.native_TOC.clear()
    
    # Select the proper method:
    if (method=="pdfminer"):
    
        # begin by creating the parsing of the document:
        fp = open(self.documentpath + self.documentname + ".pdf", 'rb')
        parser = PDFParser(fp)
        doc = PDFDocument(parser)
        parser.set_document(doc)
    
        # Next, collect the TOC:
        try:
            
            # We use a try-except-block as outlines is a generator-object and it crashes
            # isntantly if no TOC is present in the document. The try-except-block prevents this crash.
            outlines = doc.get_outlines()
               
            # Then, transfer it to the class-array:
            # Loop over the elements in outlines; level is an int, title is a string, dest is a list
            # a is a PDFObjRef, se is yet undetermined (NoneType).
        
            for (level, title, dest, a, se) in outlines:
                
                # begin by creating a new element:
                new_element = Native_TOC_Element()
                
                # Appoint values:
                new_element.cascadelevel = level-1 # pdfminer starts with the document at 1, not 0 as our program does.
                new_element.title = title
            
                # Appoint positions (if possible):
                if (str(type(dest))=="<class 'list'>"):
                    if (len(dest)>1):
                        if ("XYZ" in str(dest[1])):
                            new_element.Xpos = dest[2]
                            new_element.Ypos = dest[3]
                            new_element.Zpos = dest[4]
            
                # Extract metadata (if possible):
                if isinstance(a, PDFObjRef):
                    meta_data = resolve1(a)
                    # It usually does not tell you more than the cascadelevel already does.
                
                # Next, append it to the array:
                self.native_TOC.append(new_element)
        
        except:
            
            # then, we jut want the array in the class to stay empty:
            self.native_TOC.clear()
        
        # Done.
    
    elif (method=="pymupdf"):
        
        # Begin by opening the document:
        doc = fitz.open(self.documentpath + self.documentname + ".pdf")
        
        # Next, obtain the table of contents:
        thetoc = doc.get_toc()
        
        # Pass values into the array:
        if (len(thetoc)>0):
            
            # Loop over toc-elements:
            for toc_el in thetoc:
                
                # begin by creating a new element:
                new_element = Native_TOC_Element()
                
                # Pass values:
                new_element.cascadelevel = toc_el[0]-1 # pymupdf starts with the document at 1, not 0 as our program does.
                new_element.title = toc_el[1]
                new_element.page = toc_el[2]
                
                # Next, append it to the array:
                self.native_TOC.append(new_element)
                
                # Done.
    
    else:
        
        # Give a message that this method was unsupported:
        print("method <"+str(method)+"> is unsupported for TOC-extraction from PDF's")
    
    
    
    
    
    
    
    
    
    
    
    
