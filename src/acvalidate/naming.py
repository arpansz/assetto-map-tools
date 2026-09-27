from __future__ import annotations

import re
from collections.abc import Iterable

from .models import Finding, Severity

# Conservative checks only. These are warnings rather than hard AC requirements.
_SAFE_NAME = re.compile(r"^[A-Za-z0-9_.-]+$")


def validate_object_names(names: Iterable[str], source: str | None = None) -> list[Finding]:
    findings: list[Finding] = []
    seen: set[str] = set()

    for name in names:
        if not name:
            findings.append(Finding(Severity.WARNING, "NAME_EMPTY", "Object has an empty name.", source))
            continue

        if name in seen:
            findings.append(
                Finding(Severity.WARNING, "NAME_DUPLICATE", f"Duplicate object/group name: {name}", source)
            )
        seen.add(name)

        if " " in name:
            findings.append(
                Finding(Severity.WARNING, "NAME_SPACE", f"Name contains spaces: {name}", source)
            )

        if not _SAFE_NAME.match(name):
            findings.append(
                Finding(
                    Severity.WARNING,
                    "NAME_UNSAFE_CHARS",
                    f"Name contains characters that may be inconvenient in an AC export pipeline: {name}",
                    source,
                )
            )

    return findings
