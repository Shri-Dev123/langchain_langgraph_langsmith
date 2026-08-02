from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

example_formatter =ChatPromptTemplate.from_messages([
  ("human","{input}"),
  ("ai","{output}"),
])

example_set = [
  {
    "input":"2 ribbit 2",
    "output":"4"
  },
  {
    "input":"5 ribbit 2",
    "output":"10"
  },
  {
    "input":"3 ribbit 3",
    "output":"9"
  }
]

few_shot_template = FewShotChatMessagePromptTemplate(
  example_prompt=example_formatter,
  examples=example_set
)

main_prompt = ChatPromptTemplate.from_messages([
  ("system","You're a whimsical mahematician"),
  few_shot_template,
  ("human","{user_prompt}")
])

invoked_prompt = main_prompt.invoke({
  "user_prompt":"3 ribbit 4"
})

print(invoked_prompt)
print(invoked_prompt.to_string())
