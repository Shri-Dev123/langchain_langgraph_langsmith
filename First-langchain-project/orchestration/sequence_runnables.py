from langchain_core.runnables import RunnableLambda, RunnableSequence


runnable1 = RunnableLambda(lambda input: input + 5)  # Define a RunnableLambda that adds 5 to the input
runnable2 = RunnableLambda(lambda input: input * 2)  # Define a RunnableLambda that multiplies the input by 2

print("----Using  RunnableSequence class to run the runnables in sequence----")

sequence_1 = RunnableSequence(
  first=runnable1,
  last=runnable2
)
result1 = sequence_1.invoke(10)  # Invoke the RunnableSequence with an input of 10
print(f"Result of sequence_1.invoke(10): {result1}")  # Expected output: (10 + 5) * 2 = 30


print("----Using Pipe() operator to run the runnables in sequence----")


sequence_2 = runnable1.pipe(runnable2)
result2 = sequence_2.invoke(4)  # Invoke the RunnableSequence with an input of 4
print(f"Result of sequence_2.invoke(4): {result2}")  # Expected output: (4 + 5) * 2 = 18



print("----Using LCEL (|) operator to run the runnables in sequence----")

sequence_3 = runnable1 | runnable2
result3 = sequence_3.invoke(8)  # Invoke the RunnableSequence with an input of 8
print(f"Result of sequence_3.invoke(8): {result3}")  # Expected output: (8 + 5) * 2 = 26