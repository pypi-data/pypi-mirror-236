import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from TextPart code:
sys.path.insert(1, '../../')
from TextPart.textpart import textpart
from TextPart.lineregion import lineregion

# Imports from Tools:
sys.path.insert(2, '../Tools/')
from FileComparison import FileComparison
from hardcodedwhitelinehist import hardcodedwhitelinehist_LineTest1
from hardcodedlineregions import hardcodedlineregions_pdfminer_LineTest1
from hardcodedlineregions import hardcodedlineregions_pdfminer_LineTest1_endpeaks

# Definition of paths:
inputpath = "../Inputs/"
outputpath = "../Calc_Outputs/"
truthpath = "../True_Outputs/"

# Definition of filenames:
filename = "SplitDoc"

# Definition of unit tests:
def lineregion_testfindlineregions() -> bool:
    """
    # Unit test for the findlineregions functionality of the textpart-class (multi-bin case):
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define histogram input:
    histogram = hardcodedwhitelinehist_LineTest1()
    
    # Define true font regions:
    truelineregions = hardcodedlineregions_pdfminer_LineTest1()

    # Create a textpart-class:
    thetest = textpart()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.set_labelname("Somelabel")
    thetest.histogramsize=100
    
    # Enter histogram information:
    thetest.whitespaceHist_perline = histogram
    
    # Then, calculate the fontsize regions:
    thetest.findlineregions()
    
    # then, find out if the output is as expected:
    Answer = True
    index = 0
    if (len(thetest.lineregions)==len(truelineregions)):
        for region in thetest.lineregions:
            if not region.compare(truelineregions[index]):
                Answer = False
                print("Computed LINEregion "+str(index)+" deviated from its intended value:")
                region.printregion()
                truelineregions[index].printregion()
                print("\n")
            index +=1
    else:
        Answer = False
        print("The number of computed LINEregions ("+str(len(thetest.lineregions))+") was different then what was expected ("+str(len(truelineregions))+"):")
        for region in thetest.lineregions:
            region.printregion()
        print("\n")
        
    return Answer

def lineregion_testfindlineregions_absorbing() -> bool:
    """
    # Unit test for the findlineregions functionality of the textpart-class (multi-bin case; absorbing of line regions):
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define histogram input:
    histogram_content = []
    for k in range(0,100):
        histogram_content.append(0.0)
    
    histogram_bins = []
    for k in range(0,101):
        histogram_bins.append(k)
        
    # Now make sure we get a situation with 3 sharp line regions & 2 very small ones that have to be absorbed:
    
    # Regular spike:
    histogram_content[80] = 100.0
    
    # 2 smaller spikes:
    histogram_content[10] = 40.0
    histogram_content[98] = 38.0
    
    # 2 spikes for absorbing:
    histogram_content[82] = 10.0
    histogram_content[78] = 10.0
    
    # Definbe histogram:
    histogram = [histogram_content, histogram_bins, histogram_bins]
   
    # Create a textpart-class:
    thetest = textpart()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.set_labelname("Somelabel")
    thetest.histogramsize=100
    
    # Enter histogram information:
    thetest.whitespaceHist_perline = histogram
    
    # Then, calculate the lineregions:
    thetest.findlineregions()
    
    # See if we have indeed 3 left:
    Answer = True
    if not (len(thetest.lineregions)==3):
        Answer = False
        print("In this absorbing test, we are supposed to have 5-2=3 regions left!")
    
    return Answer

