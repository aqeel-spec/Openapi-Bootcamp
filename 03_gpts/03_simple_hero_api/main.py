from sqlmodel import Field, SQLModel, create_engine, Session , select
from fastapi import FastAPI
from dotenv import load_dotenv, find_dotenv
from os import getenv

from typing import Optional

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None

_ : bool = load_dotenv(find_dotenv())
connection_str = getenv("POSTGRES_URL")

if not connection_str:
    raise ValueError("POSTGRES_URL environment variable is not set")

engine = create_engine(connection_str, echo=True)


# initialize app
app : FastAPI = FastAPI(
    title="Simple Hero API",
    description="A simple hero API",
    version="1.0.0",
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        }
    ]
)

# creat db and tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# add hero to database
@app.post("/heroes/")
def add_hero(hero: Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero

# get all heroes
@app.get("/heroes/")
def get_all_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes
    