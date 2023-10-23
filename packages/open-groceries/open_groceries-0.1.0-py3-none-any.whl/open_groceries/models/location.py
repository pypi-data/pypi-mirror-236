from dataclasses import dataclass
from math import radians, cos, sin, asin, sqrt

@dataclass
class LatLong:
    latitude: float
    longitude: float

    @classmethod
    def from_dict(cls, data: dict) -> "LatLong":
        return LatLong(latitude=float(data["latitude"]), longitude=float(data["longitude"]))
    
    @classmethod
    def from_list(cls, data: list, longitude_first: bool = False) -> "LatLong":
        if longitude_first:
            return LatLong(latitude=float(data[1]), longitude=float(data[0]))
        else:
            return LatLong(latitude=float(data[0]), longitude=float(data[1]))
        
    def distance_to(self, other: "LatLong") -> float:
        # convert decimal degrees to radians
        lat1, long1, lat2, long2 = map(radians, [self.latitude, self.longitude, other.latitude, other.longitude])
        # haversine formula
        dlon = long2 - long1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        # Radius of earth in kilometers is 6371
        km = 6371 * c
        return km
        
@dataclass
class Address:
    lines: list[str]
    city: str
    country: str
    zip_code: str
    province: str

@dataclass
class Location:
    type: str
    id: str
    name: str
    location: LatLong
    address: Address
    phone: str
    features: list[str]

