from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlmodel import Session

from app.db import get_session
from app.models.starwars import Starship
from app.usecases.create_entity import CreateEntityUseCase
from app.usecases.delete_entity import DeleteEntityUseCase
from app.usecases.get_entity import GetEntityUseCase
from app.usecases.pagination import PaginationUseCase
from app.usecases.slice_entity import SliceUseCase
from app.usecases.update_entity import UpdateEntityUseCase

router = APIRouter(prefix="/starships", tags=["Starships"])


@router.patch("/{starship_id}", response_model=Starship)
def update_starship(
    starship_id: int, data: dict = Body(...), session: Session = Depends(get_session)
):
    usecase = UpdateEntityUseCase(Starship)
    updated = usecase.execute(starship_id, data, session)
    if not updated:
        raise HTTPException(status_code=404, detail="Starship not found")
    return updated


@router.delete("/{starship_id}")
def delete_starship(starship_id: int, session: Session = Depends(get_session)):
    usecase = DeleteEntityUseCase(Starship)
    deleted = usecase.execute(starship_id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail="Starship not found")
    return {"ok": True}


@router.post("/", response_model=Starship)
def create_starship(starship: Starship, session: Session = Depends(get_session)):
    usecase = CreateEntityUseCase(Starship)
    return usecase.execute(starship, session)


@router.get("/")
def list_starships(
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
):
    usecase = PaginationUseCase(Starship)
    return usecase.execute(session, page, per_page)


# Slice route: restituisce solo i dati richiesti, senza metadati di paginazione
@router.get("/slice")
def slice_starships(
    session: Session = Depends(get_session),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
):
    """
    Restituisce una fetta di starships senza metadati di paginazione.
    Parametri:
        - offset: indice iniziale (inclusivo)
        - limit: quanti elementi restituire (default 10)
    """
    usecase = SliceUseCase(Starship)
    return usecase.execute(session, offset, limit)


@router.get("/{starship_id}", response_model=Starship)
def get_starship(starship_id: int, session: Session = Depends(get_session)):
    usecase = GetEntityUseCase(Starship)
    starship = usecase.execute(starship_id, session)
    if not starship:
        raise HTTPException(status_code=404, detail="Starship not found")
    return starship
