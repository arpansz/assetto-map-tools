# Validation rules

The project distinguishes **errors** from **warnings** deliberately.

## Errors

Errors identify objectively broken or incomplete source input that the validator can prove from the files it reads.

| Code | Meaning |
|---|---|
| `OBJ_READ_FAILED` | OBJ could not be read. |
| `OBJ_BAD_FACE` | A parsed OBJ face has fewer than three vertices. |
| `OBJ_NO_VERTICES` | OBJ contains no `v` records. |
| `OBJ_NO_FACES` | OBJ contains no `f` records. |
| `MTL_MISSING` | An OBJ-referenced MTL file is absent. |
| `MTL_READ_FAILED` | MTL could not be read. |
| `TEXTURE_MISSING` | A texture referenced by a supported MTL map statement does not exist relative to the MTL file. |

## Warnings

Warnings identify conditions worth reviewing. They are **not claims that Assetto Corsa will reject the asset**.

| Code | Meaning |
|---|---|
| `OBJ_NO_UV` | No OBJ texture-coordinate records were found. |
| `OBJ_NO_NORMALS` | No OBJ vertex-normal records were found. |
| `NAME_EMPTY` | An object/group name is empty. |
| `NAME_DUPLICATE` | The same object/group name appears more than once. |
| `NAME_SPACE` | A name contains spaces. |
| `NAME_UNSAFE_CHARS` | A name contains characters outside the conservative ASCII-safe set used by this project. |
| `MATERIAL_UNDECLARED` | OBJ uses a material name not found in its referenced MTL files. |

## Rule policy

New rules should satisfy at least one of these conditions:

1. The failure is objectively detectable from the source files, or
2. The check is presented as a warning and its limitations are documented.

Assetto Corsa modding has many community conventions and tool-specific behaviors. The project should not turn an anecdotal convention into a hard validation error without a reproducible reason.
