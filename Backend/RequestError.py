import sys
class RequestError(Exception):
    """Exception raised when recieving an incorrect response type.

    Attributes:
        status_code : The status code of the request
    """

    def __init__(self, status_code):
        self.status_code = status_code
