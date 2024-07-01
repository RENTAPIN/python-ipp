# examples/settings.py
# pylint: disable=W0621
"""Configuration settings for Python client for IPP."""
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(".env")


# Set printer_url from the environment
printer_url = os.getenv("PRINTER_URL", "ipps://192.168.1.92:631/ipp/print")
