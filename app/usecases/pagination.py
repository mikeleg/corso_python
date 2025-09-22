from math import ceil
from typing import Any, Dict, Type

from sqlmodel import Session, SQLModel, select

DEFAULT_PAGE = 1
DEFAULT_PER_PAGE = 10
MIN_PER_PAGE = 1
MAX_PER_PAGE = 100


class PaginationUseCase:
    def __init__(self, model: Type[SQLModel]):
        self.model = model

    def execute(
        self,
        session: Session,
        page: int = DEFAULT_PAGE,
        per_page: int = DEFAULT_PER_PAGE,
    ) -> Dict[str, Any]:
        total = session.query(self.model).count()
        stmt = select(self.model).offset((page - 1) * per_page).limit(per_page)
        items = session.exec(stmt).all()
        total_pages = ceil(total / per_page) if per_page else 1
        return {
            "data": items,
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": total_pages,
        }
