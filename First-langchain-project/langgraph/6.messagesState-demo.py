from typing import Annotated,List,TypedDict
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import HumanMessage, AIMessage

class MyGraphState(MessagesState):
  turn_count: int

def user_node(state:MyGraphState)->dict:
  print("Executing 'user_node'...")
  return {
    "messages":HumanMessage(content="What is the weather like today?")
  }

def ai_node(state:MyGraphState)->dict:
  print("Executing 'ai_node'....")

  last_message = state["messages"][-1].content
  print(f"Human prompt: {last_message}")

  response_content = f"I have recieved your message {last_message}, however I am a fake response can't response. \n But atleast my code is working"
  return {
    "messages":AIMessage(content=response_content)
  }

def counter_node(state:MyGraphState):
  print("Executing 'counter_node'....")
  return {
    "turn_count": state["turn_count"] + 1
  }



graph = StateGraph(MyGraphState)

graph.add_node(user_node)
graph.add_node(ai_node)
graph.add_node(counter_node)

graph.add_edge(START,"user_node")
graph.add_edge("user_node","ai_node")
graph.add_edge("ai_node","counter_node")
graph.add_edge("counter_node",END)


agent = graph.compile()

initial_state = {
  "turn_count":0
  
}

final_state = agent.invoke(initial_state)

print("---final state----")
print(final_state)

# in this above example we are using MessagesState so that we cannot define the TypedDict state and add Annotated message with add_messages reducer because
# MessagesState already contains:
#     List of messages
#     +
#     add_messages reducer