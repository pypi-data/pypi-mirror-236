from configparser import ConfigParser
from typing import TextIO, Optional

__all__ = ["Editor"]


class Editor:
    def __init__(self) -> None:
        self._config = ConfigParser()

    def __repr__(self) -> str:
        return f"Editor(config={self._config})"

    def read(self, stream: TextIO) -> None:
        self._config.read_file(stream)

    def write(self, stream: TextIO) -> None:
        self._config.write(stream)

    def get(self, section: Optional[str], key: Optional[str], separator: str) -> str:
        if section is None:
            return separator.join(self._config.sections())
        if key is None:
            return separator.join(self._config.options(section))
        return self._config.get(section, key)

    def set(self, section: str, key: str, value: str) -> None:
        if not self._config.has_section(section):
            self._config.add_section(section)
        self._config.set(section, key, value)

    def delete(self, section: str, key: Optional[str]) -> None:
        if key is None:
            if self._config.has_section(section):
                self._config.remove_section(section)
            return
        if self._config.has_option(section, key):
            self._config.remove_option(section, key)

    def contains(self, section: str, key: Optional[str]) -> bool:
        if key is None:
            return self._config.has_section(section)
        return self._config.has_option(section, key)
