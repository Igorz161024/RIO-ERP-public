import httpx
from config import API_URL

def get_legal_docs():
    response = httpx.get(f"{API_URL}/api/legal")
    return response.json()
