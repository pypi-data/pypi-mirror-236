# Function definition:
def GetTitleLines(filename: str) -> list[int]:
    '''
    This function returns the lines that contain the
    document title based on the filename. This means that,
    in order to know the Title-lines, the document template
    must be known in advance.
    
    Parameters:
    filename (str): name of the specific .txt/.pdf file to be worked with.
                    NB: Without the .txt/.pdf-extension.
    
    Return:
    TitleArray (List[int]): An array with integers: the textlines where
                            the document title is located. Hardcoded.
    '''

    # ------------------------------------------------------------------

    if (filename=="CADouma_DNN_Publication"): 
        TitleArray = [8, 9]
    
    elif (filename=="CADouma_Veto_Publication"): 
        TitleArray = [8, 9]
    
    elif (filename=="CADouma_BGT_Publication"): 
        TitleArray = [7, 8]
        
    elif (filename=="BigTest"): 
        TitleArray = [28, 29, 30, 31]
        
    elif (filename=="SplitDoc"): 
        TitleArray = [1, 2]
        
    else:
        TitleArray = [18, 19]
    
    return TitleArray
