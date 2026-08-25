from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import RetryPolicy
import random

class WeatherState(TypedDict):
  city:str
  temperature:float
  conditions:str


class APIERROR(Exception):
  '''Simulated Error'''
  pass

def fetch_weater(state:WeatherState):
  city = state['city']

  '''Simulate request'''
  if random.random() < 0.7:
    print(f"X - API Call failed for {city}")
    raise APIERROR(f"Weather API Timed out for {city}")

  print(f"Sucessfully fetched weather for {city}")

  temp = round(random.uniform(15,30),1)
  conditions = random.choice(["Sunny","Cloudy","Rainy","Partially Cloudy"])

  return {
    "temperature":temp,
    "conditions":conditions
  }

def format_result(state:WeatherState):
  print(f"\n weather report for {state['city']}")
  print(f"Temperature:{state['temperature']}")
  print(f"conditions: {state['conditions']}")

  return state


builder = StateGraph(WeatherState)

builder.add_node(
  "fetch_weater",
  fetch_weater,
  retry_policy=RetryPolicy(
    max_attempts = 5,
    initial_interval = 1,
    backoff_factor = 2.0,
    max_interval = 10.0,
    jitter = True,
    retry_on = APIERROR
  ))
builder.add_node(format_result)

builder.add_edge(START,"fetch_weater")
builder.add_edge("fetch_weater","format_result")
builder.add_edge("format_result",END)

graph = builder.compile()



'''Test the graph'''

try:
  result = graph.invoke({
    "city":"San Francisco",
    "temperature":0.0,
    "conditions":""
  })

  print(f"\nFinal result: {result}")
except Exception as e:
  print(f"\n All retry attempts exhausted:{e}")





