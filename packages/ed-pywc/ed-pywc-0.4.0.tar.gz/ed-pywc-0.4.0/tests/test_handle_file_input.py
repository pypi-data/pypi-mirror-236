import pathlib

import click
from click.testing import CliRunner

from pywc.main import handle_file_input


def test_handle_file_with_file_input(tmpdir):
    file_path = pathlib.Path.cwd() / "tests" / "docs_for_tests" / "test.txt"

    content, source_name = handle_file_input(file_path)

    assert "The Project Gutenberg eBook of The Art of War" in content
    assert source_name == "test.txt"


def test_handle_file_with_stdin():
    runner = CliRunner()

    @click.command()
    def mock_wc():
        content, source_name = handle_file_input()
        click.echo(content)
        click.echo(source_name)

    result = runner.invoke(mock_wc, input="Hello from stdin!")

    assert "Hello from stdin!" in result.output
    assert "stdin" in result.output
    assert result.exit_code == 0
