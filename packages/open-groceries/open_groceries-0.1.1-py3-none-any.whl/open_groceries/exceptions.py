from requests.exceptions import RequestException
from requests import Response

class ApiException(RequestException):
    def __init__(self, response: Response) -> None:
        super().__init__(request=response.request, response=response)
        self.status_code = response.status_code
        self.data = response.text

    def __str__(self) -> str:
        return f"API Error: {self.request.url} : {self.status_code}\n\n{self.data}"