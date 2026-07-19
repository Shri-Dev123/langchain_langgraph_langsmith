from langchain_core.prompts import ChatPromptTemplate

# way 1: create a chat prompt template using the ChatPromptTemplate class
chat_prompt1 = ChatPromptTemplate(
  messages=[
    ("system", "You are a helpful assistant that always replies in {language}"),
    ("human", "write a poem about {topic}"),
    ("ai", "I can help you with that!")
  ],
  input_variables=["language", "topic"]
)

# way 2: create a chat prompt template using the from_messages method (Recommended way)
chat_prompt2 = ChatPromptTemplate.from_messages([
  ("system", "You are a helpful assistant that always replies in {language}"),
  ("human", "write a poem about {topic}"),
  ("ai", "I can help you with that!")
])

actual_prompt2 = chat_prompt2.invoke({
  "language": "English",
  "topic": "Nature"
  })

print(actual_prompt2.to_string()) # This will print the actual prompt with the input variables replaced with the values provided in the invoke method. 
#In this case, it will print "You are a helpful assistant that always replies in English" and "write a poem about Nature" 