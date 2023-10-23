from dataclasses import dataclass
from typing import Any, Union
import requests
from models import *
from exceptions import *
from models import Location


WG_MAP = "pk.eyJ1IjoiaW5zdGFjYXJ0IiwiYSI6ImNqcmJrZWpmYjE0YXI0M3BkZHF2MXA4eXEifQ.YLQlO13ZFAJMx6ew3rvBrw"
WG_INSTA = "Bearer v2.2aaf35d6a9f7e4.AUjoCP_kvwWqLABrsBF8A-L6WvgCU9QKMgNLH7Jh3RQ"


@dataclass
class SessionContext:
    cookies: dict[str, str]
    user_agent: str


class Wegmans(GroceryAdapter):
    def __init__(
        self,
        user_agent: str = "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0",
    ) -> None:
        self.base = "https://shop.wegmans.com"
        self.context = self._get_session_context(
            user_agent,
            {
                "binary": "web-ecom",
                "binary_version": "4.33.26",
                "is_retina": False,
                "os_version": "Linux x86_64",
                "pixel_density": "1.0",
                "push_token": "",
                "screen_height": 1080,
                "screen_width": 1920,
            },
        )
        self.session = requests.Session()
        self.session.headers = {"User-Agent": self.context.user_agent}
        self.session.cookies.update(self.context.cookies)
        self.session.cookies.set("wfmStoreId", "1")

    def _get_session_context(
        self, user_agent: str, environment: dict[str, Any]
    ) -> SessionContext:
        first_pass = requests.get(self.base)
        cookies = dict(first_pass.cookies)
        second_pass = requests.post(
            self.base + "/api/v3/user_init",
            json=environment,
            headers={"User-Agent": user_agent},
            cookies=cookies,
        )
        cookies = dict(second_pass.cookies)
        return SessionContext(cookies=cookies, user_agent=user_agent)

    def url(self, path: str):
        return self.base.rstrip("/") + "/" + path.lstrip("/")

    def search_groceries(self, search: str) -> list[GroceryItem]:
        result = self.session.get(
            self.url("/api/v2/store_products"), params={"search_term": search}
        )
        if result.status_code >= 300:
            raise ApiException(result)

        data = result.json()
        return [self.build_wegmans_grocery_item(item) for item in data["items"]]

    def build_wegmans_grocery_item(self, data: dict) -> GroceryItem:
        return GroceryItem(
            type="wegmans",
            id=int(data["id"]),
            name=data["name"].lower().strip(),
            location=data.get("aisle").lower().strip() if data.get("aisle") else None,
            images=list(data.get("images", {"tile": {}})["tile"].values()),
            tags=data.get("tags", []),
            price=data.get("base_price", 0),
            ratings=Ratings(
                average=data["product_rating"]["average_rating"],
                count=data["product_rating"]["user_count"],
            ),
            metadata={
                "brand": data.get("brand_name").lower().strip()
                if "brand_name" in data.keys()
                else None,
                "categories": [c["name"] for c in data["categories"]],
                "size": data.get("size_string", None),
            },
        )

    def get_grocery_item(self, id: str):
        result = self.session.get(
            self.url(f"/api/v2/store_products/{id}"),
            params={"require_storeproduct": "true"},
        )

        if result.status_code >= 300:
            raise ApiException(result)

        data = result.json()
        return self.build_wegmans_grocery_item(data)

    def get_locations(self, near: str) -> list[Location]:
        map_result = requests.get(
            f"https://api.mapbox.com/geocoding/v5/mapbox.places/{near.lower()}.json",
            params={"country": "us,ca", "access_token": WG_MAP},
            headers={
                "Host": "api.mapbox.com",
                "Origin": "https://shop.wegmans.com",
                "Referer": "https://shop.wegmans.com/",
                "User-Agent": self.context.user_agent,
            },
        )
        map_data = map_result.json()
        if not "features" in map_data.keys():
            return []
        if len(map_data["features"]) == 0:
            return []
        position = LatLong.from_list(
            map_data["features"][0]["center"], longitude_first=True
        )

        store_result = self.session.get(self.url("/api/v2/stores"))
        if store_result.status_code >= 300:
            raise ApiException(store_result)

        data = store_result.json()
        distance_mapped = sorted(
            [
                (s, position.distance_to(LatLong.from_dict(s["location"])))
                for s in data["items"]
            ],
            key=lambda x: x[1],
        )
        sorted_results = [s[0] for s in distance_mapped]
        return [
            Location(
                type="wegmans",
                id=s["id"],
                name=s["name"],
                location=LatLong.from_dict(s["location"]),
                address=Address(
                    lines=[
                        s["address"][f"line{n}"]
                        for n in range(1, 4)
                        if f"line{n}" in s["address"].keys()
                        and s["address"][f"line{n}"]
                    ],
                    city=s["address"]["city"],
                    country=s["address"]["country"],
                    zip_code=s["address"]["postal_code"],
                    province=s["address"]["province"],
                ),
                phone=s.get("phone_number", ""),
                features=[i.strip().lower() for i in s.get("amenities").split(", ")]
                if s.get("amenities")
                else [],
            )
            for s in sorted_results
        ]

    def set_location(self, location: Location):
        self.session.cookies.set("wfmStoreId", location.id)

    def suggest(self, search: str) -> list[str]:
        result = requests.post(
            "https://connect.instacart.com/v2/autosuggest/autosuggestions",
            json={"limit": 10, "query": search},
            headers={
                "authorization": WG_INSTA,
                "User-Agent": self.context.user_agent,
                "Host": "connect.instacart.com",
                "Origin": "https://shop.wegmans.com",
                "Referer": "https://shop.wegmans.com/"
            },
        )

        if result.status_code >= 300:
            raise ApiException(result)

        data = result.json()
        return [s["text"] for s in data["autosuggestions"]]
