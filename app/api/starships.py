from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.models.starwars import Starship
from app.db import get_session
from typing import List

router = APIRouter(prefix="/starships", tags=["Starships"])

@router.post("/", response_model=Starship)
def create_starship(starship: Starship, session: Session = Depends(get_session)):
    session.add(starship)
    session.commit()
    session.refresh(starship)
    return starship

@router.get("/", response_model=List[Starship])
def list_starships(session: Session = Depends(get_session)):
    return session.exec(select(Starship)).all()

@router.get("/{starship_id}", response_model=Starship)
def get_starship(starship_id: int, session: Session = Depends(get_session)):
    starship = session.get(Starship, starship_id)
    if not starship:
        raise HTTPException(status_code=404, detail="Starship not found")
    return starship
