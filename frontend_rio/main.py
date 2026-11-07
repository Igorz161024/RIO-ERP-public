import rio

from ui.journal_page import JournalPage
from ui.accounts_page import AccountsPage
from ui.finance_page import FinancePage
from ui.inventory_page import InventoryPage
from ui.purchases_page import PurchasesPage
from ui.sales_page import SalesPage
from ui.legal_page import LegalPage
from ui.users_page import UsersPage

app = rio.App(
    pages=[
        rio.ComponentPage(
            "Journal",
            "",
            JournalPage,
        ),
        rio.ComponentPage(
            "Accounts",
            "accounts",
            AccountsPage,
        ),
        rio.ComponentPage(
            "Finance",
            "finance",
            FinancePage,
        ),
        rio.ComponentPage(
            "Inventory",
            "inventory",
            InventoryPage,
        ),
        rio.ComponentPage(
            "Purchases",
            "purchases",
            PurchasesPage,
        ),
        rio.ComponentPage(
            "Sales",
            "sales",
            SalesPage,
        ),
        rio.ComponentPage(
            "Legal",
            "legal",
            LegalPage,
        ),
        rio.ComponentPage(
            "Users",
            "users",
            UsersPage,
        ),
    ],
)