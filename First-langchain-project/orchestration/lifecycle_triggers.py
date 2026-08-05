from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tracers.schemas import Run
import os
from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file

model = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=os.environ.get("MY_CUSTOM_KEY_VARIABLE"))

prompt = ChatPromptTemplate.from_template("Write a short, consise sentence about {topic}.")

fact_chain = prompt | model | StrOutputParser() # This creates a simple chain using LCEL (|) that takes a topic as input, generates a prompt, sends it to the model for completion, and then parses the output as a string.

def my_listners_on_start(run: Run):
    """Logs when a run starts."""
    print(f"Run started with ID: {run.id} and name: {run.name}")
    print(f"Run inputs: {run.inputs}")
    print(f"Parent run ID: {run.parent_run_id}")
    print(f"Run tags: {run.tags}")
    print(f"Run extra metadata: {run.extra.get('metadata')}")

def my_listners_on_end(run: Run):
    """Logs when a run ends."""
    print(f"Run ended with ID: {run.id} and name: {run.name}")
    print(f"Run outputs: {type(run.outputs).__name__}, Ouput value: {run.outputs}")
    print(f"Parent run ID: {run.parent_run_id}")
    print(f"Run tags: {run.tags}")
    print(f"Run extra metadata: {run.extra.get('metadata')}")

fact_chain_with_listeners = fact_chain.with_listeners(
    on_start=my_listners_on_start,
    on_end=my_listners_on_end
)

result = fact_chain_with_listeners.invoke({"topic": "the eiffel tower"})

print("=="*50)
print(result)
