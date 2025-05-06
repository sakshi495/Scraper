import json
from pathlib import Path

def load_urls_from_json(file_path: Path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return [item["url"] for item in data]

def save_json(data: dict, path: Path):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
