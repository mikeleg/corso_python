from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.models.starwars import Planet
from app.db import get_session
from typing import List

router = APIRouter(prefix="/planets", tags=["Planets"])

@router.post("/", response_model=Planet)
def create_planet(planet: Planet, session: Session = Depends(get_session)):
    session.add(planet)
    session.commit()
    session.refresh(planet)
    return planet

@router.get("/", response_model=List[Planet])
def list_planets(session: Session = Depends(get_session)):
    return session.exec(select(Planet)).all()

@router.get("/{planet_id}", response_model=Planet)
def get_planet(planet_id: int, session: Session = Depends(get_session)):
    planet = session.get(Planet, planet_id)
    if not planet:
        raise HTTPException(status_code=404, detail="Planet not found")
    return planet
