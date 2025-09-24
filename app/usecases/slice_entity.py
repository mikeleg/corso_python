from typing import Type, List, TypeVar, Generic
from sqlmodel import Session, SQLModel, select

T = TypeVar("T", bound=SQLModel)

class SliceUseCase(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def execute(self, session: Session, offset: int = 0, limit: int = 10) -> List[T]:
        stmt = select(self.model).offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        items: List[T] = session.exec(stmt).all()
        return items
