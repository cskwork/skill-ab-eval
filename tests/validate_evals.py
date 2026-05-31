#!/usr/bin/env python3
"""Validate every examples/**/evals/evals.json against the schema. No credits used."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def validate(path: Path) -> list[str]:
    errs: list[str] = []
    doc = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(doc.get("skill_name"), str):
        errs.append("skill_name must be a string")
    evals = doc.get("evals")
    if not isinstance(evals, list) or not evals:
        return errs + ["evals must be a non-empty list"]
    seen: set[str] = set()
    for i, ev in enumerate(evals):
        where = f"evals[{i}]"
        for field in ("id", "prompt", "expected_output"):
            if not isinstance(ev.get(field), str) or not ev[field]:
                errs.append(f"{where}.{field} must be a non-empty string")
        if ev.get("id") in seen:
            errs.append(f"{where}.id duplicate: {ev.get('id')}")
        seen.add(ev.get("id"))
        asserts = ev.get("assertions")
        if not isinstance(asserts, list) or not all(isinstance(a, str) for a in asserts):
            errs.append(f"{where}.assertions must be a list of strings")
        if "files" in ev and not isinstance(ev["files"], list):
            errs.append(f"{where}.files must be a list")
    return errs


def main() -> int:
    files = sorted(ROOT.glob("examples/**/evals/evals.json"))
    if not files:
        print("no evals.json found under examples/")
        return 0
    failed = False
    for path in files:
        errs = validate(path)
        rel = path.relative_to(ROOT)
        if errs:
            failed = True
            print(f"FAIL {rel}")
            for e in errs:
                print(f"  - {e}")
        else:
            print(f"OK   {rel}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
