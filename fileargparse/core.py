import argparse
from collections.abc import Iterable
import os
import typing


class FileArgumentParser(Iterable):
    """
    Parses command-line arguments from a file.
    """

    def __init__(
        self,
        parser: argparse.ArgumentParser,
        file_path: typing.Union[str, bytes, os.PathLike],
        default_on_file_not_found: bool = False,
    ):
        self.parser = parser
        self.file_path = file_path
        self.default_on_file_not_found = default_on_file_not_found

    def __iter__(self):
        return self

    def __next__(self):
        return self.parse_args()

    def parse_args(self, namespace: typing.Union[argparse.Namespace, None] = None):
        args = self._get_raw_args()
        print(args)
        return self.parser.parse_args(args, namespace)

    def _get_raw_args(self) -> None | list[str]:
        try:
            with open(self.file_path, "r") as file:
                args = file.read().splitlines()
        except FileNotFoundError as e:
            if self.default_on_file_not_found:
                return None
            raise e
        return args


class CachedFileArgumentParser(FileArgumentParser):
    """
    Parses command-line arguments from a file, caching the last modified time.

    Note file timestamps have limited resolution.
    """

    def __init__(
        self,
        parser: argparse.ArgumentParser,
        file_path: str | bytes | os.PathLike,
        default_on_file_not_found: bool = False,
    ):
        super().__init__(parser, file_path, default_on_file_not_found)
        self.last_modified = 0
        self.args = None

    def parse_args(self, namespace: argparse.Namespace | None = None):
        if self.args is None or self._getmtime() != self.last_modified:
            self.last_modified = self._getmtime()
            self.args = super().parse_args(namespace)
        return self.args

    def _getmtime(self) -> float:
        try:
            return os.path.getmtime(self.file_path)
        except FileNotFoundError as e:
            if self.default_on_file_not_found:
                return 0
            raise e
