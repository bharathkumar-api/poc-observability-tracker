import base64
import csv
from fastapi import APIRouter, Query
from app.models import SystemGraph
from app.health import build_dag, traverse_and_check_health
from app.visualization import generate_graph_image
from typing import Optional

router = APIRouter()

@router.post("/healthcheck")
async def check_system_health(
    graph: SystemGraph,
    visualize: Optional[bool] = Query(False, description="Save graph visualization as an image file"),
    output: Optional[str] = Query("json", description="Output format: 'json' or 'table' (saves table as CSV)")
):
    adj, in_degree = build_dag(graph)
    health_status = await traverse_and_check_health(adj, in_degree)
    result_table = [{"node": node, "healthy": health_status.get(node, True)} for node in graph.nodes]
    
    response_data = {"health_table": result_table}

    if visualize:
        graph_image = generate_graph_image(graph, health_status)
        if graph_image:
            image_filename = "graph.png"
            with open(image_filename, "wb") as f:
                f.write(base64.b64decode(graph_image))
            response_data["graph_image_file"] = image_filename

    if output.lower() == "table":
        table_filename = "health_table.csv"
        with open(table_filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["node", "healthy"])
            writer.writeheader()
            for row in result_table:
                writer.writerow(row)
        response_data["table_file"] = table_filename

    return response_data
