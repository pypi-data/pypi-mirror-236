def summarize_textsplitter(self, text: str, verbose_option: int) -> str:
    """
    This function takes a certain amount of text and uses a chosen
    backend to summarize that tekst. Configuration-parameters in
    the textsplitter-class will determine which backend-function
    will be used (dummy, openai, private LLM, etc.)

    # Parameters:
    text: str: the text that has to be summarized (possible a long string).
    verbose_option: int: 0: then nothing will be printed. higher numbers will print in-between stages in the terminal.
    # Return: str: the summary of the text.
    """

    # ---------------------------------------------------------------------

    # Begin by deciding whether we have to use the dummy-function or not:
    if self.UseDummySummary:

        # Notify the user that we use dummy-mode:
        if (verbose_option>=0):
            print("NOTE: The summarization procedure was carried out using a dummy-function!")

        # Handle the summarization:
        return self.summarize_dummy(text,verbose_option)

    # Next, do not summarize anything if the number of words is below the threshold:
    elif (len(text.split())<self.summarization_threshold): return text

    # Then, see if we have to use a ChatGPT backend:
    elif (self.BackendChoice == "openai"): return self.summarize_openai(text,verbose_option)

    # Also, see if we have to use our private option:
    elif (self.BackendChoice == "private_huggingface"): return self.summarize_private_huggingface(text,verbose_option)

    # Implement a default option that is easily spotted:
    else: return ""

def summarize_dummy_textsplitter(self, text: str, verbose_option: int) -> str:
    """
    This function takes a certain amount of text and uses a dummy-algorithm
    to summarize the text: selecting the first n words from the text.
    This is meant for testing purposes, so that the CPU-time
    and financial costs are small, while the entire functionality
    of the package can be tested, except for the actual summarization
    code. The number of words (n) that is used, is 2*MaxSummaryLength,
    to account for the fact that ChatGPT takes MaxSummaryLength
    more as a guidance then an actual fact.

    # Parameters:
    text: str: the text that has to be summarized (possible a long string).
    verbose_option: int: 0: then nothing will be printed. higher numbers will print in-between stages in the terminal.
    # Return: str: the summary of the text.
    """

    # Begin by splitting the full string in words:
    text_array = text.split()

    # Then, decide whether the string is longer or shorter then the limit:
    if (len(text_array)>2*self.MaxSummaryLength):

        # If the string is too long, cap it at the desired number of words:
        text_array = text_array[0:2*self.MaxSummaryLength]

    # Then, compose the answer by putiing the words back into one string:
    Answer = ""
    for word in text_array:
        Answer = Answer + word + " "
    
    # Handle vebosity:
    if (verbose_option>1): print("==> Dummy-Answer = " + str(Answer))

    # Return the answer:
    return Answer
    
