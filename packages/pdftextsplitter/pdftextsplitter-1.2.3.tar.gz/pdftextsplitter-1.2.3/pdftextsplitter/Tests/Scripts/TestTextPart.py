import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from TextPart code:
sys.path.insert(1, '../../')
from TextPart.textpart import textpart
from TextPart.CurrentLine import CurrentLine
from TextPart.textgeneration import is_italic
from TextPart.textgeneration import is_bold

# Imports from Tools:
sys.path.insert(2, '../Tools/')
from FileComparison import FileComparison
from CompareImages import CompareImages
from Platformdetection import detectsystem
from Platformdetection import MySystem

# Definition of paths:
inputpath = "../Inputs/"
outputpath = "../Calc_Outputs/"
truthpath = "../True_Outputs/"

# Definition of filenames:
filename_export = "textpart_exporttest"
filename_load = "textpart_loadtest"
filename_gen = "TextExtraction_001"

# Definition of unit tests:
def textpart_basetest() -> bool:
    """
    # Unit test for the basic functionality of the textpart-class:
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Create the testclass:
    thetest = textpart()
    Answer = True
    
    # Create a CurrentLine-object:
    thisline = CurrentLine()
    
    # Check default values:
    if (not(thetest.get_labelname()=="Textpart")): 
        Answer = False
        print('Testing the default-value for textpart.labelname failed.\n')
    if (not(thetest.get_documentpath()=="./")): 
        Answer = False
        print('Testing the default-value for textpart.documentpath failed.\n')
    if (not(thetest.get_documentname()=="")): 
        Answer = False
        print('Testing the default-value for textpart.documentname failed.\n')
    if (not(thetest.get_outputpath()=="./")): 
        Answer = False
        print('Testing the default-value for textpart.outputpath failed.\n')
    if (not(len(thetest.get_textcontent())==0)): 
        Answer = False
        print('Testing the default-value for textpart.textcontent failed.\n')
    if (abs(thetest.get_histogramsize()-100.0)>1e-3): 
        Answer = False
        print('Testing the default-value for textpart.histogramsize failed.\n')
    if (not(thetest.get_ruleverbosity()==0)): 
        Answer = False
        print('Testing the default-value for textpart.ruleverbosity failed.\n')
    if (not(thetest.get_verbosetextline()=="")): 
        Answer = False
        print('Testing the default-value for textpart.verbosetextline failed.\n')
    
    # Use the setters:
    thetest.set_labelname("SomeLabel")
    thetest.set_documentpath("/some/path/for/testing/")
    thetest.set_outputpath("/some/path/to/output/")
    thetest.set_documentname("Testname")
    thetest.set_histogramsize(150.0)
    thetest.set_ruleverbosity(1)
    thetest.set_verbosetextline("mytextline")
    thisline.textline = "Some document text for testing"
    thetest.blindfill(thisline)
    thisline.textline = "And some more stupid tests"
    thetest.blindfill(thisline)
    
    # Check the new values:
    if (not(thetest.get_labelname()=="SomeLabel")): 
        Answer = False
        print('Testing the get/set for textpart.labelname failed.\n')
    if (not(thetest.get_documentpath()=="/some/path/for/testing/")): 
        Answer = False
        print('Testing the get/set for textpart.documentpath failed.\n')
    if (not(thetest.get_documentname()=="Testname")): 
        Answer = False
        print('Testing the get/set for textpart.documentname failed.\n')
    if (not(thetest.get_outputpath()=="/some/path/to/output/")): 
        Answer = False
        print('Testing the get/set for textpart.outputpath failed.\n')
    if (not(len(thetest.get_textcontent())==2)): 
        Answer = False
        print('Testing the length for textpart.textcontent failed.\n')
    if (not(thetest.get_textcontent()==["Some document text for testing", "And some more stupid tests"])): 
        Answer = False
        print('Testing the get for textpart.textcontent failed.\n')
    if (abs(thetest.get_histogramsize()-150.0)>1e-3): 
        Answer = False
        print('Testing the get for textpart.histogramsize failed.\n')
    if (not(thetest.get_ruleverbosity()==1)): 
        Answer = False
        print('Testing the get for textpart.ruleverbosity failed.\n')
    if (not(thetest.get_verbosetextline()=="mytextline")): 
        Answer = False
        print('Testing the get for textpart.verbosetextline failed.\n')
    
    # Check get/set directly for textcontent:
    thetest.set_textcontent(["Some document text for testing", "And some more stupid tests"])
    if (not(thetest.get_textcontent()==["Some document text for testing", "And some more stupid tests"])): 
        Answer = False
        print('Testing the full get/set for textpart.textcontent failed.\n')
    
    # Check the fillcontent-function. For textpart itself, masterrule is not overwritten, so it should
    # always return False. That makes testing it really easy:
    thisline.textline = "Add some more text"
    thetest.fillcontent(thisline)
    if (not(thetest.get_textcontent()==["Some document text for testing", "And some more stupid tests"])): 
        Answer = False
        print('Testing the fillcontent-function based on textpart-masterrulle failed.\n')
    
    # Now check the blindfill-function. This should always perform filling, regardless of masterrule:
    thisline.textline = "Add some more text"
    thetest.blindfill(thisline)
    if (not(thetest.get_textcontent()==["Some document text for testing", "And some more stupid tests", "Add some more text"])): 
        Answer = False
        print('Testing the blindfill-function of the textpart-class failed.\n')
    
    # Complete the test:
    return Answer

# Definition of unit tests:
def textpart_shallowcopytest() -> bool:
    """
    # Unit test for the basic functionality of the textpart-class:
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Create a CurrentLine-object:
    thisline = CurrentLine()
    
    # Create some test classes:
    thetest1 = textpart()
    thetest1.set_labelname("SomeLabel")
    thetest1.set_documentpath("/some/path/for/testing/")
    thetest1.set_outputpath("/some/path/to/output/")
    thetest1.set_documentname("Testname")
    thetest1.set_histogramsize(150.0)
    thetest1.set_ruleverbosity(1)
    thetest1.set_verbosetextline("mytextline")
    thisline.textline = "Some document text for testing"
    thetest1.blindfill(thisline)
    thisline.textline = "And some more stupid tests"
    thetest1.blindfill(thisline)
    
    # Create one more:
    thetest2 = textpart()
    thetest2.set_labelname("OtherLabel")
    thetest2.set_documentpath("/some/other/path/for/testing/")
    thetest2.set_outputpath("/some/other/path/to/output/")
    thetest2.set_documentname("Testy")
    thetest2.set_histogramsize(152.0)
    thetest2.set_ruleverbosity(2)
    thetest2.set_verbosetextline("Othertextline")
    thisline.textline = "En nu gaan we weer even"
    thetest2.blindfill(thisline)
    thisline.textline = "een stapje verder"
    thetest2.blindfill(thisline)
    thisline.textline = "en dan nog een keer"
    thetest2.blindfill(thisline)
    
    # Now shallow-copy the second one into the first:
    thetest1.fill_from_other_textpart(thetest2)
    
    # Compare quantities:
    Answer = True
    if not (thetest1.labelname==thetest2.labelname): Answer = False
    if not (thetest1.documentpath==thetest2.documentpath): Answer = False
    if not (thetest1.outputpath==thetest2.outputpath): Answer = False
    if not (thetest1.documentname==thetest2.documentname): Answer = False
    if not (thetest1.headerboundary==thetest2.headerboundary): Answer = False
    if not (thetest1.footerboundary==thetest2.footerboundary): Answer = False
    if not (thetest1.histogramsize==thetest2.histogramsize): Answer = False
    if not (thetest1.ruleverbosity==thetest2.ruleverbosity): Answer = False
    if not (len(thetest1.textcontent)==len(thetest2.textcontent)): Answer = False
    
    if not Answer:
        print("textpart_shallowcopytest: some of the comparisons failed!")
    
    # return the answer:
    return Answer

