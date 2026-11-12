# Tidy

A simple, zero-dependency Python CLI tool that organizes messy folders by sorting files and subdirectories into clean categories (`Images`, `Videos`, `Audio`, `Documents`, `Archives`, `Executables`, `Code`, `Folders`, and `Miscellaneous`).

## How It Works
- **Dynamic Folders:** Only creates category folders when matching files are found.
- **Safe Moves:** Never overwrites files—duplicates are automatically renamed (e.g., `file_1.pdf`).
- **Smart Filtering:** Moves uncategorized subfolders into `Folders/` while ignoring hidden files (like `.git`) and existing category folders.

## Usage
Requires **Python 3.6+** (no external libraries needed).

```bash
# Clean a specific directory
python tidy.py ~/Downloads

# Clean the current directory immediately
python tidy.py .

# Interactive mode (prompts for a path, or press Enter for current folder)
python tidy.py
