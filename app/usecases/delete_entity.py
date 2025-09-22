from typing import Type

from sqlmodel import Session, SQLModel


class DeleteEntityUseCase:
    def __init__(self, model: Type[SQLModel]):
        self.model = model

    def execute(self, entity_id: int, session: Session) -> bool:
        entity = session.get(self.model, entity_id)
        if not entity:
            return False
        session.delete(entity)
        session.commit()
        return True
