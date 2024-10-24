# examples/settings.py
# pylint: disable=W0621
"""Configuration settings for Python client for IPP."""
import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
if Path(".env").exists():
    load_dotenv(".env")


# Set printer_url from the environment
printer_url = os.getenv("PRINTER_URL", "")

print(printer_url)
