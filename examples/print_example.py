# pylint: disable=W0621
"""Asynchronous Python client for IPP."""
import asyncio
from pathlib import Path

from pyipp import IPP
from pyipp.enums import IppOperation
from settings import printer_url


async def execute_print_job(content: bytes, document_format: str) -> None:
    """Show example of executing operation against your IPP print server."""
    async with IPP(printer_url) as ipp:
        response = await ipp.execute(
            IppOperation.PRINT_JOB,
            {
                "operation-attributes-tag": {
                    "requesting-user-name": "Me",
                    "job-name": "My Test Job",
                    "document-format": document_format,
                },
                "data": content,
            },
        )

        print(response)


if __name__ == "__main__":
    document_format = "text/plain"  # "application/pdf" for pdf, etc.
    file_name = __file__  # just print this file as an example
    with Path(file_name).open("rb") as f:
        content = f.read()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(execute_print_job(content, document_format))
