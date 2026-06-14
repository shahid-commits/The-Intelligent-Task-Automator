import shutil                                           # moves files on disk
import time                                             # sleep between loop ticks
from pathlib import Path                                # file path operations
from watchdog.observers import Observer                 # monitors the inbox folder
from watchdog.events import FileSystemEventHandler      # base class for the handler
from datetime import date                               # for today's date in renamed file

from config import setup_folders, INBOX_DIR, LOG_FILE, FOLDERS  # config file
from pdf_reader import extract_text                             # pdf_reader file
from ai_classifier import get_category                          # ai_classifier file

def log_action(filename, category):
    # append one timestamped line to the log file
    entry = f"{category} | {filename}\n"
    with open(LOG_FILE, "a") as f:          # "a" = append, never overwrites
        f.write(entry)
    print(f"Logged: {entry.strip()}")

def build_new_name(filepath, category):
    # get today's date as a string: 2026-06-12
    today = date.today().isoformat()

    # clean the original stem - lowercase + underscores instead of spaces
    clean_stem = filepath.stem.lower().replace(" ", "_")

    # combine all three parts into the new filename
    new_name = f"{category}_{today}_{clean_stem}.pdf"

    return new_name

def sort_file(filepath, category):
    filepath = Path(filepath)               # ensure it's a Path object

    # get destination folder from dictionary - no if/else required
    dest_folder = FOLDERS[category]
    dest_folder.mkdir(parents=True, exist_ok=True)      # create if missing

    new_name = build_new_name(filepath, category)       # build the clean new name
    destination = dest_folder / new_name                # use new name as destination

    shutil.move(str(filepath), str(destination))                # physically move the file
    print(f"Moved: {new_name} -> {dest_folder.name}/")

    log_action(new_name, category)         # record what happened

class InvoiceHandler(FileSystemEventHandler):
    def on_created(self, event):
        # watchdog fires for folders too - ignore those
        if event.is_directory:
            return
        
        # ignore anything that isn't a PDF
        if not event.src_path.endswith(".pdf"):
            return
        
        # wait 1 second - file may still be copying into the folder
        time.sleep(1)

        # Step 1 - extract text from PDF
        filepath = Path(event.src_path)
        print(f"\nNew invoice detected: {filepath.name}")

        text = extract_text(filepath)
        if not text:
            print("No text found - moving to Miscellaneous")
            sort_file(filepath, "miscellaneous")
            return
        
        # Step 2 - ask AI for the category
        category = get_category(text)
        print(f"Category: {category}")

        # Step 3 - move file to the right folder
        sort_file(filepath, category)

def start_watcher():
    setup_folders()                 # ensure all category folders exist

    handler = InvoiceHandler()      # custom event handler
    observer = Observer()           # watchdog's folder monitor
    observer.daemon = True          # thread dies cleanly when main script exits
    observer.schedule(
        handler,
        path = str(INBOX_DIR),      # watch the inbox folder
        recursive = False           # don't watch subfolders
    )

    observer.start()
    print(f"Watching: {INBOX_DIR}")
    print(f"Drop a PDF into invoices/inbox/ to sort it.")
    print(f"Press Ctrl + C to stop.\n")

    try:
        while True:
            time.sleep(1)           # keep script alive
    except KeyboardInterrupt:
        print("\nStopping watcher...")
        observer.stop()               # signal observer to stop

    observer.join()                 # wait for thread to finish
    print("Done.")

if __name__ == "__main__":
    start_watcher()                 # run only when executed directly