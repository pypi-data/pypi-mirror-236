# Python import commands:
import sys
import os
import openai
sys.path.insert(1, '../TextPart/')
from textsplitter import textsplitter

# Process the document:
mysplitter = textsplitter()
mysplitter.set_documentpath("./")
mysplitter.set_documentname("Burgerlijk wetboek pag 1")
mysplitter.set_outputpath("./output_wetboek/")
mysplitter.standard_params()
mysplitter.set_footerboundary(0.0)
mysplitter.set_ruleverbosity(1)
mysplitter.set_UseDummySummary(True)
mysplitter.process()

# Next, attempt to make a chatGPT-call to see if there are
# any contradictions in the text with respect to a new proposal:
MyProposal = "Aanverwantschap eindigt door middel van een huwelijk."
# MyProposal = "Een ambtenaar mag een kind ambtshalve nooit een voornaam geven."

# Loop through the textual elements:
Base_Instruction = "Antwoordt met een enkel ja of nee: spreekt de volgende text zichzelf tegen?;"
Boolean_Array = []

for alinea in mysplitter.textalineas:
        
    # Obtain the prompt:
    # TODO: Take token limit into account.
    prompt = Base_Instruction + MyProposal + "; "
    for textline in alinea.textcontent:
        prompt = prompt + textline
    
    # Create the message-array:
    MyMessage = [{"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}]
    
    # Call ChatGPT:
    # TODO: Rate limit, exception catching, etc. Basically all that Summarize does.
    openai.api_key = mysplitter.ChatGPT_Key
    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=MyMessage,
                        max_tokens=1000,
                        n=1,
                        stop=None,
                        temperature=0.01)
    
    # Obtain the textual response:
    text_responce = response.choices[0]["message"]["content"]
    
    # process:
    text_responce = text_responce.replace("\n","")
    text_responce = text_responce.replace(" ","")
    text_responce = text_responce.replace(".","")
    text_responce = text_responce.replace(",","")
    text_responce = text_responce.lower()
    print(text_responce)
    if (text_responce=="ja"):
        Boolean_Array.append(True)
    else:
        Boolean_Array.append(False)

# Next, goet our source of the contradition:
alinea_index = 0
for answer in Boolean_Array:
    
    thisindex = alinea_index
    if answer:
        # then, we found a contradiction:
        print("\n")
        print("Your proposal contradicts with the following parts of the documents:")
        
        while (thisindex>=0):
            print("--> " + mysplitter.textalineas[thisindex].texttitle)
            thisindex = mysplitter.textalineas[thisindex].parentID
    
    alinea_index = alinea_index + 1
    
# Ja, ChatGPT kan de tegenspraken wel detecteren. Maar alleen in hele kleine porties.
# Als we een complexere Proposal doen en/of de tegenspraak is minder duidelijk, wordt
# het al lastiger voor ChatGPT. Dat is waarschijnlijk waarom het met langchain niet werkt.
# Daar testen we meerdere brieven tegelijk. 

# gpt-4 lijkt wel iets beter dan gpt-3.5-turbo (zoals verwacht), maar tegenspraken detecteren
# werkt alleen in kleine documentstukjes en o.b.v. de testen die ik heb uitgevoerd, zou
# ik het antwoord niet te veel vertrouwen. En dat maakt toepassingen lastig. Een incorrecte
# ja is nog 1 ding, maar een incorrecte nee is uit den boze. Als je die 1x hebt is je hele
# test waardeloos omdat de gebruiker dan toch zelf het hele document moet doornemen.
    
    
    
    
    
    
