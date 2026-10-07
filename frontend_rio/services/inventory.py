import httpx
from config import API_URL, API_TOKEN  # додай API_TOKEN у config.py

BASE_URL = f"{API_URL}/api/inventory/"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

def get_inventory():
    """Отримати список усіх товарів на складі"""
    response = httpx.get(BASE_URL, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return data.get("data", data)

def add_inventory_entry(entry: dict):
    """Додати новий товар у склад"""
    response = httpx.post(BASE_URL, json=entry, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_inventory_by_id(entry_id: int):
    """Отримати товар за ID"""
    response = httpx.get(f"{BASE_URL}{entry_id}", headers=HEADERS)
    response.raise_for_status()
    return response.json()

def update_inventory_entry(entry_id: int, updated_data: dict):
    """Оновити дані товару"""
    response = httpx.put(f"{BASE_URL}{entry_id}", json=updated_data, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def delete_inventory_entry(entry_id: int):
    """Видалити товар зі складу"""
    response = httpx.delete(f"{BASE_URL}{entry_id}", headers=HEADERS)
    response.raise_for_status()
    return response.json()