def lineregion_testfindlineregions_endpeaks() -> bool:
    """
    # Unit test for the findlineregions functionality of the textpart-class (multi-bin case with endpeaks):
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define histogram input:
    histogram = hardcodedwhitelinehist_LineTest1()
    histogram[0][0] = 12.0
    histogram[0][99] = 12.0
    
    # Define true font regions:
    truelineregions = hardcodedlineregions_pdfminer_LineTest1_endpeaks()

    # Create a textpart-class:
    thetest = textpart()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.set_labelname("Somelabel")
    thetest.histogramsize=100
    
    # Enter histogram information:
    thetest.whitespaceHist_perline = histogram
    
    # Then, calculate the fontsize regions:
    thetest.findlineregions()
    
    # then, find out if the output is as expected:
    Answer = True
    index = 0
    if (len(thetest.lineregions)==len(truelineregions)):
        for region in thetest.lineregions:
            if not region.compare(truelineregions[index]):
                Answer = False
                print("Computed LINEregion "+str(index)+" deviated from its intended value:")
                region.printregion()
                truelineregions[index].printregion()
                print("\n")
            index +=1
    else:
        Answer = False
        print("The number of computed LINEregions ("+str(len(thetest.lineregions))+") was different then what was expected ("+str(len(truelineregions))+"):")
        for region in thetest.lineregions:
            region.printregion()
        print("\n")
        
    return Answer

def lineregion_testfindlineregions_2bin_a() -> bool:
    """
    # Unit test for the findlineregions functionality of the textpart-class (2-bin case):
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define histogram input:
    histcontent = [ 100.0, 79.0 ]
    histbins = [ 1.0, 2.0, 3.0 ]
    histogram = [histcontent, histbins, histbins]
    
    # Define true line regions:
    trueregion = lineregion()
    
    trueregion.set_left(0.0)
    trueregion.set_right(1e5)
    trueregion.set_value(1.5)
    trueregion.set_frequency(100.0/179.0)
    trueregion.set_isregular(True)
    trueregion.set_isvalid(True)
    trueregion.set_iszero(False)
    trueregion.set_issmall(False)
    trueregion.set_isbig(False)

    # Create a textpart-class:
    thetest = textpart()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.set_labelname("Somelabel")
    thetest.histogramsize=2
    
    # Enter histogram information:
    thetest.whitespaceHist_perline = histogram
    
    # Then, calculate the fontsize regions:
    thetest.findlineregions()
    
    # then, find out if the output is as expected:
    Answer = True
    if (len(thetest.lineregions)==1):
            if not thetest.lineregions[0].compare(trueregion):
                Answer = False
                print("The 2-bin computed LINEregion deviated from its intended value:")
                thetest.lineregions[0].printregion()
                trueregion.printregion()
                print("\n")
    else:
        Answer = False
        print("The number of computed LINEregions ("+str(len(thetest.lineregions))+") was different then what was expected (1):")
        for region in thetest.lineregions:
            region.printregion()
        print("\n")
        
    return Answer

def lineregion_testfindlineregions_2bin_b() -> bool:
    """
    # Unit test for the findlineregions functionality of the textpart-class (2-bin case):
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define histogram input:
    histcontent = [ 79.0, 100.0 ]
    histbins = [ 1.0, 2.0, 3.0 ]
    histogram = [histcontent, histbins, histbins]
    
    # Define true line regions:
    trueregion = lineregion()
    
    trueregion.set_left(1.0)
    trueregion.set_right(1e5)
    trueregion.set_value(2.5)
    trueregion.set_frequency(100.0/179.0)
    trueregion.set_isregular(True)
    trueregion.set_isvalid(True)
    trueregion.set_iszero(False)
    trueregion.set_issmall(False)
    trueregion.set_isbig(False)

    # Create a textpart-class:
    thetest = textpart()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.set_labelname("Somelabel")
    thetest.histogramsize=2
    
    # Enter histogram information:
    thetest.whitespaceHist_perline = histogram
    
    # Then, calculate the fontsize regions:
    thetest.findlineregions()
    
    # then, find out if the output is as expected:
    Answer = True
    if (len(thetest.lineregions)==1):
            if not thetest.lineregions[0].compare(trueregion):
                Answer = False
                print("The 2-bin computed LINEregion deviated from its intended value:")
                thetest.lineregions[0].printregion()
                trueregion.printregion()
                print("\n")
    else:
        Answer = False
        print("The number of computed LINEregions ("+str(len(thetest.lineregions))+") was different then what was expected (1):")
        for region in thetest.lineregions:
            region.printregion()
        print("\n")
        
    return Answer

def lineregion_testfindlineregions_1bin() -> bool:
    """
    # Unit test for the findlineregions functionality of the textpart-class (1-bin case):
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Define histogram input:
    histcontent = [ 100.0 ]
    histbins = [ 1.0, 2.0 ]
    histogram = [histcontent, histbins, histbins]
    
    # Define true font regions:
    trueregion = lineregion()
    
    trueregion.set_left(0.0)
    trueregion.set_right(1e5)
    trueregion.set_value(1.5)
    trueregion.set_frequency(1.0)
    trueregion.set_isregular(True)
    trueregion.set_isvalid(True)
    trueregion.set_iszero(False)
    trueregion.set_issmall(False)
    trueregion.set_isbig(False)

    # Create a textpart-class:
    thetest = textpart()
    thetest.set_documentpath(inputpath)
    thetest.set_documentname(filename)
    thetest.set_outputpath(outputpath)
    thetest.set_labelname("Somelabel")
    thetest.histogramsize=1
    
    # Enter histogram information:
    thetest.whitespaceHist_perline = histogram
    
    # Then, calculate the fontsize regions:
    thetest.findlineregions()
    
    # then, find out if the output is as expected:
    Answer = True
    if (len(thetest.lineregions)==1):
            if not thetest.lineregions[0].compare(trueregion):
                Answer = False
                print("The 2-bin computed LINEregion deviated from its intended value:")
                thetest.lineregions[0].printregion()
                trueregion.printregion()
                print("\n")
    else:
        Answer = False
        print("The number of computed LINEregions ("+str(len(thetest.lineregions))+") was different then what was expected (1):")
        for region in thetest.lineregions:
            region.printregion()
        print("\n")
        
    return Answer
    
