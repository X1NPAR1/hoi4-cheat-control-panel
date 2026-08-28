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


def _game_dir() -> Path | None:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    try:
        from generate_data import find_game_dir

        return find_game_dir(None)
    except SystemExit:
        return None


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
        head = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()[:3]
        if not any(GENERATED_BANNER in line for line in head):
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
    from .languages import NATIVE

    per_language = _localisation_keys(mod_dir)
    if "english" not in per_language:
        report.error("mod/localisation/english is missing or contains no keys")
        return

    for language in NATIVE:
        if language not in per_language:
            report.error(f"mod/localisation/{language} is missing")
    for language in per_language:
        if language not in NATIVE:
            report.error(
                f"mod/localisation/{language} is not a language Hearts of Iron IV loads"
            )

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


SPRITE_DEFINITION = re.compile(r'name\s*=\s*"(GFX_[A-Za-z0-9_]+)"')
SPRITE_TEXTURE = re.compile(r'texturefile\s*=\s*"([^"]+)"')
SPRITE_USE = re.compile(r'(?:spriteType|quadTextureSprite)\s*=\s*"(GFX_[A-Za-z0-9_]+)"')
WIDGET_NAME = re.compile(r'name\s*=\s*"(ccp_[A-Za-z0-9_]+)"')

SCRIPTED_GUI_SUFFIXES = (
    "_click",
    "_click_enabled",
    "_visible",
    "_alt_click",
    "_right_click",
    "_shift_click",
    "_control_click",
    "_alt_right_click",
)


def check_sprite_references(mod_dir: Path, report: Report) -> None:
    defined: set[str] = set()
    for path in sorted(mod_dir.rglob("*.gfx")):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        defined |= set(SPRITE_DEFINITION.findall(text))
        for texture in SPRITE_TEXTURE.findall(text):
            if not (mod_dir / texture).is_file():
                report.error(f"{path}: texture `{texture}` does not exist")

    for path in sorted(mod_dir.rglob("*.gui")):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        for sprite in sorted(set(SPRITE_USE.findall(text))):
            if sprite.startswith("GFX_ccp_") and sprite not in defined:
                report.error(f"{path}: `{sprite}` is not defined in any .gfx file")


def check_gui_element_references(mod_dir: Path, report: Report) -> None:
    """Scripted GUI effects, triggers and properties must name a widget that exists."""
    widgets: set[str] = set()
    for path in sorted(mod_dir.rglob("*.gui")):
        widgets |= set(WIDGET_NAME.findall(path.read_text(encoding="utf-8-sig", errors="replace")))

    handler = re.compile(r"^\s*(ccp_[A-Za-z0-9_]+)\s*=\s*\{", re.MULTILINE)
    for path in sorted((mod_dir / "common" / "scripted_guis").glob("*.txt")):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        for name in sorted(set(handler.findall(text))):
            for suffix in SCRIPTED_GUI_SUFFIXES:
                if name.endswith(suffix):
                    widget = name[: -len(suffix)]
                    if widget not in widgets:
                        report.error(
                            f"{path}: `{name}` targets widget `{widget}`, "
                            "which no .gui file defines"
                        )
                    break


EFFECT_CALL = re.compile(r"^\s*(CCP_[A-Za-z0-9_]+)\s*=\s*yes\s*$", re.MULTILINE)
EFFECT_DEF = re.compile(r"^(CCP_[A-Za-z0-9_]+)\s*=\s*\{", re.MULTILINE)


def check_effect_references(mod_dir: Path, report: Report) -> None:
    """Every CCP_ effect the mod calls must be defined by the mod."""
    defined: set[str] = set()
    called: dict[str, Path] = {}

    for path in sorted((mod_dir / "common").rglob("*.txt")):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        defined |= set(EFFECT_DEF.findall(text))
        for name in EFFECT_CALL.findall(text):
            called.setdefault(name, path)

    for path in sorted((mod_dir / "common" / "scripted_guis").glob("*.txt")):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        for name in EFFECT_CALL.findall(text):
            called.setdefault(name, path)

    for name, path in sorted(called.items()):
        if name not in defined:
            report.error(f"{path}: calls `{name}`, which no scripted effect defines")

    unused = sorted(defined - set(called))
    for name in unused:
        report.warn(f"`{name}` is defined but never called")


