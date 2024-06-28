# pylint: disable=W0621
"""Asynchronous Python client for IPP."""
import asyncio
from pathlib import Path

from pyipp import IPP
from pyipp.enums import IppOperation


async def execute_print_job(content: bytes) -> None:
    """Show example of executing operation against your IPP print server."""
    async with IPP("ipp://192.168.1.92:631/ipp/print") as ipp:
        response = await ipp.execute(
            IppOperation.PRINT_JOB,
            {
                "operation-attributes-tag": {
                    "requesting-user-name": "Me",
                    "job-name": "My Test Job",
                    "document-format": "application/pdf",
                },
                "data": content,
            },
        )

        print(response)


if __name__ == "__main__":
    pdf_file = "/path/to/pdf.pfd"
    with Path(pdf_file).open("rb") as f:
        content = f.read()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(execute_print_job(content))
