from dataclasses import dataclass
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.runtime import Runtime

class GraphState(TypedDict):
  input:str
  result:str

@dataclass
class MyGraphContext:
  user_agent:str
  docs_url:str = "https://docs.langchain.com"
  db_connection:str = "mysql://user:password@localhost:3306/my_db"

def context_access_node(state:GraphState, runtime:Runtime[MyGraphContext]):
  print("---Executing Node---")
  db_string = runtime.context.db_connection
  docs_url = runtime.context.docs_url
  user_agent = runtime.context.user_agent

  print(f"Current DB String: {db_string}")
  print(f"Documentation url: {docs_url}")
  print(f"User Agent: {user_agent}")

  return {
    "result":f"context accessed. DB:{db_string.split('//')[0]}..."

  }

builder = StateGraph(GraphState, context_schema=MyGraphContext)

builder.add_node(context_access_node)
builder.add_edge(START, "context_access_node")
builder.add_edge("context_access_node",END)

graph = builder.compile()

initial_state = {
  "input":"Start process"
}

final_state = graph.invoke(
  input=initial_state,
  context={
    "user_agent":"default-paltform",
    "db_connection":"postgress://new_user@remote_host:5432/" # Here we are chaging the context in db_connection from mysql to postgres
 })

print("final State")
print(final_state)