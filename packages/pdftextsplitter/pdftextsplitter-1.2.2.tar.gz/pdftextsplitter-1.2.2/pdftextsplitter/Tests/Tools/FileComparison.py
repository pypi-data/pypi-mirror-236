# Function definition:
def FileComparison(filename1: str, filename2: str, option: str) -> str:
    """
    This function compares 2 textfiles and generates a 
    report on which lines are different.

    # Parameters:
    filename1 (str): absolute path + name of the first  file to compare (without the .txt)
    filename2 (str): absolute path + name of the second file to compare (without the .txt)
    option (str): determines the filetype: txt or html.

    # Returns (str):
    string that can be printed or processed about the differences
    """

    # ------------------------------------------------------------

    # Begin with reading the files, according to the filetype:
    if (option=="txt"):
        f1 = open(filename1 + ".txt", "r", encoding='utf-8', errors='ignore')
        f2 = open(filename2 + ".txt", "r", encoding='utf-8', errors='ignore')
        
    elif(option=="html"):
        f1 = open(filename1, "r", encoding="utf-8")
        f2 = open(filename2, "r", encoding="utf-8")
    
    else:
        return "Filetype <"+option+"> is unsupported!"

    # Next, read the lines from the files:
    f1_data = f1.readlines()
    f2_data = f2.readlines()

    # initialize indices & rapport:
    i = 0
    j = 0
    rapport = ""

    # loop over the first file:
    for line1 in f1_data:

        # increase first index:
        i = i + 1
        j = 0

        # then, loop over the second file: 
        for line2 in f2_data:

            # Also, update this index:
            j = j + 1

            # Then, we should obviously only act if the indices are the same:
            if i == j:

                # then, compare:
                if not (line1 == line2):
                    # Then, append to the rapport:
                    rapport = rapport + "LINE " + str(i) + ": File1=<" + line1.replace("\n","") + "> && File2=<" + line2.replace("\n", "") + ">\n"

    # Then, also check if the total number of lines are the same:
    if not (i == j):
        rapport = rapport + "==> len(File1)=" + str(i) + " && len(File2)=" + str(j) + "\n\n"

    # Then, close the files:
    f1.close()
    f2.close()
    
    # Add filenames to the rapport:
    if not (rapport == ""):
        rapport = "==> File1 = " + str(filename1) + "\n" + "==> File2 = " + str(filename2) + "\n" + rapport

    # And return the rapport:
    return rapport
