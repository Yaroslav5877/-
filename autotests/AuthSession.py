import requests
import time


class AuthSession:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.token_expiration_time = 0

    def authenticate(self):
        login_url = "https://www.chitai-gorod.ru/api/login"  # замените на правильный URL для авторизации
        payload = {
            "username": "your_username",  # замените на ваше имя пользователя
            "password": "your_password"  # замените на ваш пароль
        }
        headers = {
            "Content-Type": "application/json"
        }

        response = self.session.post(login_url, json=payload, headers=headers)
        response.raise_for_status()  # выбросить исключение, если запрос не был успешным

        self.token = response.json().get("access_token")  # замените на правильное имя поля, если оно отличается
        self.token_expiration_time = time.time() + 300  # токен действителен 5 минут

        self.session.headers.update({"Authorization": f"Bearer {self.token}"})

    def get_session(self):
        if not self.token or time.time() > self.token_expiration_time:
            self.authenticate()
        return self.session


auth_session = AuthSession()
