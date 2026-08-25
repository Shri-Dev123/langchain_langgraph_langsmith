from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command

class GraphState(TypedDict):
  temperature: int
  status_message: str
  warning_sent: bool
  final_action_performed:str

def check_temp_node(state:GraphState)->Command[Literal["warn_user","success"]]:
  temp = state["temperature"]

  if temp > 90:
    print("---- Alert: Temp too hight! Issuing command to warn user---")

    return Command( # this is what the Command which navigates to the next node on the basis of condtion
      update = {
        "status_message":"Routing to warning handler...",
      },
      goto = "warn_user"
    )
  else:
    print("----OK Temp is ok, Issuing command to route to 'success'...----")
    return Command(
    update = {
        "status_message":"Routing to success handler...",
    },
      goto="success"
    )

def warn_user(state:GraphState):
  print(f"Executing 'warn_user': Warning successfully sent at {state['temperature']}")

  return {
    "warning_sent":True,
    "final_action_performed":"warning notification sent"
  }

def success(state:GraphState):
  print(f"Executing 'success_user': All systems clear")

  return {
    "final_execution_performed":"Temperature Safety Confirmed",
    "final_action_performed":"warning notification sent"
  }

builder = StateGraph(GraphState)

builder.add_node(check_temp_node)
builder.add_node(warn_user)
builder.add_node(success)

builder.add_edge(START,"check_temp_node") # on the basis of Command() condtionally we deside the further edge so END and all is not needed here

graph = builder.compile()

''' Test the graph'''

initial_state = {
  "temperature":90
}

final_state = graph.invoke(initial_state)

print("final state")
print(final_state)

