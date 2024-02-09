from fastapi import FastAPI, HTTPException , Depends , status
from pydantic import BaseModel
from typing import Annotated

app : FastAPI = FastAPI(
    titile="Location",
    description="Get the Location of the user",
    version="1.0.0",
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        }
    ]
)

class Location(BaseModel):
    name : str
    location : str

# dummy user locations
locations = {
    "zia":Location(name="zia",location="Karachi"),
    "ali":Location(name="ali",location="Lahore"),
    "waseem":Location(name="waseem",location="Islamabad"),
    "hamza":Location(name="hamza",location="Faisalabad"),
    "aqeel":Location(name="aqeel",location="Chiniot"),
}

# dependency function
def get_location_or_404(name:str)->Location:
    loc = locations.get(name.lower())
    if not loc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No location found for {name}")
    return loc


# get location to specific person
@app.get("/locations/{name}")
def get_person_location(name:str, location: Annotated[Location, Depends(get_location_or_404)]):
    return location

# get location of all users
@app.get("/locations")
def get_all_locations():
    return locations
