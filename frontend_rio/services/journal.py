import httpx
from config import API_URL, API_TOKEN  # переконайся, що API_TOKEN є у config.py

BASE_URL = f"{API_URL}/api/journal/"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

def get_journal():
    """Отримати список усіх записів журналу"""
    response = httpx.get(BASE_URL, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return data.get("data", data)

def add_journal_entry(entry: dict):
    """Створити новий запис у журналі"""
    response = httpx.post(BASE_URL, json=entry, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_journal_by_id(entry_id: int):
    """Отримати запис журналу за ID"""
    response = httpx.get(f"{BASE_URL}{entry_id}", headers=HEADERS)
    response.raise_for_status()
    return response.json()

def update_journal_entry(entry_id: int, updated_data: dict):
    """Оновити дані запису журналу"""
    response = httpx.put(f"{BASE_URL}{entry_id}", json=updated_data, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def delete_journal_entry(entry_id: int):
    """Видалити запис журналу"""
    response = httpx.delete(f"{BASE_URL}{entry_id}", headers=HEADERS)
    response.raise_for_status()
    return response.json()
