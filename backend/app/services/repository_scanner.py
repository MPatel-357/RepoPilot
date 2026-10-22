
from pathlib import Path

from app.services.scanner import scan_python_file


IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    "dist",
    "build",
}

MAX_FILE_SIZE = 1_000_000  # One million bytes per file


def scan_repository(repository_path: str) -> dict:
    """
    Analyze Python files in a local repository.

    Skip ignored directories, symbolic links, and oversized files.
    Record errors without stopping the entire scan.
    """
    root = Path(repository_path).resolve()

    if not root.is_dir():
        raise NotADirectoryError(
            f"Repository directory not found: {repository_path}"
        )

    results = {
        "repository": str(root),
        "total_files": 0,
        "total_functions": 0,
        "total_classes": 0,
        "total_imports": 0,
        "files": [],
        "errors": [],
    }

    for path in root.rglob("*.py"):

        # Work with paths relative to the repository.
        relative_path = path.relative_to(root)

        # Ignore virtual environments, Git metadata, etc.
        if any(
            part in IGNORED_DIRECTORIES
            for part in relative_path.parts
        ):
            continue

        # Do not follow symbolic links.
        if path.is_symlink():
            continue

        try:
            if path.stat().st_size > MAX_FILE_SIZE:
                results["errors"].append({
                    "file": str(relative_path),
                    "error": "File exceeds size limit",
                })
                continue

            file_result = scan_python_file(str(path))
            file_result["file"] = str(relative_path)

            results["files"].append(file_result)

            results["total_files"] += 1
            results["total_functions"] += len(
                file_result["functions"]
            )
            results["total_classes"] += len(
                file_result["classes"]
            )
            results["total_imports"] += len(
                file_result["imports"]
            )

        except (OSError, UnicodeError, SyntaxError, ValueError) as error:
            results["errors"].append({
                "file": str(relative_path),
                "error": str(error),
            })

    results["files"].sort(key=lambda f: f["file"])

    return results
