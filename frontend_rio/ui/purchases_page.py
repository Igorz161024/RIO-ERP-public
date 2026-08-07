from rio import PageView, Table
from services.purchases import get_purchases

def purchases_page(page: PageView):
    data = get_purchases()
    page.add(Table(data, columns=["id", "supplier", "date", "status", "total"]))
    return page