import requests

def request_code(phone_number):
    url = "https://web-gate.chitai-gorod.ru/api/v2/auth/request"
    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json"
    }
    data = {
        "phone": phone_number
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    print("SMS code requested")
    return response.json()

def confirm_code(phone_number, code):
    url = "https://web-gate.chitai-gorod.ru/api/v2/auth/confirm"
    headers = {
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json"
    }
    data = {
        "phone": phone_number,
        "code": code
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    token = response.json().get("access_token")
    print(f"Access Token: {token}")
    return token

def authenticate(phone_number):
    request_code(phone_number)
    code = input("Enter the code you received via SMS: ")
    return confirm_code(phone_number, code)

# Пример использования
phone_number = "79995313162"
token = authenticate(phone_number)