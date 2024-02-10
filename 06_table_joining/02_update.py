from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select


class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    headquarters: str


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)

    team_id: Optional[int] = Field(default=None, foreign_key="team.id")


connection_str = "postgresql://aqeelshahzad1215:lyALVYh48Pom@ep-dry-block-77954970.us-east-2.aws.neon.tech/gpts?sslmode=require"

engine = create_engine(connection_str)


# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)


# update spider boy team_id and assign foreign key of team.id
def update_spider_boy():
    with Session(engine) as session:
        spider_boys = session.exec(select(Hero).where(Hero.name == "Spider-Boy")).all()
        preventers = session.exec(select(Team).where(Team.name == "Preventers")).all()

        # take ids from spider boys and get id from preventers
        for spider_boy , preventer in zip(spider_boys, preventers):
            spider_boy.team_id = preventer.id

            print(f"Preventer id:  {preventer.id}")
            print("================")
            print(f"spider boys : {spider_boy}")
            print("================")
            session.add(spider_boy)
            session.commit()
            session.refresh(spider_boy)
            
        
        # print(f"preventers : {preventers}")


def main():
    # create_db_and_tables()
    update_spider_boy()


if __name__ == "__main__":
    main()

# create db and tables
    # create_db_and_tables()
    # create_heroes()