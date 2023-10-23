from exceptions import ApiException
from models import GroceryAdapter, GroceryItem, Location, Ratings, LatLong, Address
import requests
from bs4 import BeautifulSoup
import esprima
import re
from datetime import date
from time import time
from typing import Union
from urllib.parse import quote
import json

VE_KEY = "AoWdiSwL2YlMr-nYYLxUFEipSBsTNtYPYUIF4aIEF4S0yrbbca0I9aRMRAA7H8SS"
ECOM_CLIENT = "45823696-9189-482d-89c3-0c067e477ea1"
AUTOCOMPLETE_KEY = "Basic dHlwZWFoZWFkOiM+OVZBdHJBN2ImJ0A/R0hZKzIp"
AUTOCOMPLETE_LOC = "1260-3pl,1321-wm,1508-3pl,283-wm,561-wm,725-wm,729-dz,731-wm,758-wm,759-wm,847_0-cor,847_0-cwt,847_0-edi,847_0-ehs,847_0-membership,847_0-mpt,847_0-spc,847_0-wm,847_1-edi,847_d-fis,847_lg_n1a-edi,847_NA-cor,847_NA-pharmacy,847_NA-wm,847_ss_u358-edi,847_wp_r451-edi,951-wm,952-wm,9847-wcs,729-bd,1195-wh"


class Costco(GroceryAdapter):
    def __init__(
        self,
        user_agent: str = "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0",
    ) -> None:
        self.user_agent = user_agent
        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": user_agent,
            "Host": "www.costco.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
        }
        self.base_url = "https://www.costco.com/"

    def search_groceries(self, search: str) -> list[GroceryItem]:
        req = self.session.get(
            self.base_url + "CatalogSearch", params={"dept": "All", "keyword": search}
        )
        soup = BeautifulSoup(req.text, features="html.parser")
        results = []
        for product in soup.select(".product"):
            data_script = product.select("script")[1]
            sc_tokens = esprima.tokenize(data_script.contents[0])
            data_mapping = {}
            for token in range(len(sc_tokens)):
                try:
                    if (
                        sc_tokens[token].type == "Identifier"
                        and sc_tokens[token + 1].type == "Punctuator"
                        and sc_tokens[token + 2].type in ["String", "Numeric"]
                    ):
                        data_mapping[sc_tokens[token].value] = sc_tokens[
                            token + 2
                        ].value
                except:
                    pass

            metas = {
                i.attrs["itemprop"]: i.attrs["content"] for i in product.select("meta")
            }
            results.append(
                GroceryItem(
                    type="costco",
                    id=int(data_mapping["SKU"].strip("'")),
                    name=data_mapping["name"].strip("'").replace("\\", ""),
                    location=None,
                    images=[
                        data_mapping["productImageUrl"].strip("'").replace("\\", "")
                    ],
                    tags=[
                        i.contents[0].replace("\\", "")
                        for i in product.select(".product-features li")
                        if i.contents and len(i.contents) > 0
                    ],
                    price=float(data_mapping["priceTotal"]),
                    ratings=Ratings(
                        average=float(metas.get("ratingValue", "0")),
                        count=int(metas.get("reviewCount", "0")),
                    ),
                    metadata={},
                )
            )

        return results

    def get_grocery_item(self, id: str) -> GroceryItem:
        req = self.session.get(self.base_url + f"{id}.product.{id}.html")
        soup = BeautifulSoup(req.text, features="html.parser")
        try:
            price = float(
                re.search("priceTotal\: initialize\([0-9\.]*\)", req.text)[0]
                .split("(")[1]
                .split(")")[0]
            )
        except:
            price = 0
        return GroceryItem(
            type="costco",
            id=id,
            name=soup.select_one(".product-title").text.strip(),
            location=None,
            images=[soup.select_one("#initialProductImage").attrs["src"]],
            tags=[i.text for i in soup.select(".pdp-features li")],
            price=price,
            ratings=None,
            metadata={},
        )

    def get_locations(self, near: str) -> list[Location]:
        location_request = requests.get(
            "https://dev.virtualearth.net/REST/v1/Locations",
            params={"q": near, "maxResults": "4", "key": VE_KEY},
            headers={
                "User-Agent": self.user_agent,
                "Host": "dev.virtualearth.net",
                "Origin": "https://www.costco.com",
                "Referer": "https://www.costco.com/",
            },
        )
        location_data = location_request.json()
        if len(location_data["resourceSets"]) == 0:
            return []
        if len(location_data["resourceSets"][0]["resources"]) == 0:
            return []

        have_point = list(
            filter(
                lambda x: "point" in x.keys(),
                location_data["resourceSets"][0]["resources"],
            )
        )
        if len(have_point) == 0:
            return []

        coords = LatLong.from_list(have_point[0]["point"]["coordinates"])
        today = date.fromtimestamp(time()).isoformat()
        warehouse_request = requests.get(
            "https://ecom-api.costco.com/warehouseLocatorMobile/v1/warehouses.json",
            params={
                "client_id": ECOM_CLIENT,
                "latitude": str(coords.latitude),
                "longitude": str(coords.longitude),
                "limit": "50",
                "openingDate": today,
            },
            headers={
                "User-Agent": self.user_agent,
                "Host": "ecom-api.costco.com",
                "Origin": "https://www.costco.com",
                "Referer": "https://www.costco.com/",
            },
        )
        warehouse_data = warehouse_request.json()
        return [
            Location(
                type="costco",
                id=w["warehouseId"],
                name=w["name"][0]["value"],
                location=LatLong.from_dict(w["address"]),
                address=Address(
                    lines=[w["address"]["line1"]],
                    city=w["address"]["city"],
                    country=w["address"]["countryName"],
                    zip_code=w["address"]["postalCode"],
                    province=w["address"]["territory"],
                ),
                phone=w.get("phone", ""),
                features=[s["name"][0]["value"] for s in w.get("services", [])],
            )
            for w in warehouse_data["warehouses"]
        ]

    def set_location(self, location: Union[Location, None]):
        if location:
            new_cookies = {
                "invCheckCity": location.address.city,
                "invCheckPostalCode": location.address.zip_code,
                "invCheckStateCode": location.address.province,
                "STORELOCATION": quote(
                    json.dumps(
                        {
                            "storeLocation": {
                                "zip": location.address.zip_code,
                                "city": location.address.city,
                            }
                        }
                    )
                ),
            }
            for name, value in new_cookies.items():
                self.session.cookies.set(name, value)
        else:
            self.session.cookies.clear()

    def suggest(self, search: str) -> list[str]:
        result = requests.get(
            "https://search.costco.com/api/apps/www_costco_com/query/www_costco_com_typeahead",
            headers={
                "Authorization": AUTOCOMPLETE_KEY,
                "Host": "search.costco.com",
                "Origin": "https://www.costco.com",
                "Referer": "https://www.costco.com/",
                "User-Agent": self.user_agent
            },
            params={
                "q": search,
                "loc": AUTOCOMPLETE_LOC,
                "rowsPerGroup": 10
            }
        )

        if result.status_code >= 300:
            raise ApiException(result)
        
        data = result.json()
        return [i["term"] for i in data["response"]["docs"] if i["type"] == "PopularSearch"]
