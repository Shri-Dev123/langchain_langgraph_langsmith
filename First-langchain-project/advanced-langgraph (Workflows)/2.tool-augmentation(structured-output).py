from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List
import json
import os
from dotenv import load_dotenv
load_dotenv()

class ProductReview(BaseModel):
  product_name: str = Field(description="it will be the name of the product")
  sentiment: str = Field(description="it will be the sentiment of the review possitive, negative or neutral")
  rating: float = Field(description="it will be the rating provided for the product",le=5,ge=1)
  pros: str = Field(description="it will be the pros of the product")
  cons: str = Field(description="it will be the cons of the product")
  summary: str = Field(description="it will be the overall summary of the product")

llm = ChatOpenAI(model="gpt-5.6", api_key=os.getenv("MY_CUSTOM_KEY_VARIABLE"))

llm_with_structure_output = llm.with_structured_output(ProductReview)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a product review analyzer. You will be provided with a product review and you need to analyze it and provide the output in a structured format as per the ProductReview model."),
    ("user", "{input}")
])


chain = prompt_template | llm_with_structure_output

prompt = "The product is great. It has a sleek design and performs well. However, the battery life could be better. Overall, I am satisfied with my purchase."
chain_result = chain.invoke({"input": prompt})
print(json.dumps(chain_result.model_dump(), indent=4)) 

