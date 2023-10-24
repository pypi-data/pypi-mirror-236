import sys
# caution: path[0] is reserved for script path (or '' in REPL)

# Imports from TextPart code:
sys.path.insert(1, '../../')
from Source.openaiscript import generate_response

# Definition of unit tests:
def TestOpenAI_a() -> bool:
    """
    # Unit test for text the script using the GetTitleLines.py script.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    prompt = "Tell me in a single word: What is the largest city in the Netherlands?"
    response = generate_response(prompt)
    desired_response = "Amsterdam"

    Answer = False
    if ((response.lower()==desired_response.lower())or(response.lower()==(desired_response+".").lower())):
        Answer = True
    else:
        print("==> TestOpenAI_a PROMPT: "+prompt+"\n\n")
        print("==> AI response = "+response+"\n")
        print("==> Desired response = "+desired_response+"\n")   
        print("---------------------------------------------\n")
        
    return Answer

def TestOpenAI_b() -> bool:
    """
    # Unit test for text the script using the GetTitleLines.py script.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    prompt = "Tell me in a single word: Which company makes iphones?"
    response = generate_response(prompt)
    desired_response = "Apple"

    Answer = False
    if ((response.lower()==desired_response.lower())or(response.lower()==(desired_response+".").lower())):
        Answer = True
    else:
        print("==> TestOpenAI_b PROMPT: "+prompt+"\n\n")
        print("==> AI response = "+response+"\n")
        print("==> Desired response = "+desired_response+"\n")   
        print("---------------------------------------------\n")
        
    return Answer

def TestOpenAI_c() -> bool:
    """
    # Unit test for text the script using the GetTitleLines.py script.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    prompt = "Tell me in a single word: What particles obey the Pauli exclusion principle?"
    response = generate_response(prompt)
    desired_response = "Fermions"

    Answer = False
    if ((response.lower()==desired_response.lower())or(response.lower()==(desired_response+".").lower())): 
        Answer = True
    else:
        print("==> TestOpenAI_c PROMPT: "+prompt+"\n\n")
        print("==> AI response = "+response+"\n")
        print("==> Desired response = "+desired_response+"\n")   
        print("---------------------------------------------\n")
        
    return Answer

# Definition of collection:    
def TestOpenAI() -> bool:
    """
    # Collection-function of unit-tests.
    # Parameters: none; # Returns (bool): succes of the text.
    # Author: christiaan Douma
    """
    
    Answer = True
    if (TestOpenAI_a()==False): Answer=False
    if (TestOpenAI_b()==False): Answer=False
    if (TestOpenAI_c()==False): Answer=False
      
    return Answer

if __name__ == '__main__':
    if TestOpenAI():
        print("Test Succeeded!")
    else:
        print("\n==> Test FAILED!!!\n")
