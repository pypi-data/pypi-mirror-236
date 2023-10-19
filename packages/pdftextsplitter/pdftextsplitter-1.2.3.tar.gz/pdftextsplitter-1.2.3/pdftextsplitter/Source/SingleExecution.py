# Python import commands:
from .GenerateTextFile import GenerateTextFile
from .PrepareTextFile import PrepareTextFile
from .GenerateKeyWords import GenerateKeyWords
from .GenerateWordCloud import GenerateWordCloud

# Definition of paths:
pdfpath = "../FullDocs/TestDocs/"
intermediatepath = "../FullDocs/Intermediates/"
outputpath = "../FullDocs/Outputs/"

# Definition of filenames:
filename = "CADouma_DNN_Publication"
#filename = "CADouma_Veto_Publication"
#filename = "BigTest"

# Definition of parameters:
keywordextractor = "yake"
method = "pypdf2"

# Execution:
GenerateTextFile(method,pdfpath,intermediatepath,filename)
PrepareTextFile(intermediatepath,intermediatepath,filename)
GenerateKeyWords(intermediatepath,outputpath,filename,keywordextractor)
GenerateWordCloud(intermediatepath,outputpath,filename+"_Body",1000000)

