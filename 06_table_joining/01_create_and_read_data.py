from typing import Optional

from sqlmodel import Field, SQLModel, create_engine, Session , select

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)
    # now we will use team.id as a foreign key
    team_id: Optional[int] = Field(default=None,foreign_key="team.id")

# now create database and tables
connection_str = "postgresql://aqeelshahzad1215:lyALVYh48Pom@ep-dry-block-77954970.us-east-2.aws.neon.tech/gpts?sslmode=require"

engine = create_engine(connection_str)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Code above omitted 👆

def create_heroes():
    with Session(engine) as session:
        team_preventers = Team(name="Preventers", headquarters="Sharp Tower")
        team_z_force = Team(name="Z-Force", headquarters="Sister Margaret's Bar")
        # session.add(team_preventers)
        # session.add(team_z_force)
        # session.commit()

        hero_deadpond = Hero(
            name="Deadpond", secret_name="Dive Wilson", team_id=team_z_force.id
        )
        hero_rusty_man = Hero(
            name="Rusty-Man",
            secret_name="Tommy Sharp",
            age=48,
            team_id=team_preventers.id,
        )
        hero_spider_boy = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
        # session.add(hero_deadpond)
        # session.add(hero_rusty_man)
        # session.add(hero_spider_boy)
        # session.commit()

        # session.refresh(hero_deadpond)
        # session.refresh(hero_rusty_man)
        # session.refresh(hero_spider_boy)

        # print("Created hero:", hero_deadpond)
        # print("Created hero:", hero_rusty_man)
        # print("Created hero:", hero_spider_boy)

# Code above omitted 👆

def select_heroes():
    with Session(engine) as session:
        statement = select(Hero, Team).join(Team).where(Team.name == "Preventers")
        results = session.exec(statement)
        for hero, team in results:
            print("Preventer Hero:", hero, "Team:", team)


def main():
    create_db_and_tables()

if __name__ == "__main__":
    main()
    # create_heroes()
    select_heroes()