from fastapi import FastAPI, HTTPException, File, UploadFile, Depends
from app.schemas import PostCreate
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

from contextlib import asynccontextmanager

app = FastAPI(lifespan=lifespan)


# text_posts = {
#     1: {"title": "what was your pet name?", "content": "Lady Gaga"},
#     2: {"title": "fav shakespearen diss?", "content": "lady doth protest too much, me thinking"},
#     3: {"title": "introduce yourself", "content": "its brittny bitch"},
#     4: {"title": "who is your fav actor?", "content": "Nick Robynson and Belmont Cameli"},
#     5: {"title": "which college do you study in?", "content": "SIT-Sunday Institute of technology"},
#     6: {"title": "current book?", "content": "everything, everything"}
# }

# @app.get("/posts")
# def get_all_posts(limit: int = None): # by making int = None, we are making it NOT-mandatory to enter the limit
#     if limit: # if limit is non zero then:👇 else, if no limit is entered then return everything
#         return list(text_posts.values())[:limit] #[:limit] is an index so no dot (.) is used
#     return text_posts;

# @app.get("/post/{id}")
# def get_post(id: int):
#     if id not in text_posts:
#         raise HTTPException(status_code=404, detail="post not found") # raise - stop everything and throw an error
#     return text_posts.get(id)

# @app.post("/posts")
# def create_post(post: PostCreate):
#     text_posts[max(text_posts.keys())+1] = post
#     return post

# @app.delete("/post/{id}")
# def delete_post(id: int):
#     deleted_post = text_posts.pop(id, None)
#     if deleted_post is None:
#         raise HTTPException(status_code=404, detail="post not found")
#     return f"message with title'{deleted_post.get("title")}' has been deleted" 
#     # to access anything in is dictionary use .get("smtg") and not .smtg or smtg 