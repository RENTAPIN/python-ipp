# Python: Internet Printing Protocol (IPP) Client

Asynchronous Python client for Internet Printing Protocol (IPP).

## About

This package allows you to monitor printers that support the Internet Printing Protocol (IPP)
programmatically.

## Installation

This section contains an installation instruction from the global repository, and a second
installation instruction from a cloned (forked) local repository.

### Client Repository - Global

Points to the official source. This should be (*) sufficient to use pyipp in your project.

```sh
pip install pyipp
```

(*) should be, but unfortunately wasn't in my case. I had to make a few changes in a local repo.

A root cause was not yet found, but it appears that rebuilding `pyipp` with `poetry` and use a local
`pip install -e ..\python-ipp` solved the issue.

### PYIPP Repository - Local

Allows custom development - e.g. to fix a workaround to have better logging where jobs are not
printing.

The following set of well-known instruction for a fresh virtual environment:

```sh
python -m venv .venv
.venv\Scripts\activate
python.exe -m pip install --upgrade pip
```

But then, we need to install `poetry`, and use `poetry` to rebuild pyipp.

```sh
pip install poetry
poetry install
```

### Client Repository - Local

To use this local version of the pyipp package, we need to pip install it, using a local path.

1. first uninstall previous installs if they still exists
2. install from absolute path - relative path options are possible too!

```sh
pip uninstall pyipp
pip install -e d:\Repos\python-ipp
```

## Usage

```python
import asyncio

from pyipp import IPP, Printer


async def main():
    """Show example of connecting to your IPP print server."""
    async with IPP("ipps://EPSON123456.local:631/ipp/print") as ipp:
        printer: Printer = await ipp.printer()
        print(printer)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

## Setting up development environment

This Python project is fully managed using the [Poetry](https://python-poetry.org) dependency
manager. But also relies on the use of NodeJS for certain checks during
development.

You need at least:

- Python 3.9+
- [Poetry](https://python-poetry.org/docs/#installation)
- NodeJS 20+ (including NPM)

To install all packages, including all development requirements:

```bash
npm install
poetry install
```

As this repository uses the [pre-commit](https://pre-commit.com/) framework, all changes
are linted and tested with each commit. You can run all checks and tests
manually, using the following command:

```bash
poetry run pre-commit run --all-files
```

To run just the Python tests:

```bash
poetry run pytest
```