def textpart_exporttest_a() -> bool:
    """
    # Unit test for the export-function of the text-part class:
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Create the testclass:
    thetest = textpart()
    Answer = True
    
    # Create a CurrentLine-object:
    thisline = CurrentLine()
    
    # set proper parameters:
    thetest.set_labelname("Somelabel")
    thetest.set_documentname(filename_export)
    thetest.set_outputpath(outputpath)
    thetest.set_documentpath("/not/important/for/this/test/")
    
    # Give the desired input:
    thisline.textline = "This is a small textfile"
    thisline.fontsize = 10.0
    thetest.blindfill(thisline)
    thisline.textline = "to test if the export-function of the textpart"
    thisline.fontsize = 10.0
    thetest.blindfill(thisline)
    thisline.textline = "class is working properly..."
    thisline.fontsize = 10.0
    thetest.blindfill(thisline)
    
    # Then, give the export-command:
    thetest.export("default")
    
    # Next, compare the outputs:
    rapport = FileComparison(outputpath+filename_export,truthpath+filename_export,"txt")
    
    # Find out the answer:
    Answer = False
    if (rapport==""): Answer = True 
    else: print(" ==> Test textpart.export() | file-comparison rapport:\n\n" + rapport + "----------------------------------------------------")
    return Answer

def textpart_exporttest_b() -> bool:
    """
    # Unit test for the export-function of the text-part class:
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Create the testclass:
    thetest = textpart()
    Answer = True
    
    # Create a CurrentLine-object:
    thisline = CurrentLine()
    
    # set proper parameters:
    thetest.set_labelname("Somelabel")
    thetest.set_documentname(filename_export)
    thetest.set_outputpath(outputpath)
    thetest.set_documentpath("/not/important/for/this/test/")
    
    # Give the desired input:
    thisline.textline = "This is a small textfile"
    thisline.fontsize = 10.0
    thetest.blindfill(thisline)
    thisline.textline = "to test if the export-function of the textpart"
    thisline.fontsize = 10.0
    thetest.blindfill(thisline)
    thisline.textline = "class is working properly..."
    thisline.fontsize = 10.0
    thetest.blindfill(thisline)
    
    # Then, give the export-command:
    thetest.export("fontsize")
    
    # Next, compare the outputs:
    rapport = FileComparison(outputpath+filename_export,truthpath+filename_export+"_fontsize1","txt")
    
    # Find out the answer:
    Answer = False
    if (rapport==""): Answer = True 
    else: print(" ==> Test textpart.export() | file-comparison rapport:\n\n" + rapport + "----------------------------------------------------")
    return Answer

