from rio import PageView, Table, AutoForm, TextInput, NumberInput
from services.sales import get_sales, add_sales_entry
import datetime

# 🔹 Допустимі статуси продажу
ALLOWED_STATUSES = ["pending", "completed", "canceled"]

# 🔹 Допоміжна функція для перевірки введених даних
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

# 🔹 Основна функція сторінки
def sales_page(page: PageView):
    # показ таблиці з бекенду
    data = get_sales()
    if not data:
        page.alert("ℹ️ Немає записів продажів", type="info")
    else:
        page.add(Table(data, columns=["id", "date", "customer", "amount", "status"]))

    # форма для додавання запису
    form = AutoForm()
    form.add(TextInput(label="Дата (YYYY-MM-DD)", name="date", placeholder="2026-10-11"))
    form.add(TextInput(label="Клієнт", name="customer"))
    form.add(NumberInput(label="Сума", name="amount", placeholder="1000"))
    form.add(TextInput(label="Статус (pending/completed/canceled)", name="status"))

    def on_submit(values):
        ok, msg = validate_sale_entry(values["date"], values["customer"], values["amount"], values["status"])
        if not ok:
            page.alert(f"❌ Помилка: {msg}", type="error")
        else:
            add_sales_entry(values)
            page.toast("✅ Продаж успішно додано", duration=3000)
            form.clear()  # очистити форму після успішного додавання

    form.on_submit(on_submit)
    page.add(form)

    return page

