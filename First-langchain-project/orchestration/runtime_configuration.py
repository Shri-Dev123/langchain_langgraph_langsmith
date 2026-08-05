from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableConfig, ConfigurableField
from langchain_core.tracers.schemas import Run

import os
from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file

model = ChatOpenAI(model_name="gpt-3.5-turbo",  openai_api_key=os.environ.get("MY_CUSTOM_KEY_VARIABLE")).configurable_fields(
  max_tokens=ConfigurableField(
    id="llm_token_cap",
    name="LLM Maximum Response Tokens",
    description="The maximum number of tokens for response."
  )
)

prompt = ChatPromptTemplate.from_template("Write a short, consise sentence about {topic}.")

output_parser = StrOutputParser()

base_chain = prompt | model | output_parser


print("----Invoking with default token limit-----")

result_default = base_chain.invoke({"topic": "the great wall of china"})
print(f"Result with default token limit: {result_default}")


print("----Invoking with custom token limit-----")
result_custom = base_chain.invoke({"topic": "the great wall of china"}, config=RunnableConfig(configurable={"max_tokens": 20}))
print(f"Result with custom token limit: {result_custom}")
