import httpx
from config import API_URL

def get_journal():
    response = httpx.get(f"{API_URL}/api/journal")
    response.raise_for_status()  # якщо помилка — одразу виняток
    data = response.json()
    # якщо API повертає {"data": [...]} → витягуємо список
    if isinstance(data, dict) and "data" in data:
        return data["data"]
    return data
