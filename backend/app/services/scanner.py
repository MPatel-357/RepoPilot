
import ast
from pathlib import Path


def scan_python_file(file_path: str) -> dict:
    """
    Scan a Python file and extract its structural information.

    Returns imports, functions, classes, and their locations.
    """
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    if path.suffix != ".py":
        raise ValueError("Only Python files are supported.")

    source_code = path.read_text(encoding="utf-8")
    tree = ast.parse(source_code, filename=str(path))

    results = {
        "file": str(path),
        "imports": [],
        "functions": [],
        "classes": [],
    }

    # Track top-level imports.
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                results["imports"].append({
                    "module": alias.name,
                    "line": node.lineno,
                })

        elif isinstance(node, ast.ImportFrom):
            results["imports"].append({
                "module": "." * node.level + (node.module or ""),
                "names": [alias.name for alias in node.names],
                "line": node.lineno,
            })

    # Track top-level functions and classes.
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            results["functions"].append({
                "name": node.name,
                "line_start": node.lineno,
                "line_end": node.end_lineno,
                "async": isinstance(node, ast.AsyncFunctionDef),
            })

        elif isinstance(node, ast.ClassDef):
            methods = []

            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    methods.append({
                        "name": child.name,
                        "line_start": child.lineno,
                        "line_end": child.end_lineno,
                        "async": isinstance(child, ast.AsyncFunctionDef),
                    })

            results["classes"].append({
                "name": node.name,
                "line_start": node.lineno,
                "line_end": node.end_lineno,
                "methods": methods,
            })

    return results
