# creating a typed ditionary using typeddict from typing module.

from typing import TypedDict,NotRequired, ReadOnly, Required

class Address(TypedDict):
    city: str
    state: str
    postal_code: int
    country: str

class User(TypedDict):
    id:ReadOnly[int] # this is the Read only property user cannot update or change the value
    name: Required[str] # thi is the Required property user must add this in the dictionary
    age: int
    email: str
    addres: NotRequired[Address] # this is the not Required property user can skip to add this property in the dictionary

# ✅ CORRECT: Declared at module level, OUTSIDE the class block
user: User = {
    "id":1,
    "name": "shrikant",
    "age": "alsdf",# this is giving warning becuase in the User class age is assigned integer type and we are passing string here
    "emails":"kalshettysrikant@gmail.com" # this will give warning because we have used the wrong key as emails not email
  }   