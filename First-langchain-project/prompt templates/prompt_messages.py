from langchain_core.messages import HumanMessage

#user_message = HumanMessage(content="What are the ice-cream food categories under FSSAI?")

prompt = [
  # user_message
  ("system","Always reply in {language}"),
  ("human", "write a poem about {topic}")
]

print(prompt)