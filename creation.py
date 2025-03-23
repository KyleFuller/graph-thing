from node import Node
from edge import Edge
from graph_dir import GRAPH_DIR
from get_small_unused_name import get_small_unused_name

def create_edge(source: Node, target: Node, name: str) -> Edge:
    (source.fs_path / name).symlink_to(target.fs_path)
    return Edge(source, name)

def create_edge_idempotent(source: Node, target: Node, name: str) -> Edge:
    edge_fs_path = source.fs_path / name
    if edge_fs_path.exists():
        assert edge_fs_path.is_symlink() and edge_fs_path.resolve() == target.fs_path
        return Edge(source, name)
    return create_edge(source, target, name)

def create_node() -> Node:
    def is_node_name_used(name: str) -> bool:
        return (GRAPH_DIR / name).exists()

    node_id = get_small_unused_name(is_node_name_used)
    (GRAPH_DIR / node_id).mkdir()
    return Node(node_id)

def create_connected_node(source: Node, name: str) -> tuple[Node, Edge]:
    target = create_node()
    edge = create_edge(source, target, name)
    return target, edge