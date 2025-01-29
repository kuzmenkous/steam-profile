from typing import Optional


class BaseCustomException(Exception):
    error = None  # attribute to store the base error message for exception class

    def __init__(self, message: Optional[str] = None):
        if not message:
            message = self.error
        self.message = message
        super().__init__(message)
