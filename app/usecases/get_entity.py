from typing import Any, Optional, Type

from sqlmodel import Session, SQLModel


class GetEntityUseCase:
    def __init__(self, model: Type[SQLModel]):
        self.model = model

    def execute(self, entity_id: int, session: Session) -> Optional[Any]:
        return session.get(self.model, entity_id)
