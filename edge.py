from node import Node, fs_path_to_node
from pathlib import Path as FSPath
import os

class Edge:
    def __init__(self, source: Node, name: str) -> None:
        self._source = source
        self._name = name
        
        edge_fs_path = source.fs_path / name
        assert os.access(edge_fs_path, os.R_OK) # edges must be readable
        if not edge_fs_path.exists():
            raise ValueError(f"Edge '{name}' does not exist in node {source.fs_path}")
        if not edge_fs_path.is_symlink():
            raise ValueError(f"'{name}' exists but is not a symlink")
        
        target_fs_path = edge_fs_path.resolve()
        if not target_fs_path.is_dir():
            raise ValueError(f"Edge '{name}' points to {target_fs_path}, which is not a directory")

        self._target = fs_path_to_node(self.source.fs_path / self.name)

    @property
    def source(self) -> Node:
        return self._source
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def target(self) -> Node:
        return self._target
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Edge):
            return False
        return (self.source == other.source and 
                self.name == other.name)

    def __hash__(self) -> int:
        return hash((self.source, self.name))
    
def fs_path_to_edge(edge_fs_path: FSPath) -> Edge:
    source = fs_path_to_node(edge_fs_path.parent)
    return Edge(source, edge_fs_path.name)