from fastapi import FastAPI, HTTPException, File, UploadFile, Depends, Form, Query
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
from app.img_vid import upload_to_imagekit 

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

from contextlib import asynccontextmanager

app = FastAPI(lifespan=lifespan)

@app.post("/upload")
async def upload_post(
    file: UploadFile = File(...), # ... means, required. file is just a variable which is has type "UploadFile" and it must look for it or get it from File, check line 62 till 72
    caption: str = Form(""), 
    session: AsyncSession = Depends(get_async_session) 
    # get_sync_session is a function. but we dont add () to it else the func will get called immedietely when the app starts 
    # so instead it hands the function to fastapi to call it only when the /upload request arrives
    # Depends(...) says: "Before running my function, please go get this thing for me.
    # AsyncSession tells python that session (which is simply a variable is a database session)
):
    file_bytes = await file.read()
    file_name = file.filename
    try:
        upload_result = upload_to_imagekit(file_bytes=file_bytes, file_name=file_name)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    post = Post(
        caption=caption,
        url=upload_result["url"],
        file_type=upload_result["file_type"],
        file_name=upload_result["file_name"],
    )
    session.add(post) # fill the form (post) and give it to the librarian
    await session.commit() # the librarian keeps it in the rack (stores it in the db)
    await session.refresh(post) # metadata is added to the form (like id)
    return post # the form with all the new details is presented (to show the user that their post has been posted)

@app.get("/feed") # One endpoint maps to one function. like one postman can ring only one doorbell
async def get_feed(
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = result.scalars().all()

    posts_data = []
    for post in posts:
        posts_data.append({
            "id": str(post.id), # all this converting is bcuz JSON natively supports numbers (both integers and decimals) and strings 
            # (text in double quotes) as fundamental data types, but it cannot directly contain raw files or binary data.
            # JSON also natively supports booleans (true, false), null, arrays ([]), and objects ({}).
            "caption": post.caption,
            "url": post.url,
            "file_type": post.file_type,
            "file_name": post.file_name,
            "created_at": post.created_at.isoformat()
            # isoformat converts ambiguous dates (like 05/08/2026) into a strict, standard sequence (2026-08-05T14:30:00Z) that machines can universally understand and sort.
        })
    return {"posts": posts_data}

@app.delete("/post")
async def delete_post(caption: str = Query(..., min_length=1), session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Post).where(Post.caption == caption))
    posts = result.scalars().all()
    if not posts:
        raise HTTPException(status_code=404, detail="post not found")

    for post in posts:
        await session.delete(post)

    await session.commit()
    return {"detail": f"Deleted {len(posts)} post(s) with caption '{caption}'"}

''' text_posts = {
     1: {"title": "what was your pet name?", "content": "Bitz"},
     2: {"title": "fav shakespearen diss?", "content": "lady doth protest too much, me thinking"},
     3: {"title": "introduce yourself", "content": "its brittny bitch"},
     4: {"title": "who is your fav actor?", "content": "Nick Robynson and Belmont Cameli"},
     5: {"title": "which college do you study in?", "content": "SIT-Sunday Institute of technology"},
     6: {"title": "current book?", "content": "everything, everything"}
 }

 @app.get("/posts")
 def get_all_posts(limit: int = None): # by making int = None, we are making it NOT-mandatory to enter the limit
     if limit: # if limit is non zero then:👇 else, if no limit is entered then return everything
         return list(text_posts.values())[:limit] #[:limit] is an index so no dot (.) is used
     return text_posts;

 @app.get("/post/{id}")
 def get_post(id: int):
     if id not in text_posts:
         raise HTTPException(status_code=404, detail="post not found") # raise - stop everything and throw an error
     return text_posts.get(id)

 @app.post("/posts")
 def create_post(post: PostCreate):
     text_posts[max(text_posts.keys())+1] = post
     return post

 @app.delete("/post/{id}")
 def delete_post(id: int):
     deleted_post = text_posts.pop(id, None)
     if deleted_post is None:
         raise HTTPException(status_code=404, detail="post not found")
     return f"message with title'{deleted_post.get('title')}' has been deleted"
  to access anything in is dictionary use .get("smtg") and not .smtg like title
file: UploadFile = File(...)

UploadFile
Means:
"I expect a file object."

File(...)
Means:
"Find this value in the uploaded files."
'''