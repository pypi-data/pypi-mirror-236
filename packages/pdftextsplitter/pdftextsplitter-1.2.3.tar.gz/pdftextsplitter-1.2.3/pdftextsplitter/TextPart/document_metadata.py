# Python functionality:
from PyPDF2 import PdfReader
import datetime

def document_metadata_textsplitter(self):
    """
    This function extracts high-level metatdata from the document 
    like date of the last modification, author, title, etc.
    IF such information is available as metadata in the original file.
    
    # Parameters: None (taken from the class)
    # Return: None (stored in the class) 
    
    """

    # Begin by extracting the data from the pdf itself:
    pdf = PdfReader(self.documentpath + self.documentname + ".pdf")
    info = pdf.metadata
    
    # Next, store data in the class:
    self.doc_metadata_author = str(info.author)
    self.doc_metadata_creator = str(info.creator)
    self.doc_metadata_producer = str(info.producer)
    self.doc_metadata_subject = str(info.subject)
    self.doc_metadata_title = str(info.title)
    
    # Extract dates:
    self.doc_metadata_creationdate = "None"
    if not (info.creation_date==None):
        thecreationdate = info.creation_date.strftime("%d-%B-%Y")
        self.doc_metadata_creationdate = thecreationdate.replace("-"," ")
    
    self.doc_metadata_modificationdate = "None"
    if not (info.modification_date==None):
        themodifdate = info.modification_date.strftime("%d-%B-%Y")
        self.doc_metadata_modificationdate = themodifdate.replace("-"," ")
    
    # ----------------------------------------------------
    
    # Build a nice visualization of the data:
    if not (info.creation_date==None):
        self.doc_metadata_fullstring = self.doc_metadata_fullstring + "<b> <i> Created on: </i> </b>"       + self.doc_metadata_creationdate + " <br />\n"
    
    if not (info.modification_date==None): 
        self.doc_metadata_fullstring = self.doc_metadata_fullstring + "<b> <i> Last modified on: </i> </b>" + self.doc_metadata_modificationdate + " <br />\n"
    
    if not (info.author==None):
        self.doc_metadata_fullstring = self.doc_metadata_fullstring + "<b> <i> Author: </i> </b>"           + self.doc_metadata_author + " <br />\n"
        
    if not (info.producer==None):
        self.doc_metadata_fullstring = self.doc_metadata_fullstring + "<b> <i> Created with: </i> </b>"     + self.doc_metadata_producer + " <br />\n"
        
    if not (info.subject==None):
        self.doc_metadata_fullstring = self.doc_metadata_fullstring + "<b> <i> Official subject: </i> </b>" + self.doc_metadata_subject + " <br />\n"
    
    if not (info.subject==None):
        self.doc_metadata_fullstring = self.doc_metadata_fullstring + "<b> <i> Official title: </i> </b>"   + self.doc_metadata_title + " <br />\n"

    # Done.
