from typing import Literal, Union
from difflib import get_close_matches
import requests
from models import *
from exceptions import *
from adapters import *
from concurrent.futures import ThreadPoolExecutor, as_completed
from adapters.wegmans import WG_MAP

ADAPTER_TYPES = Literal["wegmans", "costco"]
ADAPTERS = ["wegmans", "costco"]

ADAPTER_MAP: dict[ADAPTER_TYPES, GroceryAdapter] = {
    "wegmans": Wegmans,
    "costco": Costco,
}

__all__ = ["OpenGrocery", "Wegmans", "Costco", "Location", "Address", "LatLong", "ApiException"]

class OpenGrocery:
    def __init__(
        self,
        features: list[ADAPTER_TYPES] = ADAPTERS,
        user_agent: str = "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0",
        adapter_kwargs: dict[ADAPTER_TYPES, dict] = {},
    ) -> None:
        """Initialize main class

        Args:
            features (list[ADAPTER_TYPES], optional): List of adapters to initialize. Defaults to ADAPTERS.
            user_agent (str, optional): User agent string. Defaults to "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0".
            adapter_kwargs (dict[ADAPTER_TYPES, dict], optional): Adapter kwargs. Defaults to {}.
        """
        self.user_agent = user_agent
        self.adapters: dict[str, GroceryAdapter] = {
            k: v(user_agent=user_agent, **(adapter_kwargs.get(k, {})))
            for k, v in ADAPTER_MAP.items()
            if k in features
        }

    def _execute_mass(self, func: str, include: list[ADAPTER_TYPES], *args, threads: int = 6, flatten: bool = False, **kwargs) -> list:
        results = []
        with ThreadPoolExecutor(max_workers=threads) as executor:
            tasks = [executor.submit(getattr(self.adapters[i], func), *args, **kwargs) for i in self.adapters.keys() if i in include]
            for task in as_completed(tasks):
                if flatten:
                    results.extend(task.result())
                else:
                    results.append(task.result())
        return results
    
    def _get_position(self, near: str) -> LatLong:
        map_result = requests.get(
            f"https://api.mapbox.com/geocoding/v5/mapbox.places/{near.lower()}.json",
            params={"country": "us,ca", "access_token": WG_MAP},
            headers={
                "Host": "api.mapbox.com",
                "Origin": "https://shop.wegmans.com",
                "Referer": "https://shop.wegmans.com/",
                "User-Agent": self.user_agent,
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
        return position
        

    def locations(self, near: str, include: list[ADAPTER_TYPES] = ADAPTERS) -> list[Location]:
        """Get locations near an address, sorted by distance

        Args:
            near (str): Address
            include (list[ADAPTER_TYPES], optional): Adapters to include. Defaults to ADAPTERS.

        Returns:
            list[Location]: List of Location objects, in order of distance
        """
        current_position = self._get_position(near)
        results = self._execute_mass("get_locations", include, near, flatten=True)
        return sorted(results, key=lambda x: current_position.distance_to(x.location))
    
    def set_nearest_stores(self, near: str, include: list[ADAPTER_TYPES] = ADAPTERS):
        """Set each adapter to the nearest store to an address

        Args:
            near (str): Address
            include (list[ADAPTER_TYPES], optional): Adapters to include. Defaults to ADAPTERS.
        """
        locations: dict[ADAPTER_TYPES, Location] = {}
        all_near = self.locations(near, include=include)
        for loc in all_near:
            if not locations.get(loc.type) and loc.type in include:
                locations[loc.type] = loc
        
        for adapter, location in locations.items():
            if self.adapters.get(adapter):
                self.adapters[adapter].set_location(location)

    def set_locations(self, locations: dict[ADAPTER_TYPES, Location]):
        """Set each adapter to a specific location

        Args:
            locations (dict[ADAPTER_TYPES, Location]): Mapping of adapter: location
        """
        for adapter, location in locations.items():
            if self.adapters.get(adapter):
                self.adapters[adapter].set_location(location)

    def search(self, query: str, include: list[ADAPTER_TYPES] = ADAPTERS) -> list[GroceryItem]:
        """Search all adapters for a query

        Args:
            query (str): Search query
            include (list[ADAPTER_TYPES], optional): Adapters to include. Defaults to ADAPTERS.

        Returns:
            list[GroceryItem]: List of results, sorted by name similarity to query
        """
        results: list[GroceryItem] = self._execute_mass("search_groceries", include, query, flatten=True)
        match_order = get_close_matches(query.lower(), [i.name.lower() for i in results], n=len(results), cutoff=0)
        return sorted(results, key=lambda x: match_order.index(x.name.lower()))
    
    def adapter(self, adapter: ADAPTER_TYPES) -> Union[GroceryAdapter, None]:
        """Utility function to get a specific adapter

        Args:
            adapter (ADAPTER_TYPES): Adapter name

        Returns:
            Union[GroceryAdapter, None]: Adapter, or None if not initialized
        """
        return self.adapters.get(adapter)
    
    def suggest(self, term: str, include: list[ADAPTER_TYPES] = ADAPTERS) -> list[str]:
        """Get autocompletion results for a search term

        Args:
            term (str): Search term
            include (list[ADAPTER_TYPES], optional): Adapters to include. Defaults to ADAPTERS.

        Returns:
            list[str]: List of suggestions in order of similarity
        """
        results: list[GroceryItem] = list(set(self._execute_mass("suggest", include, term, flatten=True)))
        match_order = get_close_matches(term.lower(), [i.lower() for i in results], n=len(results), cutoff=0)
        return sorted(results, key=lambda x: match_order.index(x.lower()))
