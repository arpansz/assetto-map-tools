from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .models import Severity
from .obj import validate_obj
from .report import to_json, to_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="acvalidate",
        description="Validate source assets used in Assetto Corsa map-building workflows.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    sub = parser.add_subparsers(dest="command", required=True)
    obj = sub.add_parser("obj", help="Validate a Wavefront OBJ and referenced MTL/textures.")
    obj.add_argument("path", type=Path, help="Path to .obj file")
    obj.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    obj.add_argument(
        "--fail-on-warning",
        action="store_true",
        help="Return non-zero status when warnings are present.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "obj":
        if not args.path.exists():
            print(f"ERROR: file does not exist: {args.path}", file=sys.stderr)
            return 2
        if args.path.suffix.lower() != ".obj":
            print("ERROR: 'obj' command expects a .obj file", file=sys.stderr)
            return 2

        summary, findings = validate_obj(args.path)
        summary_dict = {
            "file": str(args.path.resolve()),
            "vertices": summary.vertices,
            "faces": summary.faces,
            "uvs": summary.texcoords,
            "normals": summary.normals,
            "objects": len(summary.objects),
            "groups": len(summary.groups),
            "materials_used": len(set(summary.used_materials)),
        }
        print(to_json(findings, summary_dict) if args.json else to_text(findings, summary_dict))

        has_error = any(f.severity == Severity.ERROR for f in findings)
        has_warning = any(f.severity == Severity.WARNING for f in findings)
        if has_error:
            return 1
        if args.fail_on_warning and has_warning:
            return 1
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
