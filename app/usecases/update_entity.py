from typing import Dict, Type, TypeVar, Generic

from sqlmodel import Session, SQLModel

T = TypeVar("T", bound=SQLModel)


class UpdateEntityUseCase(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def execute(self, entity_id: int, data: Dict, session: Session) -> T | None:
        entity = session.get(self.model, entity_id)
        if not entity:
            return None
        for key, value in data.items():
            setattr(entity, key, value)
        session.add(entity)
        session.commit()
        session.refresh(entity)
        return entity
