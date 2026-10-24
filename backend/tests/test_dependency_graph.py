
from app.services.dependency_graph import build_dependency_graph


def test_dependency_graph(tmp_path):
    app_dir = tmp_path / "example"
    app_dir.mkdir()

    (app_dir / "__init__.py").write_text("")

    (app_dir / "utils.py").write_text(
        "def helper():\n"
        "    return 42\n"
    )

    (app_dir / "main.py").write_text(
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