def textpart_exporttest_c() -> bool:
    """
    # Unit test for the export-function of the text-part class:
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Create the testclass:
    thetest = textpart()
    Answer = True
    
    # Create a CurrentLine-object:
    thisline = CurrentLine()
    
    # set proper parameters:
    thetest.set_labelname("Somelabel")
    thetest.set_documentname(filename_export)
    thetest.set_outputpath(outputpath)
    thetest.set_documentpath("/not/important/for/this/test/")
    
    # Give the desired input:
    thisline.textline = "This is a small textfile"
    thisline.fontsize = 10.0
    thetest.blindfill(thisline)
    thisline.textline = "to test if the export-function of the textpart"
    thisline.fontsize = 10.0
    thetest.blindfill(thisline)
    thisline.textline = "class is working properly..."
    thisline.fontsize = 10.0
    thetest.blindfill(thisline)
    
    # Set internal fontsizes:
    thetest.fontsize_perline = [5.0, 6.0, 7.0]
    
    # Then, give the export-command:
    thetest.export("fontsize")
    
    # Next, compare the outputs:
    rapport = FileComparison(outputpath+filename_export,truthpath+filename_export+"_fontsize2","txt")
    
    # Find out the answer:
    Answer = False
    if (rapport==""): Answer = True 
    else: print(" ==> Test textpart.export() | file-comparison rapport:\n\n" + rapport + "----------------------------------------------------")
    return Answer

def textpart_exporttest_d() -> bool:
    """
    # Unit test for the export-function of the text-part class:
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Create the testclass:
    thetest = textpart()
    Answer = True
    
    # Create a CurrentLine-object:
    thisline = CurrentLine()
    
    # set proper parameters:
    thetest.set_labelname("Somelabel")
    thetest.set_documentname(filename_export)
    thetest.set_outputpath(outputpath)
    thetest.set_documentpath("/not/important/for/this/test/")
    
    # Give the desired input:
    thisline.textline = "This is a small textfile"
    thisline.fontsize = 10.0
    thetest.blindfill(thisline)
    thisline.textline = "to test if the export-function of the textpart"
    thisline.fontsize = 10.0
    thetest.blindfill(thisline)
    thisline.textline = "class is working properly..."
    thisline.fontsize = 10.0
    thetest.blindfill(thisline)
    
    # Set internal fontsizes:
    thetest.fontsize_perline = [5.0, 6.0, 7.0]
    
    # Then, give the export-command:
    thetest.export("estupido")
    
    # Next, compare the outputs:
    rapport = FileComparison(outputpath+filename_export,truthpath+filename_export+"_unsupported","txt")
    
    # Find out the answer:
    Answer = False
    if (rapport==""): Answer = True 
    else: print(" ==> Test textpart.export() | file-comparison rapport:\n\n" + rapport + "----------------------------------------------------")
    return Answer

