import tempfile
import pytest
from argparse import ArgumentParser
from dynargparse.core import FileArgumentParser


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
    with tempfile.NamedTemporaryFile("w") as f:
        f.write("0\n")
        f.seek(0)
        for expect, next, args in zip(range(3), range(1, 4), FileArgumentParser(basic_parser, f.name)):
            assert args.first_positional == str(expect)
            f.write(f"{next}\n")
            f.seek(0)
