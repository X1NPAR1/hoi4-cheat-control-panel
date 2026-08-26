"""Minimal reader for the Clausewitz script format used by Paradox games."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

_TOKEN = re.compile(
    r"""
      (?P<comment>\#[^\n]*)
    | (?P<string>"(?:[^"\\]|\\.)*")
    | (?P<open>\{)
    | (?P<close>\})
    | (?P<operator>>=|<=|!=|[=<>])
    | (?P<bare>[^\s{}=<>"\#]+)
    """,
    re.VERBOSE,
)


@dataclass
class Node:
    """A `key = { ... }` block. Children keep source order and allow duplicate keys."""

    key: str = ""
    values: list[str] = field(default_factory=list)
    children: list["Node"] = field(default_factory=list)

    def get(self, key: str) -> str | None:
        for child in self.children:
            if child.key == key and child.values:
                return child.values[0]
        return None

    def get_all(self, key: str) -> list[str]:
        """Values for `key`, flattening `key = { a b c }` list blocks into their members."""
        found: list[str] = []
        for child in self.children:
            if child.key != key:
                continue
            if child.values:
                found.extend(child.values)
            else:
                found.extend(item for grand in child.children for item in grand.values)
        return found

    def block(self, key: str) -> "Node | None":
        for child in self.children:
            if child.key == key and not child.values:
                return child
        return None

    def blocks(self) -> list["Node"]:
        return [child for child in self.children if child.children or not child.values]


def _tokenize(text: str):
    for match in _TOKEN.finditer(text):
        kind = match.lastgroup
        if kind == "comment":
            continue
        value = match.group()
        if kind == "string":
            value = value[1:-1]
        yield kind, value


def parse(text: str) -> Node:
    root = Node()
    stack = [root]
    pending_key: str | None = None
    tokens = list(_tokenize(text))
    index = 0

    while index < len(tokens):
        kind, value = tokens[index]

        if kind == "operator":
            index += 1
            continue

        if kind == "open":
            node = Node(key=pending_key or "")
            stack[-1].children.append(node)
            stack.append(node)
            pending_key = None
            index += 1
            continue

        if kind == "close":
            if len(stack) > 1:
                stack.pop()
            pending_key = None
            index += 1
            continue

        following = tokens[index + 1] if index + 1 < len(tokens) else (None, None)

        if following[0] == "operator":
            after = tokens[index + 2] if index + 2 < len(tokens) else (None, None)
            if after[0] == "open":
                pending_key = value
                index += 2
                continue
            if after[0] in ("bare", "string"):
                stack[-1].children.append(Node(key=value, values=[after[1]]))
                index += 3
                continue
            index += 2
            continue

        stack[-1].children.append(Node(key=value, values=[value]))
        index += 1

    return root


def parse_file(path: Path) -> Node:
    return parse(path.read_text(encoding="utf-8-sig", errors="replace"))
