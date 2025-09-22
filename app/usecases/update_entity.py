from typing import Any, Dict, Type

from sqlmodel import Session, SQLModel


class UpdateEntityUseCase:
    def __init__(self, model: Type[SQLModel]):
        self.model = model

    def execute(self, entity_id: int, data: Dict, session: Session) -> Any:
        entity = session.get(self.model, entity_id)
        if not entity:
            return None
        for key, value in data.items():
            setattr(entity, key, value)
        session.add(entity)
        session.commit()
        session.refresh(entity)
        return entity
