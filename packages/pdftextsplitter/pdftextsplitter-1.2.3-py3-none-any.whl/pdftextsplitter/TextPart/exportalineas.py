def exportalineas_textsplitter(self, option: str):
    """
    Function to export the content of the splitted alinea's
    to a .txt-file.
    
    # Parameters:
    option: str: decides what kind of export you want: default (not all textual content is printed), or complete (all is printed).
    # Return: None (the .txt-file)
    """
    
    # ---------------------------------------------------------------------------
    
    # Begin by opening a new .txt-file:
    exportfile = open(self.outputpath + self.documentname + "_BreakdownResults.txt", 'w', encoding="utf-8")
    
    # Next, loop over the alineas:
    if (len(self.textalineas)>0):
        
        # Begin by adding some general comments:
        exportfile.write("################################################################\n")
        exportfile.write("### [TEXTSPLITTER CLASS] #######################################\n")
        exportfile.write("### [Breakdown results for document "+self.documentname + "] ###\n")
        exportfile.write("################################################################\n")
        exportfile.write("\n")
        
        # Then, loop over the textalineas:
        for alinea in self.textalineas:
            
            exportfile.write("---------------------------------------------------------------------------------\n")
            exportfile.write(" [ALINEA-TITLE] Cascade-level="+str(alinea.textlevel)+"\n")
            exportfile.write(" [TITLE] = " + alinea.texttitle+"\n")
            exportfile.write(" nativeID="+str(alinea.nativeID)+" parentID="+str(alinea.parentID)+" & horizontal_ordering="+str(alinea.horizontal_ordering)+"\n")
            exportfile.write(" texttype="+str(alinea.alineatype)+" & enumeration-type="+str(alinea.enumtype)+"\n")
            exportfile.write(" Summary Flag = "+str(alinea.sum_CanbeEmpty)+"\n")
            exportfile.write("\n")
        
            exportfile.write(" [ALINEA-SUMMARY]:\n")
            exportfile.write(alinea.summary + "\n")
            exportfile.write("\n")
            
            exportfile.write(" [ALINEA-CONTENT]:\n")
            
            # Loop over the textlines:
            lineindex = 0
            contentlength = len(alinea.textcontent)
            for textline in alinea.textcontent:
                
                # Execute different options:
                if (option=="complete"):
                    exportfile.write(textline + "\n")
                    
                else: # Default setting:
                    
                    if (lineindex in range(0,3))or((contentlength-lineindex-1) in range(0,3)): exportfile.write(textline + "\n")
                    if (lineindex==2): exportfile.write("\n          ***          [--- more alinea content ---]        ***          \n\n")
                
                # Increase lineindex:
                lineindex = lineindex + 1
            
            # At the end of the alinea, print another whiteline:
            exportfile.write("\n")
        
        # Finally, close off:
        exportfile.write("---------------------------------------------------------------------------------\n")
    
    else:
        
        exportfile.write("You did not execute textsplitter.breakdown() before calling this function.\n")
        exportfile.write("As such, we could not display any splitted content for document\n")
        exportfile.write(self.documentname + "\n")
        exportfile.write("\n")
    
    # Close off:
    exportfile.close()
       
