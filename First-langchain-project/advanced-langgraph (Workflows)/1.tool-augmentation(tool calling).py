from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
import os

from dotenv import load_dotenv

load_dotenv()  # Load variables from .env into environment

@tool
def get_weather(city: str) -> str:
    """Get the weather for a city."""
    weather_data = {
        "New York": "Sunny, 72 F",
        "London": "Cloudy, 15 F",
        "Tokyo": "Rainy, 20 C"
    }

    return weather_data.get(
        city,
        "Weather data is not available for the city."
    )

@tool
def calculate_tip(bill_amount: float, tip_percentage: float) -> float:
    """Calculate tip amount based on bill and percentage."""
    return round(bill_amount * (tip_percentage / 100), 2)


llm = ChatOpenAI(
    model="gpt-4o",
    api_key=os.getenv("MY_CUSTOM_KEY_VARIABLE")
)

llm_with_tools = llm.bind_tools([
    get_weather,
    calculate_tip
])

weather_prompt = "What is the weather in Tokyo"
tip_prompt = "Calculate a 20% tip on a $50 bill"

response = llm_with_tools.invoke(weather_prompt)

tool_calls = response.tool_calls

for tool_call in tool_calls:
    if tool_call['name'] == "get_weather":
        result = get_weather.invoke(tool_call['args'])
    elif tool_call['name'] == "calculate_tip":
        result = calculate_tip.invoke(tool_call['args'])
    else:
        result = "No tool found"

print(result)


