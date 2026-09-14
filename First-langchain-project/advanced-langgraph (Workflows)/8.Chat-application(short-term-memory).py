from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-5.6",api_key=os.getenv("MY_CUSTOM_KEY_VARIABLE"))

def chatbot(state:MessagesState):

  response = llm.invoke(state["messages"])

  return {
    "messages":[response]
  }

builder = StateGraph(MessagesState)

builder.add_node(chatbot)

builder.add_edge(START,"chatbot")
builder.add_edge("chatbot",END)

checkPointer = MemorySaver()

graph = builder.compile(checkpointer=checkPointer) # it will remember the last chat and information 
#graph = builder.compile() # it is normal graph without memory

config = {
  "configurable":{
    "thread_id":"chat_session_1"
  }
}

#turn 1
message_1 = "Hi, My name is Mohit, I am a fullstack developer"

input_1 = {
  "messages": [HumanMessage(content=message_1)]
}


result_1 = graph.invoke(input_1, config=config)

print(f"User:{message_1}")
print(f"AI: {result_1['messages'][-1].content}")


#turn 2
message_2 = "Who i am?"

input_2 = {
  "messages": [HumanMessage(content=message_2)]
}


result_2 = graph.invoke(input_2, config=config)

print(f"User:{message_2}")
print(f"AI: {result_2['messages'][-1].content}")
