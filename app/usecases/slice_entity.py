from typing import Type, List
from sqlmodel import Session, SQLModel, select

class SliceUseCase:
    def __init__(self, model: Type[SQLModel]):
        self.model = model

    def execute(self, session: Session, offset: int = 0, limit: int = 10) -> List[SQLModel]:
        stmt = select(self.model).offset(offset)
        if limit is not None:
            stmt = stmt.limit(limit)
        items = session.exec(stmt).all()
        return items
