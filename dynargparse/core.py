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
        with open(self.file_path, "r") as file:
            self.last_modified = os.path.getmtime(self.file_path)
            args = file.read().splitlines()
        self.args = self.parser.parse_args(args)

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.file_path, "r") as file:
            args = file.read().splitlines()
        return self.parser.parse_args(args)
