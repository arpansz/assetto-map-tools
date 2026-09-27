from pathlib import Path

from acvalidate.obj import validate_obj


def test_valid_obj(tmp_path: Path):
    (tmp_path / "road.png").write_bytes(b"not-a-real-png-but-exists")
    (tmp_path / "track.mtl").write_text(
        "newmtl ROAD\nmap_Kd road.png\n",
        encoding="utf-8",
    )
    obj = tmp_path / "track.obj"
    obj.write_text(
        "\n".join(
            [
                "mtllib track.mtl",
                "o ROAD_MAIN",
                "v 0 0 0",
                "v 1 0 0",
                "v 0 1 0",
                "vt 0 0",
                "vt 1 0",
                "vt 0 1",
                "vn 0 0 1",
                "usemtl ROAD",
                "f 1/1/1 2/2/1 3/3/1",
            ]
        ),
        encoding="utf-8",
    )

    summary, findings = validate_obj(obj)
    assert summary.vertices == 3
    assert summary.faces == 1
    assert not [f for f in findings if f.severity.value == "error"]


def test_missing_texture_is_error(tmp_path: Path):
    (tmp_path / "track.mtl").write_text(
        "newmtl ROAD\nmap_Kd missing.png\n",
        encoding="utf-8",
    )
    obj = tmp_path / "track.obj"
    obj.write_text(
        "\n".join(
            [
                "mtllib track.mtl",
                "o ROAD_MAIN",
                "v 0 0 0",
                "v 1 0 0",
                "v 0 1 0",
                "vt 0 0",
                "vn 0 0 1",
                "usemtl ROAD",
                "f 1/1/1 2/1/1 3/1/1",
            ]
        ),
        encoding="utf-8",
    )

    _, findings = validate_obj(obj)
    assert any(f.code == "TEXTURE_MISSING" for f in findings)
