from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    raise ValueError("GROQ_API_KEY not found - check your .env file")

BASE_DIR = Path("invoices")
INBOX_DIR = BASE_DIR / "inbox"
LOG_FILE = BASE_DIR / "sorting_log.txt"

CATEGORIES = ["electricity", "food", "rent", "internet", "miscellaneous"]

FOLDERS = {
    "electricity":      BASE_DIR / "Electricity",
    "food":             BASE_DIR / "Food",
    "rent":             BASE_DIR / "Rent",
    "internet":         BASE_DIR / "Internet",
    "miscellaneous":    BASE_DIR / "Miscellaneous"
}

def setup_folders():
    for folder in FOLDERS.values():
        folder.mkdir(parents=True, exist_ok=True)
    print("Folders ready...\n")

if __name__ == "__main__":
    setup_folders()
    print(f"Watching: {INBOX_DIR}")
    print(f"Categories: {CATEGORIES}")
    print(f"API key loaded: {'yes' if API_KEY else 'no'}")