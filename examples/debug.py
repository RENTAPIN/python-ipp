# pylint: disable=W0621
"""Asynchronous Python client for IPP."""
import asyncio

from pyipp import IPP
from pyipp.enums import IppOperation
from settings import printer_url


async def main() -> None:
    """Show example of connecting to your IPP print server."""
    async with IPP(printer_url) as ipp:
        response = await ipp.raw(
            IppOperation.GET_PRINTER_ATTRIBUTES,
            {
                "version": (2, 0),  # try (1, 1) for older devices
                "operation-attributes-tag": {
                    "requested-attributes": [
                        "printer-device-id",
                        "printer-name",
                        "printer-type",
                        "printer-location",
                        "printer-info",
                        "printer-make-and-model",
                        "printer-state",
                        "printer-state-message",
                        "printer-state-reason",
                        "printer-supply",
                        "printer-up-time",
                        "printer-uri-supported",
                        "device-uri",
                        "printer-is-shared",
                        "printer-more-info",
                        "printer-firmware-string-version",
                        "marker-colors",
                        "marker-high-levels",
                        "marker-levels",
                        "marker-low-levels",
                        "marker-names",
                        "marker-types",
                    ],
                },
            },
        )

        with open("printer-attributes.bin", "wb") as file:  # noqa: PTH123, ASYNC101
            file.write(response)
            file.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
