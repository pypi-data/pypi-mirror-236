# python import commands:
import subprocess
import fitz
import shutil
import re
from PyPDF2 import PdfReader

# Function definition:
def GenerateTextFile(method: str, filepath: str, outputpath: str, filename: str):
    '''
    This function generates a .txt-file from a .pdf file.
    It executes a Linux bash shell-command to call the
    tool pdftotext with the porper (default) layout structure.
    This layout structure is very important for further
    processing the .txt-file.
    
    Parameters:
    method (str): states which method to use for text conversion: shell (pdftotext by terminal command), pydf2, pymupdf, shortcut.
    filepath (str): absolute path to where the .pdf file is located.
    outputpath (str): absolute path to where the .txt file will be stored.
    filename (str): name of the specific .pdf file to be transformed.
                    NB: Without the .pdf-extension.
    
    Return:
    -- Nothing ---
    '''

    # ------------------------------------------------------------------

    
    # if (method=="pdftotext"):
    #     # Load your PDF (with automatically closes later; r=red, b=binaryfile)::
    #     f = open(filepath + filename + ".pdf", "rb")
    #     pdf = pdftotext.PDF(f) # layout="non_raw_non_physical_layout"
        
    #     # Save all text to a txt file:
    #     fnew = open(outputpath + filename + '.txt', 'w')
    #     fnew.write("".join(pdf)) 
    #     fnew.close()

    if method== "shell":
        
        # Run the shell-command from python:
        cmd = "pdftotext " + filepath + filename + ".pdf " + outputpath + filename + ".txt"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        p.communicate()
        
    elif method=="shortcut":
        
        # copy the file from somewhere else (should only be used when textgeneration is not an issue):
        filepath="../True_Outputs/"
        shutil.copyfile(filepath+filename+".txt",outputpath+filename+".txt")
        
    elif method == "pypdf2":
        
        # Create the reader:
        reader = PdfReader(filepath + filename + ".pdf")
        
        # read the content in the pages:
        text = ""
        for page in reader.pages:
            int_res = re.sub(r'[^a-zA-Z0-9,.\s+ ]','',page.extract_text())
            text += int_res + "\n"
            # text += page.extract_text() + "\n"
            
        # Write it to an output file:    
        fnew = open(outputpath + filename + '.txt', 'w')
        fnew.write("".join(text)) 
        fnew.close()
    
    elif method == "pymupdf":
        
        # read the content in the pages:
        doc = fitz.open(filepath + filename + ".pdf")
        text = ""
        
        for page in doc:
            int_res = re.sub(r'[^a-zA-Z0-9,.\s+ ]','',page.get_text())
            text += int_res + "\n"
            # text += page.get_text()        
        
        # Remove last escape character:
        text = text[0:(len(text)-1)]
        
        # Write it to an output file:
        fnew = open(outputpath + filename + '.txt', 'w')
        fnew.write("".join(text)) 
        fnew.close()
        
    else:
        # then do not give any output:
        fnew = open(outputpath + filename + '.txt', 'w')
        fnew.write("No proper extraction method was specified.")
        fnew.close()
