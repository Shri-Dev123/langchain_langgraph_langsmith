from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatOpenAI(
  model="gpt-5.6",
  api_key = os.environ.get("MY_CUSTOM_KEY_VARIABLE"),
  max_tokens= 1000
)

response = model.invoke("Explain quantum physics")

print(response.content)

# there are other parameters that can be passed to the model like 
# temperature, 
# top_p, f
# requency_penalty, 
# presence_penalty, 
# stop,
# max_retries,
# request_timeout,
# base_url,
# api_key,
# organization,
#  etc. You can find more information about these parameters in the OpenAI API documentation.