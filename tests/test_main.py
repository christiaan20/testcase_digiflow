import sys

from fastapi.testclient import TestClient
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.main import app

client = TestClient(app)





def test_file_endpoint_returns_404_when_file_is_missing() -> None:
    response = client.post("/file", json={"path": "data/missing.pdf"})

    assert response.status_code == 404
    assert "Text file not found" in response.json()["detail"]


