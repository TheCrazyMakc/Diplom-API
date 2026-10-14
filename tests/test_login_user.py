import allure

from helpers import build_user_payload, generate_unique_email, generate_random_string


@allure.feature("Авторизация пользователя")
class TestLoginUser:

    @allure.title("Вход под существующим пользователем")
    @allure.description("POST /auth/login — успешный вход")
    def test_login_existing_user_success(self, api_client, created_user):
        with allure.step("Отправить POST /auth/login с корректными данными"):
            response = api_client.post(
                "/auth/login",
                json={
                    "email": created_user["payload"]["email"],
                    "password": created_user["payload"]["password"],
                },
            )

        with allure.step("Проверить успешный ответ"):
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["user"]["email"] == created_user["payload"]["email"]
            assert "accessToken" in data
            assert "refreshToken" in data

    @allure.title("Вход с неверным логином и паролем")
    @allure.description("POST /auth/login с несуществующими данными → 401")
    def test_login_with_wrong_credentials_returns_401(self, api_client):
        with allure.step("Отправить POST /auth/login с неверными данными"):
            response = api_client.post(
                "/auth/login",
                json={
                    "email": generate_unique_email(),
                    "password": generate_random_string(10),
                },
            )

        with allure.step("Проверить 401 и сообщение"):
            assert response.status_code == 401
            data = response.json()
            assert data["success"] is False
            assert data["message"] == "email or password are incorrect"