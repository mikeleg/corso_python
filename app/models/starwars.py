from sqlmodel import SQLModel, Field
from typing import Optional

class Character(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    species: str
    homeworld: str

class Planet(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    climate: str
    population: int

class Starship(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    model: str
    manufacturer: str
