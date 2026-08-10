#!/usr/bin/env python3
"""
Regenerate data/minecraft/enchantment/*.json from a vanilla client jar.

For every vanilla enchantment definition this pulls the file fresh from the
jar (so effects/costs/predicates always match the target game version) and
only touches two things:

  - If the vanilla file has no explicit "primary_items" (i.e. it relies on
    "supported_items" as the implicit primary pool), that original
    "supported_items" value is preserved as an explicit "primary_items" so
    enchanting-table offers stay vanilla-accurate.
  - "supported_items" is then replaced with "#bcea:all" so anvil/`/enchant`
    can put the enchantment on anything.

Any enchantment .json previously present in this pack but no longer present
in the jar (removed upstream) is left untouched and reported, since deleting
it automatically could be wrong (e.g. it should stay for backward pack
compatibility, or should not exist).

Usage:
    python3 scripts/update_enchantments.py /path/to/client.jar
"""
import json
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ENCHANTMENT_DIR = REPO_ROOT / "data" / "minecraft" / "enchantment"
JAR_PREFIX = "data/minecraft/enchantment/"
SUPPORTED_ITEMS_OVERRIDE = "#bcea:all"


def main() -> None:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} /path/to/client.jar", file=sys.stderr)
        sys.exit(1)

    jar_path = Path(sys.argv[1])
    if not jar_path.is_file():
        print(f"error: {jar_path} is not a file", file=sys.stderr)
        sys.exit(1)

    ENCHANTMENT_DIR.mkdir(parents=True, exist_ok=True)
    existing = {p.name for p in ENCHANTMENT_DIR.glob("*.json")}
    seen = set()

    with zipfile.ZipFile(jar_path) as jar:
        names = [
            n for n in jar.namelist()
            if n.startswith(JAR_PREFIX) and n.endswith(".json")
        ]
        if not names:
            print("error: found no enchantments under data/minecraft/enchantment/ in the jar", file=sys.stderr)
            sys.exit(1)

        for name in sorted(names):
            filename = name[len(JAR_PREFIX):]
            seen.add(filename)
            data = json.loads(jar.read(name))

            if "primary_items" not in data:
                data["primary_items"] = data["supported_items"]
            data["supported_items"] = SUPPORTED_ITEMS_OVERRIDE

            out_path = ENCHANTMENT_DIR / filename
            with open(out_path, "w") as f:
                json.dump(data, f, indent=2, sort_keys=True)
                f.write("\n")

    print(f"wrote {len(seen)} enchantments to {ENCHANTMENT_DIR.relative_to(REPO_ROOT)}")

    stale = existing - seen
    if stale:
        print("note: these files exist in the pack but not in the jar (left untouched):")
        for filename in sorted(stale):
            print(f"  {filename}")


if __name__ == "__main__":
    main()
