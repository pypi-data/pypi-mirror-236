import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from TextPart code:
sys.path.insert(1, '../../')
from TextPart.textpart import textpart
from TextPart.fontregion import fontregion

# Imports from Tools:
sys.path.insert(2, '../Tools/')
from FileComparison import FileComparison
from CompareImages import CompareImages
from hardcodedfontsizehist import hardcodedfontsizehist
from hardcodedfontregions import hardcodedfontregions

# Definition of paths:
inputpath = "../Inputs/"
outputpath = "../Calc_Outputs/"
truthpath = "../True_Outputs/"

# Definition of filenames:
filename = "SplitDoc"

# Definition of unit tests:
def fontregion_testfindfontregions() -> bool:
    """
    # Unit test for the findfontregions functionality of the textpart-class (multi-bin case):
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define histogram input:
    histogram = hardcodedfontsizehist()
    
    # Define true font regions:
    trueregions = hardcodedfontregions("pdfminer")

    # Create a textpart-class:
    thetest = textpart()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.set_labelname("Somelabel")
    thetest.histogramsize=100
    
    # Enter histogram information:
    thetest.fontsizeHist_percharacter = histogram
    
    # Then, calculate the fontsize regions:
    thetest.findfontregions()
    
    # then, find out if the output is as expected:
    Answer = True
    index = 0
    if (len(thetest.fontregions)==len(trueregions)):
        for region in thetest.fontregions:
            if not region.compare(trueregions[index]):
                Answer = False
                print("Computed FONTregion "+str(index)+" deviated from its intended value:")
                region.printregion()
                trueregions[index].printregion()
                print("\n")
            index +=1
    else:
        Answer = False
        print("The number of computed FONTregions ("+str(len(thetest.fontregions))+") was different then what was expected (6):")
        for region in thetest.fontregions:
            region.printregion()
        print("\n")
        
    return Answer

def fontregion_testfindfontregions_2bin_a() -> bool:
    """
    # Unit test for the findfontregions functionality of the textpart-class (2-bin case):
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define histogram input:
    histcontent = [ 100.0, 79.0 ]
    histbins = [ 1.0, 2.0, 3.0 ]
    histogram = [histcontent, histbins, histbins]
    
    # Define true font regions:
    trueregion = fontregion()
    
    trueregion.set_left(0.0)
    trueregion.set_right(3.0)
    trueregion.set_value(1.5)
    trueregion.set_frequency(100.0/179.0)
    trueregion.set_cascadelevel(1)
    trueregion.set_isregular(True)

    # Create a textpart-class:
    thetest = textpart()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.set_labelname("Somelabel")
    thetest.histogramsize=2
    
    # Enter histogram information:
    thetest.fontsizeHist_percharacter = histogram
    
    # Then, calculate the fontsize regions:
    thetest.findfontregions()
    
    # then, find out if the output is as expected:
    Answer = True
    if (len(thetest.fontregions)==1):
            if not thetest.fontregions[0].compare(trueregion):
                Answer = False
                print("The 2-bin computed FONTregion deviated from its intended value:")
                thetest.fontregions[0].printregion()
                trueregion.printregion()
                print("\n")
    else:
        Answer = False
        print("The number of computed FONTregions ("+str(len(thetest.fontregions))+") was different then what was expected (1):")
        for region in thetest.fontregions:
            region.printregion()
        print("\n")
        
    return Answer

def fontregion_testfindfontregions_2bin_b() -> bool:
    """
    # Unit test for the findfontregions functionality of the textpart-class (2-bin case):
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define histogram input:
    histcontent = [ 79.0, 100.0 ]
    histbins = [ 1.0, 2.0, 3.0 ]
    histogram = [histcontent, histbins, histbins]
    
    # Define true font regions:
    trueregion = fontregion()
    
    trueregion.set_left(1.0)
    trueregion.set_right(4.0)
    trueregion.set_value(2.5)
    trueregion.set_frequency(100.0/179.0)
    trueregion.set_cascadelevel(1)
    trueregion.set_isregular(True)

    # Create a textpart-class:
    thetest = textpart()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.set_labelname("Somelabel")
    thetest.histogramsize=2
    
    # Enter histogram information:
    thetest.fontsizeHist_percharacter = histogram
    
    # Then, calculate the fontsize regions:
    thetest.findfontregions()
    
    # then, find out if the output is as expected:
    Answer = True
    if (len(thetest.fontregions)==1):
            if not thetest.fontregions[0].compare(trueregion):
                Answer = False
                print("The 2-bin computed FONTregion deviated from its intended value:")
                thetest.fontregions[0].printregion()
                trueregion.printregion()
                print("\n")
    else:
        Answer = False
        print("The number of computed FONTregions ("+str(len(thetest.fontregions))+") was different then what was expected (1):")
        for region in thetest.fontregions:
            region.printregion()
        print("\n")
        
    return Answer

def fontregion_testfindfontregions_1bin() -> bool:
    """
    # Unit test for the findfontregions functionality of the textpart-class (1-bin case):
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define histogram input:
    histcontent = [ 100.0 ]
    histbins = [ 1.0, 2.0 ]
    histogram = [histcontent, histbins, histbins]
    
    # Define true font regions:
    trueregion = fontregion()
    
    trueregion.set_left(0.0)
    trueregion.set_right(3.0)
    trueregion.set_value(1.5)
    trueregion.set_frequency(1.0)
    trueregion.set_cascadelevel(1)
    trueregion.set_isregular(True)

    # Create a textpart-class:
    thetest = textpart()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.set_labelname("Somelabel")
    thetest.histogramsize=1
    
    # Enter histogram information:
    thetest.fontsizeHist_percharacter = histogram
    
    # Then, calculate the fontsize regions:
    thetest.findfontregions()
    
    # then, find out if the output is as expected:
    Answer = True
    if (len(thetest.fontregions)==1):
            if not thetest.fontregions[0].compare(trueregion):
                Answer = False
                print("The 1-bin computed FONTregion deviated from its intended value:")
                thetest.fontregions[0].printregion()
                trueregion.printregion()
                print("\n")
    else:
        Answer = False
        print("The number of computed FONTregions ("+str(len(thetest.fontregions))+") was different then what was expected (1):")
        for region in thetest.fontregions:
            region.printregion()
        print("\n")
        
    return Answer
    
