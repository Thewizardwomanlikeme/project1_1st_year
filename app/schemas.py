from pydantic import BaseModel, Field #BaseModel is like a blueprint for our body content in the API i.e for our post because that is what the body will have

class PostCreate(BaseModel): # PostCreate is a pydantic request schema. It takes the JSON coming from the user and turn it into a PostCreate object after validating the inputs
    title: str = Field(..., min_length=1, pattern=r"^[A-Za-z0-9 ]+$") 

'''
pattern=r"^[A-Za-z0-9 ]+$" is a regular expression (regex) pattern.
^
Start of the string

[ and ]
Define a character set

A-Za-z
Any uppercase or lowercase letter

0-9
Any digit

 
A space

+
One or more of the allowed characters

$
End of the string'''

'''    USER
          ↓
       JSON
          ↓
   ┌──────────────┐
   │Pydantic Model│
   │   PostCreate │
   └──────┬───────┘
          ↓
      validation
          ↓
   ┌──────────────┐
   │SQLAlchemy ORM│
   │     Post     │
   └──────┬───────┘
          ↓
       DATABASE'''