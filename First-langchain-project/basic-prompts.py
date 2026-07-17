from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-5.6")

prompt1 = PromptTemplate(template="What is the capital of France?")

prompt2 = PromptTemplate.from_template("who is the president of {country}?")

print(prompt2.invoke({"country":"India"})) #invoke needs a dictionary with the variable name as the key and the value to replace it with as the value. In this case, we are replacing {country} with "India"
print(prompt2.format(country="India")) # format is similar to invoke but it returns a string instead of a PromptValue object. It also takes the same dictionary as input. In this case, we are replacing {country} with "India"

model_response1 = model.invoke(prompt2.invoke({"country":"India"})) #invoke the model with the prompt1

print(model_response1.content) # Print the content of the model's response