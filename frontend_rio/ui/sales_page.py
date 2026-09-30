# frontend_rio/ui/sales_page.py
from rio import PageView, Table, AutoForm, TextInput, NumberInput
from services.sales import get_sales, add_sales_entry
import datetime

ALLOWED_STATUSES = ["pending", "completed", "canceled"]

def validate_sale_entry(date, customer, amount, status):
    if not date.strip():
        return False, "Дата не може бути порожньою"
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return False, "Невірний формат дати (YYYY-MM-DD)"

    if not customer.strip():
        return False, "Клієнт не може бути порожнім"

    if not isinstance(amount, (int, float)) or amount <= 0:
        return False, "Сума має бути числом > 0"

    if status not in ALLOWED_STATUSES:
        return False, f"Недопустимий статус. Дозволені: {', '.join(ALLOWED_STATUSES)}"

    return True, "OK"

def sales_page(page: PageView):
    data = get_sales()
    page.add(Table(data, columns=["id", "date", "customer", "amount", "status"]))

    form = AutoForm()
    form.add(TextInput(label="Дата (YYYY-MM-DD)", name="date"))
    form.add(TextInput(label="Клієнт", name="customer"))
    form.add(NumberInput(label="Сума", name="amount"))
    form.add(TextInput(label="Статус", name="status"))

    def on_submit(values):
        ok, msg = validate_sale_entry(values["date"], values["customer"], values["amount"], values["status"])
        if not ok:
            page.alert(msg)
        else:
            add_sales_entry(values)
            page.toast("Продаж успішно додано")

    form.on_submit(on_submit)
    page.add(form)

    return page
