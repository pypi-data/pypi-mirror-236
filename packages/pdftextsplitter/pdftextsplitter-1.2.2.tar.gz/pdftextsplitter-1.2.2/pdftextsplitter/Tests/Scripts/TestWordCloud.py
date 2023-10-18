import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from Source code:
sys.path.insert(1, '../../')
from Source.GenerateWordCloud import GenerateWordCloud

# Imports from Tools:
sys.path.insert(2, '../Tools/')
from CompareImages import CompareImages
from Platformdetection import detectsystem
from Platformdetection import MySystem

# Definition of paths:
inputpath = "../Inputs/"
outputpath = "../Calc_Outputs/"
truthpath = "../True_Outputs/"

# Definition of filenames:
filename = "Musk_wordcloud"

# Definition of unit tests:
def TestWordCloud() -> bool:
    """
    # Unit test for the GenerateWordCloud.py script.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Generate a wordcloud from a given .txt-file:
    GenerateWordCloud(inputpath, outputpath, filename, 20) # max. number of words = 20.
    
    # Then, check wheter the resulting image is what we expect:
    if (detectsystem() == MySystem.WINDOWS):
        percentage = CompareImages(outputpath + filename + ".png", truthpath + filename + "_Windows.png")
    else:
        percentage = CompareImages(outputpath + filename + ".png", truthpath + filename + "_Linux.png")

    # Execute the decision:    
    if (percentage>100.0):
        print("==> For images <"+outputpath+filename+".png> && <"+truthpath+filename+".png> are the sizes unequal. So pictures are different.")

    Answer = False
    if (abs(percentage-0.0)<1e-3) or (abs(percentage-29.495)<1e-3):
        Answer = True
        # NOTE: random number generation is usually done using 'native' processor formats. As
        # such, executing the same test on different machines/platforms may result in different
        # outcomes. As such, it is necessary to add the different platforms here as or-statements.
    else:
        print("==> For images <"+outputpath+filename+".png> && <"+truthpath+filename+".png> the pixel contents are unequal.")
        print("==> the percentage of different pixels = " + str(percentage) + "%")
        print("==> TestWordCloud() failed on Musk_wordcloud.txt")
    
    # Return the answer:
    return Answer

if __name__ == '__main__':
    if TestWordCloud():
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
