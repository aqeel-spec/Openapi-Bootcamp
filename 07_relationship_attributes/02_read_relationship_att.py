from sqlmodel import Field, Relationship , SQLModel, create_engine, Session, select
from typing import Optional, List
from dotenv import load_dotenv, find_dotenv
from os import getenv

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    heros: List["Hero"] = Relationship(back_populates="team")

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

    team_id: Optional[int] = Field(default=None, foreign_key="team.id")
    team: Optional[Team] = Relationship(back_populates="heros")


_ : bool = load_dotenv(find_dotenv())
connection_str = getenv("POSTGRES_URL")

if not connection_str:
    raise ValueError("POSTGRES_URL environment variable is not set")

engine = create_engine(connection_str,echo=True)

# now we will create heros using relationship
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def create_heros():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")

        # Now create members of heros and add them to teams
        hero_deadpond = Hero(name="Deadpond", secret_name="Dive Wilson", team=team_z_force)
        hero_rusty_man = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48, team=team_preventers)
        hero_spider_boy = Hero(name="Spider-Boy", secret_name="Pedro Parqueador", team=team_preventers)

        # Now we will add it to database and commit
        session.add_all([team_preventers, team_z_force, hero_deadpond, hero_rusty_man, hero_spider_boy])
        session.commit()
        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

        # now we will print it in the console
        print(hero_deadpond)
        print(hero_rusty_man)
        print(hero_spider_boy)

# Read heros from team
# Code above omitted 👆

def select_heros():
    with Session(engine) as session:
        statement = select(Team).where(Team.name == "Wakaland")
        result = session.exec(statement)
        team_preventers = result.one()

        print("Preventers heroes:", team_preventers.heros)

# remve relationship using updation
# Code above omitted 👆

def update_heroes():
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Rusty-Man")
        result = session.exec(statement)
        hero_spider_boy = result.one()

        hero_spider_boy.team = None
        session.add(hero_spider_boy)
        session.commit()

        session.refresh(hero_spider_boy)
        print(f"\n\n Updated hero : {hero_spider_boy} \n\n")
        print("Spider-Boy without team:", hero_spider_boy.team)

# Code below omitted 👇

# Code below omitted 👇

if __name__ == "__main__":
    # create_db_and_tables()
    # create_heros()
    # select_heros()
    update_heroes()


       