import allure
import pytest

from helpers import build_user_payload, generate_unique_email


@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.title("Создание уникального пользователя")
    @allure.description("POST /auth/register — успешная регистрация нового уникального пользователя")
    def test_create_unique_user_success(self, api_client):
        payload = build_user_payload()

        with allure.step("Отправить POST /auth/register"):
            response = api_client.post("/auth/register", json=payload)

        with allure.step("Проверить код ответа 200 и тело"):
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["user"]["email"] == payload["email"]
            assert data["user"]["name"] == payload["name"]
            assert "accessToken" in data
            assert "refreshToken" in data

        # Постусловие: удаляем созданного пользователя
        with allure.step("Удалить созданного пользователя"):
            headers = {"Authorization": data["accessToken"]}
            api_client.delete("/auth/user", headers=headers)

    @allure.title("Создание уже зарегистрированного пользователя")
    @allure.description("POST /auth/register — повторная регистрация существующего пользователя → 403")
    def test_create_duplicate_user_returns_403(self, api_client, created_user):
        with allure.step("Отправить POST /auth/register с теми же данными"):
            response = api_client.post("/auth/register", json=created_user["payload"])

        with allure.step("Проверить код 403 и сообщение"):
            assert response.status_code == 403
            data = response.json()
            assert data["success"] is False
            assert data["message"] == "User already exists"

    @allure.title("Создание пользователя без одного из обязательных полей")
    @allure.description("POST /auth/register без email → 403")
    def test_create_user_without_email_returns_403(self, api_client):
        payload = build_user_payload()
        payload.pop("email")

        with allure.step("Отправить POST /auth/register без email"):
            response = api_client.post("/auth/register", json=payload)

        with allure.step("Проверить код 403"):
            assert response.status_code == 403
            data = response.json()
            assert data["success"] is False
            assert data["message"] == "Email, password and name are required fields"

    @allure.title("Создание пользователя без пароля")
    @allure.description("POST /auth/register без password → 403")
    def test_create_user_without_password_returns_403(self, api_client):
        payload = build_user_payload()
        payload.pop("password")

        response = api_client.post("/auth/register", json=payload)

        assert response.status_code == 403
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "Email, password and name are required fields"

    @allure.title("Создание пользователя без имени")
    @allure.description("POST /auth/register без name → 403")
    def test_create_user_without_name_returns_403(self, api_client):
        payload = build_user_payload()
        payload.pop("name")

        response = api_client.post("/auth/register", json=payload)

        assert response.status_code == 403
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "Email, password and name are required fields"