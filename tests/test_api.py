import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

TEST_FILE_PATH = "tests/sample.txt"

@pytest.fixture(scope="session", autouse=True)
def setup_sample_file():
    os.makedirs("tests", exist_ok=True)
    with open(TEST_FILE_PATH, "w") as f:
        f.write("This is a test document. It contains basic information about FastAPI and Python.")
    yield
    os.remove(TEST_FILE_PATH)

def test_upload_file():
    with open(TEST_FILE_PATH, "rb") as f:
        response = client.post("/api/files/", files={"file": ("sample.txt", f)})
    assert response.status_code == 200
    assert "file_id" in response.json()

def test_list_files():
    response = client.get("/api/files/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_ask_question():
    payload = {"question": "What is this document about?"}
    response = client.post("/api/ask/", json=payload)
    assert response.status_code == 200
    assert "answer" in response.json()
