#!/usr/bin/env python3
"""
Convert the TTP CatA/B/C results workbook into data.json for the dashboard.

Usage:
    python scripts/xlsx_to_json.py <input.xlsx> <output.json>

Assumes the same layout as the original file:
  - Row 1: citation labels (only over the method columns)
  - Row 2: method names (columns J..? onward)
  - Row 3+: one row per instance, columns A..I are metadata:
        Classe, Category, Folder, TSP Base, Cities (n), Item Multiplier,
        Num Items, KP Type, Instance Name
    columns J.. onward: one score per method.

The LAST populated method column is treated as "yours" and gets
" (Ours)" appended to its name (unless already present), so it is
highlighted in the dashboard. If you add more literature methods,
insert their columns BEFORE your own column so it stays last.
"""
import re
import sys
import json
import pathlib
import openpyxl

# strips emoji / pictographs while keeping letters, digits, and common
# method-name punctuation (+ * . - _ ( ) and spaces)
_EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF\U00002190-\U000021FF]+"
)

METADATA_COLS = ["class", "category", "folder", "base", "cities",
                  "multiplier", "numItems", "kpType", "name"]
FIRST_METHOD_COL_INDEX = 9  # 0-based; column J


def clean(text):
    if text is None:
        return None
    # drop non-printable / emoji-ish trailing characters, collapse whitespace
    cleaned = "".join(ch for ch in str(text) if ch.isprintable())
    cleaned = _EMOJI_RE.sub("", cleaned).strip()
    return cleaned


def main():
    src = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(
        "ttp_literature_catABC_results_updated.xlsx")
    out = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else pathlib.Path("data.json")

    wb = openpyxl.load_workbook(src, data_only=True)
    ws = wb[wb.sheetnames[0]]
    rows = list(ws.iter_rows(values_only=True))

    header_names = rows[1]  # row 2: method names
    method_idxs = [i for i in range(FIRST_METHOD_COL_INDEX, len(header_names))
                   if header_names[i] not in (None, "")]
    method_names = [clean(header_names[i]) for i in method_idxs]

    if not method_names:
        raise SystemExit("No method columns found — check the sheet layout.")

    if "(Ours)" not in method_names[-1]:
        method_names[-1] = f"{method_names[-1]} (Ours)"

    records = []
    for r in rows[2:]:
        if r[0] is None:
            continue
        record = dict(zip(METADATA_COLS, r[:9]))
        values = {}
        for name, idx in zip(method_names, method_idxs):
            v = r[idx] if idx < len(r) else None
            values[name] = float(v) if isinstance(v, (int, float)) else None
        record["values"] = values
        records.append(record)

    out.write_text(json.dumps(records, ensure_ascii=False))
    print(f"Wrote {len(records)} instances x {len(method_names)} methods -> {out}")
    print(f"Methods: {method_names}")


if __name__ == "__main__":
    main()
