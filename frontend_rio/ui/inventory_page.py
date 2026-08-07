from rio import PageView, Table
from services.inventory import get_inventory

def inventory_page(page: PageView):
    data = get_inventory()
    page.add(Table(data, columns=["id", "item", "quantity", "location"]))
    return page