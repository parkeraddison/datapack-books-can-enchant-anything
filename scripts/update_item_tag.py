#!/usr/bin/env python3
"""
Regenerate data/bcea/tags/item/all.json from a vanilla client jar.

Every item in the game has an item model definition at
assets/minecraft/items/<name>.json (since the 1.21.2 item model rework), so
that directory listing is used as the authoritative item list. "air" has a
model file too (used for the empty-hand item model) but isn't a real,
enchantable item, so it's excluded explicitly.

Usage:
    python3 scripts/update_item_tag.py /path/to/client.jar
"""
import json
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TAG_PATH = REPO_ROOT / "data" / "bcea" / "tags" / "item" / "all.json"
ITEMS_PREFIX = "assets/minecraft/items/"


def extract_item_ids(jar_path: Path) -> list[str]:
    ids = []
    with zipfile.ZipFile(jar_path) as jar:
        for name in jar.namelist():
            if not name.startswith(ITEMS_PREFIX) or not name.endswith(".json"):
                continue
            item_name = name[len(ITEMS_PREFIX):-len(".json")]
            if not item_name or item_name == "air":
                continue
            ids.append(f"minecraft:{item_name}")
    return sorted(set(ids))


def main() -> None:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} /path/to/client.jar", file=sys.stderr)
        sys.exit(1)

    jar_path = Path(sys.argv[1])
    if not jar_path.is_file():
        print(f"error: {jar_path} is not a file", file=sys.stderr)
        sys.exit(1)

    item_ids = extract_item_ids(jar_path)
    if not item_ids:
        print("error: found no items under assets/minecraft/items/ in the jar", file=sys.stderr)
        sys.exit(1)

    TAG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(TAG_PATH, "w") as f:
        json.dump({"values": item_ids}, f, indent=2)
        f.write("\n")

    print(f"wrote {len(item_ids)} items to {TAG_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
