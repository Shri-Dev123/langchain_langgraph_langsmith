from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

# prompt template properties with string prompt template
prompt_template = PromptTemplate(
  template="What is the capital of {country}?",
  input_types={"country": "str"},
  optional_variables=[],
  validate_template=True,
  input_variables=["country"]
  )

print(prompt_template.template) # This will print the template string "What is the capital of {country}?"
print(prompt_template.template_format) # This will print the template string "What is the capital of {country}?"
print(prompt_template.input_variables) # This will print the list of input variables ["country"]
print(prompt_template.input_types) # This will print the list of input types ["str"]
print(prompt_template.optional_variables) # This will print the list of optional variables []
print(prompt_template.validate_template) # This will print True if the template is valid, False otherwise. In this case, it will print True since the template is valid.


# prompt template properties with chat prompt template

chat_prompt_template = ChatPromptTemplate(
  messages=[
    ("system", "You are a helpful assistant that always replies in {language}"),
    ("human", "write a poem about {topic}"),
    ("ai", "I can help you with that!")
  ],
  input_types={"language": "str", "topic": "str"},
  optional_variables=[],
  validate_template=True,
  input_variables=["language", "topic"]
)