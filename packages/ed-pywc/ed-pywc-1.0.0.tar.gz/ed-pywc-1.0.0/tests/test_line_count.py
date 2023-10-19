import pathlib

from click.testing import CliRunner

from pywc.main import wc


def test_line_count_of_file():
    file_path = pathlib.Path.cwd() / "tests" / "docs_for_tests" / "test.txt"

    runner = CliRunner()
    result = runner.invoke(wc, ["-l", str(file_path)])

    assert result.exit_code == 0
    assert "7144" in result.output


def test_byte_count_of_non_existent_file(tmpdir):
    # Create an empty file
    file_path = tmpdir.join("empty.txt")
    file_path.ensure()
    runner = CliRunner()
    result = runner.invoke(wc, ["-l", str(file_path)])

    assert result.exit_code == 0
    assert "0" in result.output
