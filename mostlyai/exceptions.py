class APIError(Exception):
    def __init__(
        self,
        message: str = None,
    ):
        self.message = message

    def __str__(self):
        return self.message


class APIStatusError(APIError):
    pass