def lineregion_testcompare() -> bool:
    """
    # Unit test for the compare-functionality of the fontregion-class:
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    lineregions = hardcodedlineregions_pdfminer_LineTest1()
    
    someregion1 = lineregions[0]
    someregion2 = lineregion()
    someregion3 = lineregion()
    someregion4 = lineregion()
    
    someregion2.set_right(someregion1.get_right())
    someregion2.set_left(someregion1.get_left())
    someregion2.set_value(someregion1.get_value())
    someregion2.set_frequency(someregion1.get_frequency())
    someregion2.set_isregular(someregion1.get_isregular())
    someregion2.set_isvalid(someregion1.get_isvalid())
    someregion2.set_iszero(someregion1.get_iszero())
    someregion2.set_issmall(someregion1.get_issmall())
    someregion2.set_isbig(someregion1.get_isbig())
    
    someregion3.set_right(someregion1.get_right())
    someregion3.set_left(someregion1.get_left())
    someregion3.set_value(someregion1.get_value()+1.0)
    someregion3.set_frequency(someregion1.get_frequency())
    someregion3.set_isregular(someregion1.get_isregular())
    someregion3.set_isvalid(someregion1.get_isvalid())
    someregion3.set_iszero(someregion1.get_iszero())
    someregion3.set_issmall(someregion1.get_issmall())
    someregion3.set_isbig(someregion1.get_isbig())
    
    someregion4.set_right(someregion1.get_right())
    someregion4.set_left(someregion1.get_left())
    someregion4.set_value(someregion1.get_value())
    someregion4.set_frequency(someregion1.get_frequency())
    someregion4.set_isregular(someregion1.get_isregular())
    someregion4.set_isvalid(someregion1.get_isvalid())
    someregion4.set_iszero(not(someregion1.get_iszero()))
    someregion4.set_issmall(someregion1.get_issmall())
    someregion4.set_isbig(someregion1.get_isbig())
    
    Answer = True
    if not someregion1.compare(someregion2): Answer = False # 1 & 2 are supposed to be the same.
    if someregion1.compare(someregion3): Answer = False # 1 & 2 are supposed to be treated as NOT the same.
    if someregion1.compare(someregion4): Answer = False # 1 & 2 are supposed to be treated as NOT the same.
    
    if not Answer:
        print("lineregion_testcompare(): Comparing lineregions did not work as expected.")

    return Answer

def lineregion_testisinregion() -> bool:
    """
    # Unit test for the compare-functionality of the lineregion-class:
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    someregion1 = lineregion()
    someregion1.set_left(20.919190000000008)
    someregion1.set_right(24.78710000000001)
    someregion1.set_value(24.70301500000001)
    someregion1.set_frequency(0.06736842105263158)
    someregion1.set_isregular(False)
    someregion1.set_isbig(False)
    someregion1.set_issmall(False)
    someregion1.set_isvalid(False)
    someregion1.set_iszero(False)
    
    Answer = True
    if not someregion1.isinregion(24.72): Answer = False
    if someregion1.isinregion(24.79): Answer = False
    if someregion1.isinregion(20.9): Answer = False
    
    if not Answer:
        print("fontregion_testisinregion(): fontregion.isinregion() did not work as expected.")

    return Answer

