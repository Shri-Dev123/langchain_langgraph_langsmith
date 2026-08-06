from langchain.agents import create_agent
from langchain.tools import tool
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

model = ChatOpenAI(
  model="gpt-5",  # or another model you have access to
  api_key=os.getenv("MY_CUSTOM_KEY_VARIABLE"),

)

@tool
def get_account_balance(account_type:str)-> str: 
  """Return the most recent transactions for an account."""

  balances = {
    "checking": 2500.00,
    "savings":1500.00,
    "investment":45000.00
  }

  balance = balances.get(account_type.lower())
  if balance is not None:
    return f"Your {account_type} account balance is ${balance:,.2f}"
  return f"Unknown account type:{account_type}. Available: checking, savings, and investment"

@tool
def get_recent_transactions(account_type:str, limit:int =5)-> str:
  """getting recent transactions"""
  transactions = {
    "checking": [
        {
            "date": "2025-01-03",
            "description": "Salary Deposit",
            "amount": 5000.00,
        },
        {
            "date": "2025-01-05",
            "description": "Grocery Store",
            "amount": -125.45,
        },
        {
            "date": "2025-01-08",
            "description": "Electricity Bill",
            "amount": -89.75,
        },
        {
            "date": "2025-01-12",
            "description": "Restaurant",
            "amount": -42.30,
        },
        {
            "date": "2025-01-18",
            "description": "Freelance Payment",
            "amount": 850.00,
        },
        {
            "date": "2025-01-25",
            "description": "ATM Withdrawal",
            "amount": -200.00,
        },
    ],
    "savings": [
        {
            "date": "2025-01-01",
            "description": "Opening Balance",
            "amount": 10000.00,
        },
        {
            "date": "2025-01-10",
            "description": "Transfer from Checking",
            "amount": 1000.00,
        },
        {
            "date": "2025-01-15",
            "description": "Emergency Fund Withdrawal",
            "amount": -500.00,
        },
        {
            "date": "2025-01-20",
            "description": "Interest Credit",
            "amount": 15.50,
        },
        {
            "date": "2025-01-28",
            "description": "Monthly Savings Deposit",
            "amount": 750.00,
        },
    ],
    "investment": [
        {
            "date": "2025-01-04",
            "description": "Initial Investment",
            "amount": 3000.00,
        },
        {
            "date": "2025-01-09",
            "description": "Bought ETF Shares",
            "amount": -1200.00,
        },
        {
            "date": "2025-01-16",
            "description": "Dividend Received",
            "amount": 45.75,
        },
        {
            "date": "2025-01-22",
            "description": "Bought Tech Stocks",
            "amount": -800.00,
        },
        {
            "date": "2025-01-30",
            "description": "Investment Gain",
            "amount": 220.00,
        },
    ],
}

  account_transactions = transactions.get(account_type.lower(),[])[:limit]

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

system_prompt = """You are a helpful personal finance assstant.

Your capabilities:
- Check account balances (cheking, savings, investment)
- View recent transactions
- Calculate budget recommendations

Guidelines:
- Be helpful and informative
- provide clear, acitionable advice
- Use tools to get accurate information before responding
- Format monetary values clearly"""


agent = create_agent(
  model = model,
  tools=[
    get_account_balance,
    get_recent_transactions,
    calculate_budget
  ],
  system_prompt=system_prompt
)

def main():
  print("="*60)
  print("Stage 1: Simple Finance Assistant")
  print("="*60)

  # Test 1: Check Balance

  balance_messaage = "What is my checking account balance"

  print(f"\nQuery: {balance_messaage}")
  response = agent.invoke(
    {
      "messages":[{"role":"user","content":balance_messaage}]
    }
  )
  print(f"Agent: {response['messages'][-1].content}")

  # Test 2: Multi-tool query

  multi_tool_prompt = "Show me my savings balance and recent transactions"

  print(f"\nQuery: {multi_tool_prompt}")
  resonse2 = agent.invoke(
    {"messages":[{"role":"user", "content":multi_tool_prompt}]}
  )
  print(f"Agent:{resonse2["messages"][-1].content}")


  # Test 3: Budget Calculation
  budget_prompt = "I make $5000/month. How much should I spend on housing"
  print(f"\nQuery:{budget_prompt}")
  response3 = agent.invoke(
    {"messages":[{"role":"user","content":budget_prompt}]}
  )
  print(f"Agent:{response3["messages"][-1].content}")


if __name__ == "__main__":
  main()