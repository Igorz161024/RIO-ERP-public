from rio import App, PageView, Button

from ui.journal_page import journal_page
from ui.finance_page import finance_page
from ui.inventory_page import inventory_page
from ui.sales_page import sales_page
from ui.purchases_page import purchases_page
from ui.legal_page import legal_page
from ui.users_page import users_page
from ui.accounts_page import accounts_page


app = App()


def main_menu() -> PageView:
    page = PageView(
        title="RIO ERP",
        size=(1200, 800)
    )

    page.add(Button("Journal", on_click=lambda: journal_page(page)))
    page.add(Button("Accounts", on_click=lambda: accounts_page(page)))
    page.add(Button("Finance", on_click=lambda: finance_page(page)))
    page.add(Button("Inventory", on_click=lambda: inventory_page(page)))
    page.add(Button("Sales", on_click=lambda: sales_page(page)))
    page.add(Button("Purchases", on_click=lambda: purchases_page(page)))
    page.add(Button("Legal", on_click=lambda: legal_page(page)))
    page.add(Button("Users", on_click=lambda: users_page(page)))

    journal_page(page)

    return page


app.pages.append(main_menu)
app.pages.append(journal_page)
app.pages.append(accounts_page)
app.pages.append(finance_page)
app.pages.append(inventory_page)
app.pages.append(sales_page)
app.pages.append(purchases_page)
app.pages.append(legal_page)
app.pages.append(users_page)