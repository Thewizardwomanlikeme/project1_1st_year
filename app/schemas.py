from pydantic import BaseModel #BaseModel is like a blueprint for our body content in the API i.e for our post because that is what the body will have

class PostCreate(BaseModel): # PostCreate is a pydantic request schema. It takes the JSON coming from the user and turn it into a PostCreate object after validating the inputs
    title: str
    content: str

'''     USER
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