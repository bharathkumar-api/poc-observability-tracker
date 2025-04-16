import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def system_graph_payload():
    return {
        "nodes": [
            "Web/mobile",
            "Akamani/CDN",
            "Gateway",
            "UI sdk",
            "Authentication",
            "Internal Services",
            "External Service",
            "DB check for credentials"
        ],
        "edges": [
            { "Upstream_application": "Web/mobile", "Downstream_application": "Akamani/CDN" },
            { "Upstream_application": "Akamani/CDN", "Downstream_application": "Gateway" },
            { "Upstream_application": "Gateway", "Downstream_application": "UI sdk" },
            { "Upstream_application": "Gateway", "Downstream_application": "Authentication" },
            { "Upstream_application": "Authentication", "Downstream_application": "Internal Services" },
            { "Upstream_application": "Authentication", "Downstream_application": "External Service" },
            { "Upstream_application": "Internal Services", "Downstream_application": "DB check for credentials" },
            { "Upstream_application": "External Service", "Downstream_application": "DB check for credentials" }
        ]
    }

def test_json_output(system_graph_payload):
    response = client.post("/api/healthcheck?visualize=false&output=json", json=system_graph_payload)
    assert response.status_code == 200
    data = response.json()
    assert "health_table" in data
    nodes = [entry["node"] for entry in data["health_table"]]
    for node in system_graph_payload["nodes"]:
        assert node in nodes
    assert "table_file" not in data
    assert "graph_image_file" not in data

def test_table_output(system_graph_payload):
    response = client.post("/api/healthcheck?visualize=false&output=table", json=system_graph_payload)
    assert response.status_code == 200
    data = response.json()
    assert "health_table" in data
    assert "table_file" in data
    table_file = data["table_file"]
    assert os.path.exists(table_file)
    with open(table_file, "r") as f:
        content = f.read()
        assert len(content) > 0
    os.remove(table_file)

def test_visualize_output(system_graph_payload):
    response = client.post("/api/healthcheck?visualize=true&output=json", json=system_graph_payload)
    assert response.status_code == 200
    data = response.json()
    assert "health_table" in data
    assert "graph_image_file" in data
    graph_file = data["graph_image_file"]
    assert os.path.exists(graph_file)
    with open(graph_file, "rb") as f:
        content = f.read()
        assert len(content) > 0
    os.remove(graph_file)
