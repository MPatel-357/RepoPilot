
import pytest

from app.services.impact_analyzer import analyze_impact


def test_change_impact(tmp_path):
    (tmp_path / "base.py").write_text(
        "def helper(): return 42\n"
    )

    (tmp_path / "service.py").write_text(
        "import base\n"
    )

    (tmp_path / "main.py").write_text(
        "import service\n"
    )

    result = analyze_impact(str(tmp_path), "base.py")

    assert result["total_affected"] == 2

    affected = {
        item["file"]: item
        for item in result["affected_files"]
    }

    assert affected["service.py"]["impact_type"] == "direct"
    assert affected["main.py"]["impact_type"] == "indirect"
    assert affected["main.py"]["distance"] == 2

    assert affected["main.py"]["dependency_path"] == [
        "base.py",
        "service.py",
        "main.py",
    ]


def test_unknown_target(tmp_path):
    with pytest.raises(ValueError):
        analyze_impact(str(tmp_path), "missing.py")

