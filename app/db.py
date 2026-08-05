from collections.abc import AsyncGenerator
import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime, timezone

# An ORM (Object Relational Model) is like a translator that lets you talk to a database using Python instead of SQL.

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

class Base(DeclarativeBase):
    pass

class Post(Base): #inherits from the declarative base data model
    __tablename__ = "post"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) # primarykey = True tell sqlalchemy that this column is unique and it must use this column for identification purpose.
    caption = Column(Text) #create a column which holds 'text' datatype only
    url = Column(String, nullable=False) #nullable decides whether that that coloumn can be left empty or it is mandatory to fill it
    file_type = Column(String, nullable=False) 
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    # putting () to utcnow will result in calling the function once and storing a default, fixed "return value" which came by calling it 
    # while using utcnow w/o the () will store the "function" as its default and not the return value

engine = create_async_engine(DATABASE_URL) #make the road which connects your app to the database
async_sessionmaker = async_sessionmaker(engine, expire_on_commit=False) 
# make the session factory. expire_on_commit=False tells SQLAlchemy: "After saving changes, or commit() keep the loaded objects in the session's memory instead of forgetting them so that we dont 
# have to go all the way back to the database to fetch the details freshly when asked"

async def create_db_and_tables():
    async with engine.begin() as conn: # this line says: "I will send a car to the database". conn is the vehicle or delivery guy who goes to the database to make the request
        # async with says, "Borrow this async resource, use it, and automatically clean it up afterward." i.e I'll rent the car, use it, and retur it back
        await conn.run_sync(Base.metadata.create_all) #await means pause here until this task finishes.". run_sync because create.all is not async. create.all creates every table that doesn't already exist.
        # this whole line means "Go through your notebook (metadata) and create every table you know about"
        # w/o await we get back a 'promise' (called a coroutine) not the actuall thing, and a TypeError or a RuntimeWarninglater when we try to perform some action on it

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_sessionmaker() as session:  #Session = The waiter who takes customer order.
        yield session # return will give the session and dust its hands off, but yield will give fastapi the session and pause there until the request is completed and will ask python to resume from after it"

''' My App
    │
    ▼
 Engine (road)
    │
    ▼
Connection (car)
    │
    ▼
Restaurant (database)
    │
    ▼
Session (waiter)'''

'''async def = "I'm willing to wait for my food." or "This function is capable of pausing while waiting, so the event loop may run other tasks during those pauses."
await = "I'll wait until my pizza arrives." or "Pause here until this finishes."
async with = "I'll borrow a table, and when I'm done, 
the waiter will automatically clear the table." or "I'll open this resource for you now, and I'll make sure it's properly closed when you're finished using it."'''

''' class User(Base):
    posts = relationship("Post")
here posts is just a variable name
relationship is a SQLAlchemy function that creates a relationship.
Post is the model name or the type of object this relationship points to. 
HOW DOES SQLALCHEMY KNOW WHICH TABLE TO FETCH THE OBJECTS FROM?
it knows cuz every model class (name) points to a table name so, whenever someone says Post, they mean the posts table.'''