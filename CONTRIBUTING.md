# Contributing

Thanks for helping improve Assetto Map Tools.

## Development setup

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -e ".[dev]"
pytest -q
```

## Scope

Please keep validation rules evidence-based and reproducible. Assetto Corsa modding
contains many community conventions that are not hard engine requirements, so:

- use **errors** for objectively broken input (missing file, malformed face, etc.),
- use **warnings** for conservative workflow recommendations,
- document any Assetto-specific rule added to the project,
- add a test or minimal reproduction whenever possible.

## Pull requests

Keep PRs focused. Explain the failure case being detected, how to reproduce it,
and why the proposed rule is safe to apply to other projects.
