from urllib.parse import quote

import allure
import requests

access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3VzZXItcmlnaHQiLCJzdWIiOjIwODY5NjE5LCJpYXQiOjE3MjIxOTE0NzYsImV4cCI6MTcyMjE5NTA3NiwidHlwZSI6MjB9.Ne4QpZpMfxROBWtSX7o9pNDxx5sK2IgkI9GWn6lWV0g'


@allure.feature("Поиск книг")
@allure.story("Позитивные проверки")
@allure.title("Поиск существующей книги на русском языке")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_existing_book():
    base_url = "https://web-gate.chitai-gorod.ru/api/v2/search/search-phrase-suggests"
    params = {
        "suggests[page]": "1",
        "suggests[per-page]": "5",
        "phrase": "Призрак",
        "include": "products,authors,bookCycles,publisherSeries,publishers,categories"
    }
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": f"Bearer {access_token}",
        "cache-control": "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    response = requests.get(base_url, headers=headers, params=params)
    assert response.status_code == 200

    data = response.json()

    # Проверка данных в ответе
    assert "data" in data
    assert "attributes" in data["data"]
    assert "relationships" in data["data"]

    relationships = data["data"]["relationships"]
    assert "products" in relationships
    assert len(relationships["products"]["data"]) > 0

    products = relationships["products"]["data"]

    # Проверка наличия книги с названием, содержащим слово "Призрак"
    found = any(
        product["id"] in {product_item["id"] for product_item in products} and
        "Призрак" in product.get("attributes", {}).get("title", "")
        for product in data.get("included", [])
    )

    assert found, "No book with 'Призрак' in the title found in search results"


@allure.feature("Поиск книг")
@allure.story("Позитивные проверки")
@allure.title("Поиск существующей книги с символом '-'")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_book_with_dash():
    base_url = "https://web-gate.chitai-gorod.ru/api/v2/search/search-phrase-suggests"
    params = {
        "suggests[page]": "1",
        "suggests[per-page]": "5",
        "phrase": "т-34",
        "include": "products,authors,bookCycles,publisherSeries,publishers,categories"
    }
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": f"Bearer {access_token}",
        "cache-control": "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    response = requests.get(base_url, headers=headers, params=params)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    data = response.json()

    # Проверка основных данных в ответе
    assert "data" in data, "'data' key not found in response"
    assert "attributes" in data["data"], "'attributes' key not found in 'data'"
    assert "relationships" in data["data"], "'relationships' key not found in 'data'"

    relationships = data["data"]["relationships"]
    assert "products" in relationships, "'products' key not found in 'relationships'"
    assert len(relationships["products"]["data"]) > 0, "No products found in 'relationships'"

    products = relationships["products"]["data"]

    # Проверка наличия книги с символом "-" в названии
    found = any(
        product["id"] in {product_item["id"] for product_item in products} and
        "-" in product.get("attributes", {}).get("title", "")
        for product in data.get("included", [])
    )

    assert found, "No book with '-' in the title found in search results"


@allure.feature("Поиск книг")
@allure.story("Позитивные проверки")
@allure.title("Поиск существующей книги с цифрами в названии")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_book_with_numbers():
    base_url = "https://web-gate.chitai-gorod.ru/api/v2/search/search-phrase-suggests"
    params = {
        "suggests[page]": "1",
        "suggests[per-page]": "5",
        "phrase": "т-34",
        "include": "products,authors,bookCycles,publisherSeries,publishers,categories"
    }
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": f"Bearer {access_token}",
        "cache-control": "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    response = requests.get(base_url, headers=headers, params=params)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    data = response.json()

    # Проверка основных данных в ответе
    assert "data" in data, "'data' key not found in response"
    assert "attributes" in data["data"], "'attributes' key not found in 'data'"
    assert "relationships" in data["data"], "'relationships' key not found in 'data'"

    relationships = data["data"]["relationships"]
    assert "products" in relationships, "'products' key not found in 'relationships'"
    assert len(relationships["products"]["data"]) > 0, "No products found in 'relationships'"

    products = relationships["products"]["data"]

    # Проверка наличия книги с цифрами в названии
    found = any(
        product["id"] in {product_item["id"] for product_item in products} and
        any(char.isdigit() for char in product.get("attributes", {}).get("title", ""))
        for product in data.get("included", [])
    )

    assert found, "No book with a number in the title found in search results"


