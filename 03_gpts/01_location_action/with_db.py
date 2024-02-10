from multiprocessing import connection
from fastapi import FastAPI, HTTPException , Depends , status, Query
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Annotated, Optional
from dotenv import load_dotenv, find_dotenv
from os import getenv

app : FastAPI = FastAPI(
    titile="Location with DB",
    description="Get the Location of the user",
    version="1.0.0",
    servers=[
        # By default first server automatically selected by fastapi
        {
            "url": "https://generally-modest-dolphin.ngrok-free.app/",
            "description": "Production ngrok server for gpts server"
        },
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        }
    ]
)

class Location(SQLModel, table=True):
    name : str = Field(default=None, primary_key=True)
    location : str

_ : bool = load_dotenv(find_dotenv())
database_url = getenv("POSTGRES_URL")

if not database_url:
    raise ValueError("POSTGRES_URL environment variable is not set")

engine = create_engine(database_url)

def create_db_and_tables():
    """
    Function to create the database and tables.
    No parameters and no return type.
    """
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup():
    """
    This function is called on startup and creates the necessary database and tables.
    """
    create_db_and_tables()


# get all persons from database
def get_persons_from_db():
    """
    Get persons from the database and return them.
    """
    with Session(engine) as session:
        persons = session.exec(select(Location)).all()
        return persons  
# get single person fron database
async def get_person_from_db(name:str):
    """
    Asynchronous function to retrieve a person from the database by name.

    Args:
        name (str): The name of the person to retrieve from the database.

    Returns:
        The person object retrieved from the database.

    Raises:
        HTTPException: If no person is found for the given name, HTTP 404 Not Found error is raised.
    """
    with Session(engine) as session:
        person = session.exec(select(Location).where(Location.name == name)).first()
        if not person:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No person found for {name}")
        return person  

@app.get("/persons/{name}")
def get_person(name:str, person: Annotated[Location, Depends(get_person_from_db)]):
    """
    Get information about a person from the database.

    Args:
        name (str): The name of the person.
        person (Annotated[Location, Depends(get_person_from_db)]): The person information retrieved from the database.

    Returns:
        The person information retrieved from the database.
    """
    return person

@app.get("/persons/")
def get_persons(persons: Annotated[list[Location], Depends(get_persons_from_db)]):
    """
    Get a list of persons from the database.

    Parameters:
        persons (list[Location]): The list of persons obtained from the database.

    Returns:
        list[Location]: The list of persons obtained from the database.
    """
    return persons

# add or create persons on database
@app.post("/person/")
def add_person(person: Location):
    """
    Add a person to the database.

    Args:
        person (Location): The person to be added.

    Returns:
        Location: The added person.
    """
    with Session(engine) as session:
        session.add(person)
        session.commit()
        session.refresh(person)
        return person

# now update the person location and save it on database
@app.put("/person/{name}")
async def update_person(name: str, location_update: Optional[str] = None) -> Location:
    """
    Update a person's location in the database.

    Args:
        name (str): The name of the person to update.
        location_update (Optional[str], optional): The new location to update. Defaults to None.

    Returns:
        Location: The updated location of the person.
    """
    with Session(engine) as session:
        db_person = await get_person_from_db(name)  # Reuse get_person
        name = db_person.name
        if not db_person:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No person found for {name}")
        # Update location if provided
        if location_update:
            db_person.location = location_update
        else:
            db_person.location = db_person.location

        session.add(db_person)
        session.commit()
        session.refresh(db_person)
        return db_person

# delete person from database
@app.delete("/person/{name}")
async def delete_person(name: str):
    """
    Delete a person from the database by name and return the deleted person.
    
    Parameters:
    - name: str, the name of the person to be deleted from the database
    
    Returns:
    - The deleted person from the database
    """
    with Session(engine) as session:
        db_person = await get_person_from_db(name)
        if not db_person:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No person found for {name}")
        session.delete(db_person)
        session.commit()
        return db_person



