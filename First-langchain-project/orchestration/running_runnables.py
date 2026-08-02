from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(
    model="gpt-5.6",  # or "gpt-5", "gpt-5-mini" if your account has access
    api_key=os.getenv("MY_CUSTOM_KEY_VARIABLE"),
    # temperature=0
)

# Demo 1 - Invoke

invoked_prompt = "Where is the Eiffel Tower located?"

invoked_response = model.invoke(invoked_prompt)

print(f"invoked_prompt: {invoked_prompt}")
print(f"invoked_response: {invoked_response.content}")


# Demo 2 - Batch

batch_prompts = [
    "Where is the Eiffel Tower located?",
    "What is the capital of France?",
    "What is the largest ocean on Earth?",
]

batched_response = model.batch(batch_prompts)

print(f"batch_prompts: {batch_prompts}")
for response in batched_response:
    print(f"batched-response: {response.content}")


# Demo 3 - Stream

streamed_prompt = "Tell me a story about a brave knight."

streamed_response = model.stream(streamed_prompt)

print(f"streamed_prompt: {streamed_prompt}")
for chunk in streamed_response:
    print(chunk.content, end=" | ", flush=True) # Print each chunk as it arrives, separated by a pipe symbol which is a common delimiter for streaming data. The flush=True argument ensures that the output is immediately displayed in the console without buffering.
