from dataclasses import dataclass
from .literal import SortOrder


@dataclass(frozen=True)
class FindAllParams:
    q: str | None
    order: SortOrder
    sort: str
    page: int
    per_page: int
