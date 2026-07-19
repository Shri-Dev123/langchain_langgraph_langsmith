from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model="gpt-5.6", api_key=os.environ.get("MY_CUSTOM_KEY_VARIABLE"))

streamed_response = model.stream("tell me about NBA")

for chunk in streamed_response:
    print(chunk.content, end="", flush=True) # end="" ensures that the output is printed on the same line, and flush=True forces the output to be written to the console immediately. This is useful for streaming responses where you want to see the output as it is generated.