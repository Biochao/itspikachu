#!/usr/bin/env python3
"""
Generate images.json listing image paths (relative to the HTML file) for the gallery.
Usage: python3 generate_images_manifest.py
"""
import os
import json

ROOT = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(ROOT, 'images')
OUT_FILE = os.path.join(ROOT, 'images.json')

def is_image(filename):
    return filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'))

def is_silhouette(filename):
    # silhouette files end with _1 before the extension
    low = filename.lower()
    return any(low.endswith(suf) for suf in (
        '_1.jpg', '_1.jpeg', '_1.png', '_1.gif', '_1.webp', '_1.svg'
    ))

def main():
    if not os.path.isdir(IMAGES_DIR):
        print('images/ directory not found in', ROOT)
        return

    # Walk subdirectories in images/ and group silhouette files by immediate folder name
    seasons = {}
    # Include files directly under images/ as 'root'
    root_files = []
    for entry in os.listdir(IMAGES_DIR):
        full = os.path.join(IMAGES_DIR, entry)
        if os.path.isdir(full):
            season_name = entry
            season_list = []
            for subentry in os.listdir(full):
                if is_image(subentry) and is_silhouette(subentry):
                    season_list.append(os.path.join('images', season_name, subentry))
            season_list.sort()
            if season_list:
                seasons[season_name] = season_list
        else:
            # file directly in images/
            if is_image(entry) and is_silhouette(entry):
                root_files.append(os.path.join('images', entry))

    root_files.sort()
    if root_files:
        seasons['root'] = root_files

    # Write a JSON object mapping season folder -> list of files
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(seasons, f, ensure_ascii=False, indent=2)

    total = sum(len(v) for v in seasons.values())
    print(f'Wrote {total} entries across {len(seasons)} seasons to {OUT_FILE}')

if __name__ == '__main__':
    main()
