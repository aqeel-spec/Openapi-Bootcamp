from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

app : FastAPI = FastAPI(
    titile="Session",
    description="Get the Session",
    version="1.0.0",
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        }
    ]
)

class HeroBase(SQLModel):
    name: str
    secret_name: str
    age: Optional[int] = None

class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class HeroRead(HeroBase):
    id: int

class CreateHero(HeroBase):
    pass

class UpdateHero(HeroBase):
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None


database_url = "postgresql://aqeelshahzad1215:lyALVYh48Pom@ep-dry-block-77954970.us-east-2.aws.neon.tech/gpts?sslmode=require"

# connect_args = {"check_same_thread": False}
engine = create_engine(database_url, echo=True)

# create db and tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# create session function 
def get_session():
    with Session(engine) as session:
        yield session


# on startup run create_db_and_tables
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# add hero
@app.post("/heroes/")
def add_hero(* , session: Session = Depends(get_session), hero : CreateHero):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

# get all heroes
@app.get("/heroes/")
def get_all_heroes(* , session: Session = Depends(get_session), offset: int = 0, limit: int = Query(default=100, le=100),):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

# read one hero
@app.get("/heroes/{hero_id}")
def read_hero(*, session: Session = Depends(get_session),hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

# update hero
@app.put("/heroes/{hero_id}", response_model=HeroRead)
def update_hero(
    *, session: Session = Depends(get_session), hero_id: int, hero: UpdateHero
):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(db_hero, key, value)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

# delete hero
@app.delete("/heroes/{hero_id}")
def delete_hero(*, session: Session = Depends(get_session), hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}