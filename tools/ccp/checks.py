"""Release checklist implemented as individual, independently reportable checks."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

SCRIPT_SUFFIXES = {".txt", ".gui", ".gfx", ".mod"}

WORKSHOP_PAYLOAD_DIR = "mod"

FORBIDDEN_IN_PAYLOAD = re.compile(r"\.(md|py|yml\.bak)$|(^|/)\.git", re.IGNORECASE)

PLACEHOLDER_WORDS = re.compile(r"\b(TODO|FIXME|XXX|coming soon|placeholder|lorem ipsum)\b", re.IGNORECASE)

LOC_KEY = re.compile(r"^\s*([A-Za-z0-9_.@\-]+):\s*\d*\s*\"", re.MULTILINE)

GENERATED_BANNER = "# GENERATED FILE - DO NOT EDIT"


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    @property
    def ok(self) -> bool:
        return not self.errors


def _script_files(mod_dir: Path) -> list[Path]:
    return [
        path
        for path in sorted(mod_dir.rglob("*"))
        if path.is_file() and path.suffix in SCRIPT_SUFFIXES
    ]


def _strip_comments_and_strings(text: str) -> str:
    out: list[str] = []
    for line in text.splitlines():
        stripped: list[str] = []
        in_string = False
        for char in line:
            if char == '"':
                in_string = not in_string
                continue
            if char == "#" and not in_string:
                break
            if not in_string:
                stripped.append(char)
        out.append("".join(stripped))
    return "\n".join(out)


def check_braces(mod_dir: Path, report: Report) -> None:
    for path in _script_files(mod_dir):
        body = _strip_comments_and_strings(path.read_text(encoding="utf-8-sig", errors="replace"))
        depth = 0
        for number, line in enumerate(body.splitlines(), start=1):
            depth += line.count("{") - line.count("}")
            if depth < 0:
                report.error(f"{path}: unbalanced closing brace at line {number}")
                break
        else:
            if depth != 0:
                report.error(f"{path}: {depth} unclosed brace(s)")


def check_descriptor(mod_dir: Path, report: Report) -> None:
    descriptor = mod_dir / "descriptor.mod"
    if not descriptor.is_file():
        report.error("mod/descriptor.mod is missing")
        return

    text = descriptor.read_text(encoding="utf-8-sig")
    for required in ("name", "supported_version", "tags"):
        if not re.search(rf"^\s*{required}\s*=", text, re.MULTILINE):
            report.error(f"descriptor.mod: missing `{required}`")

    version = re.search(r'supported_version\s*=\s*"([^"]+)"', text)
    if version and not re.fullmatch(r"\d+\.\d+(\.\*|\.\d+)?(\.\*)?|\d+\.\*", version.group(1)):
        report.warn(f"descriptor.mod: unusual supported_version `{version.group(1)}`")


def check_payload_is_clean(repo_root: Path, report: Report) -> None:
    mod_dir = repo_root / WORKSHOP_PAYLOAD_DIR
    for path in sorted(mod_dir.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(mod_dir).as_posix()
        if FORBIDDEN_IN_PAYLOAD.search(relative):
            report.error(f"mod/{relative} must not ship to the Workshop")


def check_no_placeholders(mod_dir: Path, report: Report) -> None:
    targets = _script_files(mod_dir) + sorted(mod_dir.rglob("*.yml"))
    for path in targets:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        for number, line in enumerate(text.splitlines(), start=1):
            if PLACEHOLDER_WORDS.search(line):
                report.error(f"{path}:{number}: placeholder text `{line.strip()}`")


def check_generated_banners(mod_dir: Path, report: Report) -> None:
    for path in sorted(mod_dir.rglob("*generated*")):
        if not path.is_file():
            continue
        head = path.read_text(encoding="utf-8-sig", errors="replace")[: len(GENERATED_BANNER) + 8]
        if GENERATED_BANNER not in head:
            report.error(f"{path}: generated file is missing its DO-NOT-EDIT banner")


def _localisation_keys(mod_dir: Path) -> dict[str, set[str]]:
    per_language: dict[str, set[str]] = {}
    root = mod_dir / "localisation"
    if not root.is_dir():
        return per_language
    for language_dir in sorted(root.iterdir()):
        if not language_dir.is_dir():
            continue
        keys: set[str] = set()
        for path in sorted(language_dir.glob("*.yml")):
            keys |= set(LOC_KEY.findall(path.read_text(encoding="utf-8-sig", errors="replace")))
        per_language[language_dir.name] = keys
    return per_language


def check_localisation_parity(mod_dir: Path, report: Report) -> None:
    per_language = _localisation_keys(mod_dir)
    if "english" not in per_language:
        report.error("mod/localisation/english is missing or contains no keys")
        return
    english = per_language["english"]
    for language, keys in per_language.items():
        if language == "english":
            continue
        missing = sorted(english - keys)
        if missing:
            preview = ", ".join(missing[:6])
            report.error(
                f"localisation/{language}: {len(missing)} key(s) missing from english, e.g. {preview}"
            )


def check_localisation_encoding(mod_dir: Path, report: Report) -> None:
    for path in sorted((mod_dir / "localisation").rglob("*.yml")):
        raw = path.read_bytes()
        if not raw.startswith(b"\xef\xbb\xbf"):
            report.error(f"{path}: localisation files must be UTF-8 with BOM")
        first = raw.lstrip(b"\xef\xbb\xbf").splitlines()[0].decode("utf-8", "replace").strip()
        expected = f"l_{path.parent.name}:"
        if first != expected:
            report.error(f"{path}: first line must be `{expected}`, found `{first}`")


def check_referenced_localisation_keys(mod_dir: Path, report: Report) -> None:
    """Every CCP_* key used in script or GUI must exist in the english localisation."""
    per_language = _localisation_keys(mod_dir)
    english = per_language.get("english", set())

    used: dict[str, Path] = {}
    pattern = re.compile(r"\bCCP_[A-Z0-9_]+\b")
    for path in _script_files(mod_dir):
        if "generated" in path.name:
            continue
        for match in pattern.findall(path.read_text(encoding="utf-8-sig", errors="replace")):
            used.setdefault(match, path)

    for key, path in sorted(used.items()):
        if key.startswith("CCP_Get"):
            continue
        if key not in english:
            report.error(f"{path}: `{key}` has no english localisation entry")


ALL_CHECKS = [
    ("descriptor", lambda repo, mod, rep: check_descriptor(mod, rep)),
    ("braces", lambda repo, mod, rep: check_braces(mod, rep)),
    ("generated banners", lambda repo, mod, rep: check_generated_banners(mod, rep)),
    ("placeholders", lambda repo, mod, rep: check_no_placeholders(mod, rep)),
    ("localisation encoding", lambda repo, mod, rep: check_localisation_encoding(mod, rep)),
    ("localisation parity", lambda repo, mod, rep: check_localisation_parity(mod, rep)),
    ("localisation coverage", lambda repo, mod, rep: check_referenced_localisation_keys(mod, rep)),
    ("workshop payload", lambda repo, mod, rep: check_payload_is_clean(repo, rep)),
]
