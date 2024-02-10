from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Session 
from dotenv import load_dotenv, find_dotenv
from os import getenv

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None

hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

_ : bool = load_dotenv(find_dotenv())
connection_str = getenv("POSTGRES_URL")

if not connection_str:
    raise ValueError("POSTGRES_URL environment variable is not set")

engine = create_engine(connection_str)

SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    session.add(hero_1)
    session.add(hero_2)
    session.add(hero_3)
    session.commit()
