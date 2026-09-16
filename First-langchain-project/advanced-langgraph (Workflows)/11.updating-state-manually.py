from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver


# 1. STATE
class MyState(TypedDict):
    number: int
    message: str


# 2. NODES
def add_number(state: MyState):
    print("Executing add_number")

    return {
        "number": state["number"] + 10,
        "message": "Added 10"
    }


def double_number(state: MyState):
    print("Executing double_number")

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


# 4. CHECKPOINTER
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

print("Original Result:")
print(result)


# 7. RETRIEVE CURRENT STATE
snapshot = graph.get_state(config)

print("\nBefore Manual Update:")
print(snapshot.values)


# 8. MANUALLY UPDATE STATE
graph.update_state(
    config,
    {
        "number": 100,
        "message": "Manually updated"
    }
)


# 9. RETRIEVE UPDATED STATE
updated_snapshot = graph.get_state(config)

print("\nAfter Manual Update:")
print(updated_snapshot.values)


# 10. CHECK STATE HISTORY
print("\nCheckpoint History:")

for snapshot in graph.get_state_history(config):
    print("----------------------")
    print("State:", snapshot.values)
    print("Next:", snapshot.next)