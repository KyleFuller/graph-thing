from pathlib import Path as FSPath
from graph_dir import GRAPH_DIR

class Node:
    def __init__(self, node_id: str) -> None:
        self._fs_path = (GRAPH_DIR / node_id).resolve()
        if not self._fs_path.is_dir():
            raise ValueError(f"Not a valid node: {node_id}")
        if not self._fs_path.parent.samefile(GRAPH_DIR):
            raise ValueError(f"Path {self._fs_path} is not in {GRAPH_DIR}")
    @property
    def fs_path(self) -> FSPath:
        return self._fs_path

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return False
        return self.fs_path == other.fs_path

    def __hash__(self) -> int:
        return hash(self.fs_path)

def fs_path_to_node(fs_path: FSPath) -> Node:
    return Node(fs_path.resolve(strict=True).name)

def is_fs_path_node(fs_path: FSPath) -> bool:
    try:
        fs_path_to_node(fs_path)
        return True
    except ValueError:
        return False