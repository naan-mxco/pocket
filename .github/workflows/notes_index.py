import os
import json
import re
from urllib.parse import quote
from bs4 import BeautifulSoup

BASE_URL = "https://naan-mxco.github.io/pocket/"
NOTES_DIR = "notes"
OUTPUT_FILE = "notes_index.json"

def extract_note_data(file_path):
    filename = os.path.basename(file_path)
    print(f"Opening {filename}")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

            # Extract title
            h2 = soup.select_one(".note h2") or soup.select_one(".notehead h2")
            if h2:
                title = h2.get_text(strip=True)
                print("h2 found")
            else:
                note_div = soup.select_one(".note[data-title]")
                if note_div:
                    title = note_div.get("data-title", "").strip()
                    print("h2 not found, data-title found")
                else:
                    title_tag = soup.title
                    if title_tag:
                        title = title_tag.get_text(strip=True)
                        print("h2 and data-title not found, using <title>")
                    else:
                        title = ""
                        print("h2, data-title, and <title> not found, title left empty")

            # Extract date: first from <h4>, fallback to filename
            date = None
            h4 = soup.select_one(".note h4") or soup.select_one(".notehead h4")
            if h4:
                m = re.search(r'(\d{2})(\d{2})-AD(\d{4})', h4.get_text(strip=True))
                if m:
                    day, month, year = m.groups()
                    date = f"{year}-{month}-{day}"
                    print(f"date found from h4: {date}")
            if not date:
                m = re.search(r'note-(\d{2})(\d{2})(\d{2,4})\.html', filename)
                if m:
                    day, month, year = m.groups()
                    if len(year) == 2:
                        year = "20" + year
                    date = f"{year}-{month}-{day}"
                    print(f"date found from filename: {date}")
                else:
                    print("date not found in h4 or filename")

            # Relative path and URL
            rel_path = os.path.relpath(file_path).replace("\\", "/")
            url_path = quote(rel_path)
            url = BASE_URL + url_path

            print(f"file indexed: {filename}, {title}, {date}\n")

            return {
                "filename": filename,
                "title": title,
                "date": date if date else "",
                "path": rel_path,
                "url": url
            }

    except Exception as e:
        print(f"Failed to parse {filename}: {e}")
        return None

def scan_notes(directory):
    notes_dict = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".html"):
                file_path = os.path.join(root, file)
                note_data = extract_note_data(file_path)
                if note_data:
                    # Use filename as unique key to prevent duplicates
                    notes_dict[note_data["filename"]] = note_data
    return list(notes_dict.values())

def main():
    notes = scan_notes(NOTES_DIR)
    notes_sorted = sorted(notes, key=lambda x: x["date"] or "")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(notes_sorted, f, indent=4, ensure_ascii=False)
    print(f"\nAll notes indexed: {len(notes_sorted)} entries written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
