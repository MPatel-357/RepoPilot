
from app.services.dependency_graph import build_dependency_graph


def test_dependency_graph(tmp_path):
    package = tmp_path / "example"
    package.mkdir()

    (package / "__init__.py").write_text("")

    (package / "utils.py").write_text(
        "def helper():\n"
        "    return 42\n"
    )

    (package / "main.py").write_text(
        "import example.utils\n"
        "print(example.utils.helper())\n"
    )

    result = build_dependency_graph(str(tmp_path))

    assert result["total_nodes"] == 3
    assert result["total_edges"] == 1

    assert {
        "source": "example/main.py",
        "target": "example/utils.py",
    } in result["edges"]


def test_relative_import_dependency(tmp_path):
    package = tmp_path / "mypackage"
    package.mkdir()

    (package / "__init__.py").write_text("")

    (package / "utils.py").write_text(
        "def helper(): return 42\n"
    )

    (package / "service.py").write_text(
        "from . import utils\n"
    )

    result = build_dependency_graph(str(tmp_path))

    assert {
        "source": "mypackage/service.py",
        "target": "mypackage/utils.py",
    } in result["edges"]
