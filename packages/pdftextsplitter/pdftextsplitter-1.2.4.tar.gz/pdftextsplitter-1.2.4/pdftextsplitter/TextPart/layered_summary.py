# Textpart imports:
from .textalinea import textalinea

def layered_summary_textsplitter(self, verbose_option=0) -> int:
    """
    This function utilizes textsplitter.summarize() to provide
    each textalinea-element in textsplitter with a filled summary-field.
    The idea is that for textalineas with the highest cascade-level, 
    we simply fill textalinea.summary by calling textsplitter.summarize
    on the content of textalinea.textcontent. For lower cascade-levels,
    we call textalinea.summary on textalinea.textcontent + sum(textalinea.summary)
    where the sum runs over all direct childern of the element. This
    can be identified using the parentID-field and the order of the
    sum is prescribed by the horizontal_ordering field. As such,
    textsplitter.calculatetree() should be called before calling this function.
    
    # Parameters:
    verbose_option: int: 0 be default, but can be different then 0 to suppress or display warnings.
    # Return: int: the number of errors we encountered due to encountering
    # children of an alinea with empty summaries.
    """
    
    # ---------------------------------------------------------------------
    
    # Before we begin: if there are no alineas, we cannot do anything:
    if (len(self.textalineas)==0): return -1
    
    # First, define the number of possible errors:
    Num_Errors = 0
    
    # Next, open a log-file for ChatGPT-calls:
    if (verbose_option>=0):
        self.logfile = open(self.outputpath + self.documentname + "_ChatGPT_Logging.txt",'w')
    
    # Then, clean out all flags (they are properly set in this function):
    for alinea in self.textalineas:
        alinea.sum_CanbeEmpty = False
    
    # The code is written in such a way that the ordering of the textalineas
    # does not matter. so we begin by extracting all cascadelevels:
    allcascades = []
    
    for alinea in self.textalineas:
        allcascades.append(alinea.textlevel)
    
    # Define max and min:
    mincascadelevel = 0
    maxcascadelevel = max(allcascades)
    
    # Define other variables we need:
    text_tosummarize = ""
    thissummary = ""
    children_array = []
    
    # Now: we need to loop over textalineas multiple times, because we
    # need to start summarizing the lower levels before we can do the
    # upper ones:
    for thiscascade in range(mincascadelevel,maxcascadelevel+1):
        
        # Define current cascade level. we want to loop from high to low:
        current_cascade = maxcascadelevel - thiscascade
        
        # Then, loop over all alineas:
        for currentalinea in self.textalineas:
            
            # Then, only deal with the alineas that conform to
            # the selected cascade level:
            if (current_cascade==currentalinea.textlevel):
                
                # Then, start generating the text to summarize:
                text_tosummarize = ""
                for textline in currentalinea.textcontent:
                    
                    # Append the textline:
                    text_tosummarize = text_tosummarize + textline
                    
                    # If the textline does not end in a newline, add it:
                    if (len(text_tosummarize)>0):
                        if not (text_tosummarize[len(text_tosummarize)-1]=="\n"):
                            text_tosummarize = text_tosummarize + "\n"
                
                # Now, if this is one of the highest levels, creating it is easy;
                if (current_cascade==maxcascadelevel):
                    
                    # Now, check if there is something to be summarized:
                    if (len(text_tosummarize)>5):
                    
                        # Then, we can just summarize text_tosummarize:
                        thissummary = self.summarize(text_tosummarize,verbose_option)
                        # 0: verbose-option = quiet.
                    
                        # and add it to the current alinea:
                        currentalinea.summary = thissummary
                        
                        # And properly set the flag:
                        currentalinea.sum_CanbeEmpty = False
                        
                    else:
                        
                        # Then, there is nothing to summarize:
                        currentalinea.sum_CanbeEmpty = True
                        currentalinea.summary = ""
                    
                    # Next, calculate word-statistics:
                    currentalinea.summarized_wordcount = len(currentalinea.summary.split())
                    currentalinea.total_wordcount = 0
                    for textline in currentalinea.textcontent:
                        currentalinea.total_wordcount = currentalinea.total_wordcount + len(textline.split())
                    
                    # Calculate meta-data:
                    currentalinea.nr_decendants = 0 # If this object has no children, it is easy. Just all 0.
                    currentalinea.nr_children = 0   # If this object has no children, it is easy. Just all 0.
                    currentalinea.nr_depths = 0     # If this object has no children, it is easy. Just all 0.
                    
                    # Calculate number of pages:
                    if (len(currentalinea.pagenumbers)==0):
                        currentalinea.nr_pages = 0
                    else:
                        max_page = max(currentalinea.pagenumbers)
                        min_page = min(currentalinea.pagenumbers)
                        currentalinea.nr_pages = max_page - min_page + 1
                
                else:
                    
                    # Then, we must also look for the children of the current alinea:
                    children_array.clear()
                    
                    for child_alinea in self.textalineas:
                        
                        # test that we do not take the same one:
                        if not (child_alinea.nativeID==currentalinea.nativeID):
                            
                            # Then, test for the parent:
                            if (child_alinea.parentID==currentalinea.nativeID):
                                
                                # Then, this alinea is a child of currentalinea:
                                children_array.append(child_alinea)
                    
                    # Next, we must sort this array based on increasing horizontal ordering:
                    children_array = sorted(children_array, key=lambda x: x.horizontal_ordering, reverse=False)
                    
                    # and then, we must add the summary of the children to text_tosummarize:
                    for thischild in children_array:
                        
                        # Then, test if the summary is not empty when it should not be empty:
                        if (len(thischild.summary)<3)and(thischild.sum_CanbeEmpty==False):
                            
                            # Then, give a warning:
                            if (verbose_option>=0): print("WARNING: you used an empty child-summary that is not supposed to be empty. This should not be possible!")
                                # NOTE: we are supposed to 
                            
                            # And, count the error:
                            Num_Errors = Num_Errors + 1
                            
                        else:
                            
                            # Then, append the summary-text:
                            text_tosummarize = text_tosummarize + thischild.summary
                        
                            if (len(text_tosummarize)>0):
                                if not (text_tosummarize[len(text_tosummarize)-1]=="\n"):
                                    text_tosummarize = text_tosummarize + "\n"
                    
                    # and then, after closing the for-loop on the children, we can create a new summary:
                    # So, check if there is something to be summarized:
                    if (len(text_tosummarize)>5):
                        
                        thissummary = self.summarize(text_tosummarize,verbose_option)
                        # 0: verbose-option = quiet.
                    
                        # and add it to the current alinea:
                        currentalinea.summary = thissummary
                        
                        # And properly set the flag:
                        currentalinea.sum_CanbeEmpty = False
                        
                    else:
                        
                        # Then, there is nothing to summarize:
                        currentalinea.sum_CanbeEmpty = True
                        currentalinea.summary = ""
                    
                    # Next, calculate word-statistics:
                    currentalinea.summarized_wordcount = len(currentalinea.summary.split())
                    for thischild in children_array:
                        currentalinea.summarized_wordcount = currentalinea.summarized_wordcount + len(thischild.texttitle.split())
                    
                    currentalinea.total_wordcount = 0
                    for textline in currentalinea.textcontent:
                        currentalinea.total_wordcount = currentalinea.total_wordcount + len(textline.split())
                        
                    for thischild in children_array:
                        currentalinea.total_wordcount = currentalinea.total_wordcount + thischild.total_wordcount
                    
                    # Next, calculate meta-data. 
                    currentalinea.nr_decendants = 0 # If this object has no children, it is easy. Just all 0.
                    currentalinea.nr_children = 0   # If this object has no children, it is easy. Just all 0.
                    currentalinea.nr_depths = 0     # If this object has no children, it is easy. Just all 0.
                    
                    # Next, loop over the children-arrays to add the proper information.
                    # Begin by appointing arrays that we may need:
                    depth_array = []
                     
                    # Then, start the for-loop:
                    for thischild in children_array:
                        
                        # Total number of decendants:
                        currentalinea.nr_decendants = currentalinea.nr_decendants + thischild.nr_decendants + 1
                        
                        # Total number of direct children:
                        currentalinea.nr_children = currentalinea.nr_children + 1
                        
                        # Total depth:
                        depth_array.append(thischild.nr_depths)
                        
                        # Total number of pages:
                        for somenumber in thischild.pagenumbers:
                            currentalinea.pagenumbers.append(somenumber)
                    
                    # Next, finish up meta-data after closing the for-loop:
                    if (len(depth_array)==0):
                        currentalinea.nr_depths = 0
                    else:
                        currentalinea.nr_depths = max(depth_array)+1
                    
                    # Finish Calculation of the number of pages:
                    if (len(currentalinea.pagenumbers)==0):
                        currentalinea.nr_pages = 0
                    else:
                        max_page = max(currentalinea.pagenumbers)
                        min_page = min(currentalinea.pagenumbers)
                        currentalinea.nr_pages = max_page - min_page + 1
    
    # That should do the trick and summarize everything. First handle the log-file:
    if (verbose_option>=0):
        self.logfile.write("\nThe number of counted calls = " + str(self.callcounter) + "\n")
        self.logfile.write("The total costs for the document are: " + str(self.api_totalprice) + " euro's\n")
        self.logfile.write("We had to accept " + str(self.api_wrongcalls_duetomaxwhile) + " incorrect summaries due to the while-limit.\n")
        self.logfile.write("We use language-option " + str(self.LanguageChoice) + ".\n")
        self.logfile.write("We use language model " + str(self.LanguageModel) + ".\n")
    
    # Add some information in dummy-mode:
    if (self.UseDummySummary==True)and(verbose_option>=0):
        self.logfile.write("==> ATTENTION: We used the textsplitter in dummy-mode. So the logging information is meaningless!!!\n")
    
    if (verbose_option>=0):
        self.logfile.close()
    
    # Return the output:
    return Num_Errors
