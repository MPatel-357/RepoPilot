
from pathlib import Path

import networkx as nx

from app.services.repository_scanner import scan_repository


def build_dependency_graph(repository_path: str) -> dict:
    """
    Build a directed graph of local Python module imports.

    An edge A -> B means that file A imports file B.
    """
    scan = scan_repository(repository_path)
    graph = nx.DiGraph()

    # Map Python module names to their file paths.
    module_map = {}

    for file in scan["files"]:
        file_path = file["file"]
        module = Path(file_path).with_suffix("")

        parts = list(module.parts)

        if parts[-1] == "__init__":
            parts.pop()

        module_name = ".".join(parts)

        if module_name:
            module_map[module_name] = file_path

        graph.add_node(file_path)

    # Connect files through their imports.
    for file in scan["files"]:
        source = file["file"]

        for imported in file["imports"]:
            if imported["module"].startswith("."):
                # Relative imports will be handled later.
                continue

            imported_module = imported["module"]

            # Try the full module, then its parent modules.
            parts = imported_module.split(".")

            for length in range(len(parts), 0, -1):
                candidate = ".".join(parts[:length])

                if candidate in module_map:
                    target = module_map[candidate]

                    if source != target:
                        graph.add_edge(source, target)

                    break

    return {
        "total_nodes": graph.number_of_nodes(),
        "total_edges": graph.number_of_edges(),
        "nodes": list(graph.nodes),
        "edges": [
            {"source": source, "target": target}
            for source, target in graph.edges
        ],
    }

