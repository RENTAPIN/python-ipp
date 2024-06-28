# examples/settings.py
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(".env")


# Set printer_url from the environment
printer_url = os.getenv("PRINTER_URL", "ipps://192.168.1.92:631/ipp/print")
