import argparse
from collections.abc import Iterable
import os


class FileArgumentParser(Iterable):
    """
    Parses command-line arguments from a file.
    """

    def __init__(
        self, parser: argparse.ArgumentParser, file_path: str | bytes | os.PathLike
    ):
        self.parser = parser
        self.file_path = file_path

    def __iter__(self):
        return self

    def __next__(self):
        return self.parse_args()

    def parse_args(self, namespace: argparse.Namespace | None = None):
        with open(self.file_path, "r") as file:
            args = file.read().splitlines()
        self.args = self.parser.parse_args(args, namespace)
        return self.args


class CachedFileArgumentParser(FileArgumentParser):
    """
    Parses command-line arguments from a file, caching the last modified time.

    Note file timestamps have limited resolution.
    """

    def __init__(
        self, parser: argparse.ArgumentParser, file_path: str | bytes | os.PathLike
    ):
        super().__init__(parser, file_path)
        self.last_modified = 0

    def parse_args(self, namespace: argparse.Namespace | None = None):
        if os.path.getmtime(self.file_path) != self.last_modified:
            with open(self.file_path, "r") as file:
                self.last_modified = os.path.getmtime(self.file_path)
                args = file.read().splitlines()
            self.args = self.parser.parse_args(args, namespace)
        return self.args
