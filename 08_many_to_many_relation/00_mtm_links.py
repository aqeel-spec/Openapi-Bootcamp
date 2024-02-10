from typing import List , Optional

from sqlmodel import Field, Relationship , SQLModel, create_engine, Session, select
from dotenv import load_dotenv, find_dotenv
from os import getenv

class HeroTeamLink(SQLModel, table=True):
    team_id: Optional[int] = Field(default=None, foreign_key="team.id", primary_key=True)
    hero_id: Optional[int] = Field(default=None,foreign_key="hero.id", primary_key=True)

# Team Model
class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

    heros: List["Hero"] = Relationship(back_populates="teams", link_model=HeroTeamLink)

class Hero(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    name : str = Field(index=True)
    secret_name : str
    age : Optional[int] = Field(default=None, index=True)

    teams: List["Team"] = Relationship(back_populates="heros", link_model=HeroTeamLink)

# load environment variables
_ : bool = load_dotenv(find_dotenv())
connection_str = getenv("POSTGRES_URL")

if not connection_str:
    raise ValueError("POSTGRES_URL environment variable is not set")

# create engine
engine = create_engine(connection_str,echo=True)

# create tables on database
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def main():
    create_db_and_tables()

if __name__=="__main__":
    main()
