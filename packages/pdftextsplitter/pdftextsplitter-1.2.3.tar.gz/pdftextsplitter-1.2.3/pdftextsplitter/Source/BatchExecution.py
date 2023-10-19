# Python import commands:
import os
from .GenerateTextFile import GenerateTextFile
from .PrepareTextFile import PrepareTextFile
from .GenerateKeyWords import GenerateKeyWords
from .GenerateWordCloud import GenerateWordCloud

# Definition of paths:
pdfpath = "../FullDocs/TestDocs/"
intermediatepath = "../FullDocs/Intermediates/"
outputpath = "../FullDocs/Outputs/"

# Definition of parameters:
keywordextractor = "yake"
method = "pypdf2"

# obtain the list of all names:
names = os.listdir(pdfpath)

# Loop over the names:
for name in names:
    
    # only select the PDFs:
    if (".pdf" in name):
        
        # Then, perform execution:
        namecontent = name.replace(".pdf","")
        GenerateTextFile(method,pdfpath,intermediatepath,namecontent)
        PrepareTextFile(intermediatepath,intermediatepath,namecontent)
        GenerateKeyWords(intermediatepath,outputpath,namecontent,keywordextractor)
        GenerateWordCloud(intermediatepath,outputpath,namecontent+"_Body",1000)
        
        # Next, return some output:
        print("Processed file " + name + " on a total of " + str(len(names)) + " files.")

