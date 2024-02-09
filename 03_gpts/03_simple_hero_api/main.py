from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Session , select
from fastapi import FastAPI

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None


engine = create_engine("postgresql://aqeelshahzad1215:lyALVYh48Pom@ep-dry-block-77954970.us-east-2.aws.neon.tech/gpts?sslmode=require")


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
    