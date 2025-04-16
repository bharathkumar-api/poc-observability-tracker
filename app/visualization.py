import base64
from typing import Optional, Dict
from app.models import SystemGraph

try:
    from graphviz import Digraph
except ImportError:
    Digraph = None

def generate_graph_image(graph: SystemGraph, health_status: Dict[str, bool]) -> Optional[str]:
    if Digraph is None:
        return None
    dot = Digraph(comment="System Health DAG")
    for node in graph.nodes:
        color = "green" if health_status.get(node, True) else "red"
        dot.node(node, node, style="filled", fillcolor=color)
    for edge in graph.edges:
        dot.edge(edge.from_node, edge.to_node)
    img_bytes = dot.pipe(format="png")
    base64_img = base64.b64encode(img_bytes).decode("utf-8")
    return base64_img
