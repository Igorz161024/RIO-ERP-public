import httpx
from config import API_URL, API_TOKEN  # переконайся, що API_TOKEN є у config.py

BASE_URL = f"{API_URL}/api/accounts/"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

def get_accounts():
    """Отримати список усіх рахунків"""
    response = httpx.get(BASE_URL, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return data.get("data", data)

def add_account_entry(entry: dict):
    """Створити новий рахунок"""
    response = httpx.post(BASE_URL, json=entry, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_account_by_id(account_id: int):
    """Отримати рахунок за ID"""
    response = httpx.get(f"{BASE_URL}{account_id}", headers=HEADERS)
    response.raise_for_status()
    return response.json()

def update_account_entry(account_id: int, updated_data: dict):
    """Оновити дані рахунку"""
    response = httpx.put(f"{BASE_URL}{account_id}", json=updated_data, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def delete_account_entry(account_id: int):
    """Видалити рахунок"""
    response = httpx.delete(f"{BASE_URL}{account_id}", headers=HEADERS)
    response.raise_for_status()
    return response.json()
