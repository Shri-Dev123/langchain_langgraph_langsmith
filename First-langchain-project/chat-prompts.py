from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-5.6")

prompts = [
  ("system","Reply every prompt in {language}"),
  ("user","Who is the president of {country}?"),
       ]

myPrompt = ChatPromptTemplate(prompts)

chat_prompt = myPrompt.invoke({"language":"English","country":"USA"})

response = model.invoke(chat_prompt)

print(response.content)