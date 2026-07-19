from langchain_openai import ChatOpenAI
from langchain_community.callbacks.manager import get_openai_callback
import os
from dotenv import load_dotenv

load_dotenv()
model = ChatOpenAI(
  model="gpt-5.6",
  api_key=os.environ.get("MY_CUSTOM_KEY_VARIABLE"))

with get_openai_callback() as callback:
    response = model.invoke("What are the Mandatory nurtrients as per the  USA FDA?")
    response2 = model.invoke("who is the preseident of USA?")
    print(callback) # callback is an object that contains information about the usage of the model, such as the number of tokens used, the time taken for the request, and any errors that occurred. This information can be useful for monitoring and optimizing the usage of the model.