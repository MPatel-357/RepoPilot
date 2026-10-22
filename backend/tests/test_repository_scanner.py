
from app.services.repository_scanner import scan_repository


def test_scan_repository(tmp_path):
    # Create a small example repository.
    source = tmp_path / "example.py"

    source.write_text(
        "import math\n"
        "def square(x):\n"
        "    return x * x\n",
        encoding="utf-8",
    )

    result = scan_repository(str(tmp_path))

    assert result["total_files"] == 1
    assert result["total_functions"] == 1
    assert result["total_imports"] == 1
    assert result["total_classes"] == 0
    assert result["errors"] == []


def test_ignored_directories(tmp_path):
    # Files inside virtual environments should be skipped.
    venv = tmp_path / ".venv"
    venv.mkdir()

    (venv / "ignored.py").write_text(
        "def ignored(): pass\n",
        encoding="utf-8",
    )

    result = scan_repository(str(tmp_path))

    assert result["total_files"] == 0


def test_syntax_error_is_recorded(tmp_path):
    broken = tmp_path / "broken.py"

    broken.write_text(
        "def broken(\n",
        encoding="utf-8",
    )

    result = scan_repository(str(tmp_path))

    assert result["total_files"] == 0
    assert len(result["errors"]) == 1
