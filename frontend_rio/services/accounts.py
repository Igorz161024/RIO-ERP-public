import httpx
from config import API_URL, API_TOKEN  # додай API_TOKEN у config.py

BASE_URL = f"{API_URL}/api/accounts/"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

def get_accounts():
    """Отримати список усіх рахунків"""
    response = httpx.get(BASE_URL, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return data.get("data", data)

def create_account(name: str, balance: float = 0.0):
    """Створити новий рахунок"""
    payload = {"name": name, "balance": balance}
    response = httpx.post(BASE_URL, json=payload, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_account_by_id(account_id: int):
    """Отримати рахунок за ID"""
    response = httpx.get(f"{BASE_URL}{account_id}", headers=HEADERS)
    response.raise_for_status()
    return response.json()

def update_account(account_id: int, name: str = None, balance: float = None):
    """Оновити дані рахунку"""
    payload = {}
    if name is not None:
        payload["name"] = name
    if balance is not None:
        payload["balance"] = balance
    response = httpx.put(f"{BASE_URL}{account_id}", json=payload, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def delete_account(account_id: int):
    """Видалити рахунок"""
    response = httpx.delete(f"{BASE_URL}{account_id}", headers=HEADERS)
    response.raise_for_status()
    return response.json()
