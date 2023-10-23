from dataclasses import dataclass
from typing import Optional, Any
from .util import *


@dataclass
class Store:
    instance: Any
    id: int
    name: str
    address: Optional[Address]
    location: Optional[Location]
    phone_number: Optional[str]
    url: Optional[str]
    amenities: list[str]

    @classmethod
    def from_data(cls, instance: Any, data: dict) -> "Store":
        return Store(
            instance=instance,
            id=int(data.get("id", "0")),
            name=data.get("name", ""),
            address=Address.from_data(data["address"])
            if "address" in data.keys()
            else None,
            location=Location.from_dict(data["location"])
            if "location" in data.keys()
            else None,
            phone_number=data.get("phone_number"),
            url=data.get("external_url"),
            amenities=[a.strip().lower() for a in data["amenities"].split(",")]
            if "amenities" in data.keys() and data["amenities"]
            else [],
        )
