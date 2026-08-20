from typing import Annotated,List,TypedDict
from langgraph.graph import StateGraph, START, END

from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-5.6", api_key=os.environ.get("MY_CUSTOM_KEY_VARIABLE"))

class AgentState(TypedDict):
  messages:Annotated[List[BaseMessage], add_messages]


def chat_node(state:AgentState)->dict:
  conversation_history = state["messages"]
  response = llm.invoke(conversation_history)
  return {
    "messages":response
  }

graph = StateGraph(AgentState)

graph.add_node("chat_node",chat_node)
graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)

agent = graph.compile()

# Turn 1

message1 = HumanMessage(content="Helo, my name is mohit")

turn1_state = agent.invoke({
  "messages":message1
})

print("-----Graph after first run------")
print(turn1_state)
print("-"*30)

# Turn 2 

message2 = HumanMessage(content="what is your favourite color?")

turn2_state = agent.invoke({
  "messages":turn1_state["messages"]+[message2]
})

print("-----Graph after Second run------")
print(turn2_state)
print("-"*30)



