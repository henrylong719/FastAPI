from fastapi import status
from fastapi.testclient import TestClient


class TestCreateIssue:
    def test_create_issue(self, client: TestClient, auth_header: dict):
        response = client.post(
            "/api/v1/issues/",
            json={
                "title": "Bug report",
                "description": "Something is broken",
                "priority": "high",
            },
            headers=auth_header,
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == "Bug report"
        assert data["status"] == "open"
        assert "id" in data

    def test_create_issue_validation_error(
        self, client: TestClient, auth_header: dict
    ):
        response = client.post(
            "/api/v1/issues/", json={"title": "ab"}, headers=auth_header
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_issue_unauthenticated(self, client: TestClient):
        response = client.post(
            "/api/v1/issues/",
            json={
                "title": "Bug report",
                "description": "Something is broken",
                "priority": "high",
            },
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestGetIssues:
    def test_list_empty(self, client: TestClient, auth_header: dict):
        response = client.get("/api/v1/issues/", headers=auth_header)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_list_with_issue(
        self, client: TestClient, auth_header: dict, sample_issue: dict
    ):
        response = client.get("/api/v1/issues/", headers=auth_header)
        assert len(response.json()) == 1

    def test_get_by_id(
        self, client: TestClient, auth_header: dict, sample_issue: dict
    ):
        response = client.get(
            f"/api/v1/issues/{sample_issue['id']}", headers=auth_header
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == sample_issue["id"]

    def test_get_not_found(self, client: TestClient, auth_header: dict):
        response = client.get(
            "/api/v1/issues/nonexistent", headers=auth_header
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestUpdateIssue:
    def test_update_title(
        self, client: TestClient, auth_header: dict, sample_issue: dict
    ):
        response = client.put(
            f"/api/v1/issues/{sample_issue['id']}",
            json={"title": "Updated title"},
            headers=auth_header,
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["title"] == "Updated title"

    def test_update_not_found(self, client: TestClient, auth_header: dict):
        response = client.put(
            "/api/v1/issues/nonexistent",
            json={"title": "Nope"},
            headers=auth_header,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteIssue:
    def test_delete_issue(
        self, client: TestClient, auth_header: dict, sample_issue: dict
    ):
        response = client.delete(
            f"/api/v1/issues/{sample_issue['id']}", headers=auth_header
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

        response = client.get(
            f"/api/v1/issues/{sample_issue['id']}", headers=auth_header
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_not_found(self, client: TestClient, auth_header: dict):
        response = client.delete(
            "/api/v1/issues/nonexistent", headers=auth_header
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestAuth:
    def test_login_success(self, client: TestClient):
        response = client.post(
            "/api/v1/auth/token",
            data={"username": "johndoe", "password": "secret"},
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_bad_password(self, client: TestClient):
        response = client.post(
            "/api/v1/auth/token",
            data={"username": "johndoe", "password": "wrong"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_unknown_user(self, client: TestClient):
        response = client.post(
            "/api/v1/auth/token",
            data={"username": "nobody", "password": "secret"},
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestHealthCheck:
    def test_health(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"status": "ok"}
