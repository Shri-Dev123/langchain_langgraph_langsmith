from langchain_core.runnables import RunnableLambda
from typing import Any, Dict
import json
from langchain_core.tracers.schemas import Run

def failing_function(input_dict: Dict[str, Any]) -> str:

    topic = input_dict.get("topic","unknown")
    if "error" in topic.lower():
        raise ValueError("This is a simulated error for demonstration purposes.")
    elif "network" in topic.lower():
        raise ConnectionError("This is a simulated network error for demonstration purposes.")
    elif "json" in topic.lower():
        bad_json = "{ 'invalid_json': True, }"  # This is intentionally malformed JSON
        return json.loads(bad_json)  # This will raise a JSONDecodeError
    else:
        return f"Successfully processed topic: {topic}"

error_runnable = RunnableLambda(failing_function)

def my_listeners_on_error(run: Run):
    """Logs when a run encounters an error."""
    print(f"Run encountered an error with ID: {run.id} and name: {run.name}")
    print(f"Start time: {run.start_time}, End time: {run.end_time}")
    print(f"Run inputs: {run.inputs}")
    print(f"Parent run ID: {run.parent_run_id}")
    print(f"Run tags: {run.tags}")
    print(f"Run extra metadata: {run.extra.get('metadata')}")
    print(f"Error details: {run.error}")
    print(f"Run outputs: {run.outputs}")

    print("===============Error Details===============")
    print(run.error)


error_runnable_with_listeners = error_runnable.with_listeners(
        on_error=my_listeners_on_error
    )

print("______Demo: running error Scenarios with Listeners______")

try:
    result = error_runnable_with_listeners.invoke({"topic": "json error scenario"})
    print(result)
except Exception as e:
    print(f"Caught an exception during invocation: {e}")