import os
import pathlib

from click.testing import CliRunner

from pywc.main import wc


def test_byte_count_of_file():
    file_path = pathlib.Path.cwd() / "tests" / "docs_for_tests" / "test.txt"

    runner = CliRunner()
    result = runner.invoke(wc, ["-c", str(file_path)])

    assert result.exit_code == 0
    assert result.output.strip() == f"{os.stat(file_path).st_size} test.txt"


def test_byte_count_of_non_existent_file():
    runner = CliRunner()
    result = runner.invoke(wc, ["-c", "non_existent.txt"])

    assert result.exit_code != 0
    assert "Error" in result.output
