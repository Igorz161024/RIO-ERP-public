# sales.py
import httpx
from config import API_URL, API_TOKEN

BASE_URL = f"{API_URL}/api/sales/"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

def get_sales():
    response = httpx.get(BASE_URL, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def add_sales_entry(entry: dict):
    response = httpx.post(BASE_URL, json=entry, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_sales_by_id(entry_id: int):
    response = httpx.get(f"{BASE_URL}{entry_id}", headers=HEADERS)
    response.raise_for_status()
    return response.json()

def update_sales_entry(entry_id: int, updated_data: dict):
    response = httpx.put(f"{BASE_URL}{entry_id}", json=updated_data, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def delete_sales_entry(entry_id: int):
    response = httpx.delete(f"{BASE_URL}{entry_id}", headers=HEADERS)
    response.raise_for_status()
    return response.json()
