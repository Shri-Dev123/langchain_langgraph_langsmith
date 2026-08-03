from langchain_core.runnables import RunnableLambda, RunnableParallel

runnable1 = RunnableLambda(lambda input: str(input).upper()) # This runnable takes an input and converts it to uppercase.
runnable2 = RunnableLambda(lambda input: str(input).lower()) # This runnable takes an input and converts it to lowercase.

# Demo 1 - with passing the Dictnioary
parallel_1 = RunnableParallel({
    "uppercase": runnable1,
    "lowercase": runnable2
})

result_1 = parallel_1.invoke("Wonder Woman") # This will run both runnables in parallel and return a dictionary with the results. 
print(result_1) # Output: {'uppercase': 'WONDER WOMAN', 'lowercase': 'wonder woman'}

# Demo 2 - with keyword arguments

parallel_2 = RunnableParallel(
  first=runnable1,
  second=runnable2
)
result_2 = parallel_2.invoke("Batman") # This will run both runnables in parallel and return a dictionary with the results.
print(result_2) # Output: {'first': 'BATMAN', 'second': 'batman'}


# Demo  3 - LCEL

parallel_3 = parallel_1 | (lambda input: input["uppercase"]+" "+input["lowercase"]) # This will run both runnables in parallel and then concatenate the results.
result_3 = parallel_3.invoke("Superman") # This will run both runnables in parallel and then concatenate the results.
print(result_3) # Output: 'SUPERMAN superman'
