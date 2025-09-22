from typing import Any, Type

from sqlmodel import Session, SQLModel


class CreateEntityUseCase:
    def __init__(self, model: Type[SQLModel]):
        self.model = model

    def execute(self, data: Any, session: Session) -> Any:
        session.add(data)
        session.commit()
        session.refresh(data)
        return data