def fontregion_testcompare() -> bool:
    """
    # Unit test for the compare-functionality of the fontregion-class:
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    someregion1 = fontregion()
    someregion1.set_left(20.919190000000008)
    someregion1.set_right(24.78710000000001)
    someregion1.set_value(24.70301500000001)
    someregion1.set_frequency(0.06736842105263158)
    someregion1.set_cascadelevel(1)
    someregion1.set_isregular(False)
    
    someregion2 = fontregion()
    someregion2.set_left(someregion1.get_left())
    someregion2.set_right(someregion1.get_right())
    someregion2.set_value(someregion1.get_value())
    someregion2.set_frequency(someregion1.get_frequency())
    someregion2.set_cascadelevel(someregion1.get_cascadelevel())
    someregion2.set_isregular(someregion1.get_isregular())
    
    someregion3 = fontregion()
    someregion3.set_left(20.919190000000508)
    someregion3.set_right(24.78710000000001)
    someregion3.set_value(24.70301500000001)
    someregion3.set_frequency(0.06736842105263158)
    someregion3.set_cascadelevel(1)
    someregion3.set_isregular(False)
    
    someregion4 = fontregion()
    someregion4.set_left(20.919190000000008)
    someregion4.set_right(24.78710000000001)
    someregion4.set_value(24.70301500000001)
    someregion4.set_frequency(0.16736842105263158)
    someregion4.set_cascadelevel(1)
    someregion4.set_isregular(False)
    
    Answer = True
    if not someregion1.compare(someregion2): Answer = False # 1 & 2 are supposed to be the same.
    if not someregion1.compare(someregion3): Answer = False # 1 & 2 are supposed to treated as the same.
    if someregion1.compare(someregion4): Answer = False # 1 & 2 are supposed to treated as NOT the same.
    
    if not Answer:
        print("fontregion_testcompare(): Comparing fontregions did not work as expected.")

    return Answer

def fontregion_testisinregion() -> bool:
    """
    # Unit test for the compare-functionality of the fontregion-class:
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    someregion1 = fontregion()
    someregion1.set_left(20.919190000000008)
    someregion1.set_right(24.78710000000001)
    someregion1.set_value(24.70301500000001)
    someregion1.set_frequency(0.06736842105263158)
    someregion1.set_cascadelevel(1)
    someregion1.set_isregular(False)
    
    Answer = True
    if not someregion1.isinregion(24.72): Answer = False
    if someregion1.isinregion(24.79): Answer = False
    if someregion1.isinregion(20.9): Answer = False
    
    if not Answer:
        print("fontregion_testisinregion(): fontregion.isinregion() did not work as expected.")

    return Answer

