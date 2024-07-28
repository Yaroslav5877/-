import requests
import allure
import pytest

base_url = "https://web-gate.chitai-gorod.ru/api/"

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3VzZXItcmlnaHQiLCJzdWIiOjIwODUwODA3LCJpYXQiOjE3MTI5NDUxMDgsImV4cCI6MTcxMjk0ODcwOCwidHlwZSI6MjB9.Kx5iWcfjpLzpu31j50oYOx2CtXI-7CX608WdXckXRcA",
    "cache-control": "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}


# Функциональные тесты API
@allure.feature("Поиск книг")
@allure.story("Позитивные проверки")
@allure.title("Поиск существующей книги на русском языке")
def test_search_existing_book():
    url = f"{base_url}v2/search/search-phrase-suggests"
    params = {
        "suggests[page]": "1",
        "suggests[per-page]": "5",
        "phrase": "Призраки",
        "include": "products,authors,bookCycles,publisherSeries,publishers,categories"
    }
    response = requests.get(url, headers=headers, params=params)
    assert response.status_code == 200


@allure.feature("Поиск книг")
@allure.story("Позитивные проверки")
@allure.title("Поиск книги с символом \"-\"")
def test_search_book_with_dash():
    url = f"{base_url}v2/search/product"
    params = {
        "customerCityId": "213",
        "phrase": "т-34",
        "products[page]": "1",
        "products[per-page]": "48",
        "sortPreset": "relevance"
    }
    response = requests.get(url, headers=headers, params=params)
    assert response.status_code == 200


@allure.feature("Корзина")
@allure.story("Добавление в корзину")
@allure.title("Добавление книги в корзину")
def test_add_book_to_cart():
    url = f"{base_url}v1/cart/product"
    payload = {
        "product_id": "119562401"
    }
    response = requests.post(url, headers=headers, json=payload)
    assert response.status_code == 200


@allure.feature("Корзина")
@allure.story("Удаление из корзины")
@allure.title("Удаление книги через кнопку привязанную к книге (по ID книги)")
def test_delete_book_from_cart():
    url = f"{base_url}v1/cart/product/119562401"
    response = requests.delete(url, headers=headers)
    assert response.status_code == 404


# Нефункциональные тесты API
@allure.feature("Нефункциональные тесты")
@allure.story("Тестирование производительности")
@allure.title("Проверка времени отклика на поиск книги")
def test_response_time_search():
    url = f"{base_url}v2/search/search-phrase-suggests"
    params = {
        "suggests[page]": "1",
        "suggests[per-page]": "5",
        "phrase": "Призраки",
        "include": "products,authors,bookCycles,publisherSeries,publishers,categories"
    }
    response = requests.get(url, headers=headers, params=params)
    assert response.elapsed.total_seconds() < 1


@allure.feature("Нефункциональные тесты")
@allure.story("Тестирование безопасности")
@allure.title("Проверка авторизации")
def test_authorization():
    url = f"{base_url}v2/search/search-phrase-suggests"
    headers_no_auth = headers.copy()
    headers_no_auth.pop("authorization")
    response = requests.get(url, headers=headers_no_auth)
    assert response.status_code == 401
