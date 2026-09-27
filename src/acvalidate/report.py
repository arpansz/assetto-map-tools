from __future__ import annotations

import json
from collections import Counter

from .models import Finding, Severity


def counts(findings: list[Finding]) -> Counter:
    return Counter(f.severity.value for f in findings)


def to_json(findings: list[Finding], summary: dict) -> str:
    return json.dumps(
        {
            "summary": summary,
            "findings": [finding.to_dict() for finding in findings],
        },
        indent=2,
    )


def to_text(findings: list[Finding], summary: dict) -> str:
    lines: list[str] = []
    lines.append("Assetto Map Tools — acvalidate")
    lines.append("")
    for key, value in summary.items():
        lines.append(f"{key}: {value}")

    lines.append("")
    if not findings:
        lines.append("PASS: no findings")
        return "\n".join(lines)

    icons = {
        Severity.ERROR: "ERROR",
        Severity.WARNING: "WARN ",
        Severity.INFO: "INFO ",
    }
    for finding in findings:
        where = ""
        if finding.source:
            where = f" [{finding.source}"
            if finding.line is not None:
                where += f":{finding.line}"
            where += "]"
        lines.append(f"{icons[finding.severity]} {finding.code}: {finding.message}{where}")

    c = counts(findings)
    lines.append("")
    lines.append(f"Result: {c['error']} error(s), {c['warning']} warning(s), {c['info']} info")
    return "\n".join(lines)
