#!/usr/bin/env python3.13

from node import Node, is_fs_path_node
from edge import Edge
from collections import deque
import os
from functools import cached_property
from collections import abc

from typing import TypeVar

NodeT = TypeVar('NodeT')
EdgeT = TypeVar('EdgeT')

def bfs[NodeT, EdgeT](
    start: NodeT,
    get_adjacencies: abc.Callable[[NodeT], abc.Iterable[EdgeT]],
    should_traverse: abc.Callable[[EdgeT], bool],
    get_target: abc.Callable[[EdgeT], NodeT],
    visit: abc.Callable[[NodeT], None],
) -> None:
    visited: set[NodeT] = set()
    queue: deque[NodeT] = deque([start])
    
    while queue:
        current = queue.popleft()
        if current in visited:
            continue
        
        visited.add(current)
        visit(current)
        for adjacent in get_adjacencies(current):
            if should_traverse(adjacent):
                target = get_target(adjacent)
                if target not in visited:
                    queue.append(target)
        
class Subgraph:
    def __init__(self, root: Node) -> None:
        self._root: Node = root
        self._adjacency_list: dict[Node, abc.Set[Edge]] = {}
        self._fill_adjacency_list()
    

    def _fill_adjacency_list(self) -> None:
        def add_to_adjacency_list(node: Node) -> None:
            self._adjacency_list[node] = self._read_edges_from_fs(node)
        
        bfs(
            self._root,
            get_adjacencies=self._read_edges_from_fs,
            should_traverse=lambda _: True,
            get_target=lambda edge: edge.target,
            visit=add_to_adjacency_list,
        )
    
    def _read_edges_from_fs(self, node: Node) -> abc.Set[Edge]:
        edges: set[Edge] = set()
        for item in os.listdir(node.fs_path):
            item_fs_path = node.fs_path / item
            if item_fs_path.is_symlink():
                if is_fs_path_node(item_fs_path):
                    edge = Edge(node, item)
                    edges.add(edge)
        return edges
    
    def get_edges(self, node: Node) -> abc.Set[Edge]:
        return self._adjacency_list.get(node, set())
    
    @property
    def root(self) -> Node:
        return self._root
    
    @property
    def nodes(self) -> abc.Set[Node]:
        return self._adjacency_list.keys()

    @cached_property
    def edges(self) -> abc.Set[Edge]:
        all_edges: set[Edge] = set()
        for edge_set in self._adjacency_list.values():
            all_edges.update(edge_set)
        return frozenset(all_edges)