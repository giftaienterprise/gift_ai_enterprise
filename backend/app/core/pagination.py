from typing import Generic, TypeVar

from pydantic import BaseModel


T = TypeVar("T")


class PageParams(BaseModel):
    page: int = 1
    size: int = 10

    @property
    def skip(self) -> int:
        return (self.page - 1) * self.size


class PageResult(BaseModel, Generic[T]):
    total: int
    page: int
    size: int
    items: list[T]