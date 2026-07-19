from langchain_openai import ChatOpenAI
from langchain_core.globals import set_llm_cache
from langchain_core.caches import InMemoryCache
import os
from dotenv import load_dotenv

load_dotenv()
model = ChatOpenAI(
  model="gpt-5.6",
  api_key=os.environ.get("MY_CUSTOM_KEY_VARIABLE"))

set_llm_cache(InMemoryCache()) # InMemoryCache is a class that provides an in-memory cache for storing the responses of the model. This can be useful for reducing the number of API calls made to the model, as well as for improving the performance of the application by avoiding repeated calls to the model for the same input.

prompt = "who is the FSSAI commissioner of India?"
response = model.invoke(prompt)
print(response.content)
response2 = model.invoke(prompt) # This is a repeated call to the model with the same input as the previous call. Since we have set up an in-memory cache, the response for this call will be retrieved from the cache instead of making a new API call to the model. This can help reduce the number of API calls made to the model and improve the performance of the application.

print(response2.content)