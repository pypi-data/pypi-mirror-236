# import statements:
from PIL import Image

# Function definition:
def CompareImages(file1: str, file2: str) -> float:
    """
    Function that compares the pixel content of two images and
    investigates whether the pictures are equal or not.
    
    # Parameters:
    file1 (str): filename of the first picture to compare, including the full path to the file location and including its file extension.
    file2 (str): filename of the second picture to compare, including the full path to the file location and including its file extension.
    
    # Returns:
    float: percentage of how much pixels are different between the two pictures. If the pictures are equal,
           this return argument is 0.0. If the pictures have different sizes, the answer is 101.0 (> 100%; completely different).
           If the sizes are equal, but the pixel content is different for some pixels in the pictures, but the
           same for other pixels, then the return is the percentage of pixels that are different.
    """
    
    # ------------------------------------------------------------------------------------
    
    # Open the files using Pillow
    img1 = Image.open(file1)
    img2 = Image.open(file2)

    # Get the sizes of the images
    size1 = img1.size
    size2 = img2.size

    # If the sizes are different, the images are different
    if size1 != size2:
        return 101.0 # we pretend that the difference is maximal, so 100%.

    # Then, if the sizes are equal: compare each pixel in the images:
    nr_of_equal_pixels = 0
    nr_of_unequal_pixels = 0
    
    for x in range(size1[0]):
        for y in range(size1[1]):
            if img1.getpixel((x, y)) != img2.getpixel((x, y)):
                nr_of_unequal_pixels += 1
            else:
                nr_of_equal_pixels += 1

    # Then, draw conclusions:
    if nr_of_unequal_pixels == 0:
        return 0.0 # then the difference is nonexistent, so 0%.
    else:
        # return percentage:
        percentage = 100.0*nr_of_unequal_pixels / (nr_of_equal_pixels + nr_of_unequal_pixels)
        return percentage
