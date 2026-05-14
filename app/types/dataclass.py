from dataclasses import dataclass

from .literal import SortOrder


@dataclass(frozen=True)
class FindAllParams:
    q: str | None = None
    order: SortOrder = "ASC"
    sort: str = "id"
    page: int = 1
    per_page: int = 10
