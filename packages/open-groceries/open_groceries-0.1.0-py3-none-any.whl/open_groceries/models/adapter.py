from . import GroceryItem, Location
from typing import Any

class GroceryAdapter:
    def __init__(self, user_agent: str = "") -> None:
        pass
    
    def search_groceries(self, search: str) -> list[GroceryItem]:
        raise NotImplementedError
    
    def get_grocery_item(self, id: str) -> GroceryItem:
        raise NotImplementedError
    
    def get_locations(self, near: str) -> list[Location]:
        raise NotImplementedError
    
    def set_location(self, location: Location):
        raise NotImplementedError
    
    def suggest(self, search: str) -> list[str]:
        raise NotImplementedError