import httpx

url = "http://127.0.0.1:7000/token"
payload = {
    "username": "postgres",   # твій користувач
    "password": "admin123"    # твій пароль
}

response = httpx.post(url, data=payload)
print(response.json())
