from rio import PageView, Table
from services.sales import get_sales

def sales_page(page: PageView):
    data = get_sales()
    page.add(Table(data, columns=["id", "customer", "date", "status", "amount"]))
    return page