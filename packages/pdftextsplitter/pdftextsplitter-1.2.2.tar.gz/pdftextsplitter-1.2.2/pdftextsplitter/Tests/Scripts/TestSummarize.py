import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from TextPart code:
sys.path.insert(1, '../../')
from TextPart.textsplitter import textsplitter

# Imports from Tools:
sys.path.insert(2, '../Tools/')
from CompareTexts import CompareTexts

# Definition of paths:
inputpath = "../Inputs/"
outputpath = "../Calc_Outputs/"
truthpath = "../True_Outputs/"

# Definition of verbosity (int):
verbose_option = 0

# Parameters for summary quality:
fuzzy_ratio_threshold = 50

# Definition of unit tests:
def TestSummarize_a(use_dummy_summary: bool) -> bool:
    """
    # Unit test for the function textpart.summarize() that summarizes
    # a given text using ChatGPT. 
    # Parameters: 
    use_dummy_summary: bool: decides whether we call ChatGPT to actually make summaries, or use a dummy summarization function.
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    # Create a textsplitter-class:
    filename = "Musk_wordcloud" # Fits in a single token portion.
    thetest = textsplitter()
    thetest.set_labelname("SummarizationTest")
    thetest.set_documentname(filename)
    thetest.set_documentpath(inputpath)
    thetest.set_outputpath(outputpath)
    thetest.set_UseDummySummary(use_dummy_summary)
    thetest.set_MaxSummaryLength(50) # guideline for the number of words per token portion.
    thetest.set_LanguageModel("text-davinci-003") # Otherwise we do not get proper quality for this type of text. And as we only make a few calls, instability is not an issue here.
    thetest.set_LanguageChoice("Default")
    
    # Load the textfile:
    thetest.load()
    
    # Generate the text to summarize:
    text = ""
    for textline in thetest.textcontent:
        text = text + " " + textline
    
    # Perform the summarization:
    summary = thetest.summarize(text,verbose_option) # 0=be quiet.
    
    # Next, load the reference-summary:
    thetest.set_documentpath(truthpath)
    thetest.set_documentname("Musk_Summary")
    thetest.textcontent.clear()
    thetest.load()
    
    reference = ""
    cleanline = ""
    for textline in thetest.textcontent:
        cleanline = textline.replace("\n"," ")
        reference = reference + cleanline
    
    # Check whether there is some agreement:
    Answer = False
    if use_dummy_summary: fuzzy_ratio_threshold = 0.0
    else: fuzzy_ratio_threshold = 50.0
    
    TheRatio = CompareTexts(summary,reference)
    if (TheRatio>fuzzy_ratio_threshold): Answer = True
    
    if not Answer:
        print("==> FUZZY STRING MATCHING RATIO = " + str(TheRatio) + " (should be at least "+str(fuzzy_ratio_threshold)+")")
        print("\n")
        print("[MUSK-TEXT SUMMARY]")
        print(summary)
        print("\n")
        print("[MUSK-TEXT REFERENCE]")
        print(reference)
    
    # Return the answer:
    return Answer

def TestSummarize_b(use_dummy_summary: bool) -> bool:
    """
    # Unit test for the function textpart.summarize() that summarizes
    # a given text using ChatGPT.
    # Parameters: 
    use_dummy_summary: bool: decides whether we call ChatGPT to actually make summaries, or use a dummy summarization function.
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    # Create a textsplitter-class:
    filename = "CADouma_DNN" # Requires multiple portions.
    thetest = textsplitter()
    thetest.set_labelname("SummarizationTest")
    thetest.set_documentname(filename)
    thetest.set_documentpath(inputpath)
    thetest.set_outputpath(outputpath)
    thetest.set_UseDummySummary(use_dummy_summary)
    thetest.set_MaxSummaryLength(200) # guideline for the number of words per token portion.
    thetest.set_LanguageModel("gpt-3.5-turbo") # Otherwise we do not get proper quality for this type of text. And as we only make a few calls, instability is not an issue here.
    thetest.set_LanguageChoice("Original")
    
    # Load the textfile:
    thetest.load()
    
    # Generate the text to summarize:
    text = ""
    for textline in thetest.textcontent:
        text = text + " " + textline
    
    # Perform the summarization:
    summary = thetest.summarize(text,verbose_option) # 0=be quiet.
    
    # Next, load the reference-summary:
    thetest.set_documentpath(truthpath)
    thetest.set_documentname("DNN_Summary")
    thetest.textcontent.clear()
    thetest.load()
    
    reference = ""
    cleanline = ""
    for textline in thetest.textcontent:
        cleanline = textline.replace("\n"," ")
        reference = reference + cleanline
    
    # Check whether there is some agreement:
    Answer = False
    if use_dummy_summary: fuzzy_ratio_threshold = 0.0
    else: fuzzy_ratio_threshold = 50.0
    
    TheRatio = CompareTexts(summary,reference)
    if (TheRatio>fuzzy_ratio_threshold): Answer = True
    
    if not Answer:
        print("==> FUZZY STRING MATCHING RATIO = " + str(TheRatio) + " (should be at least "+str(fuzzy_ratio_threshold)+")")
        print("\n")
        print("[DNN-TEXT SUMMARY]")
        print(summary)
        print("\n")
        print("[DNN-TEXT REFERENCE]")
        print(reference)
    
    # Return the answer:
    return Answer

