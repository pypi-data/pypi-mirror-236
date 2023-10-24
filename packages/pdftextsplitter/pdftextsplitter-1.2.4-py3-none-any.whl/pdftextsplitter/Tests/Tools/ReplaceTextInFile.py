def ReplaceTextInFile(thefile: str, theoriginal: str, thereplaced: str):
    """
    This function will open a textfile and then replace one phrase
    with another everywhere it occurs.
    # Parameters:
    thefile: str: the file to work on, including its full path.
    theoriginal: str: the text that has to be replaced
    thereplaced: str: the text we replace it with.
    # Return: None.
    """
  
    # Opening our text file in read only
    # mode using the open() function
    with open(thefile, 'r') as myfile:
  
        # Reading the content of the file
        # using the read() function and storing
        # them in a new variable
        data = myfile.read()
  
        # Searching and replacing the text
        # using the replace() function
        data = data.replace(theoriginal, thereplaced)
  
    # Opening our text file in write only
    # mode to write the replaced content
    with open(thefile, 'w') as myfile:
  
        # Writing the replaced data in our
        # text file
        myfile.write(data)
  
    # Done.
    
