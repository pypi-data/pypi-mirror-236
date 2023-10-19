import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '../TextPart/')
import inspect
import openai
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage,HumanMessage,SystemMessage
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.document_loaders import TextLoader
from OpenAI_Keys import OpenAI_Keys

if __name__ == '__main__':
    
    thekeys = OpenAI_Keys()
    the_openai_key = thekeys.standard_key
    
    print("Input variables from function 'ChatOpenAI':")
    myproperties = inspect.signature(ChatOpenAI)
    input_variables = list(myproperties.parameters.keys())
    print(input_variables)
    print("\n")
    
    print("Input variables from function 'OpenAIEmbeddings':")
    myproperties = inspect.signature(OpenAIEmbeddings)
    input_variables = list(myproperties.parameters.keys())
    print(input_variables)
    print("\n")
    
    print("Input variables from function 'Chroma.from_texts':")
    myproperties = inspect.signature(Chroma.from_texts)
    input_variables = list(myproperties.parameters.keys())
    print(input_variables)
    print("\n")
    
    print("Input variables from function 'Chroma.from_documents':")
    myproperties = inspect.signature(Chroma.from_documents)
    input_variables = list(myproperties.parameters.keys())
    print(input_variables)
    print("\n")
    
    print("Input variables from function 'RetrievalQAWithSourcesChain.from_chain_type':")
    myproperties = inspect.signature(RetrievalQAWithSourcesChain.from_chain_type)
    input_variables = list(myproperties.parameters.keys())
    print(input_variables)
    print("\n")
    
    print("Input variables from function 'TextLoader':")
    myproperties = inspect.signature(TextLoader)
    input_variables = list(myproperties.parameters.keys())
    print(input_variables)
    print("\n")
    
    loader = TextLoader("./abstract.txt")
    loader.load()
    
    chat = ChatOpenAI(temperature=0,
                      openai_api_key=the_openai_key,
                      model="gpt-3.5-turbo",
                      max_tokens=2000,
                      )    
    
    MyMessages = [SystemMessage(content="You are a helpful assistant."),
                  HumanMessage(content="Translate this sentence from English to French; I love programming.")]
    
    """
    Outcome = chat.predict_messages(MyMessages)
    print(Outcome.__dict__.keys())
    Response = Outcome.content
    
    print("\n The ChatGPT Response is:")
    print(Response)
    """
