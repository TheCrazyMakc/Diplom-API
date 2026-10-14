import pytest
import requests
import allure

from helpers import build_user_payload

BASE_URL = "https://stellarburgers.education-services.ru/api"


@pytest.fixture
def api_client():
    """Простая обёртка над requests.Session с базовым URL."""
    class ApiClient:
        def __init__(self):
            self.session = requests.Session()
            self.base_url = BASE_URL

        def post(self, endpoint, json=None, headers=None):
            return self.session.post(f"{self.base_url}{endpoint}", json=json, headers=headers)

        def get(self, endpoint, headers=None):
            return self.session.get(f"{self.base_url}{endpoint}", headers=headers)

        def patch(self, endpoint, json=None, headers=None):
            return self.session.patch(f"{self.base_url}{endpoint}", json=json, headers=headers)

        def delete(self, endpoint, headers=None):
            return self.session.delete(f"{self.base_url}{endpoint}", headers=headers)

        def close(self):
            self.session.close()

    client = ApiClient()
    yield client
    client.close()


@pytest.fixture
def created_user(api_client):
    """
    Создаёт уникального пользователя перед тестом.
    Возвращает dict: {payload, accessToken, refreshToken}.
    После теста — удаляет пользователя.
    """
    payload = build_user_payload()
    with allure.step("Предусловие: создать уникального пользователя"):
        response = api_client.post("/auth/register", json=payload)
        assert response.status_code == 200, f"Не удалось создать пользователя: {response.text}"
        data = response.json()

    yield {
        "payload": payload,
        "accessToken": data["accessToken"],
        "refreshToken": data["refreshToken"],
    }

    # Постусловие: удалить пользователя
    with allure.step("Постусловие: удалить пользователя"):
        headers = {"Authorization": data["accessToken"]}
        api_client.delete("/auth/user", headers=headers)