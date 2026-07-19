from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
model = ChatOpenAI(
  model="gpt-5.6",
  api_key=os.environ.get("MY_CUSTOM_KEY_VARIABLE"))

response = model.invoke("What are the Mandatory nurtrients as per the  USA FDA?")

#print(response.usage_metadata) # usage_metadata is a property of the response object that contains information about the usage of the model, such as the number of tokens used, the time taken for the request, and any errors that occurred. This information can be useful for monitoring and optimizing the usage of the model.

print(response.response_metadata["token_usage"]) # response_metadata is a property of the response object that contains information about the response, such as the number of tokens used, the time taken for the request, and any errors that occurred. This information can be useful for monitoring and optimizing the usage of the model. The token_usage key in the response_metadata dictionary contains information about the number of tokens used in the request and response.