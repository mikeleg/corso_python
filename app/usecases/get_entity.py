from typing import Optional, Type, TypeVar, Generic

from sqlmodel import Session, SQLModel

T = TypeVar("T", bound=SQLModel)


class GetEntityUseCase(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def execute(self, entity_id: int, session: Session) -> Optional[T]:
        return session.get(self.model, entity_id)
