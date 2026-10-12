import httpx
from frontend_rio.config import API_URL, API_TOKEN

BASE_URL = f"{API_URL}/api/sales/"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

def get_sales():
    """Отримати список усіх продажів"""
    response = httpx.get(BASE_URL, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return data.get("data", data)

def add_sales_entry(entry: dict):
    """Створити новий запис продажу"""
    response = httpx.post(BASE_URL, json=entry, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_sales_by_id(entry_id: int):
    """Отримати запис продажу за ID"""
    response = httpx.get(f"{BASE_URL}{entry_id}", headers=HEADERS)
    response.raise_for_status()
    return response.json()

def update_sales_entry(entry_id: int, updated_data: dict):
    """Оновити дані продажу"""
    response = httpx.put(f"{BASE_URL}{entry_id}", json=updated_data, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def delete_sales_entry(entry_id: int):
    """Видалити запис продажу"""
    response = httpx.delete(f"{BASE_URL}{entry_id}", headers=HEADERS)
    response.raise_for_status()
    return response.json()
