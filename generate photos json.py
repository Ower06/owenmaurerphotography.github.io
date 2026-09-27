"""
Generates photos.json for an album by listing every image file
inside that album's "main" subfolder.

Assumes the fixed structure: photos/<album-title>/main/<filename>
photos.json is written into photos/<album-title>/ (the parent of "main"),
matching what album.html fetches.

Usage:
    python generate_photos_json.py photos/huskies

This scans photos/huskies/main/ for image files and writes
photos/huskies/photos.json with full relative src paths like
"photos/huskies/main/img001.jpg".
"""

import sys
import json
from pathlib import Path

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

def generate_photos_json(album_folder_path):
    album_folder = Path(album_folder_path)
    main_folder = album_folder / "main"

    if not main_folder.is_dir():
        print(f"Error: '{main_folder}' is not a valid folder.")
        sys.exit(1)

    album_slug = album_folder.name  # e.g. "huskies" from "photos/huskies"

    # Grab every image file in main/, sorted alphabetically
    # (so img001, img002, ... come out in order)
    image_files = sorted(
        f.name for f in main_folder.iterdir()
        if f.suffix.lower() in IMAGE_EXTENSIONS
    )

    if not image_files:
        print(f"No image files found in '{main_folder}'.")
        return

    # Build the list of {"src": "..."} objects with the full relative
    # path your album.html expects: photos/<album>/main/<filename>
    photos_data = [
        {"src": f"photos/{album_slug}/main/{filename}"}
        for filename in image_files
    ]

    output_path = album_folder / "photos.json"
    with open(output_path, "w") as f:
        json.dump(photos_data, f, indent=2)

    print(f"Wrote {len(photos_data)} entries to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_photos_json.py <album_folder_path>")
        print("Example: python generate_photos_json.py photos/huskies")
        sys.exit(1)

    generate_photos_json(sys.argv[1])
