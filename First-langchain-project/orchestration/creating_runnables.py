from langchain_core.runnables import RunnableLambda
import asyncio

# Demo 1 - Lambda function as Runnable

runnable_multiply = RunnableLambda(lambda x: x * 10) # Define a RunnableLambda that multiplies the input by 10

invoked_result = runnable_multiply.invoke(5) # Invoke the RunnableLambda with an input of 5
print(f"Result: {invoked_result}")

batched_inputs = [1, 2, 3, 4, 5]
batched_results = runnable_multiply.batch(batched_inputs)
print(f"Batched Results: {batched_results}")


# Demo 2 - Regular function as Runnable

def reverse_text_function(text: str) -> str:
    return text[::-1]  # Reverse the input string

runnable_reverse = RunnableLambda(reverse_text_function)

invoked_text_result = runnable_reverse.invoke("Hello, World!")
print(f"reversed Result: {invoked_text_result}")

batched_text_inputs = ["Hello", "World", "LangChain"]
batched_text_results = runnable_reverse.batch(batched_text_inputs)

for result in batched_text_results:
    print(f"Batched Reversed Result: {result}")


# asynchronous invocation

batch_async_inputs = ["Async Hello", "Async World", "Async LangChain"]

async def run_asynhronous():
    aresult  = await runnable_reverse.ainvoke("Asynchronous call") # ainvoke the RunnableLambda asynchronously
    abatched_results = await runnable_reverse.abatch(batch_async_inputs) # abatch the RunnableLambda asynchronously
    print(f"Asynchronous Result: {aresult}")
    print(f"Asynchronous Batch Results: {abatched_results}")

asyncio.run(run_asynhronous())