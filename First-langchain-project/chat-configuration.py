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