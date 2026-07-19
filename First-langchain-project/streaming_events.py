from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

model = ChatOpenAI(model='gpt-5.6',api_key=os.environ.get("MY_CUSTOM_KEY_VARIABLE"))

async def stream_response_events():
  event_limit = 0
  prompt = "Describe the NBA"

  async for event_chunk in model.astream_events(prompt, version="v2"):
    event_limit += 1

    if event_limit >= 5:
      print("event streaming done.....")
      return
    print(event_chunk)

asyncio.run(stream_response_events())


# in the above code, we are using the astream_events method to stream events from the model. 
# This allows us to receive real-time updates about the generation process, which can be useful for monitoring and debugging purposes.