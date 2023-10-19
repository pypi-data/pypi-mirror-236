PYWC
====

Python implementation of the UNIX wc (Word Count) utility

https://pypi.org/project/ed-pywc/

---

## Installation and Usage

Installation
```shell
pip install ed-pywc
```

Usage
```shell
Usage: pywc [OPTIONS] [FILE]

  A Python-based version of the UNIX wc command which counts lines, words, and
  bytes in a file.

  Examples:
      pywc --lines sample.txt      # Counts lines in sample.txt
      pywc --words sample.txt      # Counts words in sample.txt
      pywc --bytes sample.txt      # Counts bytes in sample.txt
      pywc sample.txt              # Counts lines, words, and bytes in sample.txt
      cat sample.txt | pywc        # Pipe the output of another command as input

Options:
  -l, --lines  Count the number of lines in the specified file.
  -w, --words  Count the number of words in the specified file.
  -c, --bytes  Count the number of bytes in the specified file.
  --help       Show this message and exit.

```

---

## Development Setup
[Development Setup](docs/development_setup.md)

---

## Publish
[Publishing to Pypi](docs/publishing_to_pypi.md)
