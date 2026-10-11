import httpx
from config import API_URL, API_TOKEN  # переконайся, що API_TOKEN є у config.py

BASE_URL = f"{API_URL}/api/entry_lines/"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

def get_entry_lines():
    """Отримати список усіх проводок"""
    response = httpx.get(BASE_URL, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return data.get("data", data)

def add_entry_line(entry: dict):
    """Створити нову проводку"""
    response = httpx.post(BASE_URL, json=entry, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_entry_line_by_id(entry_id: int):
    """Отримати проводку за ID"""
    response = httpx.get(f"{BASE_URL}{entry_id}", headers=HEADERS)
    response.raise_for_status()
    return response.json()

def update_entry_line(entry_id: int, updated_data: dict):
    """Оновити дані проводки"""
    response = httpx.put(f"{BASE_URL}{entry_id}", json=updated_data, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def delete_entry_line(entry_id: int):
    """Видалити проводку"""
    response = httpx.delete(f"{BASE_URL}{entry_id}", headers=HEADERS)
    response.raise_for_status()
    return response.json()