def textpart_exporttest_e() -> bool:
    """
    # Unit test for the export-function of the text-part class:
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Create the testclass:
    thetest = textpart()
    Answer = True
    
    # Create a CurrentLine-object:
    thisline = CurrentLine()
    
    # set proper parameters:
    thetest.set_labelname("Somelabel")
    thetest.set_documentname(filename_export)
    thetest.set_outputpath(outputpath)
    thetest.set_documentpath("/not/important/for/this/test/")
    
    # Give the desired input:
    thisline.textline = "This is a small textfile"
    thisline.previous_whiteline = 10.0
    thisline.next_whiteline = 10.0
    thetest.blindfill(thisline)
    thisline.textline = "to test if the export-function of the textpart"
    thisline.previous_whiteline = 10.0
    thisline.next_whiteline = 10.0
    thetest.blindfill(thisline)
    thisline.textline = "class is working properly..."
    thisline.previous_whiteline = 10.0
    thisline.next_whiteline = 10.0
    thetest.blindfill(thisline)
    
    # Then, give the export-command:
    thetest.whitelinesize = [15.0, 16.0, 17.0]
    thetest.export("whitelines")
    
    # Next, compare the outputs:
    rapport = FileComparison(outputpath+filename_export,truthpath+filename_export+"_whitelines1","txt")
    
    # Find out the answer:
    Answer = False
    if (rapport==""): Answer = True 
    else: print(" ==> Test textpart.export() | file-comparison rapport:\n\n" + rapport + "----------------------------------------------------")
    return Answer

def textpart_exporttest_f() -> bool:
    """
    # Unit test for the export-function of the text-part class:
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Create the testclass:
    thetest = textpart()
    Answer = True
    
    # Create a CurrentLine-object:
    thisline = CurrentLine()
    
    # set proper parameters:
    thetest.set_labelname("Somelabel")
    thetest.set_documentname(filename_export)
    thetest.set_outputpath(outputpath)
    thetest.set_documentpath("/not/important/for/this/test/")
    
    # Give the desired input:
    thisline.textline = "This is a small textfile"
    thisline.previous_whiteline = 10.0
    thisline.next_whiteline = 10.0
    thetest.blindfill(thisline)
    thisline.textline = "to test if the export-function of the textpart"
    thisline.previous_whiteline = 10.0
    thisline.next_whiteline = 10.0
    thetest.blindfill(thisline)
    thisline.textline = "class is working properly..."
    thisline.previous_whiteline = 10.0
    thisline.next_whiteline = 10.0
    thetest.blindfill(thisline)
    
    # Then, give the export-command:
    thetest.export("whitelines")
    
    # Next, compare the outputs:
    rapport = FileComparison(outputpath+filename_export,truthpath+filename_export+"_fontsize1","txt")
    
    # Find out the answer:
    Answer = False
    if (rapport==""): Answer = True 
    else: print(" ==> Test textpart.export() | file-comparison rapport:\n\n" + rapport + "----------------------------------------------------")
    return Answer

