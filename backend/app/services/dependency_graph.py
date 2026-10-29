
from pathlib import Path

import networkx as nx

from app.services.repository_scanner import scan_repository


def build_dependency_graph(repository_path: str) -> dict:
    """
    Build a graph of local Python imports.

    An edge A -> B means file A imports file B.
    Supports absolute and relative static imports.
    """
    scan = scan_repository(repository_path)
    graph = nx.DiGraph()
    module_map = {}

    # Step 1: Map module names to repository files.
    for file in scan["files"]:
        file_path = file["file"]
        parts = list(Path(file_path).with_suffix("").parts)

        if parts[-1] == "__init__":
            parts.pop()

        module_name = ".".join(parts)

        if module_name:
            module_map[module_name] = file_path

        graph.add_node(file_path)

    def find_module(module_name):
        """Find the closest existing local module."""
        parts = module_name.split(".")

        for length in range(len(parts), 0, -1):
            candidate = ".".join(parts[:length])

            if candidate in module_map:
                return module_map[candidate]

        return None

    # Step 2: Resolve local import relationships.
    for file in scan["files"]:
        source = file["file"]
        source_parts = list(Path(source).with_suffix("").parts)

        # __init__.py belongs to the package itself.
        if source_parts[-1] == "__init__":
            package_parts = source_parts[:-1]
        else:
            package_parts = source_parts[:-1]

        for imported in file["imports"]:
            module = imported["module"]
            names = imported.get("names", [])

            if module.startswith("."):
                level = len(module) - len(module.lstrip("."))
                remainder = module[level:]

                if level > len(package_parts):
                    continue

                base_parts = package_parts[:len(package_parts) - level + 1]

                if remainder:
                    base_parts.extend(remainder.split("."))

                base_module = ".".join(base_parts)

            else:
                base_module = module

            # A "from package import module" statement may
            # refer to a submodule rather than a symbol.
            candidates = []

            for name in names:
                if name != "*":
                    candidates.append(
                        f"{base_module}.{name}" if base_module else name
                    )

            if base_module:
                candidates.append(base_module)

            targets = set()

            for candidate in candidates:
                target = find_module(candidate)

                if target and target != source:
                    targets.add(target)

            for target in targets:
                graph.add_edge(source, target)

    return {
        "total_nodes": graph.number_of_nodes(),
        "total_edges": graph.number_of_edges(),
        "nodes": sorted(graph.nodes),
        "edges": [
            {"source": source, "target": target}
            for source, target in sorted(graph.edges)
        ],
    }
