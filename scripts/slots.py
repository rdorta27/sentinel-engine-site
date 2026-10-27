#!/usr/bin/env python3
"""Write the number slots of the pages from site/numbers.json.

numbers.json is written in sentinel-engine (scripts/site_numbers.py) from the
frozen summary.json runs and copied here. This script only formats it.

    python3 scripts/slots.py          # rewrite the slots of every page
    python3 scripts/slots.py --check  # exit 1 if a slot is stale
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from paths import NUMBERS, ROOT, SITE  # noqa: E402


def load() -> dict:
    return json.loads(NUMBERS.read_text())


def rounded(entry: dict) -> str:
    """A reading form for a large count: 79,191 becomes 79,000+ and 390.8 becomes 390+."""
    value = entry["value"]
    if isinstance(value, (int, float)) and value >= 1000:
        return f"{int(value) // 1000 * 1000:,}+"
    if isinstance(value, (int, float)) and value >= 100:
        return f"{int(value) // 10 * 10:,}+"
    return entry["text"]


# <span data-num="id">, data-num-round="id", data-num-type="id" and
# data-num-den="id" hold no nested tags. The script writes their text from
# numbers.json. data-num-round shows a large count in a reading form (79,000+).
SLOT = re.compile(
    r'(<(\w+)[^>]*?\bdata-(num|num-round|num-type|num-den)="(\w+)"[^>]*>)(.*?)(</\2>)',
    re.S,
)

TYPE_NAMES = {
    "es-419": {"Test suite": "Suite de pruebas", "Simulation": "Simulación", "Synthetic": "Sintético", "Projection": "Proyección"},
    "pt-br": {"Test suite": "Suíte de testes", "Simulation": "Simulação", "Synthetic": "Sintético", "Projection": "Projeção"},
}


def loc(text: str, lang: str) -> str:
    """Decimal comma and thousands point for Portuguese. English and Spanish keep the point."""
    return text.translate(str.maketrans(",.", ".,")) if lang == "pt-br" else text


def slot_text(numbers: dict, kind: str, key: str, lang: str = "en") -> str:
    entry = numbers[key]
    if kind == "num":
        return loc(entry["text"], lang)
    if kind == "num-round":
        return loc(rounded(entry), lang)
    if kind == "num-type":
        return TYPE_NAMES.get(lang, {}).get(entry["type"], entry["type"])
    return loc(f"{int(entry['denominator']):,}", lang)


def page_lang(page: Path, site: Path = SITE) -> str:
    first = page.relative_to(site).parts[0]
    return first if first in ("es-419", "pt-br") else "en"


def fill(text: str, numbers: dict, lang: str) -> str:
    return SLOT.sub(lambda m: m.group(1) + slot_text(numbers, m.group(3), m.group(4), lang) + m.group(6), text)


def sync_pages(data: dict, site: Path = SITE) -> list[Path]:
    """Rewrite the text of each number slot. Return the pages that changed."""
    changed = []
    for page in sorted(site.rglob("*.html")):
        old = page.read_text()
        new = fill(old, data["numbers"], page_lang(page, site))
        if new != old:
            page.write_text(new)
            changed.append(page)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = load()
    if args.check:
        stale = [p for p in sorted(SITE.rglob("*.html")) if fill(p.read_text(), data["numbers"], page_lang(p)) != p.read_text()]
        for page in stale:
            print(f"stale number in {page.relative_to(ROOT)}")
        if stale:
            print("The pages are stale. Run scripts/slots.py.")
            return 1
        print("The number slots are current.")
        return 0
    pages = sync_pages(data)
    print(f"updated {len(pages)} page(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
