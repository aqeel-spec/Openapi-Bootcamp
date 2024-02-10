from typing import List , Optional

from sqlmodel import Field, Relationship , SQLModel, create_engine, Session, select
from dotenv import load_dotenv, find_dotenv
from os import getenv, name

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

def create_heros():
    with Session(engine) as session:
        team_precenters = Team(name="The Pre-Centers", headquarters="Earth")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")

        # Now we will create hero 
        # one hero should belong to many teams
        hero_deadpond = Hero(
            name="Deadpond",
            secret_name="Dive Wilson",
            teams=[team_precenters, team_z_force],
        )
        # create one hero for one team -> with age = 48
        hero_rusty_man = Hero(
            name = "Rusty-Man",
            secret_name = "Tommy Sharp",
            age = 48,
            teams = [team_precenters]
        )
        # create one hero for one team -> with no age
        hero_spider_boy = Hero(
            name = "Spider-Boy",
            secret_name = "Pedro Parqueador",
            teams = [team_precenters]
        )

        # Now we will add it to database and commit
        # Now we will add heroes to the database and commit
        session.add_all([hero_deadpond, hero_rusty_man, hero_spider_boy])
        session.commit()

        session.refresh(hero_deadpond)
        session.refresh(hero_rusty_man)
        session.refresh(hero_spider_boy)

        # printing all the results
        print("Deadpond:", hero_deadpond)
        print("Deadpond teams:", hero_deadpond.teams)
        print("Rusty-Man:", hero_rusty_man)
        print("Rusty-Man Teams:", hero_rusty_man.teams)
        print("Spider-Boy:", hero_spider_boy)
        print("Spider-Boy Teams:", hero_spider_boy.teams)


def update_heros():
    with Session(engine) as session:
        # hero_id = 10
        hero_deadpond = session.exec(select(Hero).where(Hero.name=="Deadpond")).one()
        # Now get z-force data also

        # team_id = 7
        team_z_force = session.exec(select(Team).where(Team.name=="Z-Force")).one()

        # we have to remove 7 from 10 

        # team_z_force.heros.append(hero_spider_boy)
        # session.add(team_z_force)
        # session.commit()

        # print("\n\npdated Spider-Boy's Teams:", hero_spider_boy.teams)
        # print("\n\nZ-Force heroes:", team_z_force.heros)

        # ########### Remove Spider-Boy from Z-Force's team #############
        # hero_spider_boy.teams.remove(team_z_force)
        hero_deadpond.teams.remove(team_z_force)
        session.add(team_z_force)
        session.commit()

        print("\n\nReverted Z-Force's heroes:", team_z_force.heros)
        print("\n\nReverted Spider-Boy's teams:", hero_deadpond.teams)




def main():
    # create_heros()
    # create_db_and_tables()
    update_heros()

if __name__=="__main__":
    main()
