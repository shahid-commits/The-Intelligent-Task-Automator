import pdfplumber
from config import INBOX_DIR

def extract_text(filepath, max_pages=2, max_chars=1500):
    full_text = ""                              # accumulator - we add each page's text here

    with pdfplumber.open(filepath) as pdf:      # open pdf at filepath, with:- auto-close when done
        for page in pdf.pages[:max_pages]:      # only read first 2 pages (max_pages=2)
            page_text = page.extract_text()     # returns str or None
            if page_text:                       # checks the content inside file is text (not blank/image pages)
                full_text += page_text + "\n"   # append with line break

    return full_text.strip()[:max_chars]        # strip removes accidental whitespaces, max_chars (count of characters specified)

if __name__ == "__main__":
    from pathlib import Path                    # only needed here for the test - not in production

    test_files = list(INBOX_DIR.glob("*.pdf"))  # find all pdf files in inbox

    if not test_files:                          # a clear message for user if no PDF's found
        print(f"No PDF's found in invoices/inbox/")
        print(f"Drop a PDF in there then run this again.")
    else:
        for filepath in test_files:             # loop through every pdf found
            print(f"\nFile: {filepath.name}")
            text = extract_text(filepath)       # call the function
            if text:                                # if text came back non-empty
                print(f"Extracted {len(text)} chars")
                print(f"Preview: {text[:200]}")     # show first 200 characters only
            else:
                print(f"No text extracted - possibly a Scanned PDF")