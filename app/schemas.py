from pydantic import BaseModel #BaseModel is like a blueprint for our body content in the API i.e for our post because that is what the body will have

class PostCreate(BaseModel):
    title: str
    content: str