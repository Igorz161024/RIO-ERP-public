import httpx
from config import API_URL

def get_legal():
    response = httpx.get(f"{API_URL}/api/legal")
    response.raise_for_status()
    data = response.json()
    return data["data"] if isinstance(data, dict) and "data" in data else data

def add_legal_entry(entry: dict):
    response = httpx.post(f"{API_URL}/api/legal", json=entry)
    response.raise_for_status()
    return response.json()