def check_no_vanilla_overrides(mod_dir: Path, game_dir: Path | None, report: Report) -> None:
    """The mod is additive: no file may share a path with a vanilla file."""
    if game_dir is None or not game_dir.is_dir():
        report.warn("game directory not found; vanilla override check skipped")
        return
    for path in sorted(mod_dir.rglob("*")):
        if not path.is_file() or path.name == "descriptor.mod":
            continue
        relative = path.relative_to(mod_dir)
        if (game_dir / relative).is_file():
            report.error(f"mod/{relative.as_posix()} overrides a vanilla file")


LOC_LINE = re.compile(r'^ [A-Za-z0-9_.@\-]+:\d* ".*"$')


def check_localisation_lines(mod_dir: Path, report: Report) -> None:
    """Every entry must be one well-formed line.

    Hearts of Iron IV stops reading a localisation file at the first line it cannot
    parse, so one stray newline inside a value silently drops every key after it.
    """
    for path in sorted((mod_dir / "localisation").rglob("*.yml")):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        for number, line in enumerate(text.splitlines(), start=1):
            if number == 1 or not line.strip() or line.lstrip().startswith("#"):
                continue
            if not LOC_LINE.match(line):
                report.error(f"{path}:{number}: malformed localisation line `{line[:70]}`")


ASSIGNMENT = re.compile(r"^\s*([a-z_][a-z0-9_]*)\s*=", re.MULTILINE)


def check_effect_vocabulary(mod_dir: Path, game_dir: Path | None, report: Report) -> None:
    """Every lowercase name the scripts assign to must be one the game knows.

    A misspelled or renamed effect fails silently in game: the button clicks and
    nothing happens. Checking the names against the game's own documentation turns
    that into a build error.
    """
    if game_dir is None or not game_dir.is_dir():
        report.warn("game directory not found; effect vocabulary check skipped")
        return

    from .effect_names import known_effects

    known = known_effects(game_dir)
    if not known:
        report.warn("effects documentation not found; vocabulary check skipped")
        return

    unknown: dict[str, Path] = {}
    for path in sorted((mod_dir / "common").rglob("*.txt")):
        text = _strip_comments_and_strings(path.read_text(encoding="utf-8-sig", errors="replace"))
        for name in ASSIGNMENT.findall(text):
            if name.startswith("ccp_") or name in known:
                continue
            unknown.setdefault(name, path)

    for name, path in sorted(unknown.items()):
        report.error(f"{path}: `{name}` is not an effect the game documents")


ICON_WITH_SIZE = re.compile(r"iconType = \{(?:[^{}]|\{[^{}]*\})*?\bsize\s*=")
BARE_READ = re.compile(r"var:(?!ROOT\.|global\.)ccp_")
SHORTHAND_COMPARE = re.compile(r"check_variable = \{[^{}]*[<>]=")


def check_gui_property_grammar(mod_dir: Path, report: Report) -> None:
    """`iconType` has no `size`; the parser stops at the file, not at the line.

    One unsupported property discards every widget declared after it, so a whole
    panel goes missing with a single line in error.log to explain it.
    """
    for path in sorted((mod_dir / "interface").glob("*.gui")):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        for match in ICON_WITH_SIZE.finditer(text):
            line = text.count("\n", 0, match.end()) + 1
            report.error(f"{path}:{line}: iconType does not accept `size`")


def check_variable_comparisons(mod_dir: Path, report: Report) -> None:
    """`check_variable` shorthand parses `=`, `>` and `<` only.

    `>=` and `<=` are not shorthand operators: the engine reads the `>` and then
    trips over the rest, taking the surrounding effect down with it. The long form
    with `compare = greater_than_or_equals` is the documented way to say it.
    """
    for path in sorted((mod_dir / "common").rglob("*.txt")):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        for match in SHORTHAND_COMPARE.finditer(text):
            line = text.count("\n", 0, match.end()) + 1
            report.error(f"{path}:{line}: check_variable shorthand has no `>=` or `<=`")


def check_variable_scope_entry(mod_dir: Path, report: Report) -> None:
    """`var:` enters a scope held in a country variable, never a global one.

    The engine rejects `var:global.name` as a malformed token. A stored scope is
    kept twice: `global.name` for triggers in foreign scopes, and a country copy
    for `var:name` here.
    """
    for path in sorted((mod_dir / "common").rglob("*.txt")):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        for number, line in enumerate(text.splitlines(), start=1):
            if "var:global." in line:
                report.error(f"{path}:{number}: `var:global.` is not a scope the engine reads")


