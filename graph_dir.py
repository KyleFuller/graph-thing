from pathlib import Path
from os import getenv

graph_dir = getenv('GRAPH_DIR')
if not graph_dir:
    raise RuntimeError("GRAPH_DIR environment variable must be set")

GRAPH_DIR = Path(graph_dir).resolve()
if not GRAPH_DIR.is_dir():
    raise RuntimeError("GRAPH_DIR must point to a valid directory")
