from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file

model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=os.environ.get("MY_CUSTOM_KEY_VARIABLE"))

prompt = ChatPromptTemplate.from_template("Write a short, consise sentence about {topic}.")

output_parser = StrOutputParser()

simple_chain = prompt | model | output_parser # This creates a simple chain using LCEL (|) that takes a topic as input, generates a prompt, sends it to the model for completion, and then parses the output as a string.

result = simple_chain.invoke({"topic": "LangChain"})
print(result)


# Demo 2 - Chain to a runnable

combined_chain = simple_chain |(lambda chain_output: chain_output + " This is a great tool for building applications with LLMs.") # This creates a combined chain that takes the output of the simple_chain and appends a sentence to it.
combined_chain_result = combined_chain.invoke({"topic": "Model Context Protocol"})
print(combined_chain_result)


# Demo 3 - Chain to Chain

fact_checking_prompt = ChatPromptTemplate.from_messages([
    ("system", "Start by quoting the statement, then give the reason"),
    ("user", "How correct is this statement: {statement}")
])

checker_chain = fact_checking_prompt | model | output_parser # This creates a chain that takes a statement as input, generates a prompt for fact-checking, sends it to the model for completion, and then parses the output as a string.

fact_checking_chain = {
  "statement":simple_chain,
} | checker_chain 

dual_chain_result = fact_checking_chain.invoke({"topic":"Functional Programming"})
print("=="*50)
print(dual_chain_result)