def check_variable_reads_name_a_scope(mod_dir: Path, report: Report) -> None:
    """A `var:` read must say which scope holds the variable.

    A variable belongs to the scope that set it, so a bare `var:name` reads
    nothing once an effect has stepped into another country or a state. The block
    it guards is then skipped with no complaint in error.log, which is the most
    expensive failure this project has had: the button clicks and nothing happens.
    """
    for path in sorted((mod_dir / "common").rglob("*.txt")):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        for number, line in enumerate(text.splitlines(), start=1):
            if BARE_READ.search(line):
                report.error(f"{path}:{number}: `var:` read does not name a scope")


def check_translations_differ(mod_dir: Path, report: Report) -> None:
    """A translation that is still the English text is not a translation.

    The parity check only proves the key exists in every file; a row copied from
    English passes it while showing English in game. Rows that are genuinely the
    same word in every language are listed in strings.SHARED_ACROSS_LANGUAGES, so
    the exceptions are written down rather than tolerated.
    """
    from .strings import untranslated

    for language, keys in sorted(untranslated().items()):
        for key in keys:
            report.error(f"{key}: {language} is still the English text")


def check_installed_copy_is_shippable(repo_root: Path, report: Report) -> None:
    """The installed copy is what the launcher uploads, so it must match mod/.

    Turkish and Dutch used to ship as an overlay written over
    `localisation/english/`, because the engine has no folder for either. That was
    correct for playing and catastrophic for publishing: an upload made while the
    overlay was applied put Turkish text under English keys for every subscriber,
    and the Workshop comments were people asking why the English menus were
    Turkish. The overlay is gone now, and this makes sure nothing else drifts into
    the copy the launcher sends.
    """
    import os

    documents = Path(os.environ.get("USERPROFILE", Path.home())) / "Documents"
    installed = (
        documents
        / "Paradox Interactive"
        / "Hearts of Iron IV"
        / "mod"
        / "hoi4_cheat_control_panel"
    )
    if not installed.is_dir():
        return

    stale = installed.with_name(installed.name + ".ccp-language")
    if stale.is_file():
        report.error(
            f"{stale} is left over from the language overlay. Delete it and run "
            "tools/install_local.py again before publishing."
        )

    for path in sorted((repo_root / "mod" / "localisation").rglob("*.yml")):
        other = installed / path.relative_to(repo_root / "mod")
        if other.is_file() and other.read_bytes() != path.read_bytes():
            report.error(
                f"installed {path.name} differs from mod/. The launcher uploads the "
                "installed copy, so run tools/install_local.py before publishing."
            )


ALL_CHECKS = [
    ("descriptor", lambda repo, mod, rep: check_descriptor(mod, rep)),
    ("braces", lambda repo, mod, rep: check_braces(mod, rep)),
    ("sprite references", lambda repo, mod, rep: check_sprite_references(mod, rep)),
    ("gui element references", lambda repo, mod, rep: check_gui_element_references(mod, rep)),
    ("effect references", lambda repo, mod, rep: check_effect_references(mod, rep)),
    ("vanilla overrides", lambda repo, mod, rep: check_no_vanilla_overrides(mod, _game_dir(), rep)),
    ("effect vocabulary", lambda repo, mod, rep: check_effect_vocabulary(mod, _game_dir(), rep)),
    ("gui property grammar", lambda repo, mod, rep: check_gui_property_grammar(mod, rep)),
    ("variable comparisons", lambda repo, mod, rep: check_variable_comparisons(mod, rep)),
    ("variable scope entry", lambda repo, mod, rep: check_variable_scope_entry(mod, rep)),
    ("variable reads", lambda repo, mod, rep: check_variable_reads_name_a_scope(mod, rep)),
    ("generated banners", lambda repo, mod, rep: check_generated_banners(mod, rep)),
    ("placeholders", lambda repo, mod, rep: check_no_placeholders(mod, rep)),
    ("localisation encoding", lambda repo, mod, rep: check_localisation_encoding(mod, rep)),
    ("localisation lines", lambda repo, mod, rep: check_localisation_lines(mod, rep)),
    ("translations differ", lambda repo, mod, rep: check_translations_differ(mod, rep)),
    ("localisation parity", lambda repo, mod, rep: check_localisation_parity(mod, rep)),
    ("localisation coverage", lambda repo, mod, rep: check_referenced_localisation_keys(mod, rep)),
    ("installed copy", lambda repo, mod, rep: check_installed_copy_is_shippable(repo, rep)),
    ("workshop payload", lambda repo, mod, rep: check_payload_is_clean(repo, rep)),
]
