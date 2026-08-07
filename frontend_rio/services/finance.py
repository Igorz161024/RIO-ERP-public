import httpx
from config import API_URL

def get_finance_report():
    response = httpx.get(f"{API_URL}/api/finance")
    return response.json()
