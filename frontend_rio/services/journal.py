import httpx
from config import API_URL

def get_journal():
    response = httpx.get(f"{API_URL}/api/journal")
    return response.json()
