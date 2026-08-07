from rio import PageView, Table
from services.journal import get_journal

def journal_page(page: PageView):
    data = get_journal()
    page.add(Table(data, columns=["id", "date", "operation", "status", "amount"]))
    return page