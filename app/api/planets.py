from fastapi import APIRouter, Body, Depends, HTTPException, Query
from sqlmodel import Session

from app.db import get_session
from app.models.starwars import Planet
from app.usecases.create_entity import CreateEntityUseCase
from app.usecases.delete_entity import DeleteEntityUseCase
from app.usecases.get_entity import GetEntityUseCase
from app.usecases.pagination import PaginationUseCase
from app.usecases.update_entity import UpdateEntityUseCase

router = APIRouter(prefix="/planets", tags=["Planets"])


@router.patch("/{planet_id}", response_model=Planet)
def update_planet(
    planet_id: int, data: dict = Body(...), session: Session = Depends(get_session)
):
    usecase = UpdateEntityUseCase(Planet)
    updated = usecase.execute(planet_id, data, session)
    if not updated:
        raise HTTPException(status_code=404, detail="Planet not found")
    return updated


@router.delete("/{planet_id}")
def delete_planet(planet_id: int, session: Session = Depends(get_session)):
    usecase = DeleteEntityUseCase(Planet)
    deleted = usecase.execute(planet_id, session)
    if not deleted:
        raise HTTPException(status_code=404, detail="Planet not found")
    return {"ok": True}


@router.post("/", response_model=Planet)
def create_planet(planet: Planet, session: Session = Depends(get_session)):
    usecase = CreateEntityUseCase(Planet)
    return usecase.execute(planet, session)


@router.get("/")
def list_planets(
    session: Session = Depends(get_session),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
):
    usecase = PaginationUseCase(Planet)
    return usecase.execute(session, page, per_page)


@router.get("/{planet_id}", response_model=Planet)
def get_planet(planet_id: int, session: Session = Depends(get_session)):
    usecase = GetEntityUseCase(Planet)
    planet = usecase.execute(planet_id, session)
    if not planet:
        raise HTTPException(status_code=404, detail="Planet not found")
    return planet
