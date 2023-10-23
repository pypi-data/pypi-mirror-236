import sys
from typing import List, TextIO
from . import __version__
from .arguments import create_argument_parser, Arguments, Argument, Action
from .editor import Editor


def main(args: List[str] = sys.argv[1:]) -> None:
    parser = create_argument_parser()
    arguments = parser.parse_args(args, Arguments())

    if arguments.get_boolean(Argument.VERSION):
        print(f"{parser.prog} {__version__}")
        return

    action = arguments.get_string_optional(Argument.ACTION)
    if action is None:
        parser.error("Require action")
        return

    editor = Editor()
    filename = arguments.get_string(Argument.FILENAME)
    if filename == "-":
        if arguments.get_boolean(Argument.IN_PLACE):
            raise RuntimeError("Can not write to in place file while reading from stdin")
        with sys.stdin as stream:
            editor.read(stream)
    else:
        if arguments.get_boolean(Argument.IN_PLACE) and not arguments.get_string_optional(Argument.OUTPUT) is None:
            raise RuntimeError("Can not write to output file and in place simultaneously")
        with open(filename, mode="rt", encoding="utf-8") as stream:
            editor.read(stream)

    output: TextIO
    if not arguments.get_string_optional(Argument.OUTPUT) is None:
        output = open(arguments.get_string(Argument.OUTPUT), mode="wt", encoding="utf-8")
    elif arguments.get_boolean(Argument.IN_PLACE):
        output = open(filename, mode="wt", encoding="utf-8")
    else:
        output = sys.stdout

    with output as stream:
        action = arguments.get_string(Argument.ACTION)
        if action == Action.GET:
            output.write(
                editor.get(
                    arguments.get_string_optional(Argument.SECTION),
                    arguments.get_string_optional(Argument.KEY),
                    arguments.get_string(Argument.SEPARATOR),
                )
            )
        elif action == Action.SET:
            editor.set(
                arguments.get_string(Argument.SECTION),
                arguments.get_string(Argument.KEY),
                arguments.get_string(Argument.VALUE),
            )
            editor.write(stream)
        elif action == Action.DELETE:
            editor.delete(arguments.get_string(Argument.SECTION), arguments.get_string_optional(Argument.KEY))
            editor.write(output)
        elif action == Action.EXISTS:
            exists = editor.contains(
                arguments.get_string(Argument.SECTION), arguments.get_string_optional(Argument.KEY)
            )
            output.write("true" if exists else "false")
        else:
            raise RuntimeError(f'Action "{action}" does not exists')