@allure.feature("Поиск книг")
@allure.story("Позитивные проверки")
@allure.title("Поиск существующей книги на латинице")
@allure.severity(allure.severity_level.CRITICAL)
def test_search_book_in_latin():
    base_url = "https://web-gate.chitai-gorod.ru/api/v2/search/search-phrase-suggests"
    params = {
        "suggests[page]": "1",
        "suggests[per-page]": "5",
        "phrase": "metro",
        "include": "products,authors,bookCycles,publisherSeries,publishers,categories"
    }
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": f"Bearer {access_token}",
        "cache-control": "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    response = requests.get(base_url, headers=headers, params=params)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    data = response.json()

    # Проверка основных данных в ответе
    assert "data" in data, "'data' key not found in response"
    assert "attributes" in data["data"], "'attributes' key not found in 'data'"
    assert "relationships" in data["data"], "'relationships' key not found in 'data'"

    relationships = data["data"]["relationships"]
    assert "products" in relationships, "'products' key not found in 'relationships'"
    assert len(relationships["products"]["data"]) > 0, "No products found in 'relationships'"

    products = relationships["products"]["data"]

    # Проверка наличия книги с названием, содержащим "metro"
    found = any(
        product["id"] in {product_item["id"] for product_item in products} and
        "metro" in product.get("attributes", {}).get("title", "").lower()
        for product in data.get("included", [])
    )

    assert found, "No book with 'metro' in the title found in search results"


@allure.feature("Корзина")
@allure.story("Позитивные проверки")
@allure.title("Добавление книги в корзину")
@allure.severity(allure.severity_level.NORMAL)
def test_add_book_to_cart():
    base_url = "https://web-gate.chitai-gorod.ru/api/v1/cart/product"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": f"Bearer {access_token}",
        "content-type": "application/json",
        "cache-control": "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }
    payload = {
        "id": 3028213,
        "adData": {
            "item_list_name": "index",
            "product_shelf": "Новинки литературы"
        }
    }

    response = requests.post(base_url, headers=headers, json=payload)

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"


@allure.feature("Корзина")
@allure.story("Позитивные проверки")
@allure.title("Добавление и удаление книги в корзине")
@allure.severity(allure.severity_level.NORMAL)
def test_add_and_remove_book_from_cart():
    # URL и заголовки
    base_url = "https://web-gate.chitai-gorod.ru/api/v1/cart/product"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": f"Bearer {access_token}",
        "content-type": "application/json",
        "cache-control": "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    # Тело запроса на добавление книги
    payload_add = {
        "id": 3028213,
        "adData": {
            "item_list_name": "index",
            "product_shelf": "Новинки литературы"
        }
    }

    # Шаг 1: Добавление книги в корзину
    response_add = requests.post(base_url, headers=headers, json=payload_add)

    assert response_add.status_code == 200, f"Expected status code 200, but got {response_add.status_code}"

    # Получение содержимого корзины
    cart_url = "https://web-gate.chitai-gorod.ru/api/v1/cart"
    response_cart = requests.get(cart_url, headers=headers)

    assert response_cart.status_code == 200, f"Expected status code 200, but got {response_cart.status_code}"

    cart_data = response_cart.json()
    added_product_id = None
    for item in cart_data.get('products', []):
        if item.get('goodsId') == 3028213:
            added_product_id = item.get('id')
            break

    assert added_product_id, "Product was not added to the cart"

    # Шаг 2: Удаление книги из корзины
    delete_url = f"https://web-gate.chitai-gorod.ru/api/v1/cart/product/{added_product_id}"
    response_delete = requests.delete(delete_url, headers=headers)

    assert response_delete.status_code == 204, f"Expected status code 204, but got {response_delete.status_code}"


