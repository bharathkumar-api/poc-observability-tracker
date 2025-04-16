from pydantic import BaseModel, Field
from typing import List

class Edge(BaseModel):
    from_node: str = Field(..., alias="Upstream_application")
    to_node: str = Field(..., alias="Downstream_application")

class SystemGraph(BaseModel):
    nodes: List[str]
    edges: List[Edge]
