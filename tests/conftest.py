import shutil
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.config import settings


@pytest.fixture(autouse=True)
def _isolate_data(tmp_path: Path):
    """Redirect storage to a temp directory so tests never touch real data."""
    original = settings.data_dir
    test_data_dir = tmp_path / "data"
    test_data_dir.mkdir()
    settings.data_dir = test_data_dir

    import app.storage as storage_mod

    storage_mod.DATA_FILE = test_data_dir / "issues.json"

    yield

    settings.data_dir = original
    storage_mod.DATA_FILE = original / "issues.json"
    shutil.rmtree(test_data_dir, ignore_errors=True)


@pytest.fixture()
def client() -> TestClient:
    from app.main import create_app

    return TestClient(create_app())


@pytest.fixture()
def auth_header(client: TestClient) -> dict[str, str]:
    """Authenticate as the test user and return an Authorization header."""
    response = client.post(
        "/api/v1/auth/token",
        data={"username": "johndoe", "password": "secret"},
    )
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def sample_issue(client: TestClient, auth_header: dict[str, str]) -> dict:
    response = client.post(
        "/api/v1/issues/",
        json={
            "title": "Sample issue",
            "description": "A description for testing",
            "priority": "high",
        },
        headers=auth_header,
    )
    return response.json()
