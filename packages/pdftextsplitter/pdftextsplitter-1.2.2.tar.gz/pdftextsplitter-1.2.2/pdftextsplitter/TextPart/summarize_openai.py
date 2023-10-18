# Python functionality:
import io
import openai
import tiktoken
import time
import math

# Textpart imports:
from .regex_expressions import text_isnotcapped
from .regex_expressions import remove_nonletters

def summarize_openai_textsplitter(self, text: str, verbose_option: int) -> str:
    """
    This function takes a certain amount of text and uses ChatGPT
    to summarize that tekst. ChatGPT is connected through the 
    python openai-library that allows command-line interaction
    with ChatGPT. Key parameters are the access token of the 
    ChatGPT-account and the maximum number of words in the summary.
    Both these parameters are stored in the textsplitter-class.
    
    NOTE: The text should preferably keep as many newline characters
    as possible, so be sure to add them when appending a textcontent-array to text.
    
    # Parameters: 
    text: str: the text that has to be summarized (possible a long string).
    verbose_option: int: 0: then nothing will be printed. higher numbers will print in-between stages in the terminal.
    # Return: str: the summary of the text.
    """
    
    # ---------------------------------------------------------------------
    
    # Begin by setting the maximum token length of prompt plus answer:
    Account_maxtokens = 4000 # This is 20% cheapter then 4096
    
    # Define a margin (for the summary instruction, counting errors, etc:
    Token_margin = 50
    
    # Calculate the number of required tokens in the answer:
    Answer_required = 5*self.MaxSummaryLength
    
    # Calculate how long a piece of tekst can be:
    Token_portion = Account_maxtokens - Token_margin - Answer_required
    
    # Define the base instruction:
    Base_Instruction = "Summarize the following text in at most " + str(self.MaxSummaryLength) + " words; "
    if (self.LanguageChoice=="English"): 
        Base_Instruction = "Summarize the following text in English and in at most " + str(self.MaxSummaryLength) + " words; "
    elif (self.LanguageChoice=="Dutch"): 
        Base_Instruction = "Vat de volgende tekst samen in het Nederlands en in maximaal " + str(self.MaxSummaryLength) + " woorden; "
    elif (self.LanguageChoice=="Original"):
        Base_Instruction = "Summarize the following text in its own language and in at most " + str(self.MaxSummaryLength) + " words; "
    elif (self.LanguageChoice=="French"):
        Base_Instruction = "Résumez le texte suivant en français et en " + str(self.MaxSummaryLength) + " mots maximum; "
        
    # Define the base-message structure for ChatCompletions on this base_prompt:
    MyMessage = [{"role": "system", "content": "You are a helpful assistant."},
                 {"role": "user", "content": Base_Instruction}]
    
    # Next, count how many tokens our text-piece contains:
    encoding = tiktoken.encoding_for_model(self.LanguageModel)
    # Options: gpt2, gpt-3.5-turbo, gpt-4, cl100k_base, p50k_base, text-davinci-002, text-davinci-003
    # functions: get_encoding() or encoding_for_model()
    # gpt2 is closest to how ChatGPT (at least: this account) counts.
    
    # then, continue:
    tokens = encoding.encode(text)
    Number_of_tokens = len(tokens)
    
    # Also count how many words our text contains:
    text_array = text.split()
    Number_of_words = len(text_array)
    
    # Next, we need to split our text in portions of Token_portion
    # and ask a summary for each piece separately.
   
    Start_Token = 0
    Array_to_summarize = []
    Tokens_in_array = []
    
    while (Start_Token<Number_of_tokens):
        
        # First, check if have less then Token_portion:
        if ((Number_of_tokens-Start_Token)<Token_portion):
            
            # Then, this is easy. Just take all that is left:
            tokens_part = tokens[Start_Token:Number_of_tokens-1]
        
        else:
            
            # Then, we only need to take the next piece:
            tokens_part = tokens[Start_Token:(Start_Token+Token_portion-1)]
        
        # Then, take the corresponding piece of text:
        text_part = encoding.decode(tokens_part)
        
        # Append it to the summarization-array:
        Array_to_summarize.append(text_part)
        Tokens_in_array.append(len(tokens_part))
        
        # Next, update the Start_Token:
        Start_Token = Start_Token + Token_portion
    
    # Now, our array is ready to pass to ChatGPT:
    openai.api_key = self.ChatGPT_Key
    TheSummary = []
    ArrayIndex = 0
    
    # If this is the first call that we make, reset the trackers for the rate limit:
    if (self.callcounter==0):
        self.api_rate_starttime = time.time()
        self.api_rate_currenttime = 0.0
        self.api_rate_currenttokens = 0
        self.api_rate_currentcalls = 0
        self.api_totalprice = 0.0
        self.api_wrongcalls_duetomaxwhile = 0
    
    # Next, loop over all textpieces in the text to be summarized:
    for textpiece in Array_to_summarize:
        
        # Then, continue looping & calling to ChatGPT until we get a response that we like:
        Response_IsOK = False
        
        # Calculate the length for a textpiece. Note that without the replace, 
        # a proper length calculation is not possible:
        textpiece_nobreaks = textpiece.replace("\n"," ")
        length_textpiece = len(textpiece_nobreaks.split())
        
        # Manage temperature settings. each time we retry, we want to raise temperature a little to
        # allow for more variations, so the probability increases that the next call will be accepted.
        Base_Temperature = self.LanguageTemperature
        
        # Use a while-loop:
        WhileCounter = 0
        while (not(Response_IsOK))and(WhileCounter<self.MaxCallRepeat):
            
            # Begin with managing the while-counter:
            WhileCounter = WhileCounter + 1
            
            # Convert Base temperature into actual temperature using the while-counter:
            Actual_Temperature = Base_Temperature + 0.05*(WhileCounter-1)
            if (Actual_Temperature>0.95): Actual_Temperature = 0.95 
            
            # Log if we actually hit the maximum number of loops:
            if (WhileCounter==self.MaxCallRepeat):
                self.api_wrongcalls_duetomaxwhile = self.api_wrongcalls_duetomaxwhile + 1
                
                # Log this case:
                if isinstance(self.logfile, io.TextIOBase):
                    if self.logfile.writable():
                        self.logfile.write("This is the last time we can attempt to summarize the textpiece. We will keep the outcome no matter what!")
                
                # print it:
                if (verbose_option>=0):
                    print(" ==> This is the last time we can attempt to summarize the textpiece. We will keep the outcome no matter what!")
            
            # Before making the call, we will measure time, rate & tokens to manage the rate limit
            # of the OpenAI API-connection:
            self.api_rate_currenttime = time.time() - self.api_rate_starttime
            self.api_rate_currenttokens = self.api_rate_currenttokens + Tokens_in_array[ArrayIndex] + Answer_required + Token_margin # Tokens in tekst, plus margin plus answer.
            self.api_rate_currentcalls = self.api_rate_currentcalls + 1
            self.callcounter = self.callcounter + 1
            
            # Sleep if we passed the rate limit:
            if (self.api_rate_currenttokens>self.ratelimit_tokens)or(self.api_rate_currentcalls>self.ratelimit_calls):
                # Then, sleep for the amount of time that we still have left in our window:
                if (self.api_rate_currenttime<=self.ratelimit_timeunit):
                    print("===> textsplitter.summarize() will sleep for " + str(self.ratelimit_timeunit - self.api_rate_currenttime) + " seconds to prevent an OpenAI RateLimitError. Tokens = " + str(self.api_rate_currenttokens) + "/" + str(self.ratelimit_tokens) + " and Calls = " + str(self.api_rate_currentcalls) + "/" + str(self.ratelimit_calls))
                    time.sleep(self.ratelimit_timeunit - self.api_rate_currenttime)
            
            # When sufficient time has passed, we will reset the counters:
            if ((time.time() - self.api_rate_starttime)>self.ratelimit_timeunit): # Should always be the case after a sleep!
                print(" ===> textsplitter.summarize() has reset the rate-limit counters after " + str(self.ratelimit_timeunit) + " seconds. Tokens = " + str(self.api_rate_currenttokens) + "/" + str(self.ratelimit_tokens) + " and Calls = " + str(self.api_rate_currentcalls) + "/" + str(self.ratelimit_calls))
                self.api_rate_starttime = time.time()                                                       # In seconds!
                self.api_rate_currenttime = 0.0                                                             # In seconds!
                self.api_rate_currenttokens = Tokens_in_array[ArrayIndex] + Answer_required + Token_margin  # We haven't made the actual call, so we must include the future call-to-be-made.
                self.api_rate_currentcalls = 1                                                              # We haven't made the actual call, so we must include the future call-to-be-made.
            
            # Give some general output on rate limit tracking:
            if (verbose_option>0):
                print("RATE LIMIT TRACKING: Time = " + str(time.time()) + " and Tokens = " + str(self.api_rate_currenttokens) + "/" + str(self.ratelimit_tokens) + " and Calls = " + str(self.api_rate_currentcalls) + "/" + str(self.ratelimit_calls) + " and Total Calls = " + str(self.callcounter))
            
            # Update the message-structure with the current textpiece:
            MyMessage[1]["content"] = Base_Instruction+textpiece
            
            # Then, actually make the call. text-davinci-002 is the gpt-3.5-turbo model that costs 0.2 ct per 1000 tokens.
            # text-davinci-003 can also be used and is of much better quality, but that one is much more expensive. Surround it by try-except block,
            # so we can keep on trying if it fails:
            openai_call_succeeded = True
            response = ""
            
            try:
                
                # decide upon model-choice:
                if ("gpt" in self.LanguageModel):
                    
                    # then, we use a ChatCompletion-instruction, which is appropriate for models such as gpt3.5-turbo:
                    response = openai.ChatCompletion.create(
                        model=self.LanguageModel,
                        messages=MyMessage,
                        max_tokens=Account_maxtokens-Token_portion+Token_margin,
                        n=1,
                        stop=None,
                        temperature=Actual_Temperature,
                    )
                    
                else:
                    
                    # then, we use a completion-instruction, which is appropriate for models such as davinci:
                    response = openai.Completion.create(
                        engine=self.LanguageModel,
                        prompt=Base_Instruction+textpiece,
                        max_tokens=Account_maxtokens-Token_portion+Token_margin,
                        n=1,
                        stop=None,
                        temperature=Actual_Temperature,
                    )
                    
            except Exception as openai_exception:
                
                # Then, begin by marking that we caught an exception:
                openai_call_succeeded = False
                
                # Print it:
                print(" ==> The OpenAI API for ChatGPT raised the following exception:")
                print(openai_exception)
                print("")
                print(" ==> No problem, we will just try again until we succeed; managing the API rate limit of course.")
                print("")
                
                # Log our data:
                if isinstance(self.logfile, io.TextIOBase):
                    if self.logfile.writable():
                        self.logfile.write("ChatGPT Call " + str(self.callcounter) + " made at " + str(time.time()) + " raised exception: " + str(openai_exception) + ". We will re-try the call.\n")
                
                # Add our failed attempt to the price calculation. NOTE: We add it as a single call only, as a proper token-calculation cannot be done
                # when completion-tokens are unknown and only tiktoken-estimates are available for prompt-tokens:
                self.api_totalprice = self.api_totalprice + self.Costs_price
                
            # If no exception was made, we can safely continue. Otherwise, we must simply state that there was no success
            # and wait for the next iteration in the while-loop:
            if not openai_call_succeeded:
                
                # Then, we simply state that there is no success and stop doing anything until the next while-iteration:
                Response_IsOK = False
                
            else:
                
                # Next, we mus decide whether the obtained response suffices, so begin by declaring the boolian to be true:
                Response_IsOK = True
                
                # Then, we can move on. Begin by adding the call to the Calculated cost:
                if hasattr(response, "usage"):
                    if (hasattr(response.usage, "prompt_tokens"))and(hasattr(response.usage, "completion_tokens"))and(hasattr(response.usage, "total_tokens")):
                        # If this is the case, we can move on:
                     
                        # Log our data:
                        if isinstance(self.logfile, io.TextIOBase):
                            if self.logfile.writable():
                                self.logfile.write("ChatGPT Call " + str(self.callcounter) + " made at " + str(time.time()) + " | " + str(int(response.usage.prompt_tokens)) + " tokens in prompt | " + str(int(response.usage.completion_tokens)) + " in completion.\n")
                                
                        # Calculate costs:
                        TheValue = math.ceil((int(response.usage.total_tokens))/self.Costs_tokenportion)
                        self.api_totalprice = self.api_totalprice + TheValue*self.Costs_price
                    
                    else:
                        # Then, the call was clearly not OK, so we should try again in the while-loop:
                        Response_IsOK = False
                        
                        if (verbose_option>=0):
                            print("ChatGPT returned a response without usage.tokens, so that response is not usable.  We will re-try the call.")
                        
                        if isinstance(self.logfile, io.TextIOBase):
                            if self.logfile.writable():
                                self.logfile.write("ChatGPT Call " + str(self.callcounter) + " made at " + str(time.time()) + " did not have usage.token attributes, so it could not be logged.  We will re-try the call.\n")
                        
                        # Add our failed attempt to the price calculation. NOTE: We add it as a single call only, as a proper token-calculation cannot be done
                        # when completion-tokens are unknown and only tiktoken-estimates are available for prompt-tokens:
                        self.api_totalprice = self.api_totalprice + self.Costs_price
                
                else:
                    # Again, not OK:
                    Response_IsOK = False
                    
                    if (verbose_option>=0):
                            print("ChatGPT returned a response without usage, so that response is not usable. We will re-try the call.")
                    
                    if isinstance(self.logfile, io.TextIOBase):
                        if self.logfile.writable():
                            self.logfile.write("ChatGPT Call " + str(self.callcounter) + " made at " + str(time.time()) + " did not have a usage attribute, so it could not be logged.  We will re-try the call.\n")
                    
                    # Add our failed attempt to the price calculation. NOTE: We add it as a single call only, as a proper token-calculation cannot be done
                    # when completion-tokens are unknown and only tiktoken-estimates are available for prompt-tokens:
                    self.api_totalprice = self.api_totalprice + self.Costs_price
                
                # Next, we can start to process the actual responce into a usable text-string.
                # ATTENTION: For some reason, This way of calling ChatGPT has the habit of keeping parts 
                # of the orginal text that do not contribute to thesummary at all. So we must only keep the 
                # part after the last newline:
                if Response_IsOK:
                    
                    # then, it is safe to disect the responce-attributes. First, decide for completion/ChatCompletion
                    # which determines how to disect the response:
                    if ("gpt" in self.LanguageModel):
                        
                        # Then, we have to follow the ChatCompletion-structure for gpt-models:
                        text_responce = response.choices[0]["message"]["content"]
                        short_responce = text_responce
                    
                    else:
                        
                        # Then, we have to follow the completion-structure for davinci-models:
                        text_responce = response.choices[0].text.strip()
                        split_responce = text_responce.split("\n")
                    
                        # then, only take the last part:
                        if (len(split_responce)>0):
                            short_responce = split_responce[len(split_responce)-1]
                        else:
                            short_responce = ""
                
                        # Remove first 'Summarize'-part:
                        short_responce = short_responce.replace(" Summarize: ","")
                    
                else:
                    
                    # Then, short_responce should obviously be empty:
                    short_responce = ""
            
                # Check the length of the response. It should not be too short: we want at least 0.4* of the max. summary length,
                # unless the text we summarize is shorter. Then we want at least 0.4* that length. This is crucial, as otherwise
                # some texts may never succeed.
                length_summary = len(short_responce.split())
                
                if (length_summary<0.3*min(self.MaxSummaryLength,length_textpiece)):
                    # Then, the returned summary is too short:
                    Response_IsOK = False
                
                    if (verbose_option>=0):
                        print("ChatGPT returned a summary that is way too short. len(summary)="+str(length_summary)+" and len(text)=" + str(length_textpiece))
                        
                        if (verbose_option>0):
                            print(" ==> textpiece: ==> ")
                            print(textpiece)
                            print("")
                            print(" ==> Summary: ==> ")
                            print(short_responce)
                            print("")
                    
                    # Log our data:
                    if isinstance(self.logfile, io.TextIOBase):
                        if self.logfile.writable():
                            self.logfile.write("ChatGPT Call " + str(self.callcounter) + " returned a summary that was too short. We will re-try the call.\n")
            
                # Check for capped-text. This should only be done if the text-string is indeed natural language and not some type numbers, etc.
                letters_in_response = remove_nonletters(short_responce)
                length_letters = len(letters_in_response)
                length_ratio = 0.0
                if (length_summary>0.4): length_ratio = length_letters/length_summary
                isnotcapped = text_isnotcapped(short_responce)
                # A quick measurement reveals that Copernicus: 13514/16464 = 0.82082 & cellar: 129719/156212 = 0.83040
                
                # Now, we only need to refuse the summary is BOTH length_ratio is above a certain value (meaning that we are talking about normal text).
                # Given the measurements on the other docs, we take a safety margin and use 0.75. For curie this happens too often to test on it:
                if (not(isnotcapped))and(length_ratio>0.75)and("curie" not in self.LanguageModel):
                    # Then, the returned summary does not end with a dot, while it is normal text and, actually, should end in a dot:
                    Response_IsOK = False
                
                    if (verbose_option>=0):
                        print("ChatGPT returned a summary that contained capped text (not ending in a dot)")
                        
                        if (verbose_option>=0):
                            print(" ==> textpiece: ==> ")
                            print(textpiece)
                            print("")
                            print(" ==> Summary: ==> ")
                            print(short_responce)
                            print("")
                    
                    # Log our data:
                    if isinstance(self.logfile, io.TextIOBase):
                        if self.logfile.writable():
                            self.logfile.write("ChatGPT Call " + str(self.callcounter) + " returned a summary that did not end with a dot. As such, the text is probably capped and we will re-try.\n")
                
                # So, if at this point the response suffices, then we have that Response_IsOK==True and we move on to the next item in the summarize-array.
            
        # -----------------------------------------------------------------------
        # Next, end the while-loop & exception-test and keep the response from ChatGPT that we like:
        TheSummary.append(short_responce)
        
        # Increase index of the summarization-array:
        ArrayIndex = ArrayIndex + 1
    
    # ---------------------------------------------------------------------------------------------------
    # Next, close our for-loop over the summarization-array. Now, we must combine the different responses
    # of ChatGPT into a single answer:
    Answer = ""
    for assum in TheSummary:
        Answer = Answer + assum + " "
    
    # Give some output (verbosity):
    if (verbose_option>1):
        print("textsplitter.summarize() is under development")
        print("Number of tokens = " + str(Number_of_tokens))
        print("Number of words = " + str(Number_of_words))
        print("\n")
        print("[TEXT]")
        print("\n")
        for piece in Array_to_summarize:
            if (verbose_option>1): print(piece)
            print("------ token split ----------")
    
        print("\n")
        print("[SUMMARY]")
        for piece in TheSummary:
            print(piece)
            print("------ token split ----------")
    
    # Then, we can now return the answer:
    return Answer
