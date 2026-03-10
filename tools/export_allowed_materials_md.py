# tools/export_allowed_materials_md.py

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from bvillage.core.materials.material_registry import BASES, VARIANTS


OUT_PATH = Path("generated/BVILLAGE Allowed Materials List.md")


def build_index():
    grouped: dict[str, dict[str, list[str]]] = {}

    for mid in BASES:
        family = mid.split(".", 1)[0]
        grouped.setdefault(family, {"bases": [], "variants": []})
        grouped[family]["bases"].append(mid)

    for mid in VARIANTS:
        family = mid.split(".", 1)[0]
        grouped.setdefault(family, {"bases": [], "variants": []})
        grouped[family]["variants"].append(mid)

    for fam in grouped:
        grouped[fam]["bases"].sort()
        grouped[fam]["variants"].sort()

    return dict(sorted(grouped.items()))


def render_md(data):
    lines = []

    lines.append("# BVILLAGE Allowed Materials List\n")
    lines.append(
        "Canonical source: `bvillage.core.materials.material_registry`\n"
    )
    lines.append(
        "This document is automatically generated from the MaterialRegistry.\n"
    )

    for family, bucket in data.items():
        lines.append(f"\n## {family}\n")

        if bucket["bases"]:
            lines.append("**Bases**\n")
            for m in bucket["bases"]:
                lines.append(f"- `{m}`")
            lines.append("")

        if bucket["variants"]:
            lines.append("**Variants**\n")
            for m in bucket["variants"]:
                lines.append(f"- `{m}`")
            lines.append("")

    return "\n".join(lines)


def main():
    data = build_index()
    md = render_md(data)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(md, encoding="utf8")

    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