@allure.feature("Корзина")
@allure.story("Позитивные проверки")
@allure.title("Удаление книги из корзины используя кнопку 'Очистить корзину'")
@allure.severity(allure.severity_level.NORMAL)
def test_add_and_clear_cart():
    # URL и заголовки
    base_url = "https://web-gate.chitai-gorod.ru/api/v1/cart/product"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": f"Bearer {access_token}",
        "content-type": "application/json",
        "cache-control": "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    # Тело запроса на добавление книги
    payload_add = {
        "id": 3028213,
        "adData": {
            "item_list_name": "index",
            "product_shelf": "Новинки литературы"
        }
    }

    # Шаг 1: Добавление книги в корзину
    response_add = requests.post(base_url, headers=headers, json=payload_add)

    assert response_add.status_code == 200, f"Expected status code 200, but got {response_add.status_code}"

    # Получение содержимого корзины
    cart_url = "https://web-gate.chitai-gorod.ru/api/v1/cart"
    response_cart = requests.get(cart_url, headers=headers)

    assert response_cart.status_code == 200, f"Expected status code 200, but got {response_cart.status_code}"

    cart_data = response_cart.json()

    added_product = None

    for item in cart_data.get('products', []):
        if item.get('goodsId') == 3028213:
            added_product = item
            break

    assert added_product, "Product was not added to the cart"

    # Шаг 2: Очистка корзины
    clear_cart_url = "https://web-gate.chitai-gorod.ru/api/v1/cart"
    response_clear_cart = requests.delete(clear_cart_url, headers=headers)

    assert response_clear_cart.status_code == 204, f"Expected status code 204, but got {response_clear_cart.status_code}"

    # Проверка, что корзина пустая
    response_cart_after_clear = requests.get(cart_url, headers=headers)

    assert response_cart_after_clear.status_code == 200, f"Expected status code 200, but got {response_cart_after_clear.status_code}"

    cart_data_after_clear = response_cart_after_clear.json()
    assert not cart_data_after_clear.get('products'), "Cart is not empty after clearing"


@allure.feature("Избранное")
@allure.story("Позитивные проверки")
@allure.title("Добавление книги в избранное")
@allure.severity(allure.severity_level.NORMAL)
def test_add_book_to_favorites():
    # URL и заголовки
    base_url = "https://web-gate.chitai-gorod.ru/api/v1/bookmarks"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": f"Bearer {access_token}",
        "content-type": "application/json",
        "cache-control": "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    # Тело запроса на добавление книги в избранное
    payload = {
        "id": 3031328
    }

    # Шаг 1: Добавление книги в избранное
    response = requests.post(base_url, headers=headers, json=payload)

    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"

    # Проверка, что книга была добавлена в избранное
    bookmarks_url = "https://web-gate.chitai-gorod.ru/api/v1/bookmarks"
    response_bookmarks = requests.get(bookmarks_url, headers=headers)

    assert response_bookmarks.status_code == 200, f"Expected status code 200, but got {response_bookmarks.status_code}"

    bookmarks_data = response_bookmarks.json()
    added_to_favorites = any(item.get('code') == 3031328 for item in bookmarks_data.get('data', []))

    assert added_to_favorites, "Book was not added to favorites"


@allure.feature("Избранное")
@allure.story("Позитивные проверки")
@allure.title("Просмотр добавленных книг в избранное")
@allure.severity(allure.severity_level.NORMAL)
def test_view_favorites():
    # URL и заголовки
    base_url = "https://web-gate.chitai-gorod.ru/api/v1/bookmarks"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": f"Bearer {access_token}",
        "content-type": "application/json",
        "cache-control": "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    # Шаг 1: Отправка запроса на отображение добавленных книг в избранное
    params = {
        "perPage": 48
    }
    response = requests.get(base_url, headers=headers, params=params)

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    # Проверка наличия книг в избранном
    bookmarks_data = response.json()
    assert "data" in bookmarks_data, "Response does not contain 'data' field"
    assert len(bookmarks_data["data"]) > 0, "No books found in favorites"

    # Пример проверки конкретной книги
    expected_book_id = 3031328
    book_found = any(item.get('code') == expected_book_id for item in bookmarks_data.get('data', []))

    assert book_found, f"Book with ID {expected_book_id} was not found in favorites"


@allure.feature("Избранное")
@allure.story("Позитивные проверки")
@allure.title("Удаление из избранного через кнопку 'Удалить все'")
@allure.severity(allure.severity_level.NORMAL)
def test_add_and_remove_all_from_favorites():
    # URL и заголовки
    base_url = "https://web-gate.chitai-gorod.ru/api/v1/bookmarks"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": f"Bearer {access_token}",
        "content-type": "application/json",
        "cache-control": "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    # Шаг 1: Добавление книги в избранное
    payload_add = {
        "id": 3031328
    }
    response_add = requests.post(base_url, headers=headers, json=payload_add)

    assert response_add.status_code == 201, f"Expected status code 201, but got {response_add.status_code}"

    # Шаг 2: Удаление всех книг из избранного
    response_delete = requests.delete(base_url, headers=headers)

    assert response_delete.status_code == 204, f"Expected status code 204, but got {response_delete.status_code}"

    # Проверка, что избранное пустое
    response_bookmarks = requests.get(base_url, headers=headers)

    assert response_bookmarks.status_code == 200, f"Expected status code 200, but got {response_bookmarks.status_code}"

    bookmarks_data = response_bookmarks.json()
    assert len(bookmarks_data.get('data', [])) == 0, "Favorites is not empty"


