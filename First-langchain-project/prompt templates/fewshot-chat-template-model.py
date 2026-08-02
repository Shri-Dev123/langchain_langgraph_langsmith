import os
from dotenv import load_dotenv
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

# Create the LLM
llm = ChatOpenAI(
    model="gpt-5.6",   # or "gpt-5", "gpt-5-mini" if your account has access
    api_key=os.getenv("MY_CUSTOM_KEY_VARIABLE"),
    temperature=0
)

example_formatter = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{output}"),
])

example_set = [
    {
        "input": "2 ribbit 2",
        "output": "4",
    },
    {
        "input": "5 ribbit 2",
        "output": "10",
    },
    {
        "input": "3 ribbit 3",
        "output": "9",
    },
]

few_shot_template = FewShotChatMessagePromptTemplate(
    example_prompt=example_formatter,
    examples=example_set,
)

main_prompt = ChatPromptTemplate.from_messages([
    ("system", "You're a whimsical mathematician."),
    few_shot_template,
    ("human", "{user_prompt}"),
])

# Create the messages
messages = main_prompt.invoke({
    "user_prompt": "3 ribbit 4"
})

formatted_prompt = main_prompt.format(
  user_prompt="6 ribbit 5"
)
# Invoke the model
response = llm.invoke(formatted_prompt)

print(response.content)

# LCEL - LangChain Execution Language

chain = main_prompt | llm  # This creates a chain that first formats the prompt and then invokes the LLM.

response = chain.invoke({
    "user_prompt": "2 ribbit 7"
})

print(response.content)