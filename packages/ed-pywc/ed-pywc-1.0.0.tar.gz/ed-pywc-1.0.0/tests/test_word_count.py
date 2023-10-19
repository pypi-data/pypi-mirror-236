import pathlib

from click.testing import CliRunner

from pywc.main import wc


def test_word_count():
    file_path = pathlib.Path.cwd() / "tests" / "docs_for_tests" / "test.txt"

    runner = CliRunner()
    result = runner.invoke(wc, ["-w", str(file_path)])

    assert result.exit_code == 0
    assert "58164" in result.output


def test_word_count_empty_file(tmpdir):
    # Create an empty file
    file_path = tmpdir.join("empty_words.txt")
    file_path.ensure()

    runner = CliRunner()
    result = runner.invoke(wc, ["-w", str(file_path)])

    assert result.exit_code == 0
    assert "0" in result.output


def test_word_count_multiple_spaces(tmpdir):
    # Create a sample file with multiple spaces between words
    sample_content = "Hello  World   This   has  extra  spaces"
    file_path = tmpdir.join("sample_spaces.txt")
    with open(file_path, "w") as f:
        f.write(sample_content)

    runner = CliRunner()
    result = runner.invoke(wc, ["-w", str(file_path)])

    assert result.exit_code == 0
    assert "6" in result.output
