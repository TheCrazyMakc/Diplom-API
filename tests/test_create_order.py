import allure
import pytest

# Валидные id ингредиентов из реального API Stellar Burgers
VALID_INGREDIENT_1 = "60d3b41abdacab0026a733c6"
VALID_INGREDIENT_2 = "609646e4dc916e00276b2870"
INVALID_INGREDIENT = "000000000000000000000000"


def _get_valid_ingredients(api_client) -> list:
    """Забирает актуальные id ингредиентов с сервера."""
    response = api_client.get("/ingredients")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    return [item["_id"] for item in data["data"][:2]]


@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    @allure.description("POST /orders с токеном и валидными ингредиентами → 200")
    def test_create_order_authorized_with_ingredients(self, api_client, created_user):
        ingredients = _get_valid_ingredients(api_client)
        headers = {"Authorization": created_user["accessToken"]}

        with allure.step("Отправить POST /orders с токеном"):
            response = api_client.post(
                "/orders",
                json={"ingredients": ingredients},
                headers=headers,
            )

        with allure.step("Проверить успешный ответ"):
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert "name" in data
            assert "order" in data and "number" in data["order"]

    @allure.title("Создание заказа без авторизации")
    @allure.description("POST /orders без токена → 401")
    def test_create_order_unauthorized(self, api_client):
        ingredients = _get_valid_ingredients(api_client)

        with allure.step("Отправить POST /orders без токена"):
            response = api_client.post(
                "/orders",
                json={"ingredients": ingredients},
            )

        with allure.step("Проверить 401"):
            assert response.status_code == 401
            data = response.json()
            assert data["success"] is False
            assert data["message"] == "You should be authorised"

    @allure.title("Создание заказа без ингредиентов")
    @allure.description("POST /orders с пустым массивом ингредиентов → 400")
    def test_create_order_without_ingredients(self, api_client, created_user):
        headers = {"Authorization": created_user["accessToken"]}

        with allure.step("Отправить POST /orders с пустым ingredients"):
            response = api_client.post(
                "/orders",
                json={"ingredients": []},
                headers=headers,
            )

        with allure.step("Проверить 400 и сообщение"):
            assert response.status_code == 400
            data = response.json()
            assert data["success"] is False
            assert data["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с неверным хешем ингредиента")
    @allure.description("POST /orders с несуществующим id ингредиента → 500")
    def test_create_order_with_invalid_hash(self, api_client, created_user):
        headers = {"Authorization": created_user["accessToken"]}

        with allure.step("Отправить POST /orders с невалидным хешем"):
            response = api_client.post(
                "/orders",
                json={"ingredients": [INVALID_INGREDIENT]},
                headers=headers,
            )

        with allure.step("Проверить 500 Internal Server Error"):
            assert response.status_code == 500

    @allure.title("Создание заказа с ингредиентами (проверка валидных id)")
    @allure.description("POST /orders с двумя реальными ингредиентами → 200")
    def test_create_order_with_valid_ingredients(self, api_client, created_user):
        ingredients = [VALID_INGREDIENT_1, VALID_INGREDIENT_2]
        headers = {"Authorization": created_user["accessToken"]}

        response = api_client.post(
            "/orders",
            json={"ingredients": ingredients},
            headers=headers,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True