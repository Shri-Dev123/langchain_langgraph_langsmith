from langchain_core.prompts import PromptTemplate

# way 1: create a prompt template using the PromptTemplate class
string_prompt1 = PromptTemplate(
  template="What is the capital of {country}?",
  input_variables=["country"]
)

# way 2: create a prompt template using the from_template method (Recommended way)
string_prompt2 = PromptTemplate.from_template("What is the population of {country}?")

actual_prompt2 = string_prompt2.invoke({
  "country": "India"
  })


print(actual_prompt2) # This will print the actual prompt with the input variable replaced with the value provided in the invoke method. In this case, it will print "What is the population of India?"
