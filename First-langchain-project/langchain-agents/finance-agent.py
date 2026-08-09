from langchain.agents import create_agent
from langchain.tools import tool
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from dataclasses import dataclass
from langchain.tools import ToolRuntime

from langchain.chat_models import init_chat_model
from langchain.agents.middleware import (
  wrap_model_call,
  dynamic_prompt,
  ModelRequest,
  ModelResponse
)
load_dotenv()

basic_model = init_chat_model(
  "gpt-4o-mini",
  temperature=0.5,
  api_key=os.getenv("MY_CUSTOM_KEY_VARIABLE"),
  max_tokens=512,
)

premium_model = init_chat_model(
  "gpt-4o",
  api_key=os.getenv("MY_CUSTOM_KEY_VARIABLE"),
  max_tokens=2028,
)

platinum_model = init_chat_model(
  "gpt-4o",
  api_key=os.getenv("MY_CUSTOM_KEY_VARIABLE"),

)



model = ChatOpenAI(
  model="gpt-5",  # or another model you have access to
  api_key=os.getenv("MY_CUSTOM_KEY_VARIABLE"),

)

@dataclass
class UserContext:
  user_id:str
  user_name: str
  membership_tier:str # 'basic','premium','platinum'
  preferred_currency: str

USER_DATABASE = {
    "user_001": {
        "name": "Alice Johnson",

        "accounts": {
            "checking": 2500.00,
            "savings": 15000.00,
            "investment": 45000.00
        },

        "transactions": {
            "checking": [
                {
                    "date": "2025-01-03",
                    "description": "Salary Deposit",
                    "amount": 5000.00
                },
                {
                    "date": "2025-01-05",
                    "description": "Grocery Store",
                    "amount": -125.45
                },
                {
                    "date": "2025-01-08",
                    "description": "Electricity Bill",
                    "amount": -89.75
                },
                {
                    "date": "2025-01-12",
                    "description": "Restaurant",
                    "amount": -42.30
                }
            ],

            "savings": [
                {
                    "date": "2025-01-10",
                    "description": "Monthly Savings",
                    "amount": 1000.00
                },
                {
                    "date": "2025-01-15",
                    "description": "Emergency Withdrawal",
                    "amount": -500.00
                },
                {
                    "date": "2025-01-20",
                    "description": "Interest Credit",
                    "amount": 15.50
                }
            ],

            "investment": [
                {
                    "date": "2025-01-04",
                    "description": "Bought ETF Shares",
                    "amount": -1200.00
                },
                {
                    "date": "2025-01-16",
                    "description": "Dividend Received",
                    "amount": 45.75
                }
            ]
        }
    },

    "user_002": {
        "name": "Bob Smith",

        "accounts": {
            "checking": 4200.00,
            "savings": 22000.00,
            "investment": 68000.00
        },

        "transactions": {
            "checking": [
                {
                    "date": "2025-01-02",
                    "description": "Salary Deposit",
                    "amount": 7500.00
                },
                {
                    "date": "2025-01-06",
                    "description": "Rent Payment",
                    "amount": -1800.00
                },
                {
                    "date": "2025-01-09",
                    "description": "Grocery Store",
                    "amount": -245.80
                },
                {
                    "date": "2025-01-14",
                    "description": "Restaurant",
                    "amount": -85.50
                }
            ],

            "savings": [
                {
                    "date": "2025-01-05",
                    "description": "Monthly Savings Deposit",
                    "amount": 1500.00
                },
                {
                    "date": "2025-01-18",
                    "description": "Interest Credit",
                    "amount": 25.75
                },
                {
                    "date": "2025-01-25",
                    "description": "Transfer to Checking",
                    "amount": -1000.00
                }
            ],

            "investment": [
                {
                    "date": "2025-01-03",
                    "description": "Stock Purchase",
                    "amount": -2500.00
                },
                {
                    "date": "2025-01-12",
                    "description": "Dividend Received",
                    "amount": 125.40
                },
                {
                    "date": "2025-01-28",
                    "description": "ETF Purchase",
                    "amount": -1500.00
                }
            ]
        }
    },
}




@tool
def get_account_balance(account_type:str,runtime:ToolRuntime[UserContext])-> str: 
  """get the account balance for a specific account for a user"""

  user_id = runtime.context.user_id
  currency = runtime.context.preferred_currency
  user_data = USER_DATABASE.get(user_id,{})

  balance = user_data.get("accounts",{}).get(account_type.lower())

  if balance is not None:
    if currency == "EUR":
      balance = balance * 0.92
      return f"Your {account_type} account balance is €{balance:,.2f}"
    return f"Your {account_type} account balance is ${balance}"
  return f"Your {account_type}. Available: checking, savings, investment "


@tool
def get_recent_transactions(account_type:str, limit:int =5, runtime: ToolRuntime[UserContext] = None)-> str:
  """getting recent transactions for an account of a user """

  user_id = runtime.context.user_id
  user_data = USER_DATABASE.get(user_id,{})

  account_transactions = user_data.get("transactions",{}).get(account_type.lower(),[])[:limit]

  if not account_transactions:
    return f"No transactions found {account_type}"

  result = f"Recent transactions for {account_type}:\n"

  for t in account_transactions:
    sign = "+" if t["amount"] > 0 else ""
    result += f"{t['date']} : {t['description']} ({sign}${t['amount']:,.2f})\n"

  return result

