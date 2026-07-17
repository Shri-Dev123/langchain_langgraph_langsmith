from langchain_openai import ChatOpenAI


model = ChatOpenAI(model="gpt-5.6")

response = model.invoke("todays date")

print(response.content)