def testlineregion_searchfunctions() -> bool:
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
    trueregions = hardcodedlineregions_pdfminer_LineTest1()
    thetest.lineregions = trueregions
    Answer = True
    
    # Next, test our findlineregions:
    outcome = thetest.selectlineregion(23.0)
    if not outcome.compare(trueregions[6]):
        print("selectlineregion(23.0) was supposed to return:")
        trueregions[6].printregion()
        print("but returned instead:")
        outcome.printregion()
        print("\n")
        Answer = False
    
    outcome = thetest.selectlineregion(-2.0)
    if not outcome.compare(trueregions[0]):
        print("selectlineregion(-2.0) was supposed to return:")
        trueregions[0].printregion()
        print("but returned instead:")
        outcome.printregion()
        print("\n")
        Answer = False
        
    outcome = thetest.selectlineregion(5e4)
    if not outcome.compare(trueregions[9]):
        print("selectlineregion(5e4) was supposed to return:")
        trueregions[9].printregion()
        print("but returned instead:")
        outcome.printregion()
        print("\n")
        Answer = False
        
    outcome = thetest.selectlineregion(-0.1)
    if not outcome.compare(trueregions[1]):
        print("selectlineregion(-0.1) was supposed to return:")
        trueregions[1].printregion()
        print("but returned instead:")
        outcome.printregion()
        print("\n")
        Answer = False    
        
    outcome = thetest.selectlineregion(-10.0)
    for region in trueregions:
        if outcome.compare(region):
            print("selectlineregion(-10.0) was supposed to return no agreements with any given fontregion, but instead returned:")
            region.printregion()
            Answer = False    
    
    outcome = thetest.selectlineregion(-1000.0)
    for region in trueregions:
        if outcome.compare(region):
            print("selectlineregion(-1000.0) was supposed to return no agreements with any given fontregion, but instead returned:")
            region.printregion()
            Answer = False
            
    outcome = thetest.selectlineregion(1e6)
    for region in trueregions:
        if outcome.compare(region):
            print("selectlineregion(1e6) was supposed to return no agreements with any given fontregion, but instead returned:")
            region.printregion()
            Answer = False
    
    # Next, see if we can properly find the regular region:
    outcome = thetest.findregularlineregion()
    if not outcome.compare(trueregions[3]):
        print("findregularlineregion() was supposed to return:")
        trueregions[3].printregion()
        print("but returned instead:")
        outcome.printregion()
        print("\n")
        Answer = False    
        
    # Next, see if we can properly identify whitelines:
    if not (thetest.whiteline_isregular(13.0)==True): 
        Answer = False
        print("whiteline_isregular(13.0) is supposed to return True with the LineTest1/pdfminer-structure")
    
    if not (thetest.whiteline_isregular(12.5)==False): 
        Answer = False
        print("whiteline_isregular(12.5) is supposed to return False with the LineTest1/pdfminer-structure")
        
    if not (thetest.whiteline_isregular(16.8)==False): 
        Answer = False
        print("whiteline_isregular(16.8) is supposed to return False with the LineTest1/pdfminer-structure")
        
    # ----------------------------
    
    if not (thetest.whiteline_issmall(6.0)==True): 
        Answer = False
        print("whiteline_issmall(6.0) is supposed to return True with the LineTest1/pdfminer-structure")
    
    if not (thetest.whiteline_issmall(12.6)==False): 
        Answer = False
        print("whiteline_issmall(12.6) is supposed to return False with the LineTest1/pdfminer-structure")
        
    if not (thetest.whiteline_issmall(13.7)==False): 
        Answer = False
        print("whiteline_issmall(13.7) is supposed to return False with the LineTest1/pdfminer-structure")
        
    # ----------------------------
    
    if not (thetest.whiteline_smallerthenregular(6.0)==True): 
        Answer = False
        print("whiteline_smallerthenregular(6.0) is supposed to return True with the LineTest1/pdfminer-structure")
    
    if not (thetest.whiteline_smallerthenregular(5.6)==True): 
        Answer = False
        print("whiteline_smallerthenregular(5.6) is supposed to return True with the LineTest1/pdfminer-structure")
        
    if not (thetest.whiteline_smallerthenregular(12.6)==False): 
        Answer = False
        print("whiteline_smallerthenregular(12.6) is supposed to return False with the LineTest1/pdfminer-structure")
    
    # ----------------------------
    
    if not (thetest.whiteline_isbig(18.0)==True): 
        Answer = False
        print("whiteline_isbig(18.0) is supposed to return True with the LineTest1/pdfminer-structure")
    
    if not (thetest.whiteline_isbig(16.7)==False): 
        Answer = False
        print("whiteline_isbig(16.7) is supposed to return False with the LineTest1/pdfminer-structure")
        
    if not (thetest.whiteline_isbig(2345.0)==True): 
        Answer = False
        print("whiteline_isbig(2345.0) is supposed to return True with the LineTest1/pdfminer-structure")
    
    # ----------------------------
    
    if not (thetest.whiteline_iszero(1.0)==True): 
        Answer = False
        print("whiteline_iszero(1.0) is supposed to return True with the LineTest1/pdfminer-structure")
    
    if not (thetest.whiteline_iszero(-1.5)==False): 
        Answer = False
        print("whiteline_iszero(-1.5) is supposed to return False with the LineTest1/pdfminer-structure")
        
    if not (thetest.whiteline_iszero(5.6)==False): 
        Answer = False
        print("whiteline_iszero(5.6) is supposed to return False with the LineTest1/pdfminer-structure")
        
    # ----------------------------
    
    if not (thetest.whiteline_isvalid(-1.5)==False): 
        Answer = False
        print("whiteline_isvalid(-1.5) is supposed to return False with the LineTest1/pdfminer-structure")
    
    if not (thetest.whiteline_isvalid(-1.4)==True): 
        Answer = False
        print("whiteline_isvalid(-1.4) is supposed to return True with the LineTest1/pdfminer-structure")
        
    if not (thetest.whiteline_isvalid(13.0)==True): 
        Answer = False
        print("whiteline_isvalid(13.0) is supposed to return True with the LineTest1/pdfminer-structure")
        
    if not (thetest.whiteline_isvalid(-10.0)==False): 
        Answer = False
        print("whiteline_isvalid(-10.0) is supposed to return False with the LineTest1/pdfminer-structure")
    
    # ===========================================
    # Now, trigger bugs in the search on purpose:
    # ===========================================
    
    thetest.lineregions.pop(3)
    
    bugtest1 = thetest.selectlineregion(16.0)
    if (abs(bugtest1.get_frequency()+2.0)>1e-3):
        Answer = False
        print("After removing the regular LINEregion, selectlineregion(16.0) is supposed to return freq=-2.0")
        bugtest1.printregion()
    
    bugtest2 = thetest.findregularlineregion()
    if (abs(bugtest2.get_frequency()+1.0)>1e-3):
        Answer = False
        print("After removing the regular LINEregion, findregularlineregion() is supposed to return freq=-1.0")
        bugtest2.printregion()
    
    # then, return the total answer:
    return Answer
    
