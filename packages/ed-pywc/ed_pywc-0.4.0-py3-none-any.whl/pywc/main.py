import os
from typing import Optional, Tuple

import click


def handle_file_input(file: Optional[os.PathLike] = None) -> Tuple[str, str]:
    """
    Retrieve content from a given file or stdin if no file is specified.

    Returns:
        tuple:
            content (str): The content of the file or stdin.
            source_name (str): The base name of the file or 'stdin' if data was read from stdin.
    """

    if file:
        with open(file, "r") as f:
            content = f.read()
        source_name = os.path.basename(file)
    else:
        content = click.get_text_stream("stdin").read()
        source_name = "stdin"

    return content, source_name


@click.command(
    help="""
A Python-based version of the UNIX wc command which counts lines, words, and bytes in a file.

\b
Examples:
    wc --lines sample.txt      # Counts lines in sample.txt
    wc --words sample.txt      # Counts words in sample.txt
    wc --bytes sample.txt      # Counts bytes in sample.txt
    wc sample.txt              # Counts lines, words, and bytes in sample.txt
"""
)
@click.option(
    "-l",
    "--lines",
    is_flag=True,
    help="Count the number of lines in the specified file.",
)
@click.option(
    "-w",
    "--words",
    is_flag=True,
    help="Count the number of words in the specified file.",
)
@click.option(
    "-c",
    "--bytes",
    "bytes_",
    is_flag=True,
    help="Count the number of bytes in the specified file.",
)
@click.argument("file", type=click.Path(exists=True, readable=True), required=False)
def wc(lines, words, bytes_, file):
    """Command logic remains the same as before."""
    content, file_basename = handle_file_input(file)

    if lines:
        line_count = len(content.splitlines())
        click.echo(f"{line_count} {file_basename}")

    if words:
        word_count = len(content.split())
        click.echo(f"{word_count} {file_basename}")

    if bytes_:
        byte_count = len(content.encode("utf-8"))
        click.echo(f"{byte_count} {file_basename}")

    if not (lines or words or bytes_):  # If no options are provided, show all counts.
        line_count = len(content.splitlines())
        word_count = len(content.split())
        byte_count = len(content.encode("utf-8"))
        click.echo(
            f"Lines: {line_count} Words: {word_count} Bytes: {byte_count} {file_basename}"
        )


if __name__ == "__main__":
    wc()
