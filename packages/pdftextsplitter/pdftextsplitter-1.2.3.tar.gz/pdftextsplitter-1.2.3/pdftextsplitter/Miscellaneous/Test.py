# python import commands:
import pdftotext
import subprocess
import linecache
import re

# Define filename:
filepath = "./TestDocs/"
outputpath = "./Outputs/"
filename = "CADouma_DNN_Publication"

# Load your PDF (with automatically closes later; r=red, b=binaryfile):
# with open(filepath + filename + ".pdf", "rb") as f: 
#    pdf = pdftotext.PDF(f, layout="non_raw_non_physical_layout")
#    pdf = pdftotext.PDF(f)

# Save all text to a txt file:
# with open(filepath + outputpath + '.txt', 'w') as f:
#    f.write("\n\n".join(pdf)) 

# Run the shell-command from python:
cmd = "pdftotext " + filepath + filename + ".pdf " + outputpath + filename + ".txt"
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
# print(p.communicate())

# Process the resulted file line-by-line:
f = open(outputpath+filename+".txt", "r")

# Create new files to split the tekst:
Body = open(outputpath + filename + '_Body.txt', 'w')
Authors = open(outputpath + filename + '_Authors.txt', 'w')
Captions = open(outputpath + filename + '_Captions.txt', 'w')
Garbich = open(outputpath + filename + '_Garbich.txt', 'w')
Headlines = open(outputpath + filename + '_Headlines.txt', 'w')
Abstract = open(outputpath + filename + '_Abstract.txt', 'w')
KeyWords = open(outputpath + filename + '_KeyWords.txt', 'w')
Remain = open(outputpath + filename + '_Remain.txt', 'w')

#Define required variables:
Debug_Flag=-1 # NOTE: States which output is printed in the terminal.
prevTextLine=""
ancientTextLine=""
nLines=0
Pseudo_ancient=""
Pseudo_prev=""
Pseudo_line=""

# Define locks to make sure that if some test=OK, the next lines also are added:
BodyLock=False
AuthorsLock=False
CaptionsLock=False
GarbichLock=False
HeadlinesLock=False
AbstractLock=False
KeyWordsLock=False
RemainLock=False

