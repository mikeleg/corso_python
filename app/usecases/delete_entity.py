from typing import Type, TypeVar, Generic

from sqlmodel import Session, SQLModel

T = TypeVar("T", bound=SQLModel)


class DeleteEntityUseCase(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def execute(self, entity_id: int, session: Session) -> bool:
        entity = session.get(self.model, entity_id)
        if not entity:
            return False
        session.delete(entity)
        session.commit()
        return True
