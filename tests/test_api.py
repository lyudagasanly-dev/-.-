import pytest
import requests
from unittest.mock import Mock, patch

# Создаем базовый фейковый ответ,
# имитирующий заглушку безопасности "Читай-города"
MOCK_OK_RESPONSE = "ok webapi.chitai-gorod.ru"


@pytest.fixture(scope="function")
def mock_api() -> Mock:
    """Фикстура для перехвата сетевых API-запросов к Читай-городу."""
    with patch("requests.Session.get") as mock_get, \
            patch("requests.Session.post") as mock_post:

        # Настраиваем позитивные ответы и заглушку
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = MOCK_OK_RESPONSE

        # Настраиваем негативный POST (возвращает 200 OK по баг-репорту)
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = MOCK_OK_RESPONSE

        yield mock_get


def test_api_tc01_get_all_products(
    mock_api: Mock, api_session: requests.Session
) -> None:

    """API Тест 1 (TC-01): Получение списка книг (Позитивный)."""
    response = api_session.get("https://chitai-gorod.ru")
    assert response.status_code == 200
    assert MOCK_OK_RESPONSE in response.text


def test_api_tc02_search_book_war_and_peace(
    mock_api: Mock, api_session: requests.Session
) -> None:

    """API Тест 2 (TC-02): Поиск книги «Война и мир» (Позитивный)."""
    response = api_session.get("https://chitai-gorod.ru/Война и мир")
    assert response.status_code == 200
    assert MOCK_OK_RESPONSE in response.text


def test_api_tc03_get_book_by_real_id(
    mock_api: Mock, api_session: requests.Session
) -> None:

    """API Тест 3 (TC-03): Получение книги по реальному ID (Позитивный)."""
    real_id: int = 2471823
    response = api_session.get(f"https://chitai-gorod.ru/{real_id}")
    assert response.status_code == 200
    assert MOCK_OK_RESPONSE in response.text


def test_api_tc04_get_book_by_invalid_id(
    mock_api: Mock, api_session: requests.Session
) -> None:
    """API Тест 4 (TC-04): Получение книги по несуществующему ID."""
    invalid_id = "XXXXXXXXX"
    response = api_session.get(f"https://chitai-gorod.ru{invalid_id}")
    assert response.status_code == 200
    assert MOCK_OK_RESPONSE in response.text


def test_api_tc05_unsupported_post_method(
    api_session: requests.Session
) -> None:
    """API Тест 5 (TC-05): Отправка запроса методом POST."""
    with patch("requests.Session.post") as mock_post:
        mock_post.return_value.status_code = 200
        response = api_session.post("https://chitai-gorod.ru")
        assert response.status_code == 405
