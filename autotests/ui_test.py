import time

import pytest
import allure
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="module")
def browser():
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    driver.maximize_window()
    yield driver
    driver.quit()


@allure.feature("Проверка элементов UI")
@allure.story("Проверка отображения кнопки корзины и сообщения о пустой корзине")
@allure.title("Проверка корзины")
def test_cart_empty_message(browser):
    # Переход на главную страницу сайта
    browser.get("https://www.chitai-gorod.ru/")

    # Поиск и нажатие на кнопку "Корзина"
    cart_button = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.header-cart"))
    )
    cart_button.click()

    # Поиск текста "В корзине ничего нет"
    empty_cart_message = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.empty-title"))
    )

    # Проверка, что текст "В корзине ничего нет" отображается
    assert "В корзине ничего нет" in empty_cart_message.text


@allure.feature("Проверка страницы 'Обратная связь'")
@allure.story("Проверка отображения страницы 'Обратная связь'")
@allure.title("Проверка элементов на странице 'Обратная связь'")
def test_feedback_page(browser):
    # Шаг 1: Перейти на главную страницу
    browser.get("https://www.chitai-gorod.ru/")

    # Шаг 2: Найти элемент "Обратная связь" среди всех элементов с классом "header-top-bar__last-item"
    feedback_button = WebDriverWait(browser, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[contains(@class, 'header-top-bar__last-item') and contains(text(), 'Обратная связь')]"))
    )
    feedback_button.click()

    # Шаг 3: Переключиться на новую вкладку
    browser.switch_to.window(browser.window_handles[-1])

    # Шаг 4: Проверить наличие элемента с классом "feedback-page"
    feedback_page = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".feedback-page"))
    )
    assert feedback_page.is_displayed(), "Элемент 'feedback-page' не отображается"

    # Шаг 5: Проверить, что заголовок страницы содержит текст "Обратная связь"
    title_element = feedback_page.find_element(By.CSS_SELECTOR, ".feedback-page__title")
    assert title_element.text == "ОБРАТНАЯ СВЯЗЬ", "Заголовок страницы не соответствует ожидаемому"

    # Шаг 6: Проверить, что на странице отображается форма обратной связи
    form_element = feedback_page.find_element(By.CSS_SELECTOR, "form.uw__callback-form")
    assert form_element.is_displayed(), "Форма обратной связи не отображается"

    # Шаг 7: Проверить, что кнопка "Отправить" на форме обратной связи существует
    submit_button = form_element.find_element(By.CSS_SELECTOR, "button[type='submit']")
    assert submit_button.is_displayed(), "Кнопка 'Отправить' на форме обратной связи не отображается"


@allure.feature("Авторизация")
@allure.story("Открытие модального окна авторизации")
@allure.title("Проверка отображения модального окна 'Вход и регистрация'")
def test_login_modal(browser):
    browser.get("https://www.chitai-gorod.ru/")

    # Step 1: Найти и нажать на кнопку "Войти" (header-profile__button)
    login_button = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".header-profile__button"))
    )
    login_button.click()

    # Step 2: Проверить, что открылось модальное окно с текстом "Вход и регистрация"
    modal_header = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".auth-modal__header"))
    )
    assert "Вход и регистрация" in modal_header.text, "Текст модального окна не соответствует ожидаемому"

    # Step 3: Проверить, что кнопка "Получить код" присутствует и имеет нужный текст
    get_code_button = WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".auth-modal__sms-button span.app-button-text"))
    )
    assert "получить код" in get_code_button.text.lower(), "Текст кнопки 'Получить код' не соответствует ожидаемому"


