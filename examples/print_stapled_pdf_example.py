# pylint: disable=W0621,C0411
"""Asynchronous Python client for IPP."""
import asyncio
import logging
from pathlib import Path

from pyipp import IPP
from pyipp.enums import IppFinishing, IppOperation
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
                "job-attributes-tag": {
                    "finishings": IppFinishing.STAPLE_TOP_LEFT,
                },
                "data": content,
            },
        )

        print(response)


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    DOCUMENT_FORMAT = "application/pdf"
    FILE_NAME = __file__  # const: just print this file as an example
    with Path(FILE_NAME).open("rb") as f:
        content = f.read()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(execute_print_job(content, DOCUMENT_FORMAT))
