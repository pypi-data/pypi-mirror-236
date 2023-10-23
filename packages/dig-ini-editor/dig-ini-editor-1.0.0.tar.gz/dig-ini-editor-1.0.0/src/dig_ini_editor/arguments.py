from argparse import ArgumentParser, Namespace
from enum import Enum
from typing import Optional

__all__ = ["create_argument_parser", "Action", "Argument", "Arguments"]


class Action(str, Enum):
    GET = "get"
    SET = "set"
    EXISTS = "exists"
    DELETE = "delete"

    def __str__(self) -> str:
        if isinstance(self, str):
            return self
        return str(self)


class Argument(str, Enum):
    ACTION = "action"
    IN_PLACE = "in_place"
    FILENAME = "filename"
    SECTION = "section"
    KEY = "key"
    VALUE = "value"
    OUTPUT = "output"
    SEPARATOR = "separator"
    VERSION = "version"

    def __str__(self) -> str:
        if isinstance(self, str):
            return self
        return str(self)


class Arguments(Namespace):
    def get_boolean_optional(self, key: str) -> Optional[bool]:
        if not hasattr(self, key):
            return None
        value = getattr(self, key)
        if not isinstance(value, bool):
            return None
        return value

    def get_boolean(self, key: str, default: bool = False) -> bool:
        value = self.get_boolean_optional(key)
        if value is None:
            return default
        return value

    def get_string_optional(self, key: str) -> Optional[str]:
        if not hasattr(self, key):
            return None
        value = getattr(self, key)
        if isinstance(value, str):
            return value
        if isinstance(value, list) and len(value) >= 1:
            if isinstance(value[0], str):
                return value[0]
        return None

    def get_string(self, key: str, default: str = "") -> str:
        value = self.get_string_optional(key)
        if value is None:
            return default
        return value


ARG_IN_PLACE = Argument.IN_PLACE.replace("_", "-")


def _add_argument_in_place(parser: ArgumentParser) -> None:
    parser.add_argument(
        f"-{ARG_IN_PLACE[0]}", f"--{ARG_IN_PLACE}", action="store_true", help="Apply output directly into input file"
    )


def _add_argument_output(parser: ArgumentParser) -> None:
    parser.add_argument(
        f"-{Argument.OUTPUT[0]}", f"--{Argument.OUTPUT}", action="store", help="Filename to write the output"
    )


def _add_argument_filename(parser: ArgumentParser) -> None:
    parser.add_argument(Argument.FILENAME, nargs=1, help="INI file to be read")


def create_argument_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Command line INI editor")
    parser.add_argument(f"--{Argument.VERSION}", action="store_true", help="Show current version")
    subparser = parser.add_subparsers(title=Argument.ACTION, dest=Argument.ACTION)

    description = "Get section list or key list or key value"
    action_get = subparser.add_parser(Action.GET, aliases=[Action.GET[0]], description=description, help=description)
    _add_argument_output(action_get)
    _add_argument_filename(action_get)
    action_get.add_argument(
        f"-{Argument.SEPARATOR[0]}",
        f"--{Argument.SEPARATOR}",
        action="store",
        default="\n",
        help="Separator used when listing. Default: \\n",
    )
    action_get.add_argument(
        Argument.SECTION,
        nargs="?",
        default=None,
        help="Section of INI to be used. If not set, will return a list of sections",
    )
    action_get.add_argument(
        Argument.KEY,
        nargs="?",
        default=None,
        help="Key of INI to be used. If not set, will return a list of keys from section",
    )

    description = "Edit INI file, applying <value> to the corresponding <section> and <key>"
    action_set = subparser.add_parser(Action.SET, aliases=[Action.SET[0]], description=description, help=description)
    _add_argument_in_place(action_set)
    _add_argument_output(action_set)
    _add_argument_filename(action_set)
    action_set.add_argument(Argument.SECTION, nargs=1, help="Section to be written into. Will be created if not exists")
    action_set.add_argument(Argument.KEY, nargs=1, help="Key to be written into. Will be created if not exists")
    action_set.add_argument(Argument.VALUE, nargs=1, help="Value to be written")

    description = "Edit INI file, removing <key> from <section> or entire <section>"
    action_delete = subparser.add_parser(
        Action.DELETE, aliases=[Action.DELETE[0]], description=description, help=description
    )
    _add_argument_in_place(action_delete)
    _add_argument_output(action_delete)
    _add_argument_filename(action_delete)
    action_delete.add_argument(Argument.SECTION, nargs=1, help="Section to be used or deleted")
    action_delete.add_argument(
        Argument.KEY, nargs="?", default=None, help="Key to be deleted. If not set, entire section will be deleted"
    )

    description = 'Check if section and/or key exists. Return "false" and process exits with non-zero if not exists'
    action_exists = subparser.add_parser(
        Action.EXISTS, aliases=[Action.EXISTS[0]], description=description, help=description
    )
    _add_argument_output(action_exists)
    _add_argument_filename(action_exists)
    action_exists.add_argument(Argument.SECTION, nargs=1, help="Section to be checked")
    action_exists.add_argument(
        Argument.KEY, nargs="?", default=None, help="Key to be checked. If not set, only section will be checked."
    )
    return parser
