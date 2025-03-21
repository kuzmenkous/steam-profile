import os

from dotenv import load_dotenv

from ..exceptions.helpers import (
    DotenvListException,
    DotenvStrokeException,
    DotenvLoadException,
)


DEV_DOTENV = ".env.dev"
PROD_DOTENV = ".env.prod"


class DotenvListHelper:
    """Class for getting a list from a string value in a .env file"""

    @staticmethod
    def _assemble_list(value: str) -> list[str]:
        try:
            return [v.strip() for v in value.strip("[]").split(",") if v]
        except ValueError:
            raise DotenvListException()

    @staticmethod
    def _assemble_stroke(value: str) -> list[str]:
        try:
            return [v.strip() for v in value.split(",") if v]
        except ValueError:
            raise DotenvStrokeException()

    @classmethod
    def get_list_from_value(cls, value: str) -> list[str]:
        if value.startswith("[") and value.endswith("]"):
            return cls._assemble_list(value)
        return cls._assemble_stroke(value)


def load_environment():
    # Load the main .env file
    mode = os.getenv("MODE", "DEV")

    # Determine the environment based on the MODE variable
    env_file: str = DEV_DOTENV if mode == "DEV" else PROD_DOTENV

    try:
        load_dotenv(dotenv_path=env_file)
    except IOError:
        raise DotenvLoadException(env_file)
