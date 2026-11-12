import argparse
import shutil
from pathlib import Path

CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".heic"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi", ".webm"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv", ".md"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Executables": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".iso"],
    "Code": [".py", ".js", ".html", ".css", ".json",".c", ".cpp", ".java"],
}

PROTECTED_FOLDERS = set(CATEGORIES.keys()) | {"Folders", "Miscellaneous"}


def get_unique_destination(dest_folder: Path, file_name: str) -> Path:
    """Prevents overwriting files if a file with the same name already exists."""
    destination = dest_folder / file_name
    if not destination.exists():
        return destination

    stem = destination.stem
    suffix = destination.suffix
    counter = 1
    while destination.exists():
        destination = dest_folder / f"{stem}_{counter}{suffix}"
        counter += 1
    return destination


def clean_directory(target_dir: Path):
    script_name = Path(__file__).name
    moved_count = 0

    for item in target_dir.iterdir():
        if item.name == script_name or item.name.startswith("."):
            continue

        if item.is_dir():
            if item.name in PROTECTED_FOLDERS:
                continue
            dest_folder = target_dir / "Folders"

        elif item.is_file():
            ext = item.suffix.lower()
            dest_folder = target_dir / "Miscellaneous"

            for category, extensions in CATEGORIES.items():
                if ext in extensions:
                    dest_folder = target_dir / category
                    break
        else:
            continue

        dest_folder.mkdir(exist_ok=True)

        final_destination = get_unique_destination(dest_folder, item.name)
        shutil.move(str(item), str(final_destination))
        moved_count += 1
        print(f"Moved: {item.name} -> {dest_folder.name}/")

    print(f"\nDone! Organized {moved_count} items in '{target_dir.name}'.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize files in a folder by category.")
    parser.add_argument(
        "path",
        nargs="?",  # Makes the argument optional so we can fall back to input()
        default=None,
        help="Path to the folder to clean (optional; prompts if omitted)",
    )
    args = parser.parse_args()

    if args.path is not None:
        raw_path = args.path.strip().strip('"').strip("'")
    else:
        raw_path = input("Please enter the folder path (press Enter for current folder): ").strip().strip('"').strip("'")

    directory = Path.cwd() if not raw_path else Path(raw_path).expanduser().resolve()

    if not directory.exists() or not directory.is_dir():
        print(f"Error: '{directory}' is not a valid directory.")
    else:
        clean_directory(directory)