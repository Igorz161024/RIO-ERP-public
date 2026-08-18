import httpx
from fastapi import FastAPI
from rio import App, PageView, Button
from ui.journal_page import journal_page
from ui.finance_page import finance_page
from ui.inventory_page import inventory_page
from ui.sales_page import sales_page
from ui.purchases_page import purchases_page
from ui.legal_page import legal_page
from ui.users_page import users_page
import uvicorn

# RIO‑UI додаток
app_rio = App()

def main_menu() -> PageView:
    page = PageView(title="RIO ERP", size=(1200, 800))

    # Кнопки навігації
    page.add(Button("Journal", on_click=lambda: journal_page(page)))
    page.add(Button("Finance", on_click=lambda: finance_page(page)))
    page.add(Button("Inventory", on_click=lambda: inventory_page(page)))
    page.add(Button("Sales", on_click=lambda: sales_page(page)))
    page.add(Button("Purchases", on_click=lambda: purchases_page(page)))
    page.add(Button("Legal", on_click=lambda: legal_page(page)))
    page.add(Button("Users", on_click=lambda: users_page(page)))

    # Сторінка за замовчуванням
    journal_page(page)

    # Гарячі клавіші
    page.hotkey("Ctrl+N", lambda: page.notify("Новий документ"))
    page.hotkey("Ctrl+S", lambda: page.notify("Документ збережено"))

    return page

# Реєстрація меню та сторінок
app_rio.pages.append(main_menu)
app_rio.pages.append(journal_page)
app_rio.pages.append(finance_page)
app_rio.pages.append(inventory_page)
app_rio.pages.append(sales_page)
app_rio.pages.append(purchases_page)
app_rio.pages.append(legal_page)
app_rio.pages.append(users_page)

# FastAPI сервер
frontend = FastAPI()

@frontend.get("/")
def root():
    return {"message": "RIO Frontend server is running"}

@frontend.get("/finance")
async def finance():
    async with httpx.AsyncClient() as client:
        r = await client.get("http://rio_backend1:8000/api/finance/")
        return r.json()

@frontend.get("/sales")
async def sales():
    async with httpx.AsyncClient() as client:
        r = await client.get("http://rio_backend2:8000/api/sales/")
        return r.json()

if __name__ == "__main__":
    uvicorn.run(frontend, host="0.0.0.0", port=80)
