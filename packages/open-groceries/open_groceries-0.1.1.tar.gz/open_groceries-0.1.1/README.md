# open-groceries

Unified data acquisition across multiple grocery store sites

## Installation

```bash
python3 -m pip install open-groceries
```

## Example Usage

```python
from open_groceries import OpenGrocery

# Initialize adapter clients
client = OpenGrocery()

# Print locations near Times Square
print(client.locations("Times Square NYC"))

# Print search results for "beans"
print(client.search("beans"))

# Print search suggestions for "pot"
print(client.suggest("pot"))
```

## API Documentation

**OpenGrocery:**

The OpenGrocery class is an aggregator for all included adapters. Function/constructor signatures are as follows:

- `OpenGrocery(features = ..., user_agent = ..., adapter_kwargs = ...)`

  - `features`: Optional `str[]`, list of adapter names to initialize.
  - `user_agent`: Optional `str`, user-agent string to pass to APIs.
  - `adapter_kwargs`: Optional `{str: {str: any}}`, mapping of `adapter:{kwargs}` for individual adapter kwargs
- `OpenGrocery().locations(near, include = ...) -> Location[]`: Fetches locations near an address

  - `near`: Required `str`, address to query.
    - Example formats: `"14620"`, `"Times Square NYC"`, `"Rochester Institute of Technology"`
  - `include`: Optional `str[]`, list of adapters to query. Skips any that aren't initialized
  - Returns `Location[]` in order of distance to specified address
- `OpenGrocery().set_nearest_stores(near, include = ...) -> None`: Sets each adapter to its nearest store

  - `near`: Required `str`, address to query.
    - Example formats: `"14620"`, `"Times Square NYC"`, `"Rochester Institute of Technology"`
  - `include`: Optional `str[]`, list of adapters to query. Skips any that aren't initialized
- `OpenGrocery().set_locations(locations) -> None`: Sets each adapter to a specific store

  - `locations`: Required `{str: Location}`, mapping of adapter name to desired location. This function does not check whether the input location is valid for that adapter.
- `OpenGrocery().search(query, include = ...) -> GroceryItem[]`: Searches adapters for a search query

  - `query`: Required `str`, search term to look for
  - `include`: Optional `str[]`, list of adapters to query. Skips any that aren't initialized
  - Returns `GroceryItem[]` in order of similarity to the search term
- `OpenGrocery().adapter(adapter) -> GroceryAdapter | None`: Utility function to return an initialized adapter

  - `adapter`: Required `str`, name of adapter to get
  - Returns specified `GroceryAdapter` if found, or `None` if not
- `OpenGrocery().suggest(term, include = ...) -> str[]`: Gets autocompletion suggestions to search term

  - `term`: Required `str`, search term to suggest for
  - `include`: Optional `str[]`, list of adapters to query. Skips any that aren't initialized
  - Returns `str[]` in order of similarity to search term

**GroceryAdapter:**

The GroceryAdapter class is the abstract parent of all included Adapters. It shoul not be initialized itself, but should instead be subclassed to create Adapters.

- `GroceryAdapter(user_agent = ...)`

  - `user_agent`: Optional `str`, user agent header to send to APIs
- `GroceryAdapter().search_groceries(search) -> GroceryItem[]`: Search for groceries

  - `search`: Required `str`, search term to look for
  - Returns `GroceryItem[]` in the order returned by the website
- `GroceryAdapter().get_grocery_item(id) -> GroceryItem`: Gets a specific grocery item by ID

  - `id`: Required `str`, item ID to return
  - Returns `GroceryItem` returned by the website
- `GroceryAdapter().get_locations(near) -> Location[]`: Gets store locations near an address

  - `near`: Required `str`, address to query.
    - Example formats: `"14620"`, `"Times Square NYC"`, `"Rochester Institute of Technology"`
  - Returns `Location[]` in the order returned by the website
- `GroceryAdapter().set_location(location) -> None`: Sets preferred store location

  - `location`: Required `Location`, location to set
- `GroceryAdapter().suggest(search) -> str[]`: Gets autocomplete suggestions for a search term

  - `term`: Required `str`, search term to suggest for
  - Returns `str[]` in order returned by the website

## Supported Stores

| Store   | Item Search                                 | Item Retrieval                              | Location Search                                   | Location Filtering       | Autocomplete                                      |
| ------- | ------------------------------------------- | ------------------------------------------- | ------------------------------------------------- | ------------------------ | ------------------------------------------------- |
| Wegmans | Full support [Long Term/Versioned API]      | Full support [Long Term/Versioned API]      | Full support [Medium Term/External Versioned API] | Full Support [Long Term] | Full support [Medium Term/External Versioned API] |
| Costco  | Adequate support [Medium Term/Site Parsing] | Adequate support [Medium Term/Site Parsing] | Full support [Medium Term/External Versioned API] | Full Support [Long Term] | Full support [Long Term/Versioned API]            |
