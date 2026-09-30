import httpx
from config import API_URL

def get_sales():
    response = httpx.get(f"{API_URL}/api/sales")
    response.raise_for_status()
    data = response.json()
    return data["data"] if isinstance(data, dict) and "data" in data else data

def add_sales_entry(entry: dict):
    response = httpx.post(f"{API_URL}/api/sales", json=entry)
    response.raise_for_status()
    return response.json()
