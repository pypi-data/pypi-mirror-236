import pathlib

from click.testing import CliRunner

from pywc.main import wc


def test_all_counts():
    file_path = pathlib.Path.cwd() / "tests" / "docs_for_tests" / "test.txt"

    runner = CliRunner()

    result = runner.invoke(wc, [str(file_path)])
    assert result.exit_code == 0
    assert "Lines: 7144 Words: 58164 Bytes: 334998" in result.output
