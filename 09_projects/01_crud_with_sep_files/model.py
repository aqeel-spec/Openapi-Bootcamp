from sqlmodel import Field, SQLModel, Relationship


# ########### Team Model ############
class TeamBase(SQLModel):
    name: str
    headquarters: str

class Team(TeamBase, table=True):
    id: int = Field(default=None, primary_key=True)
    heros : list["Hero"] = Relationship(back_populates="team")

class TeamCreate(TeamBase):
    pass

class TeamResponse(TeamBase):
    id: int

class TeamUpdate(SQLModel):
    name: str | None = None
    headquarters: str | None = None


# ########### Hero Model ############
class HeroBase(SQLModel):
    name: str
    secret_name: str
    team_id : int = Field(default=None, foreign_key="team.id")

class Hero(HeroBase, table=True):
    id: int = Field(default=None, primary_key=True)
    age: int | None = None

    team : Team = Relationship(back_populates="heros")


class HeroCreate(HeroBase):
    age: int | None = None

class HeroResponse(HeroBase):
    id: int
    age: int | None = None

class HeroUpdate(HeroBase):
    name: str | None = None
    secret_name: str | None = None
    age: int | None = None

class HeroResponseWithTeam(HeroResponse):
    team: TeamResponse

class TeamResponseWithHeros(TeamResponse):
    heros: list[HeroResponse]