from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver


# 1. STATE
class MyState(TypedDict):
    number: int
    message: str


# 2. NODES
def add_number(state: MyState):
    return {
        "number": state["number"] + 10,
        "message": "Added 10"
    }


def double_number(state: MyState):
    return {
        "number": state["number"] * 2,
        "message": "Doubled number"
    }


# 3. BUILD GRAPH
builder = StateGraph(MyState)

builder.add_node("add_number", add_number)
builder.add_node("double_number", double_number)

builder.add_edge(START, "add_number")
builder.add_edge("add_number", "double_number")
builder.add_edge("double_number", END)


# 4. MEMORY / CHECKPOINTER
memory = MemorySaver()

graph = builder.compile(
    checkpointer=memory
)


# 5. THREAD CONFIG
config = {
    "configurable": {
        "thread_id": "user-1"
    }
}


# 6. RUN GRAPH
result = graph.invoke(
    {
        "number": 5,
        "message": "Starting"
    },
    config=config
)

print("FINAL RESULT:")
print(result)


# 7. GET LATEST STATE SNAPSHOT
snapshot = graph.get_state(config)

print("\nLATEST SNAPSHOT:")
print(snapshot.values)

print("NEXT NODE:")
print(snapshot.next)


# 8. GET ALL PREVIOUS SNAPSHOTS
print("\nSTATE HISTORY:")

for snapshot in graph.get_state_history(config):
    print("----------------------")
    print("State:", snapshot.values)
    print("Next:", snapshot.next)
    print("Created:", snapshot.created_at)