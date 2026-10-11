import httpx
from config import API_URL, API_TOKEN  # переконайся, що API_TOKEN є у config.py

BASE_URL = f"{API_URL}/api/purchases/"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

def get_purchases():
    """Отримати список усіх закупівель"""
    response = httpx.get(BASE_URL, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return data.get("data", data)

def add_purchase_entry(entry: dict):
    """Створити новий запис закупівлі"""
    response = httpx.post(BASE_URL, json=entry, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_purchase_by_id(entry_id: int):
    """Отримати запис закупівлі за ID"""
    response = httpx.get(f"{BASE_URL}{entry_id}", headers=HEADERS)
    response.raise_for_status()
    return response.json()

def update_purchase_entry(entry_id: int, updated_data: dict):
    """Оновити дані закупівлі"""
    response = httpx.put(f"{BASE_URL}{entry_id}", json=updated_data, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def delete_purchase_entry(entry_id: int):
    """Видалити запис закупівлі"""
    response = httpx.delete(f"{BASE_URL}{entry_id}", headers=HEADERS)
    response.raise_for_status()
    return response.json()
