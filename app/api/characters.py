from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlmodel import Session

from app.db import get_session
from app.models.starwars import Character
from app.usecases.create_entity import CreateEntityUseCase
from app.usecases.delete_entity import DeleteEntityUseCase
from app.usecases.get_entity import GetEntityUseCase
from app.usecases.pagination import PaginationUseCase
from app.usecases.slice_entity import SliceUseCase
from app.usecases.update_entity import UpdateEntityUseCase

router = APIRouter(prefix="/characters", tags=["Characters"])


@router.patch("/{character_id}", response_model=Character)
def update_character(
    character_id: int, data: dict = Body(...), session: Session = Depends(get_session)
):
    usecase = UpdateEntityUseCase(Character)
    updated = usecase.execute(character_id, data, session)
    if not updated:
        raise HTTPException(status_code=404, detail="Character not found")
    return updated


@router.delete("/{character_id}")
def delete_character(character_id: int, session: Session = Depends(get_session)):
    usecase = DeleteEntityUseCase(Character)
    deleted = usecase.execute(character_id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail="Character not found")
    return {"ok": True}


@router.post("/", response_model=Character)
def create_character(character: Character, session: Session = Depends(get_session)):
    usecase = CreateEntityUseCase(Character)
    return usecase.execute(character, session)


@router.get("/")
def list_characters(
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
):
    usecase = PaginationUseCase(Character)
    return usecase.execute(session, page, per_page)


# Slice route: restituisce solo i dati richiesti, senza metadati di paginazione
@router.get("/slice")
def slice_characters(
    session: Session = Depends(get_session),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
):
    """
    Restituisce una fetta di personaggi senza metadati di paginazione.
    Parametri:
        - offset: indice iniziale (inclusivo)
        - limit: quanti elementi restituire (default 10)
    """
    usecase = SliceUseCase(Character)
    return usecase.execute(session, offset, limit)


@router.get("/{character_id}", response_model=Character)
def get_character(character_id: int, session: Session = Depends(get_session)):
    usecase = GetEntityUseCase(Character)
    character = usecase.execute(character_id, session)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character