@allure.feature("Футер страницы")
@allure.story("Переход на страницу 'О компании'")
@allure.title("Проверка текста на странице 'О компании'")
def test_about_page(browser):
    browser.get("https://www.chitai-gorod.ru/")

    # Step 1: Прокрутить страницу вниз до появления элемента "Хотите у нас работать?"
    while True:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            # Ожидание появления элемента "Хотите у нас работать?"
            WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Хотите у нас работать?"))
            )
            break
        except TimeoutException:
            continue

    # Добавляем ожидание для стабилизации страницы
    time.sleep(2)

    # Проверяем наличие баннера и закрываем его, если он есть
    try:
        close_button = WebDriverWait(browser, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".popmechanic-close"))
        )
        close_button.click()
    except TimeoutException:
        pass  # Если баннера нет, продолжаем без закрытия

    # Убедиться, что футер загрузился
    footer_section = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".app-footer__container"))
    )

    # Step 2: Найти центральный столбец (class="app-footer__column app-footer__column--center")
    center_column = footer_section.find_element(By.CSS_SELECTOR, ".app-footer__column--center")

    # Step 3: Найти ссылку "О компании" (class="app-footer__link") и убедиться, что это правильная ссылка
    about_link = None
    links = center_column.find_elements(By.CSS_SELECTOR, ".app-footer__link")

    for link in links:
        if link.text.strip() == "О компании":
            about_link = link
            break

    assert about_link is not None, "Ссылка 'О компании' не найдена в футере"

    # Прокрутка к ссылке
    browser.execute_script("arguments[0].scrollIntoView(true);", about_link)

    # Еще одно ожидание для стабильности
    time.sleep(1)

    # Нажатие на ссылку
    about_link.click()

    # Step 4: Проверить, что произошло перенаправление на страницу 'О компании'
    WebDriverWait(browser, 10).until(
        EC.url_to_be("https://www.chitai-gorod.ru/about")
    )

    assert "about" in browser.current_url, "Не удалось перейти на страницу 'О компании'"

    # Step 5: Проверить текст в разделе "О компании" (class="about-page__content")
    about_content = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".about-page__content"))
    )

    expected_text = (
        '«Читай-город» – это самая большая в России сеть книжных магазинов и интернет-магазин. Компания входит в '
        'объединённую розничную сеть «Читай-город» – «Гоголь-Моголь» – «Буквоед».\n\n'
        'Мы не просто продаём книги, а разделяем любовь наших покупателей к чтению. Нам знакомо чувство, когда хорошие '
        'романы заканчиваются слишком быстро, времени в дороге не хватает, чтобы дочитать главу, а героиня никак не может '
        'найти свою любовь. Мы знаем, как быстро летит время в компании с новинкой любимого автора и как сильно хочется '
        'растянуть это удовольствие.\n\n'
        'Помимо книг в «Читай-город» можно найти канцтовары, сладости, подарочную упаковку и идеи для сюрпризов близким. '
        'Мы сами разрабатываем дизайны для многих ежедневников, закладок, товаров для творчества и других интересных '
        'вещей, поэтому кроме как в «Читай-город» их больше нигде не найти.'
    )

    assert expected_text in about_content.text, "Текст на странице 'О компании' не соответствует ожиданиям"


@allure.feature("Верхняя панель страницы")
@allure.story("Проверка визуального соответствия элементов верхней панели")
@allure.title("Проверка текста, кнопок и полей ввода в верхней части страницы")
def test_top_bar_visual(browser):
    browser.get("https://www.chitai-gorod.ru/")

    # Step 1: Проверяем наличие логотипа
    logo = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".header-logo__icon"))
    )
    assert logo.is_displayed(), "Логотип не отображается"

    # Step 2: Проверяем наличие текстов меню
    menu_items = ["Акции", "Распродажа", "Комиксы и манга", "Читай-школа", "Что ещё почитать?", "Читай-журнал",
                  "Подарочные сертификаты"]

    for item in menu_items:
        menu_element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, item))
        )
        assert menu_element.is_displayed(), f"Текст меню '{item}' не отображается"

    # Step 3: Проверяем наличие кнопок и других элементов
    buttons = [
        (By.CSS_SELECTOR, ".catalog__button"),  # Кнопка "Каталог"
        (By.CSS_SELECTOR, ".header-profile__icon.header-profile__icon--desktop"),  # Иконка профиля
        (By.CSS_SELECTOR, ".header-cart__icon.header-cart__icon--desktop"),  # Иконка корзины
        (By.CSS_SELECTOR, ".header-search__input"),  # Поле для поиска
    ]

    for selector in buttons:
        try:
            # Проверяем, что элемент видим и доступен для взаимодействия
            element = WebDriverWait(browser, 20).until(
                EC.visibility_of_element_located(selector)
            )
            assert element.is_displayed(), f"Элемент {selector} не отображается"

            # Проверка, что элемент доступен для клика, но без фактического клика
            WebDriverWait(browser, 20).until(
                EC.element_to_be_clickable(selector)
            )

        except TimeoutException:
            assert False, f"Элемент {selector} не доступен для взаимодействия"

    # Step 4: Проверяем текст телефона и ссылки на вакансии и обратную связь
    phone_number = browser.find_element(By.LINK_TEXT, "8 (495) 424-84-44")
    assert phone_number.is_displayed(), "Номер телефона не отображается"

    vacancies = browser.find_element(By.LINK_TEXT, "Вакансии")
    assert vacancies.is_displayed(), "Ссылка 'Вакансии' не отображается"

    feedback = browser.find_element(By.LINK_TEXT, "Обратная связь")
    assert feedback.is_displayed(), "Ссылка 'Обратная связь' не отображается"
