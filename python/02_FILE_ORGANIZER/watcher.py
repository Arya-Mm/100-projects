from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import time
import shutil

WATCH_FOLDER = Path(r"C:\Users\aryam\Downloads")

CATEGORY_MAP = {
    "images": ["jpg", "jpeg", "png", "gif", "svg"],
    "videos": ["mp4", "mkv", "mov"],
    "documents": ["pdf", "docx", "pptx", "txt"],
    "audio": ["mp3", "wav"],
    "archives": ["zip", "rar", "7z", "tar", "gz"],
    "installers": ["exe", "msi"],
    "torrents": ["torrent"],
    "code": ["py", "ipynb"],
}


def get_category(extension):
    ext = extension.replace(".", "").lower()
    for category, exts in CATEGORY_MAP.items():
        if ext in exts:
            return category
    return "others"

def move_file(file_path):
    file = Path(file_path)

    if not file.is_file():
        return

    category = get_category(file.suffix)
    target_folder = WATCH_FOLDER / category
    target_folder.mkdir(exist_ok=True)

    destination = target_folder / file.name

    if destination.exists():
        destination = target_folder / f"copy_{int(time.time())}_{file.name}"

    shutil.move(str(file), str(destination))

    print(f"[MOVED] {file.name} → {category}/")


class DownloadEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        """
        Triggered when a new file is created in the folder.
        """
        if not event.is_directory:
            time.sleep(1)   # Give time for file to finish downloading
            move_file(event.src_path)


if __name__ == "__main__":
    print("Watching folder:", WATCH_FOLDER)
    print("Auto-organizing in real-time...\n")

    event_handler = DownloadEventHandler()
    observer = Observer()
    observer.schedule(event_handler, str(WATCH_FOLDER), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
