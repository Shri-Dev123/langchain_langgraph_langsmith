from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
model = ChatOpenAI(
  model="gpt-5.6",
  api_key=os.environ.get("MY_CUSTOM_KEY_VARIABLE"),
  temperature=0,
  )

president_schema = {
    "name": "president_info_schema",
    "description": "Schema for extracting information about the president of a country",
    "parameters": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "description": "The name of the president",
        },
        "country": {
          "type": "string",
          "description": "The country of the president",
        },
        "age": {
          "type": ["integer", "null"],
          "description": "The age of the president",
        },
      },
      "required": ["name", "country"]

    }
}

structured_llm = model.with_structured_output(president_schema) # with_structured_output is a method that allows you to define a schema
                                                                # for the expected output of the model. In this case, we are defining a 
                                                                # schema for extracting information about the president of a country, including their name, 
                                                                # country, and age. The model will then return structured data that adheres to this schema when 
                                                                # invoked with a prompt.

response = structured_llm.invoke("Who is the president of India?")

print(response)