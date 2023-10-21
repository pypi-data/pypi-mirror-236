"""Example tests."""

from pathlib import Path

from xyrha_flush.example import example_function


def test_example_function() -> None:
    expected_result = 42
    result = example_function()
    assert result == expected_result


def test_use_test_resource(resource_dir: Path) -> None:
    assert resource_dir.joinpath("example_resource.txt").is_file()
