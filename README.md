# Assetto Map Tools

Open-source validation and diagnostics for **Assetto Corsa map and track-building workflows**.

The first module, **`acvalidate`**, catches common source-asset problems before they become
hard-to-debug export or editor failures.

> **Project status:** early alpha. The validator currently checks source assets; it does not
> claim to fully validate FBX, ksEditor behavior, or KN5 serialization.

Created and maintained by **Arpan Hansda** (GitHub: [@arpansz](https://github.com/arpansz)).

## Why this exists

Large Assetto Corsa map projects can involve Blender, OBJ/FBX exports, materials, textures,
editor conversion, collision geometry, and many repeated export/test cycles. A missing texture,
empty mesh, malformed OBJ face, or inconsistent source name can be cheap to detect before export
but expensive to diagnose later.

`assetto-map-tools` aims to turn those repeatable checks into open-source tooling that any map
creator can run locally or in CI.

## Current features — v0.1

- Validate Wavefront OBJ geometry at a basic structural level.
- Resolve referenced MTL files.
- Detect missing textures referenced by MTL files.
- Warn about duplicate or awkward object/group names.
- Warn when UVs or normals are absent.
- Report materials used by the OBJ but not declared by referenced MTL files.
- Output human-readable text or JSON.
- Return non-zero exit codes for validation errors.
- Run a small Blender-side source-scene validator.

## Installation

Clone the repository:

```bash
git clone https://github.com/arpansz/assetto-map-tools.git
cd assetto-map-tools
python -m pip install -e .
```

For development:

```bash
python -m pip install -e ".[dev]"
pytest -q
```

## Usage

Validate an OBJ:

```bash
acvalidate obj path/to/track.obj
```

Example output:

```text
Assetto Map Tools — acvalidate

file: C:\maps\my_track\track.obj
vertices: 158204
faces: 287110
uvs: 158204
normals: 158204
objects: 14
groups: 8
materials_used: 12

ERROR TEXTURE_MISSING: Referenced texture does not exist: road_diffuse.dds [...]
WARN  NAME_SPACE: Name contains spaces: ROAD Main [...]

Result: 1 error(s), 1 warning(s), 0 info
```

Machine-readable report:

```bash
acvalidate obj path/to/track.obj --json
```

Try the deliberately broken sample included in the repository:

```bash
acvalidate obj examples/broken_track.obj
```

It demonstrates missing-texture and source-naming/UV/normal diagnostics. The full rule catalog is in [`docs/VALIDATION_RULES.md`](docs/VALIDATION_RULES.md).

Make warnings fail CI as well:

```bash
acvalidate obj path/to/track.obj --fail-on-warning
```

## Blender source-scene check

Open `examples/blender/validate_scene.py` in Blender's Scripting workspace and run it, or use:

```bash
blender your_scene.blend --background --python examples/blender/validate_scene.py
```

The current Blender script checks for:

- mesh objects with no faces,
- missing UV layers,
- missing material slots,
- unapplied scale,
- potentially awkward export names.

These checks are deliberately conservative. A warning does **not** mean Assetto Corsa will
necessarily reject the asset.

## What this project does not do yet

V0.1 does not:

- parse every FBX variant,
- open or rewrite KN5 files,
- replace ksEditor,
- guarantee that a source asset will work in-game,
- encode undocumented community assumptions as hard failures.

Those areas require reproducible test cases and careful implementation. See
[`docs/ROADMAP.md`](docs/ROADMAP.md).

## Design principles

1. **Detect objective failures early.** Missing files and malformed source data should be errors.
2. **Separate facts from conventions.** Community workflow recommendations should normally be warnings.
3. **Never modify the user's source assets during validation.**
4. **Make every rule testable.** A validator should explain what failed and where.
5. **Keep the core useful outside one map project.** Real projects can provide test cases without becoming dependencies.

## Project structure

```text
assetto-map-tools/
├── src/acvalidate/           # Python validator
├── tests/                    # Automated tests
├── examples/blender/         # Blender-side validation example
├── docs/ROADMAP.md           # Planned modules
├── .github/workflows/        # CI
├── CONTRIBUTING.md
├── CHANGELOG.md
├── LICENSE
└── pyproject.toml
```

## Roadmap

The larger goal is a modular toolkit:

```text
assetto-map-tools
├── acvalidate   source asset validation
├── acblender    Blender preparation and export diagnostics
├── acdiag       export/build comparison and diagnostic reports
└── acgeo        large real-world map / GIS workflow helpers
```

The roadmap is intentionally incremental. Features will be added when they can be tested against
real, reproducible map-building cases.

## Contributing

Issues, minimal reproductions, documentation corrections, and pull requests are welcome.
Please read [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

MIT. See [`LICENSE`](LICENSE).

## Disclaimer

This is an independent community project. It is not affiliated with, endorsed by, or sponsored by
Kunos Simulazioni or the Assetto Corsa trademark owners. Assetto Corsa is referenced only to describe
the workflow this tool is intended to assist.
