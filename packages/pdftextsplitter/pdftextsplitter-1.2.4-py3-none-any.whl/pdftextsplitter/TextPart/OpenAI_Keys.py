import os

class OpenAI_Keys:
    """
    This stores the various keys that we can use to connect to OpenAI (different accounts).
    That will allow us to easily select one.
    """
    
    # Definition of the default-constructor:
    def __init__(self):
        self.standard_key = os.getenv("OPENAI_ANTON_PAID_KEY")
        self.other_key    = "you can store all of your OpenAI-keys here if you like."

        # Parameters to control API rate limit:
        self.ratelimit_timeunit = 60.0      # Time interval for which the rate limits of the account are defined.     
        self.ratelimit_calls = 200          # Maximum number of calls that are allowed within the time interval.
        self.ratelimit_tokens = 40000       # Maximum number of tokens that are allowed within the time interval.
        
        # Parameters to calculate the costs of a document.
        self.Costs_price = 0.002            # Amount of euro's that a single ChatGPT-call costs. gpt3.5-turbo: 0.002 & 0.06 for gpt4 (30x more expensive).
        self.Costs_tokenportion = 1000      # Amount of tokens that can maximally be within a single call to charge this price.
        