def textpart_loadtest() -> bool:
    """
    # Unit test for the load-function of the text-part class:
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Create the testclass:
    thetest = textpart()
    Answer = True
    
    # set proper parameters:
    thetest.set_labelname("Somelabel")
    thetest.set_documentname(filename_load)
    thetest.set_documentpath(truthpath)
    thetest.set_outputpath(outputpath)
    
    # Load the textfile:
    thetest.load()
    
    # Test if the content matches:
    textarray = ["This is a small textfile\n", "to test if the export-function of the textpart\n", "class is working properly...\n"]
    
    # Check if the content matches:
    correctsize = len(textarray)
    contentsize = len(thetest.textcontent)
    
    Answer = True
    if not (correctsize==contentsize):
        print("size(textpart.load())=="+str(contentsize)+" while the correct arraysize is "+str(correctsize)+" ==> we cannot make a comparison!")
        print("\n")
        
        for line in textarray:
            print(line)
        
        print("\n")
        
        for line in thetest.textcontent:
            print(line)
        
        Answer = False
    else:
        for index in range(0,correctsize):
            if not (textarray[index]==thetest.textcontent[index]):
                Answer = False
                print("textpart.load() failed at line "+str(index+1)+" | content = <"+thetest.textcontent[index]+"> while the correct answer = <"+textarray[index]+">")
    
    # Finish the test:
    return Answer

def textpart_histtest() -> bool:
    """
    # Unit test for the fontsizehist-function of the text-part class:
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Create the testclass:
    thetest = textpart()
    Answer = True
    
    # set proper parameters:
    thetest.set_labelname("Somelabel")
    thetest.set_documentname("HistTest")
    thetest.set_documentpath("/not/important/for/this/test/")
    thetest.set_outputpath(outputpath)
    
    # Put in some data:
    thetest.fontsize_perline = [1, 1, 1, 2, 3, 6, 6, 6, 6, 6, 6, 8, 8, 9, 13]
    thetest.fontsize_percharacter = [13, 13, 13, 13, 15, 15, 10, 4, 4, 4, 2, 2, 8, 16]
    
    # Generate the plots:
    thetest.fontsizehist()
    
    # Compare the images:
    Answer = True
    per1 = CompareImages(outputpath+"HistTest_Fontsizes_allcharacters.png",truthpath+"HistTest_Fontsizes_allcharacters.png")
    per2 = CompareImages(outputpath+"HistTest_Fontsizes_Firstcharacters.png",truthpath+"HistTest_Fontsizes_Firstcharacters.png")
    
    if abs(per1)>1e-3:
        print("Unit Test textpart_histtest(): Generation of the histogram for all characters went wrong.")
        Answer = False
    if abs(per2)>1e-3:
        print("Unit Test textpart_histtest(): Generation of the histogram for first characters went wrong.")
        Answer = False
    
    # Return the answer:
    return Answer        

def textpart_generationtest_a() -> bool:
    """
    # Unit test for the textgeneration-function of the text-part class:
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Create the testclass:
    thetest = textpart()
    Answer = True
    
    # set proper parameters:
    thetest.set_labelname("Somelabel")
    thetest.set_documentname(filename_gen)
    thetest.set_documentpath(inputpath)
    thetest.set_outputpath(outputpath)
    
    # Generate the output:
    thetest.textgeneration("pymupdf")
    thetest.export("default")

    # Next, compare the outputs:
    rapport = FileComparison(outputpath+filename_gen,truthpath+filename_gen,"txt")
    
    # Find out the answer:
    Answer = False
    if (rapport==""): Answer = True 
    else: print(" ==> Test textpart.textpart_generationtest_a(): pymupdf| file-comparison rapport:\n\n" + rapport + "----------------------------------------------------")
    return Answer

def textpart_generationtest_b() -> bool:
    """
    # Unit test for the textgeneration-function of the text-part class:
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Create the testclass:
    thetest = textpart()
    Answer = True
    
    # set proper parameters:
    thetest.set_labelname("Somelabel")
    thetest.set_documentname(filename_gen)
    thetest.set_documentpath(inputpath)
    thetest.set_outputpath(outputpath)
    
    # Generate the output:
    thetest.textgeneration("pypdf2")
    thetest.export("default")
    
    # Next, compare the outputs:
    rapport = FileComparison(outputpath+filename_gen,truthpath+filename_gen,"txt")
    
    # Find out the answer:
    Answer = False
    if (rapport==""): Answer = True 
    else: print(" ==> Test textpart.textpart_generationtest_b(): pypdf2| file-comparison rapport:\n\n" + rapport + "----------------------------------------------------")
    return Answer

