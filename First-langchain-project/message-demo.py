from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

model = ChatOpenAI(model="gpt-5.6")

systemInstruction = SystemMessage(content="reply every prompt in french") # System instruction to the model to reply in French
userMessage = HumanMessage(content="Who is the president of India") # User message to the model asking for the president of India

response = model.invoke([
  systemInstruction,
  userMessage
])

print(response.content) # Print the content of the model's response