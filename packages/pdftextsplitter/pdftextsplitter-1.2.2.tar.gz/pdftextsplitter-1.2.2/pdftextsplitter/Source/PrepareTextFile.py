# python import commands:
import re
from .GetTitleLines import GetTitleLines
from .ContainsCountry import ContainsCountry


# Function definition:
def PrepareTextFile(filepath: str, outputpath: str, filename: str):
    '''
    This function splits a .txt-file into several .txt-files.
    It uses python base-code to read the .txt-file 
    line-by-line and adds those lines to different output
    .txt-files for further processing. 
    
    It uses general considerations for the splitting:
    Body: 
    Title: Selects hard-coded lines from the souce .txt-file. So the template must be known for this.
    Authors: If the number of dots is >3 or comma's is >5, the line is assumed to be part of the author list.
             Also, if it contains "unive" or a country name, it is probably an address line, so part of the authors.
             If a lines has >3 dots, the next line sof the entire alinea are also part of the authors list.
    Captions: If the line starts with "Fig." and is preceded by a blank line, the whole
              alinea is considered to be a figure caption.
    Garbich: If a line is blank, contains <4 words, starts with a "[" (reference list) or contains
             >2 "/" characters (urls), the line is considered to be garbich.
    Headlines: If the line starts with number, followed by dot or space, has >7 characters
               of which >5 are letters and it does not contain "unive" or a country name, it is considered to be a headline.
    Abstract: If an alinea starts with abstract, summary of samenvatting, the whole alinea is considered to be abstract.
    Keywords: If an alinea starts with keyword, the whole alinea is considered to be abstract.
    Remain: the splitting is done with elif-commands. the else-situation is reserved for the Remain.
    
    Parameters:
    filepath (str): absolute path to where the source .txt file is located.
    outputpath (str): absolute path to where the output .txt files will be stored.
    filename (str): name of the specific .txt file to be splitted
                    NB: Without the .txt-extension.
    
    Return:
    -- Nothing ---
    '''

    # ------------------------------------------------------------------

    # Open the raw text-file generated from the PDF:
    Sourcefile = open(outputpath + filename + ".txt", "r")

    # Create new files to split the tekst:
    Body = open(outputpath + filename + '_Body.txt', 'w')
    Title = open(outputpath + filename + '_Title.txt', 'w')
    Authors = open(outputpath + filename + '_Authors.txt', 'w')
    Captions = open(outputpath + filename + '_Captions.txt', 'w')
    Garbich = open(outputpath + filename + '_Garbich.txt', 'w')
    Headlines = open(outputpath + filename + '_Headlines.txt', 'w')
    Abstract = open(outputpath + filename + '_Abstract.txt', 'w')
    KeyWords = open(outputpath + filename + '_KeyWords.txt', 'w')
    Remain = open(outputpath + filename + '_Remain.txt', 'w')

    # Define required variables:
    Debug_Flag = -1  # NOTE: States which output is printed in the terminal.
    prevTextLine = ""
    ancientTextLine = ""
    nLines = 0
    Pseudo_ancient = ""
    Pseudo_prev = ""
    Pseudo_line = ""

    # Define locks to make sure that if some test=OK, the next lines also are added:
    BodyLock = False
    TitleLock = False
    AuthorsLock = False
    CaptionsLock = False
    GarbichLock = False
    HeadlinesLock = False
    AbstractLock = False
    KeyWordsLock = False
    RemainLock = False

    # Obtain Title structure:
    TitleArray = GetTitleLines(filename)

    # loop over the textlines in the file:
    for lineOfText in Sourcefile.readlines():
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
        nDots = [ancientTextLine.count(".") - Pseudo_ancient.count("."),
                 prevTextLine.count(".") - Pseudo_prev.count("."), lineOfText.count(".") - Pseudo_line.count(".")]

        Pseudo_ancient = re.sub(r'\,(?:\s+|$)', ' stom ', ancientTextLine)
        Pseudo_prev = re.sub(r'\,(?:\s+|$)', ' stom ', prevTextLine)
        Pseudo_line = re.sub(r'\,(?:\s+|$)', ' stom ', lineOfText)
        nCommas = [ancientTextLine.count(",") - Pseudo_ancient.count(","),
                   prevTextLine.count(",") - Pseudo_prev.count(","), lineOfText.count(",") - Pseudo_line.count(",")]

        nSlashes = [ancientTextLine.count("/"), prevTextLine.count("/"), lineOfText.count("/")]
        nLetters = [sum(c.isalpha() for c in AncientLine), sum(c.isalpha() for c in prevTextLine),
                    sum(c.isalpha() for c in lineOfText)]
        nDigits = [sum(c.isdigit() for c in AncientLine), sum(c.isdigit() for c in prevTextLine),
                   sum(c.isdigit() for c in lineOfText)]
        nSpaces = [sum(c.isspace() for c in AncientLine), sum(c.isspace() for c in prevTextLine),
                   sum(c.isspace() for c in lineOfText)]

        # Investigate the first characters of the tekstlines:
        Characters = []
        Characters.append(["", "", ""])  # First Characters in the tekstline, first index ==[0]
        Characters.append(["", "", ""])  # Second Characters in the tekstline, fisrt index ==[1]
        Characters.append(["", "", ""])  # Third Characters in the tekstline, fisrt index ==[1]
        StartNumber = [False, False, False]
        StartNormal = [False, False, False]
        ThirdNumber = [False, False, False]

        # Assigne characters:
        if nWords[0] > 0:
            Characters[0][0] = ancientTextLine[0]

            if (len(ancientTextLine) >= 2):
                Characters[1][0] = ancientTextLine[1]
            else:
                Characters[1][0] = ""

            if len(ancientTextLine) >= 3:
                Characters[2][0] = ancientTextLine[2]
            else:
                Characters[2][0] = ""
        else:
            Characters[0][0] = ""

        # Assigne characters:
        if (nWords[1] > 0):
            Characters[0][1] = prevTextLine[0]

            if len(prevTextLine) >= 2:
                Characters[1][1] = prevTextLine[1]
            else:
                Characters[1][1] = ""

            if len(prevTextLine) >= 3:
                Characters[2][1] = prevTextLine[2]
            else:
                Characters[2][1] = ""
        else:
            Characters[0][1] = ""

        # Assigne characters:
        if nWords[2] > 0:
            Characters[0][2] = lineOfText[0]

            if len(lineOfText) >= 2:
                Characters[1][2] = lineOfText[1]
            else:
                Characters[1][2] = ""

            if len(lineOfText) >= 3:
                Characters[2][2] = lineOfText[2]
            else:
                Characters[2][2] = ""
        else:
            Characters[0][2] = ""

        # Test if the first character is a number or alphanumeric.
        for k in range(0, 3):
            StartNumber[k] = Characters[0][k].isnumeric()
            StartNormal[k] = Characters[0][k].isalnum()
            ThirdNumber[k] = Characters[2][k].isnumeric()

        # --------------------------------------------------------------------------------------
        # add the lines of tekst to the different files:

        # Begin by identiying blank lines. We always work with prevTextLine & index==1, so we take
        # The middle line; AncientLine comes before & ThisLine comes after.
        if (Characters[0][1] == "\n") or (nWords[1] == 0):
            Garbich.write("".join(prevTextLine))

            # Give debugging output in terminal:
            if (Debug_Flag == 0) or (Debug_Flag == 1):
                print(" <" + str(nLines) + ">: " + "NEWLINE!!!")

            # Release all locks at newline:
            BodyLock = False
            TitleLock = False
            AuthorsLock = False
            CaptionsLock = False
            GarbichLock = False
            HeadlinesLock = False
            AbstractLock = False
            KeyWordsLock = False
            RemainLock = False

        # Next, we test for the locks and, if positive, we add to that file, independent
        # of other tests. That is the puprose of the locks:
        elif BodyLock:
            Body.write("".join(prevTextLine))

            # Give debugging output in terminal:
            if (Debug_Flag == 0) or (Debug_Flag == 2):
                print(" <" + str(nLines) + ">: " + "BODY >>> " + prevTextLine)

        elif TitleLock:
            Title.write("".join(prevTextLine))

            # Give debugging output in terminal:
            if (Debug_Flag == 0) or (Debug_Flag == 10):
                print(" <" + str(nLines) + ">: " + "TITLE >>> " + prevTextLine)

        elif AuthorsLock:
            Authors.write("".join(prevTextLine))

            # Give debugging output in terminal:
            if (Debug_Flag == 0) or (Debug_Flag == 3):
                print(" <" + str(nLines) + ">: " + "AUTHORS >>> " + prevTextLine)

        elif CaptionsLock:
            Captions.write("".join(prevTextLine))

            # Give debugging output in terminal:
            if (Debug_Flag == 0) or (Debug_Flag == 4):
                print(" <" + str(nLines) + ">: " + "CAPTIONS >>> " + prevTextLine)

        elif GarbichLock:
            Garbich.write("".join(prevTextLine))

            # Give debugging output in terminal:
            if (Debug_Flag == 0) or (Debug_Flag == 5):
                print(" <" + str(nLines) + ">: " + "GARBICH >>> " + prevTextLine)

        elif HeadlinesLock:
            Headlines.write("".join(prevTextLine))

            # Give debugging output in terminal:
            if (Debug_Flag == 0) or (Debug_Flag == 6):
                print(" <" + str(nLines) + ">: " + "HEADLINES >>> " + prevTextLine)

        elif AbstractLock:
            Abstract.write("".join(prevTextLine))

            # Give debugging output in terminal:
            if Debug_Flag == 0 or Debug_Flag == 7:
                print(" <" + str(nLines) + ">: " + "ABSTRACT >>> " + prevTextLine)

        elif KeyWordsLock:
            KeyWords.write("".join(prevTextLine))

            # Give debugging output in terminal:
            if (Debug_Flag == 0) or (Debug_Flag == 9):
                print(" <" + str(nLines) + ">: " + "KEYWORDS >>> " + prevTextLine)

        elif RemainLock:
            Remain.write("".join(prevTextLine))

            # Give debugging output in terminal:
            if (Debug_Flag == 0) or (Debug_Flag == 8):
                print(" <" + str(nLines) + ">: " + "REMAIN >>> " + prevTextLine)

        # Start with filtering out the title based on line numbers:
        elif nLines in TitleArray:
            Title.write("".join(prevTextLine))
            # No need for a lock; a Title is manually selected.

            # Give debugging output in terminal:
            if (Debug_Flag == 0) or (Debug_Flag == 10):
                print(" <" + str(nLines) + ">: " + prevTextLine)

        # Next, attempt to filter out headlines by identifying if the first 
        # character is a number & the second one is a dot:
        elif ((StartNumber[1]) and ((Characters[1][1] == ".") or (Characters[1][1] == " ")) and (
                len(prevTextLine) > 7) and (not ("unive" in prevTextLine.lower())) and (nLetters[1] > 5) and (
                      ContainsCountry(prevTextLine) == False) and (nSpaces[1] < 10)):
            Headlines.write("".join(prevTextLine))
            # No need for a lock; a headline is always a single line.

            # Give debugging output in terminal:
            if (Debug_Flag == 0) or (Debug_Flag == 6):
                print(" <" + str(nLines) + ">: " + prevTextLine)

        # Next, filter out all URL-lines & Ref-lines:
        elif (nSlashes[1] > 1) or (Characters[0][1] == "["):
            Garbich.write("".join(prevTextLine))
            # Too risky to use a lock here.

            # Give debugging output in terminal:
            if (Debug_Flag == 0) or (Debug_Flag == 5):
                print(" <" + str(nLines) + ">: " + prevTextLine)

        # Test on first word:
        elif (nWords[1] > 0) and ((Characters[0][0] == "\n") or (nWords[0] == 0)):

            # Figure captions:
            if (PrevLine[0].lower().startswith("fig.")) or (PrevLine[0].lower().startswith("table")):
                Captions.write("".join(prevTextLine))
                CaptionsLock = True  # Because a caption may be on multiple lines...

                # Give debugging output in terminal:
                if (Debug_Flag == 0) or (Debug_Flag == 4):
                    print(" <" + str(nLines) + ">: " + prevTextLine)

            # Abstract:
            if ((PrevLine[0].lower().startswith("abstract")) or (PrevLine[0].lower().startswith("summary")) or (
                    PrevLine[0].lower().startswith("samenvatting"))):
                Abstract.write("".join(prevTextLine))
                AbstractLock = True  # Because te abstract extends over multiple lines.

                # Give debugging output in terminal:
                if (Debug_Flag == 0) or (Debug_Flag == 7):
                    print(" <" + str(nLines) + ">: " + prevTextLine)

        # Keywords:
        elif (nWords[1] > 0) and (PrevLine[0].lower().startswith("keyword")):
            KeyWords.write("".join(prevTextLine))
            KeyWordsLock = True  # Because the abstract extends over multiple lines.

            # Give debugging output in terminal:
            if (Debug_Flag == 0) or (Debug_Flag == 9):
                print(" <" + str(nLines) + ">: " + prevTextLine)

        # Next, filter out author lines:
        elif nDots[1] > 3:
            Authors.write("".join(prevTextLine))
            AuthorsLock = True  # A lock eliminates also a small part of the body. But no lock leaves too many author-lines for the body.
            # Using a lock is, therefore, better.

            # Give debugging output in terminal:
            if (Debug_Flag == 0) or (Debug_Flag == 3):
                print(" <" + str(nLines) + ">: " + prevTextLine)
                print(nDots[1])

        elif nCommas[1] > 5:
            Authors.write("".join(prevTextLine))
            # We do NOT use a lock for Comma's as there are some lines in the body of the text that match these criteria. So a lock would eliminate too much.

            # Give debugging output in terminal:
            if (Debug_Flag == 0) or (Debug_Flag == 3):
                print(" <" + str(nLines) + ">: " + prevTextLine)

        elif (("unive" in prevTextLine.lower()) or (
                ContainsCountry(prevTextLine))):  # Then it is probably an address line
            Authors.write("".join(prevTextLine))
            # We do NOT use a lock as this is usually just a single text line.

            # Give debugging output in terminal:
            if (Debug_Flag == 0) or (Debug_Flag == 3):
                print(" <" + str(nLines) + ">: " + prevTextLine)

        # Next, we eliminate the lines that are too short (for example, because a few words are taken from the tables:
        elif nWords[1] < 4:
            Garbich.write("".join(prevTextLine))
            # We do NOT use a lock, as these are all single-lines that are not enclosed by whitelines.

            # Give debugging output in terminal:
            if (Debug_Flag == 0) or (Debug_Flag == 5):
                print(" <" + str(nLines) + ">: " + prevTextLine)

        # The rest can go into the body:
        else:
            Body.write("".join(prevTextLine))
            # Remain.write("".join(prevTextLine))

            # Give debugging output in terminal:
            if (Debug_Flag == 0) or (Debug_Flag == 2):
                print(" <" + str(nLines) + ">: " + prevTextLine)

        # --------------------------------------------------------------------------------------
        # ### End of the loop actions: ###

        # Update FIRST ancient line and THEN previous test line:
        ancientTextLine = prevTextLine
        prevTextLine = lineOfText

        # Raise the index of the current line:
        nLines = nLines + 1
