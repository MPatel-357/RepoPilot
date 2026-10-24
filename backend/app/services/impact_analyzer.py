
from collections import deque

import networkx as nx

from app.services.dependency_graph import build_dependency_graph


def analyze_impact(repository_path: str, target_file: str) -> dict:
    """
    Find files that directly or indirectly depend on a target file.

    Graph edges point from importer -> imported module.
    """
    graph_data = build_dependency_graph(repository_path)

    graph = nx.DiGraph()

    graph.add_nodes_from(graph_data["nodes"])

    for edge in graph_data["edges"]:
        graph.add_edge(edge["source"], edge["target"])

    if target_file not in graph:
        raise ValueError(
            f"File is not present in the graph: {target_file}"
        )

    # Reverse the graph so edges lead toward dependent files.
    reversed_graph = graph.reverse(copy=False)

    visited = {target_file}
    queue = deque([(target_file, 0, [target_file])])
    affected = []

    while queue:
        current, distance, path = queue.popleft()

        for dependent in sorted(reversed_graph.successors(current)):
            if dependent in visited:
                continue

            visited.add(dependent)

            next_path = path + [dependent]
            next_distance = distance + 1

            affected.append({
                "file": dependent,
                "distance": next_distance,
                "dependency_path": next_path,
                "impact_type": (
                    "direct" if next_distance == 1 else "indirect"
                ),
            })

            queue.append((dependent, next_distance, next_path))

    return {
        "target_file": target_file,
        "total_affected": len(affected),
        "affected_files": affected,
    }

