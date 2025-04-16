import asyncio
import random
from typing import Dict, List
from app.models import SystemGraph

async def check_health(node: str) -> bool:
    await asyncio.sleep(random.uniform(0.1, 0.5))
    if node == "Web/mobile":
        return random.random() < 0.9
    elif node == "Akamani/CDN":
        return random.random() < 0.95
    elif node == "Gateway":
        return random.random() < 0.85
    elif node == "UI sdk":
        return random.random() < 0.9
    elif node == "Authentication":
        return random.random() < 0.8
    elif node == "Internal Services":
        return random.random() < 0.75
    elif node == "External Service":
        return random.random() < 0.7
    elif node == "DB check for credentials":
        return random.random() < 0.95
    else:
        return random.random() < 0.8

def build_dag(graph: SystemGraph) -> (Dict[str, List[str]], Dict[str, int]):
    adj = {node: [] for node in graph.nodes}
    in_degree = {node: 0 for node in graph.nodes}

    for edge in graph.edges:
        if edge.from_node not in adj:
            adj[edge.from_node] = []
            in_degree[edge.from_node] = 0
        if edge.to_node not in adj:
            adj[edge.to_node] = []
            in_degree[edge.to_node] = 0
        adj[edge.from_node].append(edge.to_node)
        in_degree[edge.to_node] += 1
        
    return adj, in_degree

async def traverse_and_check_health(adj: Dict[str, List[str]], in_degree: Dict[str, int]) -> Dict[str, bool]:
    health_status = {}
    queue = [node for node, deg in in_degree.items() if deg == 0]
    while queue:
        tasks = {node: asyncio.create_task(check_health(node)) for node in queue}
        results = await asyncio.gather(*tasks.values())
        for node, result in zip(queue, results):
            health_status[node] = result
        next_queue = []
        for node in queue:
            for child in adj.get(node, []):
                in_degree[child] -= 1
                if in_degree[child] == 0:
                    next_queue.append(child)
        queue = next_queue
    return health_status
