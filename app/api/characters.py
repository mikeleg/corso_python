from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from app.models.starwars import Character
from app.db import get_session
from typing import List

router = APIRouter(prefix="/characters", tags=["Characters"])

@router.post("/", response_model=Character)
def create_character(character: Character, session: Session = Depends(get_session)):
    session.add(character)
    session.commit()
    session.refresh(character)
    return character

@router.get("/", response_model=List[Character])
def list_characters(session: Session = Depends(get_session)):
    return session.exec(select(Character)).all()

@router.get("/{character_id}", response_model=Character)
def get_character(character_id: int, session: Session = Depends(get_session)):
    character = session.get(Character, character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character
