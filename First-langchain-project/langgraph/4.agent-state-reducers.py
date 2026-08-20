from langgraph.graph import StateGraph, START, END
from typing import Annotated,List,TypedDict
from operator import add

# Without reducers
class StateWithoutReducer(TypedDict):
  count:int
  animals:str

def node_to_update(state:StateWithoutReducer)->dict:
  return{
    "count":1,
    "animals":["cat"]
  }

initial_state = {
  "count":5,
  "animals":["lion","buffalo"]
}

def run_example(name:str, state_schema:type, node_func:callable, initial_state:dict):
  """
  Builds and runs a simple graph with a given state schema, node, and initial state
  """
  print(f"---Running Example:{name}---")
  graph = StateGraph(state_schema)
  graph.add_node("update_node",node_func)
  graph.add_edge(START,"update_node")
  graph.add_edge("update_node",END)

  app = graph.compile()

  final_state = app.invoke(initial_state)

  print(f"Initial State:{initial_state}")
  print(f"Final State:{final_state}")
  print(f"-"*40)

run_example(name="No Reducer",state_schema=StateWithoutReducer,node_func=node_to_update,initial_state=initial_state)

# With Reducers
def update_count(current:int, new:int)->int:  # This is the reducer to update the count
  return current + new

class StateWithReducer(TypedDict):
  count:Annotated[int,update_count]
  animals:Annotated[List[str], add] # add acts as a reducer it will combine the list

run_example(name="With Reducer", state_schema=StateWithReducer, node_func=node_to_update,initial_state=initial_state)