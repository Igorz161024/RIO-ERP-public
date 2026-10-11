import httpx
from config import API_URL, API_TOKEN  # переконайся, що API_TOKEN є у config.py

BASE_URL = f"{API_URL}/api/legal/"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

def get_legal():
    """Отримати список усіх юридичних записів"""
    response = httpx.get(BASE_URL, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return data.get("data", data)

def add_legal_entry(entry: dict):
    """Створити новий юридичний запис"""
    response = httpx.post(BASE_URL, json=entry, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_legal_by_id(entry_id: int):
    """Отримати юридичний запис за ID"""
    response = httpx.get(f"{BASE_URL}{entry_id}", headers=HEADERS)
    response.raise_for_status()
    return response.json()

def update_legal_entry(entry_id: int, updated_data: dict):
    """Оновити дані юридичного запису"""
    response = httpx.put(f"{BASE_URL}{entry_id}", json=updated_data, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def delete_legal_entry(entry_id: int):
    """Видалити юридичний запис"""
    response = httpx.delete(f"{BASE_URL}{entry_id}", headers=HEADERS)
    response.raise_for_status()
    return response.json()