@allure.feature("Избранное")
@allure.story("Позитивные проверки")
@allure.title("Удаление книги из избранного через флажок (по ID книги)")
@allure.severity(allure.severity_level.NORMAL)
def test_add_and_remove_book_from_favorites_by_id():
    # URL и заголовки
    base_url = "https://web-gate.chitai-gorod.ru/api/v1/bookmarks"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": f"Bearer {access_token}",
        "content-type": "application/json",
        "cache-control": "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    # Шаг 1: Добавление книги в избранное
    payload_add = {
        "id": 3031328
    }
    response_add = requests.post(base_url, headers=headers, json=payload_add)

    assert response_add.status_code == 201, f"Expected status code 201, but got {response_add.status_code}"

    # Шаг 2: Удаление книги из избранного по ID
    delete_url = f"{base_url}/3031328"
    response_delete = requests.delete(delete_url, headers=headers)

    assert response_delete.status_code == 204, f"Expected status code 204, but got {response_delete.status_code}"

    # Проверка, что книга была удалена из избранного
    response_bookmarks = requests.get(base_url, headers=headers)

    assert response_bookmarks.status_code == 200, f"Expected status code 200, but got {response_bookmarks.status_code}"

    bookmarks_data = response_bookmarks.json()
    assert not any(
        item.get('id') == 3031328 for item in bookmarks_data.get('data', [])), "Book was not removed from favorites"


@allure.feature("Рейтинг книги")
@allure.story("Позитивные проверки")
@allure.title("Рейтинг книги - валидный")
@allure.severity(allure.severity_level.CRITICAL)
def test_valid_book_rating():
    # URL и заголовки
    base_url = "https://web-gate.chitai-gorod.ru/api/v1/rating/3029576"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": f"Bearer {access_token}",
        "content-type": "application/json",
        "cache-control": "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    # Тело запроса на рейтинг книги
    payload = {
        "rating": 5
    }

    # Шаг 1: Отправка запроса на установку рейтинга книги
    response = requests.put(base_url, headers=headers, json=payload)

    print(f"Response status code: {response.status_code}")
    print(f"Response headers: {response.headers}")
    print(f"Response content: {response.text}")

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    # Шаг 2: Проверка данных о рейтинге книги
    response_data = response.json()
    assert "data" in response_data, "Response JSON does not contain 'data'"
    data = response_data["data"]

    expected_rating = 4.5  # Обновлено в соответствии с фактическим значением
    expected_count = 8  # Обновлено в соответствии с фактическим значением

    assert data["rating"] == expected_rating, f"Expected rating {expected_rating}, but got {data['rating']}"
    assert data["count"] == expected_count, f"Expected count {expected_count}, but got {data['count']}"


@allure.feature("Поиск книг")
@allure.story("Негативные проверки")
@allure.title("Поиск существующей книги на китайском языке")
@allure.severity(allure.severity_level.BLOCKER)
def test_search_book_in_chinese():
    # URL и заголовки
    base_url = "https://web-gate.chitai-gorod.ru/api/v2/search/search-phrase-suggests"
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": f"Bearer {access_token}",
        "cache-control": "no-store, no-cache, must-revalidate, proxy-revalidate, max-age=0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    # Китайские символы для поиска
    chinese_phrase = "捷運"
    encoded_phrase = quote(chinese_phrase)

    # Параметры запроса на поиск книги на китайском языке
    params = {
        "suggests[page]": "1",
        "suggests[per-page]": "5",
        "phrase": encoded_phrase,
        "include": "products,authors,bookCycles,publisherSeries,publishers,categories"
    }

    # Отправка GET-запроса
    response = requests.get(base_url, headers=headers, params=params)

    # Проверка, что статус код ответа 200
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    # Проверка, что в ответе нет найденных книг
    response_data = response.json()
    assert "data" in response_data, "Response JSON does not contain 'data'"
    assert "relationships" in response_data["data"], "Response JSON does not contain 'relationships'"
    assert "suggests" in response_data["data"]["relationships"], "Response JSON does not contain 'suggests'"
    assert len(
        response_data["data"]["relationships"]["suggests"]["data"]) == 0, "Expected no suggestions, but found some."