@tool
def calculate_budget(monthly_income:float, expense_category:str)->str:
  """Calculate the recommended monthly budget for an expense category."""
  allocations = {
    "housing":0.30,
    "food":0.12,
    "transportation":0.10,
    "utilities":0.08,
    "savings":0.20,
    "entertainment":0.05,
    "healthcare":0.05,
    "other":0.10
  }

  percentage = allocations.get(expense_category.lower())
  if percentage is None:
    return f"Unknown category: {expense_category}. Available {', '.join(allocations.keys())}"

  recommended = monthly_income * percentage

  return f"Recommended {expense_category} budget: ${recommended:,.2f}/month ({percentage*100:.0f}% of income)"

@tool
def get_personalized_greeting(runtime:ToolRuntime[UserContext])->str:
  
  """get a personalized greeting for the user"""

  name = runtime.context.user_name
  tier = runtime.context.membership_tier

  tier_benefits = {
    "basic":"You have access to standard features",
    "premium":"As a premium member, you get  priority support and advanced analytics!",
    "platimum":"Welcome, platinum member! You have access to all features including personal advisor consultations."
    }
  benefit_msg = tier_benefits.get(tier,"")
  return f"Hello, {name}! {benefit_msg}"



@wrap_model_call
def dynamic_model_selector(request:ModelRequest, handler) -> ModelResponse:
  """ Selects mdodel based on User's membership tier"""

  tier = request.runtime.context.membership_tier

  if tier == "platinum":
    request.override(model=platinum_model)
    print(f"[Middleware] using PLATINUM model (gpt-4o, limitless)")
  elif tier == "premium":
    request.override(model=premium_model)
    print(f"[Middleware] Using PREMIUM model (gpt-4o, 2048 tokens)")
  else:
    request.override(model=basic_model)
    print(f"[Middleware] using BASIC model (gpt-4o-mini, 512 tokens)")

  return handler(request)

@dynamic_prompt
def tier_based_prompt(request:ModelRequest)-> str:
  """Generate system prompt based on user's membership tier"""
  tier = request.runtime.context.membership_tier
  user_name = request.runtime.context.user_name

  base_prompt = f"""You are a personal finance assistant helping {user_name}.
          Your capabilities:
          - Check account balances (checking, savings, investment)
          - View recent transactions
          - Calculate budget recommendations
          - Provide Personalized greetings
  """

  if tier == "premium":
    return base_prompt + """

    PREMIUM MEMBER BENEFITS:
    - Provide helpful explainations with your responses.
    - offer occassional tips for financial improvement.
    - Be friendly and informative
    - Balance detail with brevity
    """
  elif tier == "platinum":
    return base_prompt + """

    PLATINUM MEMBER BENEFITS:
    - Proide detailed, comprehensive financial analysis
    - Offer proactive suggestions for wealth growth
    - Include market insights when relevant
    - Be thorough and consultative in your responses
    - Take extra time to explain complex concepts
    """

  else: 
    return base_prompt + """

    Guidelines:
    - Be concise and direct
    - Answer questions efficiently
    - Focus on the specific request
    - Keep responses brief but helpful
"""
    


system_prompt = """You are a helpful personal finance assstant.

Your capabilities:
- Check account balances (cheking, savings, investment)
- View recent transactions
- Calculate budget recommendations
- Provide personlized greetings

Guidelines:
- Be helpful and informative
- provide clear, acitionable advice
- Use tools to get accurate information before responding
- Format monetary values clearly
- Tailor advice based on the user's membership tier"""


agent = create_agent(
  model = basic_model,
  tools=[
    get_account_balance,
    get_recent_transactions,
    calculate_budget,
    get_personalized_greeting
  ],
  # system_prompt=system_prompt, # used for single system prompt not dynamic

  context_schema=UserContext,
  middleware=[
    dynamic_model_selector,
    tier_based_prompt
    ] 
)

def main():
  print("="*60)
  print("Stage 1: Simple Finance Assistant")
  print("="*60)

alice_context = UserContext(
    user_id="user_001",
    user_name="Alice Johnson",
    membership_tier="platinum",
    preferred_currency="USD")

bob_context = UserContext(
    user_id="user_002",
    user_name="Bob Smith",
    membership_tier="basic",
    preferred_currency="EUR")

  # # Test 1: Check Balance

  # balance_messaage = "What is my checking account balance"

  # print(f"\nQuery: {balance_messaage}")
  # response = agent.invoke(
  #   {
  #     "messages":[{"role":"user","content":balance_messaage}]
  #   },
  #   context=bob_context
  # )
  # print(f"Agent: {response['messages'][-1].content}")

  # # Test 2: Multi-tool query

  # multi_tool_prompt = "Show me my savings balance and recent transactions"

  # print(f"\nQuery: {multi_tool_prompt}")
  # resonse2 = agent.invoke(
  #   {"messages":[{"role":"user", "content":multi_tool_prompt}]},
  #   context=bob_context
  # )
  # print(f"Agent:{resonse2["messages"][-1].content}")


  # # Test 3: Budget Calculation
  # budget_prompt = "I make $5000/month. How much should I spend on housing"
  # print(f"\nQuery:{budget_prompt}")
  # response3 = agent.invoke(
  #   {"messages":[{"role":"user","content":budget_prompt}]}
  # )
  # print(f"Agent:{response3["messages"][-1].content}")

# Test 4: Financial Situation and advice.

financial_situation_query = "What is my financial situation? check all my accounts and give me advice"

print("\n Same query, different treatment")
print("-"*40)
response = agent.invoke(
  {"messages":[{"role":"user", "content":financial_situation_query}]},
  context=bob_context

  )

print(f"Agent: {response['messages'][-1].content}")


if __name__ == "__main__":
  main()