# Definition of collection:    
def TestLineRegions() -> bool:
    """
    # Collection-function of unit-tests.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    Answer = True
    
    if (lineregion_testfindlineregions()==False): 
        Answer=False
        print('\n==> Multi-bin unit-test for findlineregions() failed!\n')
    
    if (lineregion_testfindlineregions_absorbing()==False): 
        Answer=False
        print('\n==> Unit-test for lineregion_testfindlineregions_absorbing() failed!\n')
    
    if (lineregion_testfindlineregions_endpeaks()==False): 
        Answer=False
        print('\n==> Multi-bin unit-test for findlineregions_endpeaks() failed!\n')

    if (lineregion_testfindlineregions_2bin_a()==False): 
        Answer=False
        print('\n==> 2-bin unit-test (a) for findlineregions() failed!\n')
    
    if (lineregion_testfindlineregions_2bin_b()==False): 
        Answer=False
        print('\n==> 2-bin unit-test (b) for findlineregions() failed!\n')
        
    if (lineregion_testfindlineregions_1bin()==False): 
        Answer=False
        print('\n==> 1-bin unit-test for findlineregions() failed!\n')
    
    if (lineregion_testcompare()==False): 
        Answer=False
        print('\n==> compare() unit-test for lineregion failed!\n')
    
    if (lineregion_testisinregion()==False): 
        Answer=False
        print('\n==> isinregion() unit-test for lineregion failed!\n')
    
    if (testlineregion_searchfunctions()==False):
        Answer = False
        print('\n==> testlineregion_searchfunctions() unit-test for lineregion failed!\n')
    
    return Answer

if __name__ == '__main__':
    if TestLineRegions():
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