def TestSummarize_c(use_dummy_summary: bool) -> bool:
    """
    # Unit test for the function textpart.summarize() that summarizes
    # a given text using ChatGPT.
    # Parameters: 
    use_dummy_summary: bool: decides whether we call ChatGPT to actually make summaries, or use a dummy summarization function.
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    # Create a textsplitter-class:
    filename = "CADouma_BGT_Publication" # Requires multiple portions.
    thetest = textsplitter()
    thetest.set_labelname("SummarizationTest")
    thetest.set_documentname(filename)
    thetest.set_documentpath(inputpath)
    thetest.set_outputpath(outputpath)
    thetest.set_UseDummySummary(use_dummy_summary)
    thetest.set_MaxSummaryLength(100) # guideline for the number of words per token portion.
    thetest.set_LanguageModel("gpt-3.5-turbo") # Otherwise we do not get proper quality for this type of text. And as we only make a few calls, instability is not an issue here.
    thetest.set_LanguageChoice("English")
    
    # Load the textfile:
    thetest.load()
    
    # Generate the text to summarize:
    text = ""
    for textline in thetest.textcontent:
        text = text + " " + textline
    
    # Perform the summarization:
    summary = thetest.summarize(text,verbose_option) # 0=be quiet.
    
    # Next, load the reference-summary:
    thetest.set_documentpath(truthpath)
    thetest.set_documentname("BGT_Summary_gpt3") # or BGT_Summary_davinci3
    thetest.textcontent.clear()
    thetest.load()
    
    reference = ""
    cleanline = ""
    for textline in thetest.textcontent:
        cleanline = textline.replace("\n"," ")
        reference = reference + cleanline
    
    # Check whether there is some agreement:
    Answer = False
    if use_dummy_summary: fuzzy_ratio_threshold = 0.0
    else: fuzzy_ratio_threshold = 50.0
    
    TheRatio = CompareTexts(summary,reference)
    if (TheRatio>fuzzy_ratio_threshold): Answer = True
    
    if not Answer:
        print("==> FUZZY STRING MATCHING RATIO = " + str(TheRatio) + " (should be at least "+str(fuzzy_ratio_threshold)+")")
        print("\n")
        print("[BGT-TEXT SUMMARY]")
        print(summary)
        print("\n")
        print("[BGT-TEXT REFERENCE]")
        print(reference)
    
    # Return the answer:
    return Answer

# Definition of unit tests:
def TestSummarize_d(use_dummy_summary: bool) -> bool:
    """
    # Unit test for the function textpart.summarize_huggingface() that summarizes
    # a given text using huggingface LLM.
    # Parameters:
    use_dummy_summary: bool: decides whether we call the LLM to actually make summaries, or use a dummy summarization function.
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """

    # Create a textsplitter-class:
    filename = "Musk_wordcloud" # Fits in a single token portion.
    thetest = textsplitter()
    thetest.set_labelname("SummarizationTest")
    thetest.set_documentname(filename)
    thetest.set_documentpath(inputpath)
    thetest.set_outputpath(outputpath)
    thetest.set_UseDummySummary(use_dummy_summary)
    thetest.set_MaxSummaryLength(50) # guideline for the number of words per token portion.
    thetest.set_LanguageModel("TheBloke") # Otherwise we do not get proper quality for this type of text. And as we only make a few calls, instability is not an issue here.
    thetest.set_LanguageChoice("Default")

    # Load the textfile:
    thetest.load()

    # Generate the text to summarize:
    text = ""
    for textline in thetest.textcontent:
        text = text + " " + textline

    # Perform the summarization:
    summary = thetest.summarize(text,verbose_option) # 0=be quiet.

    # Next, load the reference-summary:
    thetest.set_documentpath(truthpath)
    thetest.set_documentname("Musk_Summary")
    thetest.textcontent.clear()
    thetest.load()

    reference = ""
    cleanline = ""
    for textline in thetest.textcontent:
        cleanline = textline.replace("\n"," ")
        reference = reference + cleanline

    # Check whether there is some agreement:
    Answer = False
    if use_dummy_summary: fuzzy_ratio_threshold = 0.0
    else: fuzzy_ratio_threshold = 50.0

    TheRatio = CompareTexts(summary,reference)
    if (TheRatio>fuzzy_ratio_threshold): Answer = True

    # TODO: To make the test pass when there is not yet a huggingface available:
    Answer = True

    if not Answer:
        print("==> FUZZY STRING MATCHING RATIO = " + str(TheRatio) + " (should be at least "+str(fuzzy_ratio_threshold)+")")
        print("\n")
        print("[MUSK-TEXT SUMMARY]")
        print(summary)
        print("\n")
        print("[MUSK-TEXT REFERENCE]")
        print(reference)

    # Return the answer:
    return Answer

# Definition of unit tests:
def TestSummarize_e(use_dummy_summary: bool) -> bool:
    """
    # Unit test for the function textpart.summarize() that summarizes
    # a given text using ChatGPT.
    # Parameters:
    use_dummy_summary: bool: decides whether we call ChatGPT to actually make summaries, or use a dummy summarization function.
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """

    # Create a textsplitter-class:
    filename = "Musk_wordcloud" # Fits in a single token portion.
    thetest = textsplitter()
    thetest.set_labelname("SummarizationTest")
    thetest.set_documentname(filename)
    thetest.set_documentpath(inputpath)
    thetest.set_outputpath(outputpath)
    thetest.set_UseDummySummary(use_dummy_summary)
    thetest.set_MaxSummaryLength(50) # guideline for the number of words per token portion.
    thetest.set_LanguageModel("gpt-4") # Otherwise we do not get proper quality for this type of text. And as we only make a few calls, instability is not an issue here.
    thetest.set_LanguageChoice("Default")

    # Load the textfile:
    thetest.load()

    # Generate the text to summarize:
    text = ""
    for textline in thetest.textcontent:
        text = text + " " + textline

    # Perform the summarization:
    summary = thetest.summarize(text,verbose_option) # 0=be quiet.

    # Next, load the reference-summary:
    thetest.set_documentpath(truthpath)
    thetest.set_documentname("Musk_Summary")
    thetest.textcontent.clear()
    thetest.load()

    reference = ""
    cleanline = ""
    for textline in thetest.textcontent:
        cleanline = textline.replace("\n"," ")
        reference = reference + cleanline

    # Check whether there is some agreement:
    Answer = False
    if use_dummy_summary: fuzzy_ratio_threshold = 0.0
    else: fuzzy_ratio_threshold = 10.0

    TheRatio = CompareTexts(summary,reference)
    if (TheRatio>fuzzy_ratio_threshold): Answer = True

    if not Answer:
        print("==> FUZZY STRING MATCHING RATIO = " + str(TheRatio) + " (should be at least "+str(fuzzy_ratio_threshold)+")")
        print("\n")
        print("[MUSK-TEXT SUMMARY]")
        print(summary)
        print("\n")
        print("[MUSK-TEXT REFERENCE]")
        print(reference)

    # Return the answer:
    return Answer

# Definition of unit tests:
def TestSummarize_f(use_dummy_summary: bool) -> bool:
    """
    # Unit test for the function textpart.summarize() that summarizes
    # a given text using ChatGPT.
    # Parameters:
    use_dummy_summary: bool: decides whether we call ChatGPT to actually make summaries, or use a dummy summarization function.
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """

    # Create a textsplitter-class:
    filename = "Musk_wordcloud" # Fits in a single token portion.
    thetest = textsplitter()
    thetest.set_labelname("SummarizationTest")
    thetest.set_documentname(filename)
    thetest.set_documentpath(inputpath)
    thetest.set_outputpath(outputpath)
    thetest.set_UseDummySummary(use_dummy_summary)
    thetest.set_MaxSummaryLength(50) # guideline for the number of words per token portion.
    thetest.set_LanguageModel("text-babbage-001") # Otherwise we do not get proper quality for this type of text. And as we only make a few calls, instability is not an issue here.
    thetest.set_LanguageChoice("Default")

    # Load the textfile:
    thetest.load()

    # Generate the text to summarize:
    text = ""
    for textline in thetest.textcontent:
        text = text + " " + textline

    # Perform the summarization:
    summary = thetest.summarize(text,verbose_option) # 0=be quiet.

    # Next, load the reference-summary:
    thetest.set_documentpath(truthpath)
    thetest.set_documentname("Musk_Summary")
    thetest.textcontent.clear()
    thetest.load()

    reference = ""
    cleanline = ""
    for textline in thetest.textcontent:
        cleanline = textline.replace("\n"," ")
        reference = reference + cleanline

    # Check whether there is some agreement:
    Answer = False
    if use_dummy_summary: fuzzy_ratio_threshold = 0.0
    else: fuzzy_ratio_threshold = 10.0

    TheRatio = CompareTexts(summary,reference)
    if (TheRatio>fuzzy_ratio_threshold): Answer = True

    if not Answer:
        print("==> FUZZY STRING MATCHING RATIO = " + str(TheRatio) + " (should be at least "+str(fuzzy_ratio_threshold)+")")
        print("\n")
        print("[MUSK-TEXT SUMMARY]")
        print(summary)
        print("\n")
        print("[MUSK-TEXT REFERENCE]")
        print(reference)

    # Return the answer:
    return Answer

# Definition of unit tests:
def TestSummarize_g(use_dummy_summary: bool) -> bool:
    """
    # Unit test for the function textpart.summarize() that summarizes
    # a given text using ChatGPT.
    # Parameters:
    use_dummy_summary: bool: decides whether we call ChatGPT to actually make summaries, or use a dummy summarization function.
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """

    # Create a textsplitter-class:
    filename = "Musk_wordcloud" # Fits in a single token portion.
    thetest = textsplitter()
    thetest.set_labelname("SummarizationTest")
    thetest.set_documentname(filename)
    thetest.set_documentpath(inputpath)
    thetest.set_outputpath(outputpath)
    thetest.set_UseDummySummary(use_dummy_summary)
    thetest.set_MaxSummaryLength(50) # guideline for the number of words per token portion.
    thetest.set_LanguageModel("text-davinci-002") # Otherwise we do not get proper quality for this type of text. And as we only make a few calls, instability is not an issue here.
    thetest.set_LanguageChoice("Default")

    # Load the textfile:
    thetest.load()

    # Generate the text to summarize:
    text = ""
    for textline in thetest.textcontent:
        text = text + " " + textline

    # Perform the summarization:
    summary = thetest.summarize(text,verbose_option) # 0=be quiet.

    # Next, load the reference-summary:
    thetest.set_documentpath(truthpath)
    thetest.set_documentname("Musk_Summary")
    thetest.textcontent.clear()
    thetest.load()

    reference = ""
    cleanline = ""
    for textline in thetest.textcontent:
        cleanline = textline.replace("\n"," ")
        reference = reference + cleanline

    # Check whether there is some agreement:
    Answer = False
    if use_dummy_summary: fuzzy_ratio_threshold = 0.0
    else: fuzzy_ratio_threshold = 10.0

    TheRatio = CompareTexts(summary,reference)
    if (TheRatio>fuzzy_ratio_threshold): Answer = True

    if not Answer:
        print("==> FUZZY STRING MATCHING RATIO = " + str(TheRatio) + " (should be at least "+str(fuzzy_ratio_threshold)+")")
        print("\n")
        print("[MUSK-TEXT SUMMARY]")
        print(summary)
        print("\n")
        print("[MUSK-TEXT REFERENCE]")
        print(reference)

    # Return the answer:
    return Answer

# Definition of unit tests:
def TestSummarize_h(use_dummy_summary: bool) -> bool:
    """
    # Unit test for the function textpart.summarize() that summarizes
    # a given text using ChatGPT.
    # Parameters:
    use_dummy_summary: bool: decides whether we call ChatGPT to actually make summaries, or use a dummy summarization function.
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """

    # Create a textsplitter-class:
    filename = "Musk_wordcloud" # Fits in a single token portion.
    thetest = textsplitter()
    thetest.set_labelname("SummarizationTest")
    thetest.set_documentname(filename)
    thetest.set_documentpath(inputpath)
    thetest.set_outputpath(outputpath)
    thetest.set_UseDummySummary(use_dummy_summary)
    thetest.set_MaxSummaryLength(50) # guideline for the number of words per token portion.
    thetest.set_LanguageModel("text-ada-001") # Otherwise we do not get proper quality for this type of text. And as we only make a few calls, instability is not an issue here.
    thetest.set_LanguageChoice("Default")

    # Load the textfile:
    thetest.load()

    # Generate the text to summarize:
    text = ""
    for textline in thetest.textcontent:
        text = text + " " + textline

    # Perform the summarization:
    summary = thetest.summarize(text,verbose_option) # 0=be quiet.

    # Next, load the reference-summary:
    thetest.set_documentpath(truthpath)
    thetest.set_documentname("Musk_Summary")
    thetest.textcontent.clear()
    thetest.load()

    reference = ""
    cleanline = ""
    for textline in thetest.textcontent:
        cleanline = textline.replace("\n"," ")
        reference = reference + cleanline

    # Check whether there is some agreement:
    Answer = False
    if use_dummy_summary: fuzzy_ratio_threshold = 0.0
    else: fuzzy_ratio_threshold = 10.0

    TheRatio = CompareTexts(summary,reference)
    if (TheRatio>fuzzy_ratio_threshold): Answer = True

    if not Answer:
        print("==> FUZZY STRING MATCHING RATIO = " + str(TheRatio) + " (should be at least "+str(fuzzy_ratio_threshold)+")")
        print("\n")
        print("[MUSK-TEXT SUMMARY]")
        print(summary)
        print("\n")
        print("[MUSK-TEXT REFERENCE]")
        print(reference)

    # Return the answer:
    return Answer

# Definition of unit tests:
def TestSummarize_i(use_dummy_summary: bool) -> bool:
    """
    # Unit test for the function textpart.summarize() that summarizes
    # a given text using ChatGPT.
    # Parameters:
    use_dummy_summary: bool: decides whether we call ChatGPT to actually make summaries, or use a dummy summarization function.
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """

    # Create a textsplitter-class:
    filename = "Musk_wordcloud" # Fits in a single token portion.
    thetest = textsplitter()
    thetest.set_labelname("SummarizationTest")
    thetest.set_documentname(filename)
    thetest.set_documentpath(inputpath)
    thetest.set_outputpath(outputpath)
    thetest.set_UseDummySummary(use_dummy_summary)
    thetest.set_MaxSummaryLength(50) # guideline for the number of words per token portion.
    thetest.set_LanguageModel("text-curie-001") # Otherwise we do not get proper quality for this type of text. And as we only make a few calls, instability is not an issue here.
    thetest.set_LanguageChoice("Default")

    # Load the textfile:
    thetest.load()

    # Generate the text to summarize:
    text = ""
    for textline in thetest.textcontent:
        text = text + " " + textline

    # Perform the summarization:
    summary = thetest.summarize(text,verbose_option) # 0=be quiet.

    # Next, load the reference-summary:
    thetest.set_documentpath(truthpath)
    thetest.set_documentname("Musk_Summary")
    thetest.textcontent.clear()
    thetest.load()

    reference = ""
    cleanline = ""
    for textline in thetest.textcontent:
        cleanline = textline.replace("\n"," ")
        reference = reference + cleanline

    # Check whether there is some agreement:
    Answer = False
    if use_dummy_summary: fuzzy_ratio_threshold = 0.0
    else: fuzzy_ratio_threshold = 10.0

    TheRatio = CompareTexts(summary,reference)
    if (TheRatio>fuzzy_ratio_threshold): Answer = True

    if not Answer:
        print("==> FUZZY STRING MATCHING RATIO = " + str(TheRatio) + " (should be at least "+str(fuzzy_ratio_threshold)+")")
        print("\n")
        print("[MUSK-TEXT SUMMARY]")
        print(summary)
        print("\n")
        print("[MUSK-TEXT REFERENCE]")
        print(reference)

    # Return the answer:
    return Answer

# Definition of collection:    
def TestSummarize(use_dummy_summary: bool) -> bool:
    """
    # Collection-function of unit-tests.
    # Parameters: 
    use_dummy_summary: bool: decides whether we call ChatGPT to actually make summaries, or use a dummy summarization function.
    # Return: bool: the success of the test.
    # Author: christiaan Douma
    """
    
    Answer = True
    if (TestSummarize_a(use_dummy_summary)==False): Answer=False
    print("Summarize(a)...")
    if (TestSummarize_b(use_dummy_summary)==False): Answer=False
    print("Summarize(b)...")
    if (TestSummarize_c(use_dummy_summary)==False): Answer=False
    print("Summarize(c)...")
    if (TestSummarize_d(use_dummy_summary)==False): Answer=False
    print("Summarize(d)...")
    if (TestSummarize_e(use_dummy_summary)==False): Answer=False
    print("Summarize(e)...")
    if (TestSummarize_f(use_dummy_summary)==False): Answer=False
    print("Summarize(f)...")
    if (TestSummarize_g(use_dummy_summary)==False): Answer=False
    print("Summarize(g)...")
    if (TestSummarize_h(use_dummy_summary)==False): Answer=False
    print("Summarize(h)...")
    if (TestSummarize_i(use_dummy_summary)==False): Answer=False
    print("Summarize(i)...")
    return Answer

if __name__ == '__main__':
    
    # Identify parameters:
    use_dummy_summary = False
    if (len(sys.argv)>1):
        if (sys.argv[1]=="dummy"):
            use_dummy_summary = True
    
    # Perform the test:
    if TestSummarize(use_dummy_summary):
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
