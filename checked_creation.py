from node import Node
from edge import Edge
from creation import (
    create_edge_idempotent,
    create_connected_node,
    create_edge
)

def check_edge_name_well_formed(name: str) -> None:
    if not name or '/' in name:
        raise ValueError(f"Invalid edge name: {name}")

def check_edge_name_available(source: Node, target: Node, name: str) -> None:
    check_edge_name_well_formed(name)
    edge_fs_path = source.fs_path / name
    if edge_fs_path.exists() and not (edge_fs_path.is_symlink() and edge_fs_path.resolve() == target.fs_path):
        raise ValueError(f"Name '{name}' conflicts with existing file")

def check_edge_name_available_strict(source: Node, name: str) -> None:
    check_edge_name_well_formed(name)
    edge_fs_path = source.fs_path / name
    if edge_fs_path.exists():
        raise ValueError(f"Name '{name}' conflicts with existing file")

def checked_create_edge_idempotent(source: Node, target: Node, name: str) -> Edge:
    check_edge_name_available(source, target, name)
    return create_edge_idempotent(source, target, name)

def checked_create_biedge_idempotent(
            node1: Node, node2: Node, name1: str, name2: str
        ) -> tuple[Edge, Edge]:
    check_edge_name_available(node1, node2, name1)
    check_edge_name_available(node2, node1, name2)
    edge1 = create_edge_idempotent(node1, node2, name1)
    edge2 = create_edge_idempotent(node2, node1, name2)
    return edge1, edge2

def checked_create_connected_node(source: Node, name: str) -> tuple[Node, Edge]:
    check_edge_name_available_strict(source, name)
    return create_connected_node(source, name)

def checked_create_biconnected_node(
            source: Node, name_to: str, name_from: str
        ) -> tuple[Node, Edge, Edge]:
    target, edge1 = checked_create_connected_node(source, name_to)
    edge2 = create_edge(target, source, name_from)
    return target, edge1, edge2