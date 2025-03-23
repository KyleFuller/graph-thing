from pathlib import Path as FSPath
from os import getenv

graph_root = getenv('GRAPH_ROOT')
if not graph_root:
    raise RuntimeError("GRAPH_ROOT environment variable must be set")

GRAPH_ROOT = FSPath(graph_root).resolve()
if not GRAPH_ROOT.is_dir():
    raise RuntimeError("GRAPH_ROOT must point to a valid directory")