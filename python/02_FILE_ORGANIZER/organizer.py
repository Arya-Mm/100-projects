from pathlib import Path
import shutil

folder = Path(r"C:\Users\aryam\Downloads")

Category_map = {
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
    for category, extensions in Category_map.items():
        if ext in extensions:
            return category
    return "others"


for file in folder.iterdir():

    if file.is_file():

        category = get_category(file.suffix)
        target_folder = folder / category
        target_folder.mkdir(exist_ok=True)
        destination = target_folder / file.name
        print(f"Moving → {file.name} → {category}/")
        shutil.move(str(file), str(destination))
