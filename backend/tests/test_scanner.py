
from pathlib import Path

from app.services.scanner import scan_python_file


def test_scan_python_file():
    sample = Path(__file__).parent / "sample_code.py"

    result = scan_python_file(str(sample))

    assert len(result["imports"]) == 2
    assert len(result["functions"]) == 2
    assert len(result["classes"]) == 1

    function_names = {f["name"] for f in result["functions"]}

    assert "calculate_area" in function_names
    assert "fetch_data" in function_names

    circle = result["classes"][0]

    assert circle["name"] == "Circle"
    assert len(circle["methods"]) == 2

    method_names = {m["name"] for m in circle["methods"]}

    assert "__init__" in method_names
    assert "diameter" in method_names


def test_invalid_file():
    import pytest

    with pytest.raises(FileNotFoundError):
        scan_python_file("file_that_does_not_exist.py")
