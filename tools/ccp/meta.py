"""Identity of the mod, single-sourced so the descriptor, the panel and the docs agree."""

from __future__ import annotations

MOD_NAME = "HOI4 Cheat Control Panel"
MOD_VERSION = "3.0.1"
SUPPORTED_VERSION = "1.19.*"
TAGS = ("Utilities", "Gameplay")
THUMBNAIL = "thumbnail.png"


def descriptor() -> str:
    tags = "\n".join(f'\t"{tag}"' for tag in TAGS)
    return (
        f'name="{MOD_NAME}"\n'
        f'version="{MOD_VERSION}"\n'
        f"tags={{\n{tags}\n}}\n"
        f'picture="{THUMBNAIL}"\n'
        f'supported_version="{SUPPORTED_VERSION}"\n'
    )
