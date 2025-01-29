from .base import BaseCustomException


class DotenvException(BaseCustomException):
    pass


class DotenvListException(DotenvException):
    error = "Could not parse list from environment variable"


class DotenvStrokeException(DotenvException):
    error = "Could not parse stroke from environment variable"


class DotenvLoadException(DotenvException):
    error = "Could not load environment file {env_file}"

    def __init__(self, env_file: str):
        super().__init__(self.error.format(env_file=env_file))
