import csv
import json
from pathlib import Path

FIELDS = [
    "device_name",
    "version",
    "provider",
    "driver_date",
    "device_class",
    "manufacturer",
    "signed",
    "health",
    "reason",
]

def export_csv(rows, path):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    return target

def export_json(rows, path):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    return target
