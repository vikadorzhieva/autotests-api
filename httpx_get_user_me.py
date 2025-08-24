import httpx  # Импортируем библиотеку HTTPX

# Инициализируем JSON-данные, которые будем отправлять в API
login_payload = {
    "email": "test@mailp.io",
    "password": "password"
}

# Выполняем запрос на аутентификацию
login_response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=login_payload)
login_response_data = login_response.json()

# Выводим полученные токены
print("Login response:", login_response_data)
print("Status Code:", login_response.status_code)

# Формируем headers
headers = {
    "Authorization": f"Bearer {login_response_data['token']['accessToken']}"
}

# Выполняем запрос на получение данных пользователя
user_me_response = httpx.get("http://localhost:8000/api/v1/users/me", headers=headers)
user_me_response_data = user_me_response.json()

# Выводим данные пользователя
print("User me response:", user_me_response_data)
print("Status Code:", user_me_response.status_code)