# loop over the textlines in the file:
for lineOfText in f.readlines():
    # lineOfText is the string of the current line.
    
    # split the strings in seperate words:
    ThisLine = lineOfText.split()
    PrevLine = prevTextLine.split()
    AncientLine = ancientTextLine.split()
    
    # --------------------------------------------------------------------------------------
    # Identify the text properties of our lines:
    nWords = [len(AncientLine), len(PrevLine), len(ThisLine)]
    
    # Count dots except when preceded by a number:
    Pseudo_ancient = re.sub(r'\.(?:\s+|$)', ' stom ', ancientTextLine)
    Pseudo_prev = re.sub(r'\.(?:\s+|$)', ' stom ', prevTextLine)
    Pseudo_line = re.sub(r'\.(?:\s+|$)', ' stom ', lineOfText)
    nDots = [ancientTextLine.count(".") - Pseudo_ancient.count("."), prevTextLine.count(".") - Pseudo_prev.count("."), lineOfText.count(".") - Pseudo_line.count(".")]
    
    Pseudo_ancient = re.sub(r'\,(?:\s+|$)', ' stom ', ancientTextLine)
    Pseudo_prev = re.sub(r'\,(?:\s+|$)', ' stom ', prevTextLine)
    Pseudo_line = re.sub(r'\,(?:\s+|$)', ' stom ', lineOfText)
    nCommas = [ancientTextLine.count(",") - Pseudo_ancient.count(","), prevTextLine.count(",") - Pseudo_prev.count(","), lineOfText.count(",") - Pseudo_line.count(",")]
    
    nSlashes = [ancientTextLine.count("/"), prevTextLine.count("/"), lineOfText.count("/")]
    
    # Investigate the first characters of the tekstlines:
    Characters = []
    Characters.append(["", "", ""]) # First Characters in the tekstline, first index ==[0]
    Characters.append(["", "", ""]) # Second Characters in the tekstline, fisrt index ==[1]
    StartNumber = [False, False, False]
    StartNormal = [False, False, False]
    
    # Assigne characters:
    if (nWords[0]>0): 
        Characters[0][0] = ancientTextLine[0]
        if (len(ancientTextLine)>=2):
            Characters[1][0] = ancientTextLine[1]
        else:
            Characters[1][0] = ""
    else: Characters[0][0] = ""
    
    # Assigne characters:
    if (nWords[1]>0): 
        Characters[0][1] = prevTextLine[0]
        if (len(prevTextLine)>=2):
            Characters[1][1] = prevTextLine[1]
        else:
            Characters[1][1] = ""
    else: Characters[0][1] = ""
    
    # Assigne characters:
    if (nWords[2]>0): 
        Characters[0][2] = lineOfText[0]
        if (len(lineOfText)>=2):
            Characters[1][2] = lineOfText[1]
        else:
            Characters[1][2] = ""
    else: Characters[0][2] = ""
    
    # Test if the first character is a number or alphanumeric.
    for k in range(0,3):
        StartNumber[k] = Characters[0][k].isnumeric()
        StartNormal[k] = Characters[0][k].isalnum()
    
    # --------------------------------------------------------------------------------------
    # add the lines of tekst to the different files:
    
    # Begin by identiying blank lines. We always work with prevTextLine & index==1, so we take
    # The middle line; AncientLine comes before & ThisLine comes after.
    if ((Characters[0][1]=="\n")or(nWords[1]==0)): 
        Garbich.write("".join(prevTextLine))
        
        # Give debugging output in terminal:
        if ((Debug_Flag==0)or(Debug_Flag==1)):     
            print(" <" + str(nLines) + ">: " + "NEWLINE!!!")
        
        # Release all locks at newline:
        BodyLock=False
        AuthorsLock=False
        CaptionsLock=False
        GarbichLock=False
        HeadlinesLock=False
        AbstractLock=False
        KeyWordsLock=False
        RemainLock=False
        
    # Next, we test for the locks and, if positive, we add to that file, independent
    # of other tests. That is the puprose of the locks:
    elif (BodyLock==True): 
        Body.write("".join(prevTextLine))
        
        # Give debugging output in terminal:
        if ((Debug_Flag==0)or(Debug_Flag==2)):
            print(" <" + str(nLines) + ">: " + "BODY >>> " + prevTextLine)
        
    elif (AuthorsLock==True): 
        Authors.write("".join(prevTextLine))
        
        # Give debugging output in terminal:
        if ((Debug_Flag==0)or(Debug_Flag==3)):
            print(" <" + str(nLines) + ">: " + "AUTHORS >>> " + prevTextLine)
        
    elif (CaptionsLock==True): 
        Captions.write("".join(prevTextLine))
        
        # Give debugging output in terminal:
        if ((Debug_Flag==0)or(Debug_Flag==4)):
            print(" <" + str(nLines) + ">: " + "CAPTIONS >>> " + prevTextLine)
        
    elif (GarbichLock==True): 
        Garbich.write("".join(prevTextLine))
        
        # Give debugging output in terminal:
        if ((Debug_Flag==0)or(Debug_Flag==5)):
            print(" <" + str(nLines) + ">: " + "GARBICH >>> " + prevTextLine)
        
    elif (HeadlinesLock==True): 
        Headlines.write("".join(prevTextLine))
        
        # Give debugging output in terminal:
        if ((Debug_Flag==0)or(Debug_Flag==6)):
            print(" <" + str(nLines) + ">: " + "HEADLINES >>> " + prevTextLine)
    
    elif (AbstractLock==True): 
        Abstract.write("".join(prevTextLine))
        
        # Give debugging output in terminal:
        if ((Debug_Flag==0)or(Debug_Flag==7)):
            print(" <" + str(nLines) + ">: " + "ABSTRACT >>> " + prevTextLine)
    
    elif (KeyWordsLock==True): 
        KeyWords.write("".join(prevTextLine))
        
        # Give debugging output in terminal:
        if ((Debug_Flag==0)or(Debug_Flag==9)):
            print(" <" + str(nLines) + ">: " + "KEYWORDS >>> " + prevTextLine)
    
    elif (RemainLock==True): 
        Remain.write("".join(prevTextLine))
        
        # Give debugging output in terminal:
        if ((Debug_Flag==0)or(Debug_Flag==8)):
            print(" <" + str(nLines) + ">: " + "REMAIN >>> " + prevTextLine)
    
    # Next, attempt to filter out headlines by identifying if the first 
    # character is a number & the second one is a dot:
    elif ((StartNumber[1]==True)and(Characters[1][1]==".")):
        Headlines.write("".join(prevTextLine))
        # No need for a lock; a headline is always a single line.
        
        # Give debugging output in terminal:
        if ((Debug_Flag==0)or(Debug_Flag==6)):
            print(" <" + str(nLines) + ">: " + prevTextLine)
    
    # Next, filter out all URL-lines & Ref-lines:
    elif ((nSlashes[1]>1)or(Characters[0][1]=="[")):
        Garbich.write("".join(prevTextLine))
        GarbichLock=True # URLs & Related info may extend on multiple lines.
        
        # Give debugging output in terminal:
        if ((Debug_Flag==0)or(Debug_Flag==5)):
            print(" <" + str(nLines) + ">: " + prevTextLine)
    
    # Test on first word:
    elif ((nWords[1]>0)and((Characters[0][0]=="\n")or(nWords[0]==0))):
        
        # Figure captions:
        if (PrevLine[0].lower().startswith("fig.")):
            Captions.write("".join(prevTextLine))
            CaptionsLock=True # Because a caption may be on multiple lines...
            
            # Give debugging output in terminal:
            if ((Debug_Flag==0)or(Debug_Flag==4)):
                print(" <" + str(nLines) + ">: " + prevTextLine)

        # Abstract:
        if ((PrevLine[0].lower().startswith("abstract"))or(PrevLine[0].lower().startswith("summary"))or(PrevLine[0].lower().startswith("samenvatting"))):
            Abstract.write("".join(prevTextLine))
            AbstractLock=True # Because te abstract extends over multiple lines.
            
            # Give debugging output in terminal:
            if ((Debug_Flag==0)or(Debug_Flag==7)):
                print(" <" + str(nLines) + ">: " + prevTextLine)
    
    # Keywords:
    elif (nWords[1]>0):
        if (PrevLine[0].lower().startswith("keyword")):
            KeyWords.write("".join(prevTextLine))
            KeyWordsLock=True # Because te abstract extends over multiple lines.
            
            # Give debugging output in terminal:
            if ((Debug_Flag==0)or(Debug_Flag==9)):
                print(" <" + str(nLines) + ">: " + prevTextLine)
        
    # Next, filter out author lines:
    elif (nDots[1]>3):
        Authors.write("".join(prevTextLine))
        AuthorsLock=True # We do use a lock for the dots, as that will incorporate the acknowledgements-section. That is about authors too.
        
        # Give debugging output in terminal:
        if ((Debug_Flag==0)or(Debug_Flag==3)):
            print(" <" + str(nLines) + ">: " + prevTextLine)
    
    elif (nCommas[1]>3):
        Authors.write("".join(prevTextLine))
        # We do NOT use a lock for Comma's as there are some lines in the body of the text that match these criteria. So a lock would eliminate too much.
        
        # Give debugging output in terminal:
        if ((Debug_Flag==0)or(Debug_Flag==3)):
            print(" <" + str(nLines) + ">: " + prevTextLine)
    
    # Next, we eliminate the lines that are too short (for example, because a few words are taken from the tables:
    elif (nWords[1]<4):
        Garbich.write("".join(prevTextLine))
        # We do NOT use a lock, as these are all single-lines that are not enclosed by whitelines.
        
        # Give debugging output in terminal:
        if ((Debug_Flag==0)or(Debug_Flag==5)):
            print(" <" + str(nLines) + ">: " + prevTextLine)
    
    # The rest can go into the body:
    else: 
        Body.write("".join(prevTextLine))
        #Remain.write("".join(prevTextLine)) 
        
        # Give debugging output in terminal:
        if ((Debug_Flag==0)or(Debug_Flag==2)):
            print(" <" + str(nLines) + ">: " + prevTextLine)
    
    # --------------------------------------------------------------------------------------
    # ### End of the loop actions: ###
    
    # Update FIRST ancient line and THEN previous test line:
    ancientTextLine = prevTextLine
    prevTextLine = lineOfText
    
    # Raise the index of the current line:
    nLines = nLines + 1
    
