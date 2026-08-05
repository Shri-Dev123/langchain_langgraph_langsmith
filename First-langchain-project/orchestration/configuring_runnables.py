from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableConfig
from langchain_core.tracers.schemas import Run

import os
from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file

model = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=os.environ.get("MY_CUSTOM_KEY_VARIABLE"))

prompt = ChatPromptTemplate.from_template("Write a short, consise sentence about {topic}.")

output_parser = StrOutputParser()

base_chain = prompt | model | output_parser # This creates a simple chain using LCEL (|) that takes a topic as input, generates a prompt, sends it to the model for completion, and then parses the output as a string. 


def my_listners_on_start(run: Run):
    """Logs when a run starts."""
    print(f"Run started with ID: {run.id} and name: {run.name}")
    print(f"Run inputs: {run.inputs}")
    print(f"Parent run ID: {run.parent_run_id}")
    print(f"Run tags: {run.tags}")
    print(f"Run extra metadata: {run.extra.get('metadata')}")

chain_with_listeners = base_chain.with_listeners(
    on_start=my_listners_on_start
)

my_runnable_configuration = RunnableConfig(
    run_name="Configuration Demo",
    tags=["single_run_tag", "demo_invoke"],
    metadata={
        "user_id": "12345",
        "source": "manual_test",
        "input_topic_type":"history"
    }
)

print("--------Demo1: Per-invocation configuration---------")

per_invoke_result = chain_with_listeners.invoke(
    {"topic": "the great wall of china"},
    config=my_runnable_configuration         # Passing the configuration to the invoke method 
)

print(f"Per-invocation configuration result: {per_invoke_result}")



# Demo 2: Persistent configuration

my_persistent_configuration = RunnableConfig(
    run_name="Persistent Configuration Demo",
    tags=["persistent", "demo2_invoke"],
    metadata={
        "user_id": "56789",
        "source": "manual_test",
        "input_topic_type":"animals"
    }
)

persistent_run = chain_with_listeners.with_config(my_persistent_configuration) # Applying the configuration to the runnable

print("--------Demo2: Persistent configuration---------")
persistent_result = persistent_run.invoke({"topic": "the blue whale"}) # This invocation will use the persistent configuration set above
print(f"Persistent configuration result: {persistent_result}")