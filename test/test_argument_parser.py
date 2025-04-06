import io
import os
import tempfile
from time import sleep
import pytest
from argparse import ArgumentParser
from fileargparse import CachedFileArgumentParser, FileArgumentParser

FILE_TIMESTAMP_RESOLUTION_S = 0.1

NON_EXISTANT_PATH = "test/missing.txt"
assert (
    os.path.exists(NON_EXISTANT_PATH) is False
), f"Path {NON_EXISTANT_PATH} should not exist"


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
    with pytest.raises(FileNotFoundError):
        _ = FileArgumentParser(
            basic_parser,
            NON_EXISTANT_PATH,
        ).parse_args()


@pytest.mark.parametrize(
    "cls",
    [
        FileArgumentParser,
        CachedFileArgumentParser,
    ],
)
def test_modified_cached(basic_parser: ArgumentParser, cls: type):
    ITERATIONS = 3
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


@pytest.mark.parametrize(
    "cls",
    [
        (FileArgumentParser),
        (CachedFileArgumentParser),
    ],
)
def test_file_not_found(
    monkeypatch: pytest.MonkeyPatch,
    basic_parser: ArgumentParser,
    cls: type,
):
    monkeypatch.setattr("sys.argv", ["python", "mock_std_input"])
    for i, args in zip(
        range(3),
        cls(
            basic_parser,
            NON_EXISTANT_PATH,
            default_on_file_not_found=True,
        ),
    ):
        assert args.first_positional == "mock_std_input"


@pytest.mark.parametrize(
    "cls",
    [
        (FileArgumentParser),
        (CachedFileArgumentParser),
    ],
)
def test_file_creation(
    monkeypatch: pytest.MonkeyPatch,
    basic_parser: ArgumentParser,
    cls: type,
):
    monkeypatch.setattr("sys.argv", ["python", "mock_std_input"])
    parser: FileArgumentParser = cls(
        basic_parser,
        NON_EXISTANT_PATH,
        default_on_file_not_found=True,
    )
    assert parser.parse_args().first_positional == "mock_std_input"
    with tempfile.NamedTemporaryFile("w") as f:
        parser.file_path = f.name
        f.write("0\n")
        f.seek(0)
        for i, args in zip(
            range(3),
            parser,
        ):
            sleep(FILE_TIMESTAMP_RESOLUTION_S)
            assert args.first_positional == str(i)
            f.write(f"{i+1}\n")
            f.seek(0)
    parser.file_path = NON_EXISTANT_PATH
    assert parser.parse_args().first_positional == "mock_std_input"
