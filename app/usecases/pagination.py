from math import ceil
from typing import Dict, Type, TypeVar, Generic, List

from sqlmodel import Session, SQLModel, select

T = TypeVar("T", bound=SQLModel)

DEFAULT_PAGE = 1
DEFAULT_PER_PAGE = 10
MIN_PER_PAGE = 1
MAX_PER_PAGE = 100


class PaginationUseCase(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def execute(
        self,
        session: Session,
        page: int = DEFAULT_PAGE,
        per_page: int = DEFAULT_PER_PAGE,
    ) -> Dict[str, object]:
        total = session.query(self.model).count()
        stmt = select(self.model).offset((page - 1) * per_page).limit(per_page)
        items: List[T] = session.exec(stmt).all()
        total_pages = ceil(total / per_page) if per_page else 1
        return {
            "data": items,
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": total_pages,
        }
