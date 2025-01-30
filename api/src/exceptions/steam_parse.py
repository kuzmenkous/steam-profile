from .base import BaseCustomException


class SteamParseException(BaseCustomException):
    pass


class SteamParseDownloadWebsiteException(SteamParseException):
    error = "Error while downloading website"
