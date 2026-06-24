"""
Nightly backup of Family Trips photos from Firebase to a local folder.

Reads the `photos` collection via the Firestore REST API (public read is allowed
by our security rules) and downloads each image to:

    ~/Documents/FamilyTrips-PhotoBackups/<trip>/day<N>/<filename>

Already-downloaded files are skipped, so it's safe to run every night.
No credentials needed beyond the public web API key.
"""

import os
import json
import urllib.request
import urllib.parse
from datetime import datetime

PROJECT = "familytrips-25e63"
API_KEY = "AIzaSyA4ojG1eRrvEhaPwyA0Vca-6AD2mfzTbqo"
TRIPS   = ["norway-2026"]          # add future trip ids here

DEST_ROOT = os.path.join(os.path.expanduser("~"), "Documents", "FamilyTrips-PhotoBackups")
REST = f"https://firestore.googleapis.com/v1/projects/{PROJECT}/databases/(default)/documents/photos"


def fetch_photo_docs():
    """Return all photo docs from Firestore via REST (handles pagination)."""
    docs, page = [], None
    while True:
        url = REST + f"?key={API_KEY}&pageSize=300"
        if page:
            url += f"&pageToken={urllib.parse.quote(page)}"
        with urllib.request.urlopen(url, timeout=30) as r:
            data = json.load(r)
        for d in data.get("documents", []):
            f = d.get("fields", {})
            docs.append({
                "url":  f.get("url",  {}).get("stringValue"),
                "name": f.get("name", {}).get("stringValue") or (d["name"].split("/")[-1] + ".jpg"),
                "day":  f.get("day",  {}).get("integerValue") or f.get("day", {}).get("doubleValue") or "0",
                "trip": f.get("trip", {}).get("stringValue") or "",
            })
        page = data.get("nextPageToken")
        if not page:
            break
    return docs


def main():
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{stamp}] Family Trips photo backup starting…")
    try:
        docs = fetch_photo_docs()
    except Exception as e:
        print(f"  ERROR fetching photo list: {e}")
        return

    new_count = total = 0
    for d in docs:
        if d["trip"] not in TRIPS or not d["url"]:
            continue
        total += 1
        folder = os.path.join(DEST_ROOT, d["trip"], f"day{d['day']}")
        os.makedirs(folder, exist_ok=True)
        safe = "".join(c if c.isalnum() or c in "._-" else "_" for c in d["name"])
        out = os.path.join(folder, safe)
        if os.path.exists(out):
            continue
        try:
            urllib.request.urlretrieve(d["url"], out)
            new_count += 1
            print(f"  + {d['trip']}/day{d['day']}/{safe}")
        except Exception as e:
            print(f"  ! failed: {safe} ({e})")

    print(f"[{stamp}] Done. {new_count} new of {total} photo(s). Backups in: {DEST_ROOT}")


if __name__ == "__main__":
    main()
