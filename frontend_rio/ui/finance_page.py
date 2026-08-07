from rio import PageView, Table
from services.finance import get_finance_report

def finance_page(page: PageView):
    data = get_finance_report()
    page.add(Table(data, columns=["id", "name", "balance"]))
    return page