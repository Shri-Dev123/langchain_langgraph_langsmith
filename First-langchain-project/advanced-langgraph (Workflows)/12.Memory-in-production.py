from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver


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


# 4. PRODUCTION CHECKPOINTER - POSTGRESQL
DB_URI = "postgresql://user:password@localhost:5432/mydb"

with PostgresSaver.from_conn_string(DB_URI) as checkpointer:

    # Run when setting up the checkpoint database
    checkpointer.setup()

    graph = builder.compile(
        checkpointer=checkpointer
    )


    # 5. THREAD CONFIG
    config = {
        "configurable": {
            "thread_id": "user-123"
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

    print("Result:", result)


    # 7. RETRIEVE SAVED STATE
    snapshot = graph.get_state(config)

    print("Saved State:", snapshot.values)


    # 8. RETRIEVE CHECKPOINT HISTORY
    for snapshot in graph.get_state_history(config):
        print("State:", snapshot.values)
        print("Next:", snapshot.next)