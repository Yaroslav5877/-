import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote


@pytest.fixture(scope="module")
def browser():
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.maximize_window()
    yield driver
    driver.quit()


@allure.feature("Регистрация")
@allure.story("Регистрация на сайте")
@allure.title("Регистрация нового пользователя")
def test_registration(browser):
    browser.get("https://www.chitai-gorod.ru/")

    # Step 1: Нажать на кнопку "Войти"
    login_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".header-profile__icon--desktop"))
    )
    login_button.click()

    # Step 2: Ввести корректный номер в поле "Номер телефона"
    phone_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input.phone-input__input"))
    )
    phone_input.send_keys("9856932244")

    # Step 3: Нажать кнопку "получить код"
    get_code_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.auth-modal__sms-button.blue span.app-button-text"))
    )
    get_code_button.click()

    # Step 4: Ввести код из SMS
    code_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='12345']"))
    )
    code_input.send_keys("12345")

    # Step 5: Заполнить корректно поля "Имя", "Фамилия", "Электронная почта"
    name_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='firstName']"))
    )
    name_input.send_keys("Иван")

    surname_input = browser.find_element(By.CSS_SELECTOR, "input[name='lastName']")
    surname_input.send_keys("Иванов")

    email_input = browser.find_element(By.CSS_SELECTOR, "input[name='email']")
    email_input.send_keys("ivanov@example.com")

    # Step 6: Установить чек-бокс "Я подтверждаю достижение 18 лет"
    confirm_checkbox = browser.find_element(By.CSS_SELECTOR, "input[name='isPolicyAgreed']")
    confirm_checkbox.click()

    # Step 7: Установить чек-бокс "Хочу быть в курсе скидок и новинок" (если он отмечен, снять его)
    subscribe_checkbox = browser.find_element(By.CSS_SELECTOR, "input[name='isSubscribed']")
    if subscribe_checkbox.is_selected():
        subscribe_checkbox.click()

    # Step 8: Нажать кнопку "Зарегистрироваться"
    register_button = browser.find_element(By.CSS_SELECTOR, "button.registration__button.blue span.app-button-text")
    register_button.click()

    # Проверка, что открылось окно с подтверждением регистрации
    confirmation_message = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.confirmation-message"))
    )
    assert "Перейти к покупкам" in confirmation_message.text


@allure.feature("Авторизация")
@allure.story("Авторизация на сайте")
@allure.title("Авторизация существующего пользователя")
def test_login(browser):
    browser.get("https://www.chitai-gorod.ru/")

    # Step 1: Нажать на кнопку "Войти"
    login_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".header-profile__icon--desktop"))
    )
    login_button.click()

    # Step 2: Ввести корректный номер в поле "Номер телефона"
    phone_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input.phone-input__input"))
    )
    phone_input.send_keys("9856932244")

    # Step 3: Нажать кнопку "получить код"
    get_code_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.auth-modal__sms-button.blue span.app-button-text"))
    )
    get_code_button.click()

    # Step 4: Ввести код из SMS
    code_input = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='']"))
    )
    sms_code = input('Введите код из sms: ')
    code_input.send_keys(sms_code)

    # Проверка, что кнопка "Войти" изменилась на кнопку с именем
    user_name_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.user-name-button"))
    )

    assert "Вячеслав" in user_name_button.text


@allure.feature("Поиск")
@allure.story("Поиск книги")
@allure.title("Поиск книги по названию")
def test_search_book(browser):
    browser.get("https://www.chitai-gorod.ru/")

    # Step 1: Активировать поле "Поиск" нажав на него
    search_box = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.click()

    # Step 2: Ввести название искомой книги поле "Я ищу..."
    search_box.send_keys("Призраки")

    # Step 3: Нажать кнопку "поиск"
    search_box.send_keys(Keys.RETURN)

    # Проверка, что открылось окно с результатами поиска по названию
    search_results = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".search-results"))
    )
    assert "Призраки" in search_results.text


@allure.feature("Корзина")
@allure.story("Открытие пустой корзины")
@allure.title("Проверка пустой корзины")
def test_empty_cart(browser):
    browser.get("https://www.chitai-gorod.ru/")

    # Step 1: Нажать кнопку "Корзина"
    cart_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.cart-button"))
    )
    cart_button.click()

    # Проверка, что откроется окно "Корзины" с уведомлением, что "в корзине ничего нет"
    cart_message = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.cart-empty-message"))
    )
    assert "в корзине ничего нет" in cart_message.text


@allure.feature("Корзина")
@allure.story("Открытие корзины с продуктами")
@allure.title("Добавление книг в корзину и проверка корзины")
def test_cart_with_products(browser):
    browser.get("https://www.chitai-gorod.ru/")

    # Step 1: Добавить книги в корзину на главной странице, нажав кнопку "Купить"
    buy_buttons = WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.buy-button"))
    )
    for button in buy_buttons[:3]:
        button.click()

    # Step 2: Нажать кнопку "Корзина"
    cart_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button.cart-button"))
    )
    cart_button.click()

    # Проверка, что открылась корзина с добавленными книгами
    cart_items = WebDriverWait(browser, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cart-item"))
    )
    assert len(cart_items) == 3


if __name__ == "__main__":
    pytest.main(["-s", "functional_test.py::test_login"])
