import httpx
from config import API_URL

BASE_URL = f"{API_URL}/api/entry_lines"

def get_entry_lines():
    """Отримати список усіх проводок"""
    response = httpx.get(BASE_URL)
    response.raise_for_status()
    data = response.json()
    if isinstance(data, dict) and "data" in data:
        return data["data"]
    return data

def create_entry_line(journal_id: int, account: str, debit: float = 0.0, credit: float = 0.0):
    """Створити нову проводку"""
    payload = {
        "journal_id": journal_id,
        "account": account,
        "debit": debit,
        "credit": credit
    }
    response = httpx.post(BASE_URL, json=payload)
    response.raise_for_status()
    return response.json()

def get_entry_line_by_id(entry_id: int):
    """Отримати проводку за ID"""
    response = httpx.get(f"{BASE_URL}/{entry_id}")
    response.raise_for_status()
    return response.json()

def update_entry_line(entry_id: int, account: str = None, debit: float = None, credit: float = None):
    """Оновити дані проводки"""
    payload = {}
    if account is not None:
        payload["account"] = account
    if debit is not None:
        payload["debit"] = debit
    if credit is not None:
        payload["credit"] = credit
    response = httpx.put(f"{BASE_URL}/{entry_id}", json=payload)
    response.raise_for_status()
    return response.json()

def delete_entry_line(entry_id: int):
    """Видалити проводку"""
    response = httpx.delete(f"{BASE_URL}/{entry_id}")
    response.raise_for_status()
    return {"status": "deleted", "id": entry_id}
