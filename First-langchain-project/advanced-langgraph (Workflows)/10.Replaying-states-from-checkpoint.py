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


# 6. FIRST EXECUTION
result = graph.invoke(
    {
        "number": 5,
        "message": "Starting"
    },
    config=config
)

print("\nFinal Result:")
print(result)


# 7. RETRIEVE CHECKPOINT HISTORY
history = list(
    graph.get_state_history(config)
)

for i, snapshot in enumerate(history):
    print("\nCheckpoint:", i)
    print("State:", snapshot.values)
    print("Next:", snapshot.next)


# 8. SELECT A PREVIOUS CHECKPOINT
checkpoint = history[1]

print("\nSelected Checkpoint:")
print(checkpoint.values)
print("Next:", checkpoint.next)


# 9. REPLAY FROM THAT CHECKPOINT
replayed_result = graph.invoke(
    None,
    config=checkpoint.config
)

print("\nReplayed Result:")
print(replayed_result)