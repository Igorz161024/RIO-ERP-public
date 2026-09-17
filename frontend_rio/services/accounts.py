import requests

BASE_URL = "http://localhost:7000/api/accounts/"  # бекенд RIO-ERP завжди на порту 7000

def get_accounts():
    """Отримати список усіх рахунків"""
    response = requests.get(BASE_URL)
    response.raise_for_status()
    return response.json()

def create_account(name: str, balance: float = 0.0):
    """Створити новий рахунок"""
    payload = {"name": name, "balance": balance}
    response = requests.post(BASE_URL, json=payload)
    response.raise_for_status()
    return response.json()

def get_account_by_id(account_id: int):
    """Отримати рахунок за ID"""
    response = requests.get(f"{BASE_URL}{account_id}")
    response.raise_for_status()
    return response.json()

def update_account(account_id: int, name: str = None, balance: float = None):
    """Оновити дані рахунку"""
    payload = {}
    if name is not None:
        payload["name"] = name
    if balance is not None:
        payload["balance"] = balance
    response = requests.put(f"{BASE_URL}{account_id}", json=payload)
    response.raise_for_status()
    return response.json()

def delete_account(account_id: int):
    """Видалити рахунок"""
    response = requests.delete(f"{BASE_URL}{account_id}")
    response.raise_for_status()
    return {"status": "deleted", "id": account_id}
