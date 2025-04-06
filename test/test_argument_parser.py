import tempfile
from time import sleep
import pytest
from argparse import ArgumentParser
from fileargparse.core import FileArgumentParser


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


def test_modified(basic_parser: ArgumentParser):
    ITERATIONS = 3
    FILE_TIMESTAMP_RESOLUTION_S = 3
    with tempfile.NamedTemporaryFile("w") as f:
        f.write("0\n")
        f.seek(0)
        for expect, next, args in zip(
            range(ITERATIONS),
            range(1, ITERATIONS + 1),
            FileArgumentParser(basic_parser, f.name),
        ):
            sleep(FILE_TIMESTAMP_RESOLUTION_S)
            assert args.first_positional == str(expect)
            f.write(f"{next}\n")
            f.seek(0)
