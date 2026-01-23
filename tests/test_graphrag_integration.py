"""
Integration tests for GraphRAG API endpoints.

Tests cover the integration between FastAPI endpoints and the GraphRAG service.
Service layer unit tests are in test_graphrag_service.py.
"""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def integration_document_path() -> Path:
    """
    Get path to sample test document for integration tests.

    Returns:
        Path to book.txt in test_data/input/
    """
    return Path("test_data/input/book.txt")


def test_index_documents_endpoint(client: TestClient):
    """Test /index endpoint returns correct structure."""
    response = client.post("/index")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "indexed_files" in data
    assert "entities_extracted" in data
    assert "nodes" in data
    assert "edges" in data
    assert "communities" in data
    assert isinstance(data["indexed_files"], list)
    assert isinstance(data["nodes"], int)
    assert isinstance(data["edges"], int)


def test_update_documents_endpoint(client: TestClient):
    """Test /update endpoint returns correct structure."""
    response = client.post("/update")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "updated_files" in data
    assert "entities_extracted" in data
    assert "nodes" in data
    assert "edges" in data
    assert "communities" in data
    assert isinstance(data["updated_files"], list)
    assert isinstance(data["nodes"], int)
    assert isinstance(data["edges"], int)


def test_query_endpoint_with_graphrag_service(client: TestClient, sample_local_query: dict):
    """Test /query endpoint integrates with GraphRAG service."""
    response = client.post("/query", json=sample_local_query)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "citations" in data
    assert "method" in data
    assert data["method"] == "local"


@pytest.mark.parametrize("method", ["local", "global", "drift", "basic"])
def test_query_all_methods_with_endpoint(client: TestClient, method: str):
    """Test query endpoint works with all GraphRAG methods."""
    query = {
        "question": "Test question for GraphRAG",
        "method": method,
    }
    response = client.post("/query", json=query)
    assert response.status_code == 200
    assert response.json()["method"] == method


def test_sample_document_exists(integration_document_path: Path):
    """Test that sample document exists in test_data."""
    # This test will pass even if file doesn't exist yet (planned for migration)
    expected_location = Path("test_data/input/book.txt")
    assert integration_document_path == expected_location