def textpart_generationtest_c() -> bool:
    """
    # Unit test for the textgeneration-function of the text-part class:
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Create the testclass:
    thetest = textpart()
    Answer = True
    
    # set proper parameters:
    thetest.set_labelname("Somelabel")
    thetest.set_documentname(filename_gen)
    thetest.set_documentpath(inputpath)
    thetest.set_outputpath(outputpath)
    
    # Generate the output:
    thetest.textgeneration("pdfminer")
    thetest.export("default")
    
    # Next, compare the outputs:
    rapport = FileComparison(outputpath+filename_gen,truthpath+filename_gen,"txt")
    
    # Find out the answer:
    Answer = False
    if (rapport==""): Answer = True 
    else: print(" ==> Test textpart.textpart_generationtest_c(): pdfminer| file-comparison rapport:\n\n" + rapport + "----------------------------------------------------")
    return Answer

def textpart_generationtest_e() -> bool:
    """
    # Unit test for the textgeneration-function of the text-part class:
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Create the testclass:
    thetest = textpart()
    Answer = True
    
    # set proper parameters:
    thetest.set_labelname("Somelabel")
    thetest.set_documentname(filename_gen)
    thetest.set_documentpath(inputpath)
    thetest.set_outputpath(outputpath)
    
    # Generate the output:
    thetest.textgeneration("estupido")
    
    # Execute the test:
    expected = ["No proper extraction method was specified.","So we leave the file empty for the rest of it."]
    if (len(thetest.textcontent)>1):
        if (not(thetest.textcontent[0]==expected[0]))or(not(thetest.textcontent[1]==expected[1])):
            Answer = False
            print("thetest.textgeneration(estupido) is supposed to return:")
            print(expected[0])
            print(expected[1])
            print("=======================================================")
            print("But it returned instead:")
            for line in thetest.textcontent:
                print(line)
    else:
        print("thetest.textcontent did not have the proper length!")
        Answer = False
    
    # Check special cases for font styles:
    if (is_italic(expected,"estupido")==True): 
        Answer = False
        print("is_italic(...,<unsupported method>) should always return False")
    
    if (is_bold(expected,"estupido")==True): 
        Answer = False
        print("is_bold(...,<unsupported method>) should always return False")
    
    return Answer

def textpart_generationtest_f() -> bool:
    """
    # Unit test for the textgeneration-function of the text-part class:
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    # Create the testclass:
    thetest = textpart()
    Answer = True
    
    # set proper parameters:
    thetest.set_labelname("Somelabel")
    thetest.set_documentname(filename_gen)
    thetest.set_documentpath(inputpath)
    thetest.set_outputpath(outputpath)
    thetest.histogramsize = -123 # to provoke the proper lines of code.
    
    # Generate the output:
    thetest.textgeneration("pdfminer")
    
    # According to the code, this should mean that the content is empty, 
    # as we deliberatly provoke our bug-test here:
    Answer = (len(thetest.textcontent)==0)

    # Give output:
    if not Answer:
        print("textpart_generationtest_a(): FAILED! we were supposed to delete all collected content in case we detect a bug in counting pages!") 
    
    # Return the Answer:
    return Answer

# Definition of collection:    
def TestTextPart() -> bool:
    """
    # Collection-function of unit-tests.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    Answer = True
    
    if (textpart_basetest()==False): 
        Answer=False
        print('\n==> Basetest for textpart-class failed!\n')
    
    if (textpart_shallowcopytest()==False): 
        Answer=False
        print('\n==> textpart_shallowcopytest for textpart-class failed!\n')
    
    if (textpart_exporttest_a()==False): 
        Answer=False
        print('\n==> export test a for textpart-class failed!\n')
        
    if (textpart_exporttest_b()==False): 
        Answer=False
        print('\n==> export test b for textpart-class failed!\n')
    
    if (textpart_exporttest_c()==False): 
        Answer=False
        print('\n==> export test c for textpart-class failed!\n')
    
    if (textpart_exporttest_d()==False): 
        Answer=False
        print('\n==> export test d for textpart-class failed!\n')
    
    if (textpart_exporttest_e()==False): 
        Answer=False
        print('\n==> export test e for textpart-class failed!\n')
        
    if (textpart_exporttest_f()==False): 
        Answer=False
        print('\n==> export test f for textpart-class failed!\n')
    
    if (textpart_loadtest()==False): 
        Answer=False
        print('\n==> load test for textpart-class failed!\n')
    
    if (textpart_histtest()==False): 
        Answer=False
        print('\n==> Histogram test for textpart-class failed!\n')
    
    if (textpart_generationtest_a()==False): 
        Answer=False
        print('\n==> textgeneration(pymupdf) test for textpart-class failed!\n')

    if (textpart_generationtest_b()==False): 
        Answer=False
        print('\n==> textgeneration(pypdf2) test for textpart-class failed!\n')
        
    if (textpart_generationtest_c()==False): 
        Answer=False
        print('\n==> textgeneration(pdfminer) test for textpart-class failed!\n')

    if (textpart_generationtest_e()==False): 
        Answer=False
        print('\n==> textgeneration(shell) test for textpart-class failed!\n')
    
    if (textpart_generationtest_f()==False): 
        Answer=False
        print('\n==> textgeneration(pdfminer) deletion bugtest for textpart-class failed!\n')

    return Answer

if __name__ == '__main__':
    if TestTextPart():
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
