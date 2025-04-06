import tempfile
from time import sleep
import pytest
from argparse import ArgumentParser
from fileargparse import CachedFileArgumentParser, FileArgumentParser


@pytest.fixture
def basic_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "first_positional",
    )
    return parser


def test_static(basic_parser: ArgumentParser):
    for i, args in zip(range(3), FileArgumentParser(basic_parser, "test/example.txt")):
        assert args.first_positional == str("abc123")


@pytest.mark.parametrize(
    "cls",
    [
        FileArgumentParser,
        CachedFileArgumentParser,
    ],
)
def test_modified_cached(basic_parser: ArgumentParser, cls: type):
    ITERATIONS = 3
    FILE_TIMESTAMP_RESOLUTION_S = 3
    with tempfile.NamedTemporaryFile("w") as f:
        f.write("0\n")
        f.seek(0)
        for expect, next, args in zip(
            range(ITERATIONS),
            range(1, ITERATIONS + 1),
            cls(basic_parser, f.name),
        ):
            if cls == CachedFileArgumentParser:
                sleep(FILE_TIMESTAMP_RESOLUTION_S)
            assert args.first_positional == str(expect)
            f.write(f"{next}\n")
            f.seek(0)
