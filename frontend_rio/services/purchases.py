import httpx
from config import API_URL

def get_purchases():
    response = httpx.get(f"{API_URL}/api/purchases")
    return response.json()
