from fastapi import FastAPI, Depends, HTTPException, status, Query
from typing import Annotated


from sqlmodel import SQLModel, Field, create_engine, Session, select
from dotenv import load_dotenv, find_dotenv
from os import getenv


class HeroBase(SQLModel):
    name: str
    secret_name: str

class Hero(HeroBase, table=True):
    id: int = Field(default=None, primary_key=True)
    age: int | None = None

class HeroCreate(HeroBase):
    age: int | None = None

class HeroResponse(HeroBase):
    id: int
    age: int | None = None

class HeroUpdate(HeroBase):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None

_ : bool = load_dotenv(find_dotenv())
connection_str = getenv("POSTGRES_URL")

if not connection_str:
    raise ValueError("POSTGRES_URL environment variable is not set")

engine = create_engine(connection_str)

# DB dependency injection
def get_session() :
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app : FastAPI = FastAPI(
    titile="Hero",
    description="Get the Hero",
    version="1.0.0"
)

def get_error_404():
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hero not found")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "Welcome to test api's with data"}

# Get all heros
@app.get("/heros/", response_model=list[Hero])                                
async def get_all_heroes(session : Annotated[Session, Depends(get_session)], offset: int = Query(default=0, le=4), limit: int = Query(default=1, le=4)):
    # offset = How much we leave or step 0_4     -> from 0 to 4   
    # limit =  How much client we fetch min = 1, max = 4 -> between 1 and 4
    """
    Get all heroes from the database and return them.
    """
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes
    
# create heros
@app.post("/heros/", response_model=HeroResponse)
async def add_hero(hero: HeroCreate, session : Annotated[Session, Depends(get_session)]):
    # print(f"Data from lient : {hero}")
    hero_to_insert = Hero.model_validate(hero)
    # print(f"DATA TO INSERT AFTER VALIDATION : {hero_to_insert}")
    session.add(hero_to_insert)
    session.commit()
    session.refresh(hero_to_insert)
    return hero_to_insert


# Single Hero
@app.get("/heros/{hero_id}", response_model=HeroResponse)
async def get_hero(hero_id: int, session : Annotated[Session, Depends(get_session)]):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise get_error_404()
    return hero

# Update Hero
@app.put("/heros/{hero_id}", response_model=HeroResponse)
async def update_hero(hero_id: int, hero: HeroUpdate, session : Annotated[Session, Depends(get_session)]):
    hero_to_update = session.get(Hero, hero_id)
    if not hero_to_update:
        raise get_error_404()
    hero_data = hero.model_dump(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(hero_to_update, key, value)
    session.add(hero_to_update)
    session.commit()
    session.refresh(hero_to_update)
    return hero_to_update

# Delete Hero
@app.delete("/heros/{hero_id}")
async def delete_hero(hero_id: int, session : Annotated[Session, Depends(get_session)]):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise get_error_404()
    session.delete(hero)
    session.commit()
    return {"deleted ok": True}