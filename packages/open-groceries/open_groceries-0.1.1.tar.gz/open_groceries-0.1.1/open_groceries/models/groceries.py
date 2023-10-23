from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class Ratings:
    average: int
    count: int

@dataclass
class GroceryItem:
    type: str
    id: str
    name: str
    location: Optional[str]
    images: list[str]
    tags: list[str]
    price: float
    ratings: Ratings
    metadata: dict[str, Any]