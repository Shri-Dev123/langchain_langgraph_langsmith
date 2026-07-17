from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-5.6")

prompt = [
  "who is the president of India",
  "What is the capital of Maharashtra",
  "who is the current Chief Minister of the state Tamilnadu"
]

batch_responses = model.batch(prompt)

for response in batch_responses:
    print(response.content)
