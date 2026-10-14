import random
import string


def generate_random_string(length: int = 10) -> str:
    """Генерирует случайную строку из строчных букв."""
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for _ in range(length))


def generate_unique_email() -> str:
    """Генерирует уникальный email."""
    return f"{generate_random_string(12)}@yandex.ru"


def build_user_payload(email: str = None, password: str = None, name: str = None) -> dict:
    """Собирает тело запроса для регистрации пользователя."""
    return {
        "email": email if email is not None else generate_unique_email(),
        "password": password if password is not None else generate_random_string(10),
        "name": name if name is not None else generate_random_string(8),
    }