import sys

from fastapi.testclient import TestClient
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app.main import app

client = TestClient(app)




# def test_root_endpoint_returns_message() -> None:
#     response = client.get("/")
#
#     assert response.status_code == 200
#     assert "POST /file" in response.json()["message"]
#
#
# def test_file_endpoint_returns_sample_text() -> None:
#     response = client.post("/file", json={"path": "data/sample.pdf"})
#
#     assert response.status_code == 200
#     assert response.json() == {
#         "path": "data/sample.pdf",
#         "content": (PROJECT_ROOT / "data" / "sample.pdf").read_text(encoding="utf-8"),
#     }


def test_file_endpoint_returns_404_when_file_is_missing() -> None:
    response = client.post("/file", json={"path": "data/missing.pdf"})

    assert response.status_code == 404
    assert "Text file not found" in response.json()["detail"]


# def test_file_endpoint_returns_400_for_non_txt_files() -> None:
#     response = client.post("/file", json={"path": "README.md"})
#
#     assert response.status_code == 400
#     assert response.json()["detail"] == "Only .pdf files are allowed."
#
#
# def test_file_endpoint_returns_400_for_path_traversal() -> None:
#     response = client.post("/file", json={"path": "../outside.pdf"})
#
#     assert response.status_code == 400
#     assert response.json()["detail"] == "Path must stay inside the repository root."



