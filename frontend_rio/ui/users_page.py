from rio import PageView, Table
from services.users import get_users

def users_page(page: PageView):
    data = get_users()
    page.add(Table(data, columns=["id", "username", "role", "email"]))
    return page