from rio import PageView, Table, AutoForm, TextInput, NumberInput
from services.purchases import get_purchases, add_purchase_entry
import datetime

# 🔹 Допоміжна функція для перевірки введених даних
def validate_purchase_entry(date, supplier, item, amount):
    if not date.strip():
        return False, "Дата не може бути порожньою"
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return False, "Невірний формат дати (YYYY-MM-DD)"

    if not supplier.strip():
        return False, "Постачальник не може бути порожнім"

    if not item.strip():
        return False, "Назва товару не може бути порожньою"

    if not isinstance(amount, (int, float)) or amount <= 0:
        return False, "Сума має бути числом > 0"

    return True, "OK"

# 🔹 Основна функція сторінки
def purchases_page(page: PageView):
    # показ таблиці з бекенду
    data = get_purchases()
    if not data:
        page.alert("ℹ️ Немає записів закупівель", type="info")
    else:
        page.add(Table(data, columns=["id", "date", "supplier", "item", "amount"]))

    # форма для додавання запису
    form = AutoForm()
    form.add(TextInput(label="Дата (YYYY-MM-DD)", name="date", placeholder="2026-10-11"))
    form.add(TextInput(label="Постачальник", name="supplier"))
    form.add(TextInput(label="Назва товару", name="item"))
    form.add(NumberInput(label="Сума", name="amount", placeholder="1000"))

    def on_submit(values):
        ok, msg = validate_purchase_entry(values["date"], values["supplier"], values["item"], values["amount"])
        if not ok:
            page.alert(f"❌ Помилка: {msg}", type="error")
        else:
            add_purchase_entry(values)
            page.toast("✅ Закупівлю успішно додано", duration=3000)
            form.clear()  # очистити форму після успішного додавання

    form.on_submit(on_submit)
    page.add(form)

    return page