def testfontregion_searchfunctions() -> bool:
    """
    # Unit test for the search-functionality of the textpart-class:
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Create a textpart-class:
    thetest = textpart()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.set_labelname("Somelabel")
    thetest.histogramsize=100
    
    # Specify the fontregions:
    trueregions = hardcodedfontregions("pdfminer")
    thetest.fontregions = trueregions
    Answer = True
    
    # Next, test our findfontregions:
    outcome = thetest.selectfontregion(13.1)
    if not outcome.compare(trueregions[1]):
        print("selectfontregion(13.1) was supposed to return:")
        trueregions[1].printregion()
        print("but returned instead:")
        outcome.printregion()
        print("\n")
        Answer = False
    
    outcome = thetest.selectfontregion(10.2)
    if not outcome.compare(trueregions[3]):
        print("selectfontregion(10.2) was supposed to return:")
        trueregions[3].printregion()
        print("but returned instead:")
        outcome.printregion()
        print("\n")
        Answer = False
        
    outcome = thetest.selectfontregion(27.0)
    for region in trueregions:
        if outcome.compare(region):
            print("selectfontregion(27.0) was supposed to return no agreements with any given fontregion, but instead returned:")
            region.printregion()
            Answer = False
                
    outcome = thetest.selectfontregion(7.3)
    for region in trueregions:
        if outcome.compare(region):
            print("selectfontregion(7.3) was supposed to return no agreements with any given fontregion, but instead returned:")
            region.printregion()
            Answer = False
    
    # Next, see if we can properly find the regular region:
    outcome = thetest.findregularfontregion()
    if not outcome.compare(trueregions[3]):
        print("findregularfontregion() was supposed to return:")
        trueregions[3].printregion()
        print("but returned instead:")
        outcome.printregion()
        print("\n")
        Answer = False
        
    # Next, see if we properly can compare fontregions:
    if not (thetest.fontsize_smallerthenregular(8.0)==True): 
        Answer = False
        print("fontsize_smallerthenregular(8.0) is supposed to return True with the SplitDoc-structure")
    
    if not (thetest.fontsize_smallerthenregular(10.1)==False): 
        Answer = False
        print("fontsize_smallerthenregular(10.1) is supposed to return False with the SplitDoc-structure")
    
    if not (thetest.fontsize_smallerthenregular(15.0)==False): 
        Answer = False
        print("fontsize_smallerthenregular(15.0) is supposed to return False with the SplitDoc-structure")
        
    # ----------------------------
    
    if not (thetest.fontsize_equalstoregular(8.0)==False): 
        Answer = False
        print("fontsize_equalstoregular(8.0) is supposed to return False with the SplitDoc-structure")
    
    if not (thetest.fontsize_equalstoregular(10.1)==True): 
        Answer = False
        print("fontsize_equalstoregular(10.1) is supposed to return True with the SplitDoc-structure")
    
    if not (thetest.fontsize_equalstoregular(15.0)==False): 
        Answer = False
        print("fontsize_equalstoregular(15.0) is supposed to return False with the SplitDoc-structure")
        
    # ----------------------------
    
    if not (thetest.fontsize_biggerthenregular(8.0)==False): 
        Answer = False
        print("fontsize_biggerthenregular(8.0) is supposed to return False with the SplitDoc-structure")
    
    if not (thetest.fontsize_biggerthenregular(10.1)==False): 
        Answer = False
        print("fontsize_biggerthenregular(10.1) is supposed to return False with the SplitDoc-structure")
    
    if not (thetest.fontsize_biggerthenregular(15.0)==True): 
        Answer = False
        print("fontsize_biggerthenregular(15.0) is supposed to return True with the SplitDoc-structure")
        
    # ===========================================
    # Now, trigger bugs in the search on purpose:
    # ===========================================
    
    thetest.fontregions.pop(1)
    
    bugtest1 = thetest.selectfontregion(10.0)
    if not (bugtest1.get_cascadelevel()==-2):
        Answer = False
        print("After removing the regular FONTregion, selectfontregion(10.0) is supposed to return cascade=-2")
        bugtest1.printregion()
    
    bugtest2 = thetest.findregularfontregion()
    if not (bugtest2.get_cascadelevel()==-1):
        Answer = False
        print("After removing the regular FONTregion, findregularfontregion() is supposed to return cascade=-1")
        bugtest2.printregion()
    
    # then, return the total answer:
    return Answer
    
# Definition of collection:    
def TestFontRegions() -> bool:
    """
    # Collection-function of unit-tests.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    Answer = True
    
    if (fontregion_testfindfontregions()==False): 
        Answer=False
        print('\n==> Multi-bin unit-test for findfontregions() failed!\n')
    
    if (fontregion_testfindfontregions_1bin()==False): 
        Answer=False
        print('\n==> 1-bin unit-test for findfontregions() failed!\n')
    
    if (fontregion_testfindfontregions_2bin_a()==False): 
        Answer=False
        print('\n==> 2-bin unit-test (a) for findfontregions() failed!\n')
        
    if (fontregion_testfindfontregions_2bin_b()==False): 
        Answer=False
        print('\n==> 2-bin unit-test (b) for findfontregions() failed!\n')
    
    if (fontregion_testcompare()==False): 
        Answer=False
        print('\n==> compare() unit-test for fontregion failed!\n')
    
    if (fontregion_testisinregion()==False): 
        Answer=False
        print('\n==> isinregion() unit-test for fontregion failed!\n')
        
    if (testfontregion_searchfunctions()==False):
        Answer = False
        print('\n==> testfontregion_searchfunctions() unit-test for fontregion failed!\n')
    
    return Answer

if __name__ == '__main__':
    if TestFontRegions():
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
