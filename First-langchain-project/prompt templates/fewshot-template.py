from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate

example_formatter = PromptTemplate.from_template("Question:{question}\n {answer}")

example_set = [
  {
    "question":"Tell me about the US",
    "answer":"Continent: North America | President: Donald Trump | Language: English"
  },
  {
    "question":"Tell me about the Spain",
    "answer":"Continent: Europe | Prime Minister: Pedro Sanchez | Language: Spanish"
  },
  {
    "question":"Tell me about the Portugal",
    "answer":"Continent: Europe | President: Marcelo Rebelo de Sousa | Language: Portuguese"
  }
]

few_shot_prompt_template = FewShotPromptTemplate(
  example_prompt=example_formatter,
  examples=example_set,
  suffix="Question:{user_query}"
  )

invoked_template = few_shot_prompt_template.invoke({
  "user_query":"Who build the great wall of china"
})

print(invoked_template)
print(invoked_template.text)