# Function definition:
def ByteComparison(base_image_filename: str, compare_image_filename: str) -> bool:
    """
    Compares two arbitrary files based on their Bytes-content. Returns True
    if the file-contents are exact matches and False otherwise.
  
    Parameters:
    # base_image_filename (str):    first image to compare, including the full path and file-extension
    # compare_image_filename (str): second image to compare, including the full path and file-extension
  
    Return:
    # bool: the answer to the file comparison.
          
    """

    # -----------------------------------------------------------

    # Open both files:    
    f1 = open(base_image_filename, 'rb')
    f2 = open(compare_image_filename, 'rb')

    # Extrat there content in bytes:
    contents1 = f1.read()
    contents2 = f2.read()

    # Close the images:
    f1.close()
    f2.close()

    # Compare bytes to see if the content of the files are an exact match:
    Answer = (contents1 == contents2)
    if not Answer:
        print(base_image_filename + " && " + compare_image_filename + " are NOT identical!")
    return Answer
