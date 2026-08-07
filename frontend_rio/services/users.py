import httpx
from config import API_URL

def get_users():
    response = httpx.get(f"{API_URL}/api/users")
    return response.json()
