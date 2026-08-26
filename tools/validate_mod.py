"""Runs the release checklist against mod/.

    python tools/validate_mod.py

Exits non-zero if any check fails, so it can gate a commit or a release.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ccp.checks import ALL_CHECKS, Report

REPO_ROOT = Path(__file__).resolve().parent.parent
MOD_DIR = REPO_ROOT / "mod"


def main() -> int:
    if not MOD_DIR.is_dir():
        print("mod/ not found", file=sys.stderr)
        return 2

    overall = Report()
    width = max(len(name) for name, _ in ALL_CHECKS)

    for name, check in ALL_CHECKS:
        report = Report()
        check(REPO_ROOT, MOD_DIR, report)
        status = "PASS" if report.ok else "FAIL"
        if report.ok and report.warnings:
            status = "WARN"
        print(f"  {name:<{width}}  {status}")
        for message in report.errors:
            print(f"      error: {message}")
        for message in report.warnings:
            print(f"      warn:  {message}")
        overall.errors += report.errors
        overall.warnings += report.warnings

    print()
    if overall.ok:
        print(f"All checks passed ({len(overall.warnings)} warning(s)).")
        return 0
    print(f"{len(overall.errors)} error(s), {len(overall.warnings)} warning(s).")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
