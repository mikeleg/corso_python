from typing import Type, TypeVar, Generic

from sqlmodel import Session, SQLModel

T = TypeVar("T", bound=SQLModel)


class CreateEntityUseCase(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def execute(self, data: T, session: Session) -> T:
        session.add(data)
        session.commit()
        session.refresh(data)
        return data
