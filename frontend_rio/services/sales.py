import httpx
from config import API_URL

def get_sales():
    response = httpx.get(f"{API_URL}/api/sales")
    return response.json()
