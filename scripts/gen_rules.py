"""Generate or verify RULES.md from the dddantic.rules catalog.

    python scripts/gen_rules.py --write   # regenerate RULES.md from the catalog
    python scripts/gen_rules.py --check   # fail if RULES.md is stale

RULES.md is derived data: never edit it by hand. Edit `dddantic.rules` and regenerate.
The conformance suite also fails if the committed file drifts from the catalog.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from dddantic.rules import render_rules_md

_DOC = Path(__file__).resolve().parents[1] / "RULES.md"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate RULES.md from dddantic.rules.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="fail if RULES.md is stale")
    mode.add_argument("--write", action="store_true", help="regenerate RULES.md")
    args = parser.parse_args()

    content = render_rules_md()
    if args.check:
        current = _DOC.read_text(encoding="utf-8") if _DOC.exists() else ""
        if current != content:
            print("RULES.md is stale. Run: python scripts/gen_rules.py --write")
            return 1
        print("RULES.md is up to date.")
        return 0
    _DOC.write_text(content, encoding="utf-8")
    print(f"wrote {_DOC}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
