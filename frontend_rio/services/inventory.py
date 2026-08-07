import httpx
from config import API_URL

def get_inventory():
    response = httpx.get(f"{API_URL}/api/inventory")
    return response.json()
