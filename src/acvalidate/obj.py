from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .models import Finding, Severity
from .naming import validate_object_names


@dataclass
class ObjSummary:
    vertices: int = 0
    texcoords: int = 0
    normals: int = 0
    faces: int = 0
    objects: list[str] = field(default_factory=list)
    groups: list[str] = field(default_factory=list)
    material_libraries: list[str] = field(default_factory=list)
    used_materials: list[str] = field(default_factory=list)


@dataclass
class MtlSummary:
    materials: list[str] = field(default_factory=list)
    texture_refs: list[tuple[str, int]] = field(default_factory=list)


def parse_obj(path: Path) -> tuple[ObjSummary, list[Finding]]:
    summary = ObjSummary()
    findings: list[Finding] = []

    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return summary, [Finding(Severity.ERROR, "OBJ_READ_FAILED", str(exc), str(path))]

    for line_no, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(maxsplit=1)
        key = parts[0]
        value = parts[1].strip() if len(parts) > 1 else ""

        if key == "v":
            summary.vertices += 1
        elif key == "vt":
            summary.texcoords += 1
        elif key == "vn":
            summary.normals += 1
        elif key == "f":
            summary.faces += 1
            if len(value.split()) < 3:
                findings.append(
                    Finding(Severity.ERROR, "OBJ_BAD_FACE", "Face has fewer than 3 vertices.", str(path), line_no)
                )
        elif key == "o":
            summary.objects.append(value)
        elif key == "g":
            summary.groups.append(value)
        elif key == "mtllib":
            summary.material_libraries.extend(value.split())
        elif key == "usemtl":
            summary.used_materials.append(value)

    if summary.vertices == 0:
        findings.append(Finding(Severity.ERROR, "OBJ_NO_VERTICES", "OBJ contains no vertices.", str(path)))
    if summary.faces == 0:
        findings.append(Finding(Severity.ERROR, "OBJ_NO_FACES", "OBJ contains no faces.", str(path)))
    if summary.texcoords == 0:
        findings.append(Finding(Severity.WARNING, "OBJ_NO_UV", "OBJ contains no texture coordinates (vt).", str(path)))
    if summary.normals == 0:
        findings.append(Finding(Severity.WARNING, "OBJ_NO_NORMALS", "OBJ contains no vertex normals (vn).", str(path)))

    findings.extend(validate_object_names(summary.objects + summary.groups, str(path)))
    return summary, findings


def parse_mtl(path: Path) -> tuple[MtlSummary, list[Finding]]:
    summary = MtlSummary()
    findings: list[Finding] = []

    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return summary, [Finding(Severity.ERROR, "MTL_READ_FAILED", str(exc), str(path))]

    # Common map options that reference an image file. This intentionally does not
    # try to fully implement the MTL grammar.
    texture_keys = {
        "map_Ka",
        "map_Kd",
        "map_Ks",
        "map_Ns",
        "map_d",
        "bump",
        "map_bump",
        "disp",
        "decal",
        "norm",
    }

    for line_no, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(maxsplit=1)
        key = parts[0]
        value = parts[1].strip() if len(parts) > 1 else ""

        if key == "newmtl":
            summary.materials.append(value)
        elif key in texture_keys and value:
            # MTL map statements can have options. Taking the final token catches
            # the common export forms without pretending to be a full parser.
            texture = value.split()[-1].strip('"')
            summary.texture_refs.append((texture, line_no))

    for texture, line_no in summary.texture_refs:
        texture_path = (path.parent / texture).resolve()
        if not texture_path.exists():
            findings.append(
                Finding(
                    Severity.ERROR,
                    "TEXTURE_MISSING",
                    f"Referenced texture does not exist: {texture}",
                    str(path),
                    line_no,
                )
            )

    return summary, findings


def validate_obj(path: Path) -> tuple[ObjSummary, list[Finding]]:
    path = path.resolve()
    summary, findings = parse_obj(path)

    material_names: set[str] = set()
    for mtl_ref in summary.material_libraries:
        mtl_path = (path.parent / mtl_ref).resolve()
        if not mtl_path.exists():
            findings.append(
                Finding(Severity.ERROR, "MTL_MISSING", f"Referenced MTL does not exist: {mtl_ref}", str(path))
            )
            continue
        mtl_summary, mtl_findings = parse_mtl(mtl_path)
        findings.extend(mtl_findings)
        material_names.update(mtl_summary.materials)

    for material in sorted(set(summary.used_materials)):
        if summary.material_libraries and material not in material_names:
            findings.append(
                Finding(
                    Severity.WARNING,
                    "MATERIAL_UNDECLARED",
                    f"OBJ uses material not declared in referenced MTL files: {material}",
                    str(path),
                )
            )

    return summary, findings
