from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class GraphState(TypedDict):
  input:str
  execution_path:list[str]

def node_a(state:GraphState)->dict:
  print(f"Executing 'node_a'...")
  new_path = state.get("execution_path",[]) + ["node_a"]
  return {
    "execution_path":new_path
  }


def node_b(state:GraphState)->dict:
  print(f"Executing 'node_b'...")
  new_path = state.get("execution_path",[]) + ["node_b"]
  return {
    "execution_path":new_path
  }


def node_c(state:GraphState)->dict:
  print(f"Executing 'node_c'...")
  new_path = state.get("execution_path",[]) + ["node_c"]
  return {
    "execution_path":new_path
  }

def node_d(state:GraphState)->dict:
  print(f"Executing 'node_d'...")
  new_path = state.get("execution_path",[]) + ["node_d"]
  return {
    "execution_path":new_path
  }

def should_continue(state:GraphState): # Its a routing function which will decide in which node next to go
  print("Evaluating conditional edge")
  if "go_to_c" in state["input"]:
    print("--> continuing to c")
    return "node_c"
  else:
    print("--> continuing to d")
    return "node_d"


builder = StateGraph(GraphState)

builder.add_node(node_a)
builder.add_node(node_b)
builder.add_node(node_c)
builder.add_node(node_d)

builder.add_edge(START,"node_a") # Normal Edge
builder.add_edge("node_a","node_b") # Normal Edge

builder.add_conditional_edges("node_b",should_continue) # Conditional Edge
builder.add_edge("node_c",END) # Normal Edge
builder.add_edge("node_d",END) # Normal Edge

graph = builder.compile()

initial_state_1 = {
  "input":"hello, go_to_c to continue"
}

final_state_1 = graph.invoke(initial_state_1)

print(final_state_1)





