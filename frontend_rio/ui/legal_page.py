from rio import PageView, Table
from services.legal import get_legal_docs

def legal_page(page: PageView):
    data = get_legal_docs()
    page.add(Table(data, columns=["id", "doc_type", "date", "status"]))
    return page