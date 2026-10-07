import httpx
from config import API_URL, API_TOKEN  # додай API_TOKEN у config.py

BASE_URL = f"{API_URL}/api/finance/"

HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

def get_finance():
    """Отримати список усіх фінансових записів"""
    response = httpx.get(BASE_URL, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return data.get("data", data)

def add_finance_entry(entry: dict):
    """Створити новий фінансовий запис"""
    response = httpx.post(BASE_URL, json=entry, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_finance_by_id(entry_id: int):
    """Отримати фінансовий запис за ID"""
    response = httpx.get(f"{BASE_URL}{entry_id}", headers=HEADERS)
    response.raise_for_status()
    return response.json()

def update_finance_entry(entry_id: int, updated_data: dict):
    """Оновити дані фінансового запису"""
    response = httpx.put(f"{BASE_URL}{entry_id}", json=updated_data, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def delete_finance_entry(entry_id: int):
    """Видалити фінансовий запис"""
    response = httpx.delete(f"{BASE_URL}{entry_id}", headers=HEADERS)
    response.raise_for_status()
    return response.json()
