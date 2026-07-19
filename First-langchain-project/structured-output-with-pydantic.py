from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(
  model="gpt-5.6",
  api_key=os.environ.get("MY_CUSTOM_KEY_VARIABLE"),
  temperature=0,
  )


class PresidentInfo(BaseModel):
    '''Details about the president'''
    name: str = Field(description="The name of the president")
    country: str = Field(description="The country of the president")
    age: Optional[int] = Field(default=None, description="The age of the president")

structured_llm = model.with_structured_output(PresidentInfo)

response = structured_llm.invoke("Who is the president of Nepal?")

print